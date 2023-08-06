import math
import time

import pika
from pika import frame
import asyncio
import uuid
import logging
from typing import Union, Callable, List
from concurrent.futures import ThreadPoolExecutor
import functools
import threading
from PikaBus.abstractions.AbstractPikaBusSetup import AbstractPikaBusSetup
from PikaBus.abstractions.AbstractPikaSerializer import AbstractPikaSerializer
from PikaBus.abstractions.AbstractPikaProperties import AbstractPikaProperties
from PikaBus.abstractions.AbstractPikaErrorHandler import AbstractPikaErrorHandler
from PikaBus.abstractions.AbstractPikaMessageHandler import AbstractPikaMessageHandler
from PikaBus.abstractions.AbstractPikaBus import AbstractPikaBus
from PikaBus import PikaSerializer, PikaProperties, PikaErrorHandler, PikaBus
from PikaBus.tools import PikaSteps, PikaConstants, PikaTools


class PikaBusSetup(AbstractPikaBusSetup):
    def __init__(self, connParams: pika.ConnectionParameters,
                 defaultListenerQueue: str = None,
                 defaultSubscriptions: Union[List[str], str] = None,
                 defaultDirectExchange: str = 'PikaBusDirect',
                 defaultTopicExchange: str = 'PikaBusTopic',
                 defaultListenerQueueSettings: dict = None,
                 defaultDirectExchangeSettings: dict = None,
                 defaultTopicExchangeSettings: dict = None,
                 defaultConfirmDelivery: bool = True,
                 defaultPrefetchSize: int = 0,
                 defaultPrefetchCount: int = 0,
                 defaultConsumerCount: int = 1,
                 pikaSerializer: AbstractPikaSerializer = None,
                 pikaProperties: AbstractPikaProperties = None,
                 pikaErrorHandler: AbstractPikaErrorHandler = None,
                 pikaBusCreateMethod: Callable = None,
                 retryParams: dict = None,
                 stopConsumersAtExit: bool = True,
                 maxWorkerThreads: int = None,
                 logger=logging.getLogger(__name__)):
        """
        :param pika.ConnectionParameters connParams: Pika connection parameters.
        :param str defaultListenerQueue: Pika default listener queue to receive messages. Set to None to act purely as a publisher.
        :param [str] | str defaultSubscriptions: Default topic or a list of topics to subscribe.
        :param str defaultDirectExchange: Default command exchange to publish direct command messages. The command pattern is used to directly sending a message to one consumer.
        :param str defaultTopicExchange: Default event exchange to publish event messages. The event pattern is used to publish a message to any listening consumers.
        :param dict defaultListenerQueueSettings: Default listener queue settings. 'arguments': {`ha-mode: all`} is activated by default to mirror the queue across all nodes.
        :param dict defaultDirectExchangeSettings: Default direct exchange settings.
        :param dict defaultTopicExchangeSettings: Default topic exchange settings.
        :param bool defaultConfirmDelivery: Activate confirm delivery with publisher confirms by default on all channels.
        :param int defaultPrefetchSize: Specify default prefetch window size for each channel. 0 means it is deactivated.
        :param int defaultPrefetchCount: Specify default prefetch count for each channel. 0 means it is deactivated.
        :param int defaultConsumerCount: Specify default consumer count. Default is 1.
        :param AbstractPikaSerializer pikaSerializer: Optional serializer override.
        :param AbstractPikaProperties pikaProperties: Optional properties override.
        :param AbstractPikaErrorHandler pikaErrorHandler: Optional error handler override.
        :param def pikaBusCreateMethod: Optional pikaBus creator method which returns an instance of AbstractPikaBus.
        :param dict retryParams: A set of retry parameters. See options below in code.
        :param bool stopConsumersAtExit: Automatically stop all consumers when application (main thread) stops.
        :param int maxWorkerThreads: Max number of worker threads. Default is min(32, os.cpu_count() + 4), which preserves at least 5 workers for I/0 bound tasks.
        :param logging logger: Logging object
        """
        if defaultSubscriptions is None:
            defaultSubscriptions = []
        if defaultListenerQueueSettings is None:
            defaultListenerQueueSettings = {'arguments': {'ha-mode': 'all'}}
        if defaultDirectExchangeSettings is None:
            defaultDirectExchangeSettings = {'exchange_type': 'direct'}
        if defaultTopicExchangeSettings is None:
            defaultTopicExchangeSettings = {'exchange_type': 'topic'}
        if pikaSerializer is None:
            pikaSerializer = PikaSerializer.PikaSerializer()
        if pikaProperties is None:
            pikaProperties = PikaProperties.PikaProperties()
        if pikaErrorHandler is None:
            pikaErrorHandler = PikaErrorHandler.PikaErrorHandler()
        if pikaBusCreateMethod is None:
            pikaBusCreateMethod = self._DefaultPikaBusCreator
        if retryParams is None:
            retryParams = {'tries': -1, 'delay': 1, 'max_delay': 10, 'backoff': 1, 'jitter': 1}

        self._connParams = connParams
        self._defaultListenerQueue = defaultListenerQueue
        self._defaultSubscriptions = defaultSubscriptions
        self._defaultDirectExchange = defaultDirectExchange
        self._defaultTopicExchange = defaultTopicExchange
        self._defaultListenerQueueSettings = defaultListenerQueueSettings
        self._defaultDirectExchangeSettings = defaultDirectExchangeSettings
        self._defaultTopicExchangeSettings = defaultTopicExchangeSettings
        self._defaultConfirmDelivery = defaultConfirmDelivery
        self._defaultPrefetchSize = defaultPrefetchSize
        self._defaultPrefetchCount = defaultPrefetchCount
        self._defaultConsumerCount = defaultConsumerCount
        self._pikaSerializer = pikaSerializer
        self._pikaProperties = pikaProperties
        self._pikaErrorHandler = pikaErrorHandler
        self._pipeline = self._BuildPikaPipeline()
        self._messageHandlers = []
        self._openChannels = {}
        self._forceCloseChannelIds = {}
        self._openConnections = {}
        self._pikaBusCreateMethod = pikaBusCreateMethod
        self._retryParams = retryParams
        self._allConsumingTasks = []
        self._logger = logger
        self._connectionHeartbeatIsRunning = False
        self._defaultExecutor = ThreadPoolExecutor(max_workers=maxWorkerThreads)
        self._stopConsumersAtExit = stopConsumersAtExit

    def __del__(self):
        self.Stop()

    @property
    def pipeline(self):
        return self._pipeline

    @property
    def connections(self):
        return dict(self._openConnections)

    @property
    def channels(self):
        return dict(self._openChannels)

    @property
    def messageHandlers(self):
        return self._messageHandlers

    def Init(self,
             listenerQueue: str = None,
             listenerQueueSettings: dict = None,
             topicExchange: str = None,
             topicExchangeSettings: dict = None,
             directExchange: str = None,
             directExchangeSettings: dict = None,
             subscriptions: Union[List[str], str] = None):
        listenerQueue, listenerQueueSettings = self._GetListenerQueue(listenerQueue, listenerQueueSettings)
        with pika.BlockingConnection(self._connParams) as connection:
            channel: pika.adapters.blocking_connection.BlockingChannel = connection.channel()
            self._CreateDefaultRabbitMqSetup(channel,
                                             listenerQueue,
                                             listenerQueueSettings,
                                             topicExchange,
                                             topicExchangeSettings,
                                             directExchange,
                                             directExchangeSettings,
                                             subscriptions)

    def Start(self,
              listenerQueue: str = None,
              listenerQueueSettings: dict = None,
              topicExchange: str = None,
              topicExchangeSettings: dict = None,
              directExchange: str = None,
              directExchangeSettings: dict = None,
              subscriptions: Union[List[str], str] = None,
              confirmDelivery: bool = None,
              prefetchSize: int = None,
              prefetchCount: int = None,
              loop: asyncio.AbstractEventLoop = None,
              executor: ThreadPoolExecutor = None):
        if executor is None:
            executor = self._defaultExecutor
        if loop is None:
            loop = asyncio.get_event_loop()
        if prefetchSize is None:
            prefetchSize = self._defaultPrefetchSize
        if prefetchCount is None:
            prefetchCount = self._defaultPrefetchCount
        listenerQueue, listenerQueueSettings = self._AssertListenerQueueIsSet(listenerQueue, listenerQueueSettings)
        with pika.BlockingConnection(self._connParams) as connection:
            channelId = str(uuid.uuid1())
            channel: pika.adapters.blocking_connection.BlockingChannel = connection.channel()
            onMessageCallback = functools.partial(self._OnMessageCallBack,
                                                  connection=connection,
                                                  channelId=channelId,
                                                  listenerQueue=listenerQueue,
                                                  topicExchange=topicExchange,
                                                  directExchange=directExchange)
            self._CreateDefaultRabbitMqSetup(channel,
                                             listenerQueue,
                                             listenerQueueSettings,
                                             topicExchange,
                                             topicExchangeSettings,
                                             directExchange,
                                             directExchangeSettings,
                                             subscriptions,
                                             confirmDelivery)
            channel.basic_qos(prefetch_size=prefetchSize, prefetch_count=prefetchCount)
            channel.basic_consume(listenerQueue, onMessageCallback)
            self._openChannels[channelId] = channel
            self._openConnections[channelId] = connection
            self._logger.info(f'Starting new consumer channel with id {channelId} '
                              f'and {len(self.channels)} ongoing channels.')
            if not self._connectionHeartbeatIsRunning:
                heartbeatFunc = functools.partial(self._ConnectionHeartbeat)
                connectionHeartbeatTask = loop.run_in_executor(executor, heartbeatFunc)
                futureConnectionHeartbeatTask = asyncio.ensure_future(connectionHeartbeatTask, loop=loop)
                self._allConsumingTasks += [futureConnectionHeartbeatTask]
            try:
                channel.start_consuming()
            except Exception as exception:
                if channelId not in self._forceCloseChannelIds:
                    self._logger.debug(f'Consumer with channel id {channelId} '
                                       f'failed due to unknown exception - '
                                       f'{str(type(exception))}: {str(exception)}')
            finally:
                self._openChannels.pop(channelId)
                self._openConnections.pop(channelId)
                if channelId in self._forceCloseChannelIds:
                    self._forceCloseChannelIds.pop(channelId)
                else:
                    raise Exception(f'Channel {channelId} stopped unexpectedly.')
        self._logger.info(f'Closing consumer channel with id {channelId}.')

    def Stop(self,
             channelId: str = None,
             forceCloseChannel: bool = True):
        openChannels = self.channels
        openConnections = dict(self._openConnections)
        if channelId is None:
            for openChannelId in openChannels:
                self.Stop(channelId=openChannelId,
                          forceCloseChannel=forceCloseChannel)
        else:
            channel: pika.adapters.blocking_connection.BlockingChannel = openChannels.get(channelId, None)
            if channel is not None and channel.is_open:
                if forceCloseChannel:
                    self._logger.debug(f'Force closing channel {channelId}')
                    self._forceCloseChannelIds[channelId] = channel
                self._logger.debug(f'Stopping consumer channel {channelId}')
                try:
                    channel.stop_consuming()
                except Exception as exception:
                    self._logger.debug(f'Failed stopping consumer channel {channelId} - Ignoring - {str(type(exception))}: {str(exception)}')
                    connection: pika.BlockingConnection = openConnections.get(channelId, None)
                    if connection is not None:
                        self._logger.debug(f'Closing connection with channel {channelId}')
                        PikaTools.SafeCloseConnection(connection)

    def StartConsumers(self,
                       consumerCount: int = None,
                       listenerQueue: str = None,
                       listenerQueueSettings: dict = None,
                       topicExchange: str = None,
                       topicExchangeSettings: dict = None,
                       directExchange: str = None,
                       directExchangeSettings: dict = None,
                       subscriptions: Union[List[str], str] = None,
                       confirmDelivery: bool = None,
                       prefetchSize: int = None,
                       prefetchCount: int = None,
                       loop: asyncio.AbstractEventLoop = None,
                       executor: ThreadPoolExecutor = None):
        if executor is None:
            executor = self._defaultExecutor
        listenerQueue, listenerQueueSettings = self._AssertListenerQueueIsSet(listenerQueue, listenerQueueSettings)
        if consumerCount is None:
            consumerCount = self._defaultConsumerCount
        if loop is None:
            loop = asyncio.get_event_loop()
        tasks = []
        for i in range(consumerCount):
            func = functools.partial(self._StartConsumerWithRetryHandler,
                                     listenerQueue=listenerQueue,
                                     listenerQueueSettings=listenerQueueSettings,
                                     topicExchange=topicExchange,
                                     topicExchangeSettings=topicExchangeSettings,
                                     directExchange=directExchange,
                                     directExchangeSettings=directExchangeSettings,
                                     subscriptions=subscriptions,
                                     confirmDelivery=confirmDelivery,
                                     prefetchSize=prefetchSize,
                                     prefetchCount=prefetchCount,
                                     loop=loop,
                                     executor=executor)
            task = loop.run_in_executor(executor, func)
            futureTask = asyncio.ensure_future(task, loop=loop)
            tasks.append(futureTask)

        self._allConsumingTasks += tasks

        return tasks

    def StopConsumers(self,
                      consumingTasks: List[asyncio.Future] = None,
                      loop: asyncio.AbstractEventLoop = None):
        self.Stop()
        self.LoopForever(consumingTasks=consumingTasks,
                         loop=loop)

    def LoopForever(self,
                    consumingTasks: List[asyncio.Future] = None,
                    loop: asyncio.AbstractEventLoop = None):
        if consumingTasks is None:
            consumingTasks = self._allConsumingTasks
        if loop is None:
            loop = asyncio.get_event_loop()
        result = loop.run_until_complete(asyncio.gather(*consumingTasks))
        self._defaultExecutor.shutdown(wait=True)
        return result

    def CreateBus(self,
                  listenerQueue: str = None,
                  topicExchange: str = None,
                  directExchange: str = None,
                  connection: pika.adapters.blocking_connection = None,
                  confirmDelivery: bool = None):

        closeConnectionOnDelete = False
        if connection is None:
            closeConnectionOnDelete = True
            connection = pika.BlockingConnection(self._connParams)

        channel = connection.channel()
        if confirmDelivery is None:
            confirmDelivery = self._defaultConfirmDelivery
        if confirmDelivery:
            channel.confirm_delivery()

        listenerQueue, listenerQueueSettings = self._GetListenerQueue(listenerQueue)
        data = self._CreateDefaultDataHolder(connection, channel, listenerQueue,
                                             topicExchange=topicExchange,
                                             directExchange=directExchange)
        pikaBus: AbstractPikaBus = self._pikaBusCreateMethod(data=data,
                                                             closeChannelOnDelete=True,
                                                             closeConnectionOnDelete=closeConnectionOnDelete)
        return pikaBus

    def AddMessageHandler(self, messageHandler: Union[AbstractPikaMessageHandler, Callable]):
        self._messageHandlers.append(messageHandler)

    def HealthCheck(self,
                    channelId: str = None):
        openChannels = self.channels
        openConnections = dict(self._openConnections)
        health = True
        if channelId is None:
            for openChannelId in openChannels:
                health &= self.HealthCheck(channelId=openChannelId)
            return health
        if channelId not in openChannels or \
                channelId not in openConnections:
            return health
        connection: pika.BlockingConnection = openConnections[channelId]
        channel: pika.adapters.blocking_connection.BlockingChannel = openChannels[channelId]
        health &= connection.is_open
        health &= channel.is_open
        return health

    def QueueMessagesCount(self,
                           channel: pika.adapters.blocking_connection.BlockingChannel = None,
                           queue: str = None):
        if queue is None:
            queue = self._defaultListenerQueue
        if channel is None:
            with self.CreateBus() as pikabus:
                return self._GetQueueMessagesCount(pikabus.channel, queue)
        return self._GetQueueMessagesCount(channel, queue)

    def _StartConsumerWithRetryHandler(self,
                                       listenerQueue: str,
                                       listenerQueueSettings: dict,
                                       topicExchange: str,
                                       topicExchangeSettings: dict,
                                       directExchange: str,
                                       directExchangeSettings: dict,
                                       subscriptions: Union[List[str], str],
                                       confirmDelivery: bool = None,
                                       prefetchSize: int = None,
                                       prefetchCount: int = None,
                                       loop: asyncio.AbstractEventLoop = None,
                                       executor: ThreadPoolExecutor = None):
        tries = self._retryParams.get('tries', -1)
        while tries:
            self._logger.debug(f'Starting async consumer with {tries} tries (-1 = infinite) left')
            try:
                self.Start(listenerQueue=listenerQueue,
                           listenerQueueSettings=listenerQueueSettings,
                           topicExchange=topicExchange,
                           topicExchangeSettings=topicExchangeSettings,
                           directExchange=directExchange,
                           directExchangeSettings=directExchangeSettings,
                           subscriptions=subscriptions,
                           confirmDelivery=confirmDelivery,
                           prefetchSize=prefetchSize,
                           prefetchCount=prefetchCount,
                           loop=loop,
                           executor=executor)
                self._logger.debug(f'Safely stopped async consumer')
                return
            except Exception as exception:
                self._logger.debug(f'Failed async consumer: {str(exception)}')
            tries -= 1

    def _CreateDefaultRabbitMqSetup(self,
                                    channel: pika.adapters.blocking_connection.BlockingChannel,
                                    listenerQueue: str,
                                    listenerQueueSettings: dict,
                                    topicExchange: str = None,
                                    topicExchangeSettings: dict = None,
                                    directExchange: str = None,
                                    directExchangeSettings: dict = None,
                                    subscriptions: Union[List[str], str] = None,
                                    confirmDelivery: bool = None):
        if confirmDelivery is None:
            confirmDelivery = self._defaultConfirmDelivery
        if confirmDelivery:
            channel.confirm_delivery()
        if topicExchange is None:
            topicExchange = self._defaultTopicExchange
        if topicExchangeSettings is None:
            topicExchangeSettings = self._defaultTopicExchangeSettings
        if directExchange is None:
            directExchange = self._defaultDirectExchange
        if directExchangeSettings is None:
            directExchangeSettings = self._defaultDirectExchangeSettings
        if subscriptions is None:
            subscriptions = self._defaultSubscriptions
        PikaTools.CreateExchange(channel, directExchange, settings=directExchangeSettings)
        PikaTools.CreateExchange(channel, topicExchange, settings=topicExchangeSettings)
        if listenerQueue is not None:
            PikaTools.CreateDurableQueue(channel, listenerQueue, settings=listenerQueueSettings)
            PikaTools.BasicSubscribe(channel, topicExchange, subscriptions, listenerQueue)

    def _BuildPikaPipeline(self):
        pipeline = [
            PikaSteps.TryHandleMessageInPipeline,
            PikaSteps.CheckIfMessageIsDeferred,
            PikaSteps.SerializeMessage,
            PikaSteps.HandleMessage,
            PikaSteps.AcknowledgeMessage,
        ]
        return pipeline

    def _OnMessageCallBack(self,
                           channel: pika.adapters.blocking_connection.BlockingChannel,
                           methodFrame: frame.Method,
                           headerFrame: frame.Header,
                           body: bytes,
                           connection: pika.BlockingConnection,
                           channelId: str,
                           listenerQueue: str,
                           topicExchange: str = None,
                           directExchange: str = None):
        try:
            self._logger.debug(f"Received new message on channel {channelId}")
            data = self._CreateDefaultDataHolder(connection, channel, listenerQueue,
                                                 topicExchange=topicExchange,
                                                 directExchange=directExchange)
            data[PikaConstants.DATA_KEY_MESSAGE_HANDLERS] = list(self.messageHandlers)
            incomingMessage = {
                PikaConstants.DATA_KEY_METHOD_FRAME: methodFrame,
                PikaConstants.DATA_KEY_HEADER_FRAME: headerFrame,
                PikaConstants.DATA_KEY_BODY: body,
            }
            data[PikaConstants.DATA_KEY_INCOMING_MESSAGE] = incomingMessage

            pikaBus: AbstractPikaBus = self._pikaBusCreateMethod(data=data,
                                                                 closeChannelOnDelete=False,
                                                                 closeConnectionOnDelete=False)
            data[PikaConstants.DATA_KEY_BUS] = pikaBus

            pipelineIterator = iter(self._pipeline)
            PikaSteps.HandleNextStep(pipelineIterator, data)
            self._logger.debug(f"Successfully handled message on channel {channelId}")
        except Exception as exception:
            channel.basic_nack(methodFrame.delivery_tag)
            self._logger.exception(f"Failed handling message on channel {channelId} - {str(exception)}")

    def _CreateDefaultDataHolder(self,
                                 connection: pika.BlockingConnection,
                                 channel: pika.adapters.blocking_connection.BlockingChannel,
                                 listenerQueue: str,
                                 topicExchange: str = None,
                                 directExchange: str = None):
        if topicExchange is None:
            topicExchange = self._defaultTopicExchange
        if directExchange is None:
            directExchange = self._defaultDirectExchange
        data = {
            PikaConstants.DATA_KEY_LISTENER_QUEUE: listenerQueue,
            PikaConstants.DATA_KEY_DIRECT_EXCHANGE: directExchange,
            PikaConstants.DATA_KEY_TOPIC_EXCHANGE: topicExchange,
            PikaConstants.DATA_KEY_CONNECTION: connection,
            PikaConstants.DATA_KEY_CHANNEL: channel,
            PikaConstants.DATA_KEY_SERIALIZER: self._pikaSerializer,
            PikaConstants.DATA_KEY_PROPERTY_BUILDER: self._pikaProperties,
            PikaConstants.DATA_KEY_ERROR_HANDLER: self._pikaErrorHandler,
            PikaConstants.DATA_KEY_LOGGER: self._logger,
            PikaConstants.DATA_KEY_OUTGOING_MESSAGES: []
        }
        return data

    def _GetListenerQueue(self,
                          listenerQueue: str = None,
                          listenerQueueSettings: dict = None):
        if listenerQueue is None:
            listenerQueue = self._defaultListenerQueue
        if listenerQueueSettings is None:
            listenerQueueSettings = self._defaultListenerQueueSettings
        return listenerQueue, listenerQueueSettings

    def _AssertListenerQueueIsSet(self, listenerQueue: str,
                                  listenerQueueSettings: dict = None):
        listenerQueue, listenerQueueSettings = self._GetListenerQueue(listenerQueue, listenerQueueSettings)
        if listenerQueue is None:
            msg = "Listening queue is not set, so you cannot start the listener process."
            self._logger.error(msg)
            raise Exception(msg)
        return listenerQueue, listenerQueueSettings

    def _DefaultPikaBusCreator(self, data: dict,
                               closeChannelOnDelete: bool = False,
                               closeConnectionOnDelete: bool = False):
        return PikaBus.PikaBus(data=data,
                               closeChannelOnDelete=closeChannelOnDelete,
                               closeConnectionOnDelete=closeConnectionOnDelete)

    def _ConnectionHeartbeat(self):
        if self._connectionHeartbeatIsRunning:
            return
        self._connectionHeartbeatIsRunning = True
        try:
            nextHeartbeats: dict = {}
            heartbeatInterval = self._GetHeartbeatInterval()
            self._logger.debug(f'Starting heartbeat task.')
            nEmptyOngoingConnections = 0
            while nEmptyOngoingConnections <= 1:
                connections = self.connections
                if len(connections) > 0:
                    nEmptyOngoingConnections = 0
                else:
                    nEmptyOngoingConnections += 1
                self._PopDeadChannelIds(nextHeartbeats, connections)
                for channelId in connections:
                    connection = connections.get(channelId, None)
                    if connection is None:
                        continue
                    nextHeartbeats[channelId] = self._PushHeartbeat(connection,
                                                                    channelId,
                                                                    heartbeatInterval,
                                                                    nextHeartbeats.get(channelId, -1))
                time.sleep(min(heartbeatInterval, 3))
                if self._stopConsumersAtExit and not threading.main_thread().is_alive():
                    self.Stop()
                    break
            self._logger.debug(f'Stopped heartbeat task.')
        finally:
            self._connectionHeartbeatIsRunning = False

    def _PopDeadChannelIds(self, nextHeartbeats: dict, connections: dict):
        deadChannelIds = []
        for channelId in nextHeartbeats:
            if channelId not in connections:
                deadChannelIds.append(channelId)
        for deadChannelId in deadChannelIds:
            nextHeartbeats.pop(deadChannelId, None)

    def _PushHeartbeat(self,
                       connection: pika.BlockingConnection,
                       channelId: str,
                       heartbeatInterval: int,
                       nextHeartbeat: int = -1):
        if nextHeartbeat < 0:
            nextHeartbeat = time.time() + heartbeatInterval
        heartBeatStart = time.time()
        if heartBeatStart >= nextHeartbeat:
            try:
                self._logger.debug(f'Triggering connection heartbeat with channel {channelId}')
                connection.process_data_events()
                self._logger.debug(f'Connection heartbeat triggered with channel {channelId} after {time.time() - heartBeatStart} seconds.')
            except Exception as exception:
                self._logger.debug(f'Heartbeat failure with channel {channelId}: {str(type(exception))}: {str(exception)}')
            nextHeartbeat = time.time() + heartbeatInterval
        return nextHeartbeat

    def _GetHeartbeatInterval(self):
        return math.ceil((self._connParams.heartbeat if self._connParams.heartbeat is not None else 60) / 4)

    def _GetQueueMessagesCount(self, channel: pika.adapters.blocking_connection.BlockingChannel, queue: str):
        if channel.is_closed:
            return -1
        queue = channel.queue_declare(queue=queue, passive=True)
        messagesCount = queue.method.message_count
        return messagesCount

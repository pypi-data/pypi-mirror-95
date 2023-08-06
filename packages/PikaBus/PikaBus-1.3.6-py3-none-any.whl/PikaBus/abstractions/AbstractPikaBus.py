import abc
import datetime
from typing import Union, List


class AbstractPikaBus(abc.ABC):
    @property
    @abc.abstractmethod
    def connection(self):
        """
        returns connection.
        :rtype: pika.adapters.blocking_connection
        """
        pass

    @property
    @abc.abstractmethod
    def channel(self):
        """
        returns channel.
        :rtype: pika.adapters.blocking_connection.BlockingChannel
        """
        pass

    @abc.abstractmethod
    def Send(self, payload: dict,
             queue: str = None,
             headers: dict = None,
             messageType: str = None,
             exchange: str = None):
        """
        :param dict payload: Payload to send
        :param str queue: Destination queue. If None, then it it sent back to the listener queue.
        :param dict headers: Optional headers to add or override
        :param str messageType: Specify message type if necessary.
        :param str exchange: Optional exchange to override with.
        """
        pass

    @abc.abstractmethod
    def Publish(self, payload: dict, topic: str,
                headers: dict = None,
                messageType: str = None,
                exchange: str = None,
                mandatory: bool = True):
        """
        :param dict payload: Payload to publish
        :param str topic: Topic.
        :param dict headers: Optional headers to add or override
        :param str messageType: Specify message type if necessary.
        :param str exchange: Optional exchange to override with.
        :param bool mandatory: Mandatory delivery to at least one consumer.
        """
        pass

    @abc.abstractmethod
    def Reply(self, payload: dict,
              headers: dict = None,
              messageType: str = None,
              exchange: str = None):
        """
        :param dict payload: Payload to reply
        :param dict headers: Optional headers to add or override
        :param str messageType: Specify message type if necessary.
        :param str exchange: Optional exchange to override with.
        """
        pass

    @abc.abstractmethod
    def Defer(self, payload: dict, delay: datetime.timedelta,
              queue: str = None,
              headers: dict = None,
              messageType: str = None,
              exchange: str = None):
        """
        :param dict payload: Payload to send
        :param datetime.timedelta delay: Delayed relative time from now to process the message.
        :param str queue: Destination queue. If None, then it it sent back to the listener queue.
        :param dict headers: Optional headers to add or override
        :param str messageType: Specify message type if necessary.
        :param str exchange: Optional exchange to override with.
        """
        pass

    @abc.abstractmethod
    def Subscribe(self, topic: Union[str, List[str]],
                  queue: str = None,
                  exchange: str = None):
        """
        :param str | [str] topic: A topic or a list of topics to subscribe.
        :param str queue: Queue to bind the topic(s). If None, then default listener queue is used.
        :param exchange: Optional exchange to override with.
        """
        pass

    @abc.abstractmethod
    def Unsubscribe(self, topic: Union[str, List[str]],
                    queue: str = None,
                    exchange: str = None):
        """
        :param str | [str] topic: A topic or a list of topics to unsubscribe.
        :param str queue: Queue to unbind the topic(s). If None, then default listener queue is used.
        :param exchange: Optional exchange to override with.
        """
        pass

    @abc.abstractmethod
    def StartTransaction(self):
        """
        Start a bus transaction. All outgoing messages will be stored until CommitTransaction() is triggered.
        """
        pass

    @abc.abstractmethod
    def CommitTransaction(self):
        """
        Commit ongoing bus transaction to send stored outgoing messages.
        """
        pass

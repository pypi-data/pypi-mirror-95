# default
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .Manager import IoTManager

# internal
from .Client import IoTClient
from .types import event_pair


class DeviceType:
    def __init__(self, type_name: str):
        """
        Type of device as a string, should match the device_type string provided by clients when they connect.

        :param type_name: Device type as a string.
        """
        # the type of device
        self.__type = type_name

        # a reference to the manager the type is running under
        self.__context = None

    @property
    def type(self):
        return self.__type

    @property
    def context(self) -> 'IoTManager':
        return self.__context

    def set_context(self, context: 'IoTManager'):
        """
        Used to set the context of the device type. Used by the IoTManager.

        :return:
        """
        self.__context = context

    def call_event_handler(self, event: str, message: str, client: IoTClient) -> event_pair:
        """
        Calls the event handler for the given event if it exists, if it doesnt exist then it does nothing.

        Don't overwrite.

        :param event: The event which is being invoked.
        :param message: The message to pass to the event handler.
        :param client: The client which sent the message.
        :return: None or str
        """
        try:
            response = getattr(self, "on_" + event)(message, client)

            if response is None:
                return None, None
            else:
                if isinstance(response, tuple):
                    return response[0], response[1]
                else:
                    return event, response
        except AttributeError:
            return None, None

    def on_connect(self, client: IoTClient):
        pass

    def on_disconnect(self, client: IoTClient):
        pass

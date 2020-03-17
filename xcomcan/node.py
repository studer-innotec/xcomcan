#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from struct import pack, unpack
from threading import Condition
from stucancommon.node import Service, CanNode, Timeout
from .addresses import RCC_GROUP_DEVICE_ID

logger = logging.getLogger(__name__)


class Request(Service):
    """
    Base class for a request service that have a condition to wait until notification from another thread
    """
    cv = Condition()


class Response(Service):
    """
    Base class for a response service
    """

    def handle(self, source_address, destination_address, exception=None):
        """
        Method override, handle response from a previously sended Service. It will handle response object and notify
        request service on success otherwise forward exception
        """
        with self.request_class.cv:
            if exception is None:
                self.request_class.response = self
            else:
                self.request_class.response = exception
            self.request_class.response_count -= 1
            if self.request_class.response_count == 0:
                self.request_class.cv.notify()


class ReadUserInfoRequest(Request):
    """
    Read User Info Service request inherits from Request
    """
    SERVICE_ID = 0x0
    """
    const int :
        Service identifier
    """
    PACK_FORMAT = '>H'
    """
    const string :
        Format to generate a byte-string representation of the object
    """

    def __init__(self, *args):
        self.info_id = args[0]

    def __bytes__(self):
        return pack(self.PACK_FORMAT, self.info_id)


class ReadUserInfoResponse(Response):
    """
    Read User Info Service response inherits from Response
    """
    SERVICE_ID = 0x0
    """
    const int :
        Service identifier
    """
    PACK_FORMAT = '>Hf'
    """
    const string :
        Format to generate a byte-string representation of the object
    """
    request_class = ReadUserInfoRequest
    """
    Request service object
    """

    def __init__(self, *args):
        self.info_id, self.value = args[:2]

    def __bytes__(self):
        return pack(self.PACK_FORMAT, self.info_id, self.value)


class WriteParameterRequest(Request):
    """
    Write Parameter Service request inherits from Request
    """
    SERVICE_ID = 0x2
    """
    const int :
        Service identifier
    """
    PACK_FORMAT = '>HBf'
    """
    const string :
        Format to generate a byte-string representation of the object
    """

    def __init__(self, *args):
        self.parameter_id, self.part, self.value = args[:3]

    def __bytes__(self):
        return pack(self.PACK_FORMAT, self.parameter_id, self.part, self.value)


class WriteParameterResponse(Response):
    """
    Write Parameter Service response inherits from Response
    """
    SERVICE_ID = 0x2
    """
    const int :
        Service identifier
    """
    PACK_FORMAT = '>HBf'
    """
    const string :
        Format to generate a byte-string representation of the object
    """
    request_class = WriteParameterRequest
    """
    Request service object
    """

    def __init__(self, *args):
        self.parameter_id, self.part, self.value = args[:3]

    def __bytes__(self):
        return pack(self.PACK_FORMAT, self.parameter_id, self.part, self.value)


class ReadParameterRequest(Request):
    """
    Read Parameter Service request inherits from Request
    """
    SERVICE_ID = 0x1
    """
    const int :
        Service identifier
    """
    PACK_FORMAT = '>HB'
    """
    const string :
        Format to generate a byte-string representation of the object
    """

    def __init__(self, *args):
        self.parameter_id, self.part = args[:2]

    def __bytes__(self):
        return pack(self.PACK_FORMAT, self.parameter_id, self.part)


class ReadParameterResponse(Response):
    """
    Read Parameter Service response inherits from Response
    """
    SERVICE_ID = 0x1
    """
    const int :
        Service identifier
    """
    PACK_FORMAT = '>HBf'
    """
    const string :
        Format to generate a byte-string representation of the object
    """
    request_class = ReadParameterRequest
    """
    Request service object
    """

    def __init__(self, *args):
        self.parameter_id, self.part, self.value = args[:3]

    def __bytes__(self):
        return pack(self.PACK_FORMAT, self.parameter_id, self.part, self.value)


class MessageNotification(Response):
    """
    Message Notification Service inherits from Response
    """
    SERVICE_ID = 0x3
    """
    const int :
        Service identifier
    """
    PACK_FORMAT = '>HI'
    """
    const string :
        Format to generate a byte-string representation of the object
    """
    messages = []
    """
    list :
        List of messages
    """

    def __init__(self, *args):
        self.message_id, self.value = args[:2]

    def __bytes__(self):
        return pack(self.PACK_FORMAT, self.message_id, self.value)

    def handle(self, source_address, destination_address, exception=None):
        self.messages.append((source_address, self))


error_identifier_dictionary = {
    0x01: 'INVALID_FRAME',
    0x02: 'DEVICE_NOT_FOUND',
    0x03: 'RESPONSE_TIMEOUT',

    0x12: 'INVALID_SERVICE_ARGUMENT',
    0x13: 'GATEWAY_BUSY',

    0x22: 'OBJECT_ID_NOT_FOUND',
    0x24: 'INVALID_DATA_LENGTH',
    0x25: 'PROPERTY_IS_READ_ONLY',
    0x26: 'INVALID_DATA',
    0x27: 'DATA_TOO_SMALL',
    0x28: 'DATA_TOO_BIG',
    0x29: 'WRITE_PROPERTY_FAILED',
    0x2A: 'READ_PROPERTY_FAILED',
    0x2B: 'ACCESS_DENIED',
    0x2D: 'MULTICAST_READ_NOT_SUPPORTED',
}
"""
Those error codes applies for "User Info read service" and "Parameter read/write service".
They are coded in the response in case of a request failure.
"""


class StuCanPublicError(Exception):
    """
    Class representing a StuCan2 error, also can generate a string representation of it
    """

    def __init__(self, id, error_code):
        """
        id : int
            Service identifier

        error_code : int
            Error code number
        """
        self.id = id
        self.error_code = error_code
        self.identifier = error_identifier_dictionary.get(error_code, 'UNKNOWN')

    def __str__(self):
        return 'StuCanPublicError(id={}, error_code={}, identifier={})'.format(self.id, self.error_code,
                                                                               self.identifier)


class StuCanPublicNode(CanNode):
    """
    Class representing a StuCan public node, inherits from `CanNode`
    """

    def __init__(self, driver, address, debug=False):
        """
        Initialize CanNode

        driver : PythonCanDriver
            Relying can interface

        address : int
            Node CAN address
        """
        CanNode.__init__(self, driver, address)
        if debug is True:
            logging.basicConfig(level=logging.DEBUG)

    def handle_rx_frame(self, identifier, data, dlc, flag, time):
        """
        Handle a frame received on the CAN bus

        Manage behavior as described into StuCan2 public protocol

        Parameters
        ----------
        identifier : bytes
            CAN frame id

        data : bytes
            CAN frame data
        """
        destination_address = (identifier >> 19) & 0x3FF
        if not (destination_address in (self.address, RCC_GROUP_DEVICE_ID)):
            return
        source_address = (identifier >> 9) & 0x3FF
        service_id = (identifier >> 6) & 0x7
        flags = identifier & 0x3F
        error = flags & 0x1
        for service_class in self.services:
            if service_id == service_class.SERVICE_ID:
                if error == 1:
                    id, error_code = unpack('>HI', data)
                    exception = StuCanPublicError(id, error_code)
                    logger.debug('<- rx: %s from address %d to %d', repr(exception), source_address,
                                 destination_address)
                    service = service_class(None, None, None)
                    response = service.handle(source_address, destination_address, exception)
                else:
                    service = service_class.from_bytes(data)
                    logger.debug('<- rx: %s from address %d to %d', str(service), source_address, destination_address)
                    response = service.handle(source_address, destination_address)
                if response is not None:
                    self.send_service(source_address, response)

    def send_from(self, service_id, destination_address, source_address, data):
        """
        Create CAN identifier and access underlying driver to send it and relevant data

        Parameters
        ----------
        service_id : int
            StuCan2 service identifier

        destination_address : int
            Targeted device address

        source_address : int
            Source address

        data : bytes
            The data parameter of a CAN message, length from 0 to 8 bytes
        """
        assert 0 <= service_id <= 0x7
        assert 0 <= destination_address <= 0x3FF
        assert 0 <= source_address <= 0x3FF
        identifier = (destination_address << 19) + (source_address << 9) + (service_id << 6)
        self.driver.send(identifier, data, is_extended_id=True)

    def send(self, service_id, destination_address, data):
        """
        Forward data to send by adding source address

        Parameters
        ----------
        service_id : int
            StuCan2 service identifier

        destination_address : int
            Targeted device address

        data : bytes
            The data parameter of a CAN message
        """
        self.send_from(service_id, destination_address, self.address, data)

    def send_service(self, address, service):
        """
        Send a service

        Parameters
        ----------
        address : int
            Targeted device address

        service : Service
            Service object
        """
        logger.debug('-> tx: %s to address %d', str(service), address)
        data = bytes(service)
        assert len(data) <= 8
        self.send(service.SERVICE_ID, address, data)

    def wait_response(self, address, request, timeout=None):
        """
        Entry point to send a service and then wait for the service response,
        can raise a timeout exception a StuCanPublicError or the response when successfull

        Parameters
        ----------
        address : int
            Targeted device address

        request : Request
            Request service object

        Returns
        -------
        Response
            Response object of the service
        """
        request_class = type(request)
        request_class.response_count = 1
        with request_class.cv:
            self.send_service(address, request)
            return_value = request_class.cv.wait(timeout)
            if not return_value:
                raise Timeout()
        if isinstance(request_class.response, StuCanPublicError):
            raise request_class.response
        return request_class.response

    def messages(self):
        """
        Retreive the list of messages previously happened on the CAN bus

        Returns
        -------
        list
            Notifications messages
        """
        return MessageNotification.messages

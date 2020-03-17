#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Warnings
--------

Changing parameters when the inverters are in operation should be done carefully.\r
The modification of parameters can restart the corresponding algorithm inside the inverter.\r
For example, the change of a delay can restart the timer attached to it.

When you are using the RCC remote control, the Xtender inverter/charger, VarioTrack and VarioString MPPT solar
chargers store their parameter values in a non-volatile flash memory. Because of the endurance of this memory,
the number of writes on a single parameter is only **guaranteed for 1000 write operations**. To allow the cyclic
write of parameters without count limit, the “unsaved value” feature has been created. It enables to write directly
in RAM (volatile memory) without affecting the flash. You can write parameters in RAM by setting the “Part” field
to the value *0x4*.

**We strongly recommend, when you are using the Xcom-CAN Public protocol to control the
installation, to write in RAM instead of flash using the "unsaved value" part.**

"""

from stucancommon.driver import PythonCanDriver
from .node import StuCanPublicNode
from .node import ReadUserInfoRequest, ReadUserInfoResponse
from .node import WriteParameterRequest, WriteParameterResponse
from .node import ReadParameterRequest, ReadParameterResponse
from .node import MessageNotification


class StuCanPublicClient:
    """
    Class representing a StuCan public client
    """

    def __init__(self, source_address, can_bus_speed=125000, bustype='kvaser', debug=False):
        """
        Parameters
        ----------
        source_address : int
            Client source address
        can_bus_speed : int
            CAN bus speed as selected with dip-switches inside the XcomCAN device
        bustype: string
            Name of the CAN interface used, refer to : `python-can <https://python-can.readthedocs.io/en/master/configuration.html#interface-names>`_
        debug : boolean
            Enable debug traces

        Example
        -------
        .. code-block:: python

            # Usage of with statement mandatory
            ...
            with StuCanPublicClient(YourClientAddress, YourCanBusSpeed, YourInterface, True) as client:
                result = client.read_user_info(VT_1_DEVICE_ID, 11000)
                print('result:', result)
            ...
        """
        self.source_address = source_address
        self.can_bus_speed = can_bus_speed
        self.bustype = bustype
        self.debug = debug

    def __enter__(self):
        """
        Initialize PythonCanDriver and StuCanPublicNode. Add required Response services to the node.

        Enter the runtime context related to this object.
        Use the with statement to bind this method's return value to the target
        specified in the as clause of the statement.
        """
        can_driver = PythonCanDriver(self.can_bus_speed, self.bustype)
        self.node = StuCanPublicNode(can_driver, self.source_address, self.debug)
        self.node.add_service(ReadUserInfoResponse)
        self.node.add_service(WriteParameterResponse)
        self.node.add_service(ReadParameterResponse)
        self.node.add_service(MessageNotification)
        self.node.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Stop the CAN node and wait Thread to terminate

        Exit the runtime context related to this object.
        """
        self.node.stop()
        self.node.join()

    def read_user_info(self, destination_address, info_id, timeout=1):
        """
        Allow to read a Studer User Info from a targeted device

        Note
        -----
        The available user information is the same as the values that can be chosen to be displayed
        on the *RCC*. This user information gives the current state of the system. The user information can
        not be modified and their values change during the operation of the system.

        Parameters
        ----------
        destination_address : int
            Targeted device address

        info_id : int
            User Info id number

        timeout : float
            Response timeout, default to 1 second

        Returns
        -------
        float
            User Info value

        Example
        -------
        .. code-block:: python

            # Read user info 3000, Battery voltage, from the first Xtender
            # Run this example within the 'examples/' folder using 'python ex_read_user_info.py' from a
            #   CLI after installing xcomcan package with 'pip install xcomcan'

            from xcomcan.client import StuCanPublicClient
            from xcomcan.addresses import *
            from xcomcan.node import StuCanPublicError

            # your CAN bus speed as selected inside the XcomCAN device with the dip-switches
            CAN_BUS_SPEED = 250000

            if __name__ == "__main__":
                # 'with' statement mandatory to call __enter__ / __exit__ context manager
                with StuCanPublicClient(0x00, CAN_BUS_SPEED, bustype='kvaser', debug=True) as client:

                    # Read battery voltage value (user info n°3000) from first Xtender
                    print('--- Read User Info ---')
                    try:
                        result = client.read_user_info(destination_address=XT_1_DEVICE_ID, info_id=3000)
                    except StuCanPublicError as e:
                        print(e)
                    else:
                        print('user info:', result)
        """
        request = ReadUserInfoRequest(info_id)
        response = self.node.wait_response(destination_address, request, timeout)
        return response.value

    def write_parameter(self, destination_address, parameter_id, part, value, timeout=1):
        """
        Allow to write a Studer Parameter on a targeted device

        Parameters
        ----------
        destination_address : int
            Targeted device address

        parameter_id : int
            Parameter id number

        part : int
            PARAMETER_PART_FLASH or PARAMETER_PART_RAM

        value : int
            The value to write

        timeout : float
            Response timeout, default to 1 second

        Returns
        -------
        int
            Parameter identifier that has been written

        Example
        -------
        .. code-block:: python

            # Write parameter 1286, AC out voltage, to the first Xtender
            # Run this example within the 'examples/' folder using 'python ex_write_param.py' from a CLI
            #   after installing xcomcan package with 'pip install xcomcan'

            from xcomcan.client import StuCanPublicClient
            from xcomcan.addresses import *
            from xcomcan.node import StuCanPublicError

            # your CAN bus speed as selected inside the XcomCAN device with the dip-switches
            CAN_BUS_SPEED = 250000

            if __name__ == "__main__":
                # 'with' statement mandatory to call __enter__ / __exit__ context manager
                with StuCanPublicClient(0x00, CAN_BUS_SPEED, bustype='kvaser', debug=True) as client:

                    # Set AC Output voltage value (param n°1286) to 230 Vac on first Xtender,
                    #   value stored into RAM
                    print('--- Write Parameter ---')
                    value = 230.0
                    try:
                        result = client.write_parameter(destination_address=XT_1_DEVICE_ID,
                                                        parameter_id=1286, part=PARAMETER_PART_RAM,
                                                        value=value)
                    except StuCanPublicError as e:
                        print(e)
                    else:
                        print('param write:', result)
        """
        request = WriteParameterRequest(parameter_id, part, value)
        response = self.node.wait_response(destination_address, request, timeout)
        return response.parameter_id

    def read_parameter(self, destination_address, parameter_id, part, timeout=1):
        """
        Allow to read a Studer Parameter from a targeted device

        Parameters
        ----------
        destination_address : int
            Targeted device address

        parameter_id : int
            Paramter id number

        part : int
            PARAMETER_PART_FLASH, PARAMETER_PART_FLASH_MIN, PARAMETER_PART_FLASH_MAX or PARAMETER_PART_RAM

        timeout : float
            Response timeout, default to 1 second

        Returns
        -------
        float
            Parameter value

        Example
        -------
        .. code-block:: python

            # Read param 1286, AC output voltage, from the first Xtender
            # Run this example within the 'examples/' folder using 'python ex_read_param.py' from a CLI
            #   after installing xcomcan package with 'pip install xcomcan'

            from xcomcan.client import StuCanPublicClient
            from xcomcan.addresses import *
            from xcomcan.node import StuCanPublicError

            # your CAN bus speed as selected inside the XcomCAN device with the dip-switches
            CAN_BUS_SPEED = 250000

            if __name__ == "__main__":
                # 'with' statement mandatory to call __enter__ / __exit__ context manager
                with StuCanPublicClient(0x00, CAN_BUS_SPEED, bustype='kvaser', debug=True) as client:

                    # Read AC Output voltage value (param n°1286) from first Xtender,
                    #   from flash memory
                    print('--- Read Parameter ---')
                    try:
                        result = client.read_parameter(destination_address=XT_1_DEVICE_ID,
                                                       parameter_id=1286, part=PARAMETER_PART_FLASH)
                    except StuCanPublicError as e:
                        print(e)
                    else:
                        print('param flash:', result)

                    # Read AC Output voltage Max allowed value (param n°1286) from first Xtender,
                    #   from flash memory
                    try:
                        result = client.read_parameter(destination_address=XT_1_DEVICE_ID,
                                                       parameter_id=1286, part=PARAMETER_PART_FLASH_MAX)
                    except StuCanPublicError as e:
                        print(e)
                    else:
                        print('param max:', result)

                    # Read AC Output voltage Min allowed value (param n°1286) from first Xtender,
                    #   from flash memory
                    try:
                        result = client.read_parameter(destination_address=XT_1_DEVICE_ID,
                                                       parameter_id=1286, part=PARAMETER_PART_FLASH_MIN)
                    except StuCanPublicError as e:
                        print(e)
                    else:
                        print('param min:', result)

                    # Read AC Output voltage value (param n°1286) from first Xtender, from ram memory
                    #   (not allowed, it will return value from flash)
                    try:
                        result = client.read_parameter(destination_address=XT_1_DEVICE_ID,
                                                       parameter_id=1286, part=PARAMETER_PART_RAM)
                    except StuCanPublicError as e:
                        print(e)
                    else:
                        print('param ram:', result)  # value stored in flash, ram reading not allowed
        """
        request = ReadParameterRequest(parameter_id, part)
        response = self.node.wait_response(destination_address, request, timeout)
        return response.value

    def messages(self):
        """
        Allow to retreive the list of messages previously happened on the CAN bus

        Returns
        -------
        list
            Notification messages

        Example
        ------
        .. code-block:: python

            # Read messages present on the StuCan bus
            # Run this example within the 'examples/' folder using 'python ex_read_messages.py' from a CLI
            #   after installing xcomcan package with 'pip install xcomcan'

            from xcomcan.client import StuCanPublicClient
            from xcomcan.node import StuCanPublicError

            # your CAN bus speed as selected inside the XcomCAN device with the dip-switches
            CAN_BUS_SPEED = 250000

            if __name__ == "__main__":
                # 'with' statement mandatory to call __enter__ / __exit__ context manager
                with StuCanPublicClient(0x00, CAN_BUS_SPEED, bustype='kvaser', debug=True) as client:

                    # Read messages notifications that have been present on the CAN bus
                    print('--- Messages ---')
                    try:
                        msgs = client.messages()
                    except StuCanPublicError as e:
                        print(e)
                    else:
                        print('messages:', msgs)
        """
        return self.node.messages()

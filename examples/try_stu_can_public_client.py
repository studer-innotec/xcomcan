# Read user info 3000, Battery voltage, from the first Xtender
# Write parameter 1286, AC out voltage, to the first Xtender
# Read param 1286, actual AC output voltage, from the first Xtender (flash memory)
# Read param 1286, maximal allowed AC output voltage, from the first Xtender (flash memory)
# Read param 1286, minimal allowed AC output voltage, from the first Xtender (flash memory)
# Read param 1286, actual AC output voltage, from the first Xtender
#   (try from RAM, not allowed -> return value stored into flash)
# Read messages present on the StuCan bus
# Run this example within the 'examples/' folder using 'python try_stu_can_public_client.py' from a CLI
#   after installing xcomcan package with 'pip install xcomcan'

from xcomcan.client import StuCanPublicClient
from xcomcan.addresses import *
from xcomcan.node import StuCanPublicError

CAN_BUS_SPEED = 250000  # your CAN bus speed as selected inside the XcomCAN device with the dip-switches

if __name__ == "__main__":
    # 'with' statement mandatory to call __enter__ / __exit__ context manager
    with StuCanPublicClient(0x00, CAN_BUS_SPEED, bustype='kvaser', debug=True) as client:

        print('--- Read User Info ---')
        # Read battery voltage value (user info n°3000) from first Xtender
        try:
            result = client.read_user_info(destination_address=XT_1_DEVICE_ID, info_id=3000)
        except StuCanPublicError as e:
            print(e)
        else:
            print('user info:', result)

        print('--- Write Parameter ---')
        # Set AC Output voltage value (param n°1286) to 230 Vac on first Xtender, value stored into RAM
        value = 230.0
        try:
            result = client.write_parameter(destination_address=XT_1_DEVICE_ID, parameter_id=1286,
                                            part=PARAMETER_PART_RAM, value=value)
        except StuCanPublicError as e:
            print(e)
        else:
            print('param write:', result)

        print('--- Read Parameter ---')
        # Read AC Output voltage value (param n°1286) from first Xtender, from flash memory
        try:
            result = client.read_parameter(destination_address=XT_1_DEVICE_ID, parameter_id=1286,
                                           part=PARAMETER_PART_FLASH)
        except StuCanPublicError as e:
            print(e)
        else:
            print('param flash:', result)

        # Read AC Output voltage Max allowed value (param n°1286) from first Xtender, from flash memory
        try:
            result = client.read_parameter(destination_address=XT_1_DEVICE_ID, parameter_id=1286,
                                           part=PARAMETER_PART_FLASH_MAX)
        except StuCanPublicError as e:
            print(e)
        else:
            print('param max:', result)

        # Read AC Output voltage Min allowed value (param n°1286) from first Xtender, from flash memory
        try:
            result = client.read_parameter(destination_address=XT_1_DEVICE_ID, parameter_id=1286,
                                           part=PARAMETER_PART_FLASH_MIN)
        except StuCanPublicError as e:
            print(e)
        else:
            print('param min:', result)

        # Read AC Output voltage value (param n°1286) from first Xtender, from ram memory
        #   (not allowed, it will return value from flash)
        try:
            result = client.read_parameter(destination_address=XT_1_DEVICE_ID, parameter_id=1286,
                                           part=PARAMETER_PART_RAM)
        except StuCanPublicError as e:
            print(e)
        else:
            print('param ram:', result)

        # Read messages notifications that have been present on the CAN bus
        print('--- Messages ---')
        try:
            msgs = client.messages()
        except StuCanPublicError as e:
            print(e)
        else:
            print('messages:', msgs)

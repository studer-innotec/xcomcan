# Read param 1286, AC output voltage, from the first Xtender
# Run this example within the 'examples/' folder using 'python ex_read_param.py' from a CLI after
#   installing xcomcan package with 'pip install xcomcan'

from xcomcan.client import StuCanPublicClient
from xcomcan.addresses import *
from xcomcan.node import StuCanPublicError

CAN_BUS_SPEED = 250000  # your CAN bus speed as selected inside the XcomCAN device with the dip-switches

if __name__ == "__main__":
    # 'with' statement mandatory to call __enter__ / __exit__ context manager
    with StuCanPublicClient(0x00, CAN_BUS_SPEED, bustype='kvaser', debug=True) as client:

        # Read AC Output voltage value (param n°1286) from first Xtender, from flash memory
        print('--- Read Parameter ---')
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
            print('param ram:', result)  # value stored in flash, ram reading not allowed

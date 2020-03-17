# Write parameter 1286, AC out voltage, to the first Xtender
# Run this example within the 'examples/' folder using 'python ex_write_param.py' from a CLI
#   after installing xcomcan package with 'pip install xcomcan'

from xcomcan.client import StuCanPublicClient
from xcomcan.addresses import *
from xcomcan.node import StuCanPublicError

CAN_BUS_SPEED = 250000  # your CAN bus speed as selected inside the XcomCAN device with the dip-switches

if __name__ == "__main__":
    # 'with' statement mandatory to call __enter__ / __exit__ context manager
    with StuCanPublicClient(0x00, CAN_BUS_SPEED, bustype='kvaser', debug=True) as client:

        # Set AC Output voltage value (param n°1286) to 230 Vac on first Xtender, value stored into RAM
        print('--- Write Parameter ---')
        value = 230.0
        try:
            result = client.write_parameter(destination_address=XT_1_DEVICE_ID, parameter_id=1286,
                                            part=PARAMETER_PART_RAM, value=value)
        except StuCanPublicError as e:
            print(e)
        else:
            print('param write:', result)

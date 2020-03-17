# Read user info 3000, Battery voltage, from the first Xtender
# Run this example within the 'examples/' folder using 'python ex_read_user_info.py' from a CLI
#   after installing xcomcan package with 'pip install xcomcan'

from xcomcan.client import StuCanPublicClient
from xcomcan.addresses import *
from xcomcan.node import StuCanPublicError

CAN_BUS_SPEED = 250000  # your CAN bus speed as selected inside the XcomCAN device with the dip-switches

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

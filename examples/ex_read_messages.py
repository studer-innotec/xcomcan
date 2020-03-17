# Read messages present on the StuCan bus
# Run this example within the 'examples/' folder using 'python ex_read_messages.py' from a CLI after
#   installing xcomcan package with 'pip install xcomcan'

from xcomcan.client import StuCanPublicClient
from xcomcan.node import StuCanPublicError

CAN_BUS_SPEED = 250000  # your CAN bus speed as selected inside the XcomCAN device with the dip-switches

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

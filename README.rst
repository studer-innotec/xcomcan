Package **xcomcan**
====================

Python library to access Studer-Innotec Xcom-CAN with the *Studer Public Protocol* using CAN 2.0B frames

Prerequisites
----------------

Please read the complete documentation available on : `Studer Innotec SA`_ *-> Support -> Download Center -> Software and Updates -> Communication protocols Xcom-CAN*

Getting Started
----------------

1. Package installation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: console

    $ pip install xcomcan

2. Hardware installation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Connect your *Xcom-CAN* (Studer side) to your installation using the cable provided with the device
- Connect your *Xcom-CAN* (External side) to your controller (personal computer, Raspberry Pi, etc.) using a *USB* to *CAN* adapter (*Kvaser*, etc.)
- Please refer to the *Xcom-CAN* manual for more information about commissioning the device

3. Xcom-CAN Protocol selection
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Interaction with the Xtender/Vario systems through third party devices such as PLC or SCADA requires to select *Studer Public Protocol* with dip switches as shown below. There's two operation modes available :

- Exclusive : This configuration is recommended when there is only **one** device communicating with the *Studer Public Protocol* on the external CAN interface. The *Xcom-CAN* will send a response to every frame that appears on the external CAN interface. For frames which do not fit the *Studer Public Protocol* specifications, the *Xcom-CAN* will send an error frame message. This mode is practical for debugging as every frame sent by the PLC/SCADA will get a response. It will also detect any frame that could be corrupted when transmission occurs.

- Tolerant : This configuration is recommended when there are **several** devices communicating with different protocols on the external CAN interface. The *Xcom-CAN* will only send a response to the frames that completely fit the *Studer Public Protocol* specifications. This mode enable the installer to extend the CAN bus on the external interface and to add others devices that can communicate with the PLC/SCADA on the same physical support as the *Xcom-CAN*.

**Xcom-CAN Dip switches protocol selection**

=====   =====   =====   =====   ===================
N° 1    N° 2    N° 3    N° 4    Studer Public
=====   =====   =====   =====   ===================
OFF     ON      OFF     OFF     Exclusive Protocol
OFF     ON      OFF     ON      Tolerant Protocol
=====   =====   =====   =====   ===================

4. Software configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Set the Studer CAN public client as follow :

.. code-block:: python

    StuCanPublicClient(0x00, CAN_BUS_SPEED, bustype='kvaser', debug=True)

- where '0x00' is the source address
- where `CAN_BUS_SPEED` is your CAN bus bitrate as selected inside the XcomCAN device with the dip-switches, it must be set to 10000, 20000, 50000, 100000, 125000, 250000, 500000 or 1000000
- where `bustype` is the CAN interface name has specified here : `python-can`_
- where `debug` enables you to get some useful console information for debugging purpose


**Xcom-CAN Dip switches CAN bus speed selection**

=====   =====   =====   ==============
N° 6    N° 7    N° 8    CAN bus speed
=====   =====   =====   ==============
OFF     OFF     OFF     10 kbps
OFF     OFF     ON      20 kbps
OFF     ON      OFF     50 kbps
OFF     ON      ON      100 kbps
ON      OFF     OFF     125 kbps
ON      OFF     ON      250 kbps
ON      ON      OFF     500 kbps
ON      ON      ON      1 Mbps
=====   =====   =====   ==============


5. Run an example from `/examples` folder
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Go to */examples* folder with a terminal and execute this script

.. code-block:: console

    $ python try_stu_can_public_client.py

Check `client file`_ to understand it.

6. Open documentation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Open documentation from `Read The Docs`_

Warnings
----------------

- **Please** check carefully the *Xcom-CAN* dip switches configuration as well as the jumper for CAN-H, CAN-L and GND signals
- **Use** devices addresses generated into  `addresses file`_
- It is strongly recommended **NOT** to spam the *Xcom-CAN* with multiple requests. Even if the *Xcom-CAN* has a frame buffer, the response will not be faster because of internal Studer bus load. The correct way to communicate with the *Xcom-CAN* is to send a request and to **wait** for the response before sending the next request. If no response comes from *Xcom-CAN* after a delay of 1 second, we can consider that the timeout is over and another request can be send.

Authors
----------------

**Studer Innotec SA** - *Initial work* - `Studer Innotec SA`_

License
----------------

This project is licensed under the MIT License - see the `LICENSE`_ file for details

.. External References:
.. _Studer Innotec SA: https://www.studer-innotec.com
.. _python-can: https://python-can.readthedocs.io/en/master/configuration.html#interface-names
.. _addresses file: https://xcomcan.readthedocs.io/en/latest/addresses.html
.. _client file: https://xcomcan.readthedocs.io/en/latest/client.html
.. _Read The Docs: https://xcomcan.readthedocs.io/en/latest/index.html
.. _LICENSE: https://xcomcan.readthedocs.io/en/latest/license.html

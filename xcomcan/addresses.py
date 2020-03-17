#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
WARNINGS
----------

This file **MUST NOT** be edited.

Please read the complete documentation available on : `Studer Innotec SA <https://www.studer-innotec.com>`_ *-> Support -> Download Center -> Software and Updates -> Communication protocols Xcom-CAN*

!!! DO NOT CHANGE CONFIGURATIONS BELOW !!!
"""

XT_GROUP_DEVICE_ID = 100
"""

Virtual address to access all XTH, XTM and XTS (Multicast), used in:\n
    - Read User Info\n
    - Read Parameter\n
    - Write Parameter\n
"""
XT_1_DEVICE_ID = XT_GROUP_DEVICE_ID + 1
"""

First Xtender device address, up to 9 XT allowed, ordered by the index displayed on the RCC (Unicast), used in:\n
    - Read User Info\n
    - Read Parameter\n
    - Write Parameter\n
    - Message as source address\n
"""
XT_2_DEVICE_ID = XT_GROUP_DEVICE_ID + 2
XT_3_DEVICE_ID = XT_GROUP_DEVICE_ID + 3
XT_4_DEVICE_ID = XT_GROUP_DEVICE_ID + 4
XT_5_DEVICE_ID = XT_GROUP_DEVICE_ID + 5
XT_6_DEVICE_ID = XT_GROUP_DEVICE_ID + 6
XT_7_DEVICE_ID = XT_GROUP_DEVICE_ID + 7
XT_8_DEVICE_ID = XT_GROUP_DEVICE_ID + 8
XT_9_DEVICE_ID = XT_GROUP_DEVICE_ID + 9

VT_GROUP_DEVICE_ID = 300
"""

Virtual address to access all VarioTrack (Multicast), used in:\n
    - Read User Info\n
    - Read Parameter\n
    - Write Parameter\n
"""
VT_1_DEVICE_ID = VT_GROUP_DEVICE_ID + 1
"""

First VarioTrack device address, up to 15 VarioTrack allowed, ordered by the index displayed on the RCC (Unicast), 
used in:\n
    - Read User Info\n
    - Read Parameter\n
    - Write Parameter\n
    - Message as source address\n
"""
VT_2_DEVICE_ID = VT_GROUP_DEVICE_ID + 2
VT_3_DEVICE_ID = VT_GROUP_DEVICE_ID + 3
VT_4_DEVICE_ID = VT_GROUP_DEVICE_ID + 4
VT_5_DEVICE_ID = VT_GROUP_DEVICE_ID + 5
VT_6_DEVICE_ID = VT_GROUP_DEVICE_ID + 6
VT_7_DEVICE_ID = VT_GROUP_DEVICE_ID + 7
VT_8_DEVICE_ID = VT_GROUP_DEVICE_ID + 8
VT_9_DEVICE_ID = VT_GROUP_DEVICE_ID + 9
VT_10_DEVICE_ID = VT_GROUP_DEVICE_ID + 10
VT_11_DEVICE_ID = VT_GROUP_DEVICE_ID + 11
VT_12_DEVICE_ID = VT_GROUP_DEVICE_ID + 12
VT_13_DEVICE_ID = VT_GROUP_DEVICE_ID + 13
VT_14_DEVICE_ID = VT_GROUP_DEVICE_ID + 14
VT_15_DEVICE_ID = VT_GROUP_DEVICE_ID + 15

RCC_GROUP_DEVICE_ID = 500
"""

Virtual address to access all RCC (Multicast), used in:\n

"""
RCC_1_DEVICE_ID = RCC_GROUP_DEVICE_ID + 1
"""

First RCC device (RCC, Xcom-232i, Xcom-CAN), up to 5 allowed, ordered by the index displayed on the RCC (Unicast), 
used in:\n
    - Message as source address\n
"""
RCC_2_DEVICE_ID = RCC_GROUP_DEVICE_ID + 2
RCC_3_DEVICE_ID = RCC_GROUP_DEVICE_ID + 3
RCC_4_DEVICE_ID = RCC_GROUP_DEVICE_ID + 4
RCC_5_DEVICE_ID = RCC_GROUP_DEVICE_ID + 5

BSP_GROUP_DEVICE_ID = 600
"""

Virtual address to access the BSP (Multicast, but only one BSP per installation), used in:\n
    - Read User Info\n
    - Read Parameter\n
    - Write Parameter\n
"""
BSP_DEVICE_ID = BSP_GROUP_DEVICE_ID + 1
"""

A single BSP (Unicast), used in:\n
    - Read User Info\n
    - Read Parameter\n
    - Write Parameter\n
    - Message as source address\n
"""

VS_GROUP_DEVICE_ID = 700
"""

Virtual address to access all VarioString (Multicast), used in:\n
    - Read User Info\n
    - Read Parameter\n
    - Write Parameter\n
"""
VS_1_DEVICE_ID = VS_GROUP_DEVICE_ID + 1
"""

First VarioString device address, up to 15 VarioString allowed, ordered by the index displayed on the RCC (Unicast), 
used in:\n
    - Read User Info\n
    - Read Parameter\n
    - Write Parameter\n
    - Message as source address\n
"""
VS_2_DEVICE_ID = VS_GROUP_DEVICE_ID + 2
VS_3_DEVICE_ID = VS_GROUP_DEVICE_ID + 3
VS_4_DEVICE_ID = VS_GROUP_DEVICE_ID + 4
VS_5_DEVICE_ID = VS_GROUP_DEVICE_ID + 5
VS_6_DEVICE_ID = VS_GROUP_DEVICE_ID + 6
VS_7_DEVICE_ID = VS_GROUP_DEVICE_ID + 7
VS_8_DEVICE_ID = VS_GROUP_DEVICE_ID + 8
VS_9_DEVICE_ID = VS_GROUP_DEVICE_ID + 9
VS_10_DEVICE_ID = VS_GROUP_DEVICE_ID + 10
VS_11_DEVICE_ID = VS_GROUP_DEVICE_ID + 11
VS_12_DEVICE_ID = VS_GROUP_DEVICE_ID + 12
VS_13_DEVICE_ID = VS_GROUP_DEVICE_ID + 13
VS_14_DEVICE_ID = VS_GROUP_DEVICE_ID + 14
VS_15_DEVICE_ID = VS_GROUP_DEVICE_ID + 15

PARAMETER_PART_FLASH = 0x00
"""
To read a parameter from flash or write a parameter into flash and ram
"""

PARAMETER_PART_FLASH_MIN = 0x01
"""
To read the minimum parameter value from flash
"""
PARAMETER_PART_FLASH_MAX = 0x02
"""
To read the maximal parameter value from flash
"""
PARAMETER_PART_RAM = 0x04
"""
To read a parameter from flash or write a parameter into ram only
"""

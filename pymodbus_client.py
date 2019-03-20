#!/usr/bin/env python2.7
"""
Pymodbus Synchronous Client Examples
--------------------------------------------------------------------------

The following is an example of how to use the synchronous modbus client
implementation from pymodbus.

It should be noted that the client can also be used with
the guard construct that is available in python 2.5 and up::

    with ModbusClient('127.0.0.1') as client:
        result = client.read_coils(1,10)
        print result
"""
# --------------------------------------------------------------------------- #
# import the various server implementations
# --------------------------------------------------------------------------- #
# from pymodbus.client.sync import ModbusTcpClient as ModbusClient
# from pymodbus.client.sync import ModbusUdpClient as ModbusClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.payload import BinaryPayloadBuilder
from pymodbus.compat import iteritems
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from pymodbus.bit_read_message import *
from pymodbus.framer.rtu_framer import ModbusRtuFramer
import pymodbus
import time
# --------------------------------------------------------------------------- #
# configure the client logging
# --------------------------------------------------------------------------- #
import logging
FORMAT = ('%(asctime)-15s %(threadName)-15s '
          '%(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s')
logging.basicConfig(format=FORMAT)
log = logging.getLogger()
#log.setLevel(logging.DEBUG)

#UNIT = 0x1
UNIT = 0x1

def run_sync_client():
    # ------------------------------------------------------------------------#
    # choose the client you want
    # ------------------------------------------------------------------------#
    # make sure to start an implementation to hit against. For this
    # you can use an existing device, the reference implementation in the tools
    # directory, or start a pymodbus server.
    #
    # If you use the UDP or TCP clients, you can override the framer being used
    # to use a custom implementation (say RTU over TCP). By default they use
    # the socket framer::
    #
    #    client = ModbusClient('localhost', port=5020, framer=ModbusRtuFramer)
    #
    # It should be noted that you can supply an ipv4 or an ipv6 host address
    # for both the UDP and TCP clients.
    #
    # There are also other options that can be set on the client that controls
    # how transactions are performed. The current ones are:
    #
    # * retries - Specify how many retries to allow per transaction (default=3)
    # * retry_on_empty - Is an empty response a retry (default = False)
    # * source_address - Specifies the TCP source address to bind to
    #
    # Here is an example of using these options::
    #
    #    client = ModbusClient('localhost', retries=3, retry_on_empty=True)
    # ------------------------------------------------------------------------#
    #client = ModbusClient('localhost', port=5020)
    # from pymodbus.transaction import ModbusRtuFramer
    # client = ModbusClient('localhost', port=5020, framer=ModbusRtuFramer)
    # client = ModbusClient(method='binary', port='/dev/ptyp0', timeout=1)
    # client = ModbusClient(method='ascii', port='/dev/ptyp0', timeout=1)
    #
    #client = ModbusClient(method='rtu', port='/dev/ttyUSB0', timeout=3, stopbits=1, bytesize=8 ,baudrate=9600)
    #client = ModbusClient(method='rtu', port='/dev/ttyUSB1', timeout=3, stopbits=1, bytesize=8 ,baudrate=9600)
    client = ModbusClient(method='rtu', port='/dev/ttyUSB1', timeout=3, stopbits=1, bytesize=8 ,baudrate=9600)

    
    #client = ModbusClient(method='rtu', port='/tmp/vmodem0', timeout=3,baudrate=9600)
    #client = ModbusClient(method='rtu', port='/dev/sda1', timeout=3,baudrate=9600)
    client.connect()

    # ------------------------------------------------------------------------#
    # specify slave to query
    # ------------------------------------------------------------------------#
    # The slave to query is specified in an optional parameter for each
    # individual request. This can be done by specifying the `unit` parameter
    # which defaults to `0x00`
    # ----------------------------------------------------------------------- #
    
    register =0x0
    while True:
        rr = client.read_holding_registers(register, 4, unit=UNIT)
        log.debug(rr)
        print time.strftime("%H:%M:%S",time.localtime()), rr.getRegister(0),rr.getRegister(1),rr.getRegister(2) ,rr.getRegister(3)
        time.sleep(2)

    client.close()


if __name__ == "__main__":
    run_sync_client()

import asyncio
import pytest


from iot_protocols.modbus import ModbusClient, AsyncModbusClient, request_factory


REQUESTS = [
    {
        "function": "ReadCoils",
        "unit": 1,
        "address": 320,
        "count": 4
    },
    {
        "function": "WriteCoils",
        "unit": 1,
        "address": 320,
        "values": [False]*6

    },
    {
        "function": "ReadInputRegister",
        "unit": 1,
        "address": 0x754B,
        "count": 6,
        "encoding": "string"
    },
    {
        "function": "ReadInputRegister",
        "unit": 1,
        "address": 0x7555,
        "count": 10,
        "encoding": "string"
    }
]

requests = list(map(request_factory, REQUESTS))
"""
CLIENT = client = ModbusClient.with_tcp_client(
        host="192.168.144.99",
        port=1502,
        timeout=5
    )
"""
CLIENT = client = ModbusClient.with_serial_client(
        port="COM3",
        parity="N",
        stopbits=1,
        bytesize=8,
        timeout=5
    )


def task_cb(context):
    print(f"Tasks result : {context}")


def execute_task(tasks):
    for t in tasks:
        result = client.request(t)
        print(result, type(result))



if __name__=="__main__":
    execute_task(requests)
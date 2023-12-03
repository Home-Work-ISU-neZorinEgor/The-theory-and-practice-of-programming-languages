import socket
import json
import zmq

from client import host, port
from interpreter import Interpreter

def server(host, port):
    print(f"Server started at {host}:{port}")
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind(f"tcp://{host}:{port}")
    while True:
        message = socket.recv()
        print(f"Received: {message.decode()}")
        try:
            result = Interpreter().eval(message)
        except Exception as e:
            result = {"error": str(e)}
        socket.send(json.dumps(result).encode())
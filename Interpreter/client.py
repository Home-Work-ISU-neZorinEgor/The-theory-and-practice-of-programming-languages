import socket
import json

host = "127.0.0.1"
port = 5555

def eval(sock, expr):
    expr = expr.encode("utf-8")
    sock.send(len(expr).to_bytes(4, byteorder="big"))
    sock.send(expr)

    answer_size = int.from_bytes(sock.recv(4, byteorder="big"), byteorder="big")
    answer = b""
    remaining_bytes = answer_size
    while remaining_bytes > 0:
        chunk = sock.recv(min(remaining_bytes, 4096))
        if not chunk:
            raise ValueError("Connection closed unexpectedly.")
        answer += chunk
        remaining_bytes -= len(chunk)
    answer = json.loads(answer.decode("utf-8"))
    return answer

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, port))
        expression = input("Enter a mathematical expression: ")
        result = eval(sock, expression)
        print(f"Result: {result['result']}")

if __name__ == "__main__":
    main()

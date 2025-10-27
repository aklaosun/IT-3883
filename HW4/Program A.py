# Program Name: Assignment4.py
# Course: IT3883/Section W01
# Student Name: Ayomide Laosun
# Assignment Number: 4
# Due Date: 10/26/2025
# Purpose: Program A prompts the user for a string, transmits it over a TCP socket to Program B,
#          then waits for a response and prints whatever is received.
# Specific resources used to complete the assignment: Python Standard Library documentation for Socket module

import socket
import sys
from contextlib import closing

HOST = "127.0.0.1"        # Must match Program B
PORT = 45001              # Must match Program B
ENCODING = "utf-8"
BUFFER = 4096
CONNECT_TIMEOUT_SEC = 5.0
IO_TIMEOUT_SEC = 5.0

def run_client() -> int:
    user_text = input("Enter a message to send to Program B: ")
    if not user_text:
        print("No input provided. Exiting.")
        return 0

    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        sock.settimeout(CONNECT_TIMEOUT_SEC)
        try:
            print(f"Connecting to Program B at {HOST}:{PORT} ...")
            sock.connect((HOST, PORT))
        except socket.timeout:
            print(f"[CLIENT] Connection to {HOST}:{PORT} timed out.", file=sys.stderr)
            return 1
        except ConnectionRefusedError as exc:
            print(f"[CLIENT] Connection refused: {exc}. Is Program B running?", file=sys.stderr)
            return 1
        except OSError as exc:
            print(f"[CLIENT] Network error on connect: {exc}", file=sys.stderr)
            return 1

        sock.settimeout(IO_TIMEOUT_SEC)

        try:
            sock.sendall(user_text.encode(ENCODING))
            print(f"Sent to Program B: {user_text}")
        except (socket.timeout, OSError) as exc:
            print(f"[CLIENT] Error sending data: {exc}", file=sys.stderr)
            return 1

        try:
            data = sock.recv(BUFFER)
        except socket.timeout:
            print("[CLIENT] Timed out waiting for response.", file=sys.stderr)
            return 1
        except OSError as exc:
            print(f"[CLIENT] Error receiving response: {exc}", file=sys.stderr)
            return 1

    if not data:
        print("[CLIENT] No response received.", file=sys.stderr)
        return 1

    try:
        response = data.decode(ENCODING)
    except UnicodeDecodeError:
        print("[CLIENT] Server sent non-UTF-8 bytes.", file=sys.stderr)
        return 1

    print("Response from Program B:", response)
    return 0

if __name__ == "__main__":
    raise SystemExit(run_client())
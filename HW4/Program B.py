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

HOST = "127.0.0.1"   # Must match Program A
PORT = 45001         # Must match Program A
BACKLOG = 5
BUFFER = 4096
ENCODING = "utf-8"


def handle_client(conn: socket.socket, addr: tuple[str, int]) -> None:
    """Single request/response per connection; keeps spec simple."""
    with conn:
        data = conn.recv(BUFFER)
        if not data:
            return
        try:
            text = data.decode(ENCODING)
        except UnicodeDecodeError:
            # Why: Client might send non-text; return a clear error string.
            conn.sendall(b"[SERVER ERROR] Non-UTF-8 data received.")
            return
        response = text.upper().encode(ENCODING)
        conn.sendall(response)


def main() -> int:
    print(f"[SERVER] Starting on {HOST}:{PORT}. Press Ctrl+C to stop.")
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as server_sock:
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            server_sock.bind((HOST, PORT))
        except OSError as exc:
            print(f"[SERVER] Bind failed on {HOST}:{PORT}: {exc}", file=sys.stderr)
            return 1

        server_sock.listen(BACKLOG)

        try:
            while True:
                try:
                    conn, addr = server_sock.accept()
                except OSError as exc:
                    print(f"[SERVER] Accept error: {exc}", file=sys.stderr)
                    continue

                print(f"[SERVER] Connected by {addr}")
                try:
                    handle_client(conn, addr)
                except Exception as exc:
                    print(f"[SERVER] Error handling {addr}: {exc}", file=sys.stderr)
                finally:
                    print(f"[SERVER] Closed connection {addr}")
        except KeyboardInterrupt:
            print("\n[SERVER] Shutting down gracefully.")
        except Exception as exc:
            print(f"[SERVER] Fatal error: {exc}", file=sys.stderr)
            return 1

    print("[SERVER] Stopped.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
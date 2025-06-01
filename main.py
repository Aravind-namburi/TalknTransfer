import socket
import threading

def send_file(sock, filename):
    """Function to send a file over a socket."""
    try:
        with open(filename, 'rb') as f:
            bytes_read = f.read(4096)
            while bytes_read:
                sock.sendall(bytes_read)
                bytes_read = f.read(4096)
        sock.sendall(b'EOFEOFEOF')  # Send an EOF marker that is unlikely to appear in normal data
    except FileNotFoundError:
        print("File not found.")
    except Exception as e:
        print(f"Error during sending file: {e}")

def receive_file(sock, filename):
    """Function to receive a file from a socket."""
    try:
        with open(filename, 'wb') as f:
            buffer = b''
            while True:
                data = sock.recv(4096)
                buffer += data
                if buffer.endswith(b'EOFEOFEOF'):  # Check for the EOF marker
                    buffer = buffer[:-9]  # Remove the EOF marker from the data
                    f.write(buffer)
                    break
                elif len(data) > 0:
                    f.write(buffer)
                    buffer = b''  # Clear the buffer after writing
    except Exception as e:
        print(f"Error during receiving file: {e}")

class WritingThread(threading.Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name
        port = int(input("Hello, Please input a target port number: "))
        self.port = port
        self.sock = None

    def run(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect(('localhost', self.port))
            self.sock.send(self.name.encode('utf-8'))
            print(f"Connected to port: {self.port}")

            while True:
                # message = input(f"{self.name}> ")
                message = input()
                if message.lower() == 'exit':
                    self.sock.send(b'exit')
                    break
                elif message.startswith("transfer"):
                    _, filename = message.split()
                    self.sock.send(f"transfer {filename}".encode('utf-8'))
                    send_file(self.sock, filename)
                else:
                    self.sock.send(message.encode('utf-8'))
        except Exception as e:
            print(f"Error in WritingThread: {e}")
        finally:
            if self.sock:
                self.sock.close()

class ReadingThread(threading.Thread):
    def __init__(self, server_socket):
        super().__init__()
        self.server_socket = server_socket

    def run(self):
        try:
            conn, addr = self.server_socket.accept()
            client_name = conn.recv(1024).decode('utf-8')
            # print(f"Connected to {client_name}")

            while True:
                data = conn.recv(1024)
                if not data or data == b'exit':
                    break
                message = data.decode('utf-8')
                if message.startswith("transfer"):
                    _, filename = message.split()
                    filename = f"new_{filename}"
                    print(f"Receiving file {filename} from {client_name}")
                    receive_file(conn, filename)
                else:
                    print(f"\n{client_name} : {message}")
        except Exception as e:
            print(f"Error in ReadingThread: {e}")
        finally:
            conn.close()

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 0))
    server_socket.listen(1)
    host, port = server_socket.getsockname()
    name = input("Enter your name: ")
    print(f"{name} is running.")
    print(f"The server port number is: {port}")

    reading_thread = ReadingThread(server_socket)
    reading_thread.start()

    writing_thread = WritingThread(name)
    writing_thread.start()

    reading_thread.join()
    writing_thread.join()

if __name__ == "__main__":
    main()

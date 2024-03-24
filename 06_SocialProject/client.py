import cmd
import sys
import socket
import threading
import readline


class CowClient(cmd.Cmd):

    def __init__(self, socket):
        super().__init__()
        self.prompt = '>>> '
        self.socket = socket
        self.is_running = True

    def do_who(self, args):
        self.socket.sendall(f'who\n'.encode())
    
    def do_cows(self, args):
        self.socket.sendall(f'cows\n'.encode())

    def do_quit(self, args):
        self.socket.sendall(f'quit\n'.encode())
        self.is_running = False
        return True

    def receive(self):
        while self.is_running:
            res = s.recv(1024).rstrip().decode()
            print(f'\n{res}\n{self.prompt}{readline.get_line_buffer()}', end='', flush=True)


host = 'localhost' if len(sys.argv) < 2 else sys.argv[1]
port = 1337 if len(sys.argv) < 3 else int(sys.argv[2])
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))
    cow_client = CowClient(s)
    receiver = threading.Thread(target=cow_client.receive)
    receiver.start()
    cow_client.cmdloop()

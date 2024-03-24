import cmd
import sys
import socket
import threading
import queue
import readline


class CowClient(cmd.Cmd):

    def __init__(self, socket):
        super().__init__()
        self.prompt = '>>> '
        self.socket = socket
        self.completion_queue = queue.Queue()
        self.is_running = True
        self.is_waiting = False

    def do_who(self, args):
        self.socket.sendall(f'who\n'.encode())
    
    def do_cows(self, args):
        self.socket.sendall(f'cows\n'.encode())

    def do_login(self, args):
        self.socket.sendall(f'login {args}\n'.encode())

    def do_say(self, args):
        self.socket.sendall(f'say {args}\n'.encode())

    def do_yield(self, args):
        self.socket.sendall(f'yield {args}\n'.encode())

    def do_quit(self, args):
        self.socket.sendall(f'quit\n'.encode())
        self.is_running = False
        return True

    def receive(self):
        try:
            while self.is_running:
                res = s.recv(1024).rstrip().decode()
                if not res:
                    self.is_running = False
                    return True
                elif self.is_waiting:
                    self.completion_queue.put(res)
                    self.is_waiting = False
                else:
                    print(f'\n{res}\n{self.prompt}{readline.get_line_buffer()}', end='', flush=True)
        except Exception as e:
            print(e)
            self.is_running = False


host = 'localhost' if len(sys.argv) < 2 else sys.argv[1]
port = 1337 if len(sys.argv) < 3 else int(sys.argv[2])
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))
    cow_client = CowClient(s)
    receiver = threading.Thread(target=cow_client.receive)
    receiver.start()
    cow_client.cmdloop()

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
        """
        Get the usernames of users who are online.\n
        Usage: who
        """
        self.socket.sendall(f'who\n'.encode())
    
    def do_cows(self, args):
        """
        Get available usernames, cow names.\n
        Usage: cows
        """
        self.socket.sendall(f'cows\n'.encode())

    def do_login(self, args):
        """
        Log in to the chat. The username can only be the name of a cow.\n
        Usage: login [username]
        """
        self.socket.sendall(f'login {args}\n'.encode())

    def do_say(self, args):
        """
        Send message via cowsay.\n
        Usage: say [username] [message]
        """
        self.socket.sendall(f'say {args}\n'.encode())

    def do_yield(self, args):
        """
        Send message to everyone via cowsay.\n
        Usage: yield [message]
        """
        self.socket.sendall(f'yield {args}\n'.encode())

    def do_quit(self, args):
        """
        Log out of the chat.\n
        Usage: quit
        """
        self.socket.sendall(f'quit\n'.encode())
        self.is_running = False
        return True

    def complete_login(self, text, line, begidx, endidx):
        self.awaiting_response = True
        self.is_waiting = True
        self.do_cows(None)
        res = self.completion_queue.get().split(':\n')
        res = res[1].split(' ') if len(res) == 2 else []
        return [cow for cow in res if cow.startswith(text)]

    def complete_say(self, text, line, begidx, endidx):
        self.awaiting_response = True
        self.is_waiting = True
        self.do_who(None)
        res = self.completion_queue.get().split(':\n')
        res = res[1].split(' ') if len(res) == 2 else []
        return [cow for cow in res if cow.startswith(text)]

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

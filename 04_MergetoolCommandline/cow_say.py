import sys
from cowsay import list_cows, make_bubble, cowsay, cowthink
import cmd
import shlex


class CowsayShell(cmd.Cmd):
    intro = "Cowsay shell interface. Try help or ? to list commands.\n"
    prompt = "[cowsay] >>> "

    def do_list_cows(self, args):
        args = shlex.split(args)

        if len(args) == 0:
            print(list_cows())
        elif len(args) == 1:
            print(list_cows(args[0]))
        else:
            print(f'Invalid argument!')

    def do_make_bubble(self, args):
        pass

    def do_cowsay(self, args):
        pass

    def do_cowthink(self, args):
        pass


if __name__ == '__main__':
    CowsayShell().cmdloop()

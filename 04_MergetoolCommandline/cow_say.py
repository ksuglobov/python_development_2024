import sys
from cowsay import list_cows, make_bubble, cowsay, cowthink
import cmd
import shlex


class CowsayShell(cmd.Cmd):
    intro = "Cowsay shell interface. Try help or ? to list commands.\n"
    prompt = "[cowsay] >>> "

    def do_list_cows(self, args):
        """
        Lists all cow file names in the given directory.\n
        Usage: list_cows [path_to_directory_with_cows]
        """
        args = shlex.split(args)

        if len(args) == 0:
            print(list_cows())
        elif len(args) == 1:
            print(list_cows(args[0]))
        else:
            print(f'Invalid argument!')

    def do_make_bubble(self, args):
        """
        Wraps text in a bubble.\n
        Usage: make_bubble [width [wrap_text]]
        """
        args = shlex.split(args)

        if len(args) < 1 or len(args) > 3:
            print('Invalid number of arguments!')

        text = args[0]

        width = 40
        if len(args) == 2:
            width = int(args[1])

        wrap_text = True
        if len(args) == 3:
            wrap_text = args[2]
            if wrap_text == 'True':
                wrap_text = True
            elif wrap_text == 'False':
                wrap_text = False
            else:
                print('Invalid wrap_text value! Value can be "True" or "False".')

        print(make_bubble(text=text, width=width, wrap_text=wrap_text))

    def do_cowsay(self, args):
        pass

    def do_cowthink(self, args):
        pass


if __name__ == '__main__':
    CowsayShell().cmdloop()

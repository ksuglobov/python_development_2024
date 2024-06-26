import cowsay
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

        if len(args) > 1:
            print('Invalid number of arguments!')
            return

        path2dir = cowsay.COW_PEN
        if len(args) == 1:
            path2dir = args[0]

        print(cowsay.list_cows(path2dir))

    def do_make_bubble(self, args):
        """
        Wraps text in a bubble.\n
        Usage: make_bubble text [width [wrap_text]]
        """
        args = shlex.split(args)

        if len(args) < 1 or len(args) > 3:
            print('Invalid number of arguments!')
            return

        text = args[0]

        width = 40
        if len(args) >= 2:
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
                return

        print(cowsay.make_bubble(text=text, width=width, wrap_text=wrap_text))

    def complete_make_bubble(self, text, line, begidx, endidx):
        words = (line[:endidx] + ".").split()

        if len(words) == 4:
            completions = ['True', 'False']

        return [c for c in completions if c.startswith(text)]

    def cow_action(self, action, args):
        args = shlex.split(args)

        if len(args) < 1 or len(args) > 5:
            print('Invalid number of arguments!')
            return

        message = args[0]

        cow = 'default'
        if len(args) >= 2:
            cow = args[1]

        eyes = cowsay.Option.eyes
        if len(args) >= 3:
            eyes = args[2]

        tongue = cowsay.Option.tongue
        if len(args) >= 4:
            tongue = args[3]

        print(action(message=message, cow=cow, eyes=eyes, tongue=tongue))
    
    def cow_action_complete(self, text, line, begidx, endidx):
        words = (line[:endidx] + ".").split()

        match len(words):
            case 3:
                completions = cowsay.list_cows()
            case 4:
                completions = ['..', 'oo', '00', 'OO', '$$', '66']
            case 5:
                completions = ['|', 'U', 'V', 'J']

        return [c for c in completions if c.startswith(text)]
    
    def do_cowsay(self, args):
        """
        Print message via cowsay.\n
        Usage: cowsay message [cow [eyes [tongue]]]
        """
        self.cow_action(cowsay.cowsay, args)

    def complete_cowsay(self, *args):
        return self.cow_action_complete(*args)

    def do_cowthink(self, args):
        """
        Print message via cowthink.\n
        Usage: cowthink message [cow [eyes [tongue]]]
        """
        self.cow_action(cowsay.cowthink, args)

    def complete_cowthink(self, *args):
        return self.cow_action_complete(*args)


if __name__ == '__main__':
    CowsayShell().cmdloop()

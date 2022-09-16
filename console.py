#!/usr/bin/python3
"""Module containing the entry point of the command interpreter."""
import cmd
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.review import Review
from models.amenity import Amenity
from models.place import Place
import re
import shlex
import sys


avaliable_classes = {'BaseModel': BaseModel, 'User': User,
                     'Amenity': Amenity, 'City': City, 'State': State,
                     'Place': Place, 'Review': Review}


class HBNBCommand(cmd.Cmd):
    """This class represents the command interpreter
    of this project."""

    prompt = '(hbnb) '

    def precmd(self, line):
        """Runs some actions before a line of command is executed.
        Args:
            line (str): The line of command to be transformed.
        Returns:
            str: The next line of command to execute.
        """
        patterns = (
            r'(?P<class>[a-zA-Z]+)',
            r'(?P<command>[a-zA-Z]+)',
            r'(?P<args_txt>.*)',
        )
        cls_fxn_fmt = r'{}\s*\.\s*{}\s*\({}\)'.format(
            patterns[0], patterns[1], patterns[2]
        )
        cls_fxn_match = re.fullmatch(cls_fxn_fmt, line)
        if cls_fxn_match is not None:
            class_name = cls_fxn_match.group('class')
            command_name = cls_fxn_match.group('command')
            args_txt = cls_fxn_match.group('args_txt').strip()
            args = None
            cmd_line_parts = []
            try:
                args = self.split_func_args(args_txt)
                cmd_line_parts.append(command_name)
                cmd_line_parts.append(class_name)
                for arg in args:
                    cmd_line_parts.append('"{}"'.format(arg))
                return ' '.join(cmd_line_parts)
            except Exception:
                return line
        else:
            return line

    def postcmd(self, stop, line):
        """Runs some actions after a line of command is executed.
        Args:
            stop (bool): The continuation condition.
            line (str): The line of command that was executed.
        Returns:
            bool: The continuation condition.
        """
        if not sys.__stdin__.isatty():
            print('(hbnb) ', end='')
        return stop

    def split_func_args(self, args_txt):
        """Splits a function argument section into its arguments.
        Args:
            args_txt (str): The function argument section.
        Returns:
            list: The list of arguments.
        """
        txt = args_txt.strip()
        quote = None
        brace = None
        brace_d = 0
        a = 0
        char_p = None
        pushed_a = False
        parts = []
        n = len(txt)
        for i in range(n):
            if txt[i] == ',':
                if (quote is None) and (brace is None):
                    if not pushed_a:
                        parts.append(txt[a:i])
                    else:
                        pushed_a = False
                    a = i + 1
            elif (txt[i] == '{') and (quote is None):
                if brace is None:
                    brace = '{'
                    a = i
                brace_d += 1
            elif (txt[i] == '}') and (quote is None):
                if brace_d > 0:
                    brace_d -= 1
                if brace_d == 0:
                    parts.append(txt[a:i+1])
                    pushed_a = True
                    brace = None
                    brace_d = 0
                    a = i + 1
            elif (txt[i] == '"') and (brace is None):
                if (quote is None):
                    quote = '"'
                    a = i + 1
                else:
                    parts.append(txt[a:i])
                    pushed_a = True
                    quote = None
                    a = i + 1
            elif i == n - 1:
                if not pushed_a:
                    parts.append(txt[a: i if txt[i] == ',' else n])
                    pushed_a = True
        if (quote is not None) or (brace is not None):
            raise SyntaxError()
        parts = list(map(lambda x: x.strip(), parts))
        return parts

    def do_help(self, arg):
        """To get help on a command, type help <topic>.
        """
        return super().do_help(arg)

    def do_quit(self, line):
        """Quit command to exit the program"""
        return True

    def emptyline(self):
        """Executes some actions when the command line is empty.
        """
        return False

    def do_EOF(self, line):
        """Quit command to exit the program"""
        print("")
        return True

    def do_create(self, arg):
        """Creates a new instance.
        """
        args = arg.split()
        if not check_classname(args):
            return

        new_obj = avaliable_classes[args[0]]()
        new_obj.save()
        print(new_obj.id)

    def do_show(self, arg):
        """Prints the string representation of an instance.
        """
        args = arg.split()
        if not check_classname(args, id=True):
            return

        instance_objs = storage.all()
        key = "{}.{}".format(args[0], args[1])
        req_instance = instance_objs.get(key, None)
        if req_instance is None:
            print("** no instance found **")
            return
        print(req_instance)

    def do_destroy(self, arg):
        """Deletes an instance based on the class name and id.
        """
        args = arg.split()
        if not check_classname(args, id=True):
            return

        instance_objs = storage.all()
        key = "{}.{}".format(args[0], args[1])
        req_instance = instance_objs.get(key, None)
        if req_instance is None:
            print("** no instance found **")
            return

        del instance_objs[key]
        storage.save()

    def do_all(self, arg):
        """Prints string representation of all instances.
        """
        args = arg.split()
        all_objs = storage.all()

        if len(args) < 1:
            print(["{}".format(str(v)) for _, v in all_objs.items()])
            return
        if args[0] not in avaliable_classes.keys():
            print("** class doesn't exist **")
            return
        else:
            print(["{}".format(str(v))
                  for _, v in all_objs.items() if type(v).__name__ == args[0]])
            return

    def do_update(self, arg: str):
        """Updates an instance based on the class name and id.
        """
        args = arg.split()
        if not check_classname(args, id=True):
            return

        instance_objs = storage.all()
        key = "{}.{}".format(args[0], args[1])
        req_instance = instance_objs.get(key, None)
        if req_instance is None:
            print("** no instance found **")
            return
        setattr(req_instance, args[2], args[3])
        req_instance.save()

    def do_count(self, line):
        """Prints the number of instances of a class.
        Usage: count <class name>
        """
        args = []
        try:
            args = shlex.split(line)
        except Exception:
            print('*** Unknown syntax: {}'.format(line))
            return
        class_name = args[0] if len(args) >= 1 else None
        if class_name is None:
            print("** class name missing **")
            return
        if class_name in storage.model_classes.keys():
            n = 0
            for obj in storage.all().values():
                if type(obj) is storage.model_classes[class_name]:
                    n += 1
            print(n)
        else:
            print("** class doesn't exist **")


def check_classname(args, id=False):
    """Runs checks on args to validate classname entry.
    """
    if len(args) < 1:
        print("** class name missing **")
        return False
    if args[0] not in avaliable_classes.keys():
        print("** class doesn't exist **")
        return False
    if len(args) < 2 and id:
        print("** instance id missing **")
        return False
    return True


if __name__ == '__main__':
    HBNBCommand().cmdloop()

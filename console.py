#!/usr/bin/python3
"""Module for the command line interpreter"""

import shlex
import cmd
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """Command interpreter class"""

    prompt = "(hbnb) "
    cls_map = {
            "BaseModel": BaseModel, "User": User,
            "State": State, "City": City,
            "Amenity": Amenity, "Place": Place, "Review": Review
            }

    def emptyline(self):
        """User entered no input"""
        pass

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, arg):
        """Exit the program at EOF (Ctrl+D)"""
        return True

    def do_create(self, arg):
        """Create a new instance of BaseModel,
        save it, and print the id"""

        try:
            if not arg:
                raise SyntaxError()
            tokens = arg.split(' ')
            class_name = tokens[0]
            if class_name not in self.cls_map:
                raise NameError()
            kwargs = {}
            for token in tokens[1:]:
                if '=' in token:
                    k, v = token.split('=')
                    if v.startswith('"') and v.endswith('"'):
                        v = v[1:-1]
                        v = v.replace("_", " ")
                    kwargs[k] = v
            new_instance = self.cls_map[class_name](**kwargs)
            storage.new(new_instance)
            print(new_instance.id)
            new_instance.save()
        except SyntaxError:
            print("** class name is missing **")
        except NameError:
            print("** class doesn't exist **")

    def do_show(self, arg):
        """Prints the string representation of an instance"""
        args = shlex.split(arg)
        if not args:
            print("** class name missing **")
            return
        class_name = args[0]
        if class_name not in HBNBCommand.cls_map:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        obj_id = args[1]
        key = "{}.{}".format(class_name, obj_id)
        if key in storage.all():
            print(storage.all()[key])
        else:
            print("** no instance found **")

    def do_destroy(self, arg):
        """Deletes an instance based
        on the class name and id"""

        args = arg.split()
        if not args:
            print("** class name missing **")
            return

        class_name = args[0]
        if class_name not in HBNBCommand.cls_map:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return

        obj_id = args[1]
        key = "{}.{}".format(class_name, obj_id)
        if key in storage.all():
            del storage.all()[key]
            storage.save()
        else:
            print("** no instance found **")

    def do_all(self, arg):
        """Prints all string representations of instances"""

        args = arg.split()
        obj_list = []

        if not args:
            for key, obj in storage.all().items():
                obj_list.append(str(obj))
            print(obj_list)
            return

        class_name = args[0]
        if class_name not in HBNBCommand.cls_map:
            print("** class doesn't exist **")
            return
        for key, obj in storage.all().items():
            if key.split(".")[0] == class_name:
                obj_list.append(str(obj))
        print(obj_list)

    def do_update(self, arg):
        """Updates an instance based
        on the class name and id"""

        args = arg.split()
        if not args:
            print("** class name missing **")
            return

        class_name = args[0]
        if class_name not in HBNBCommand.cls_map:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        obj_id = args[1]
        key = "{}.{}".format(class_name, obj_id)
        if key not in storage.all():
            print("** no instance found **")
            return
        if len(args) < 3:
            print("** attribute name missing **")
            return
        if len(args) < 4:
            print("** value missing **")
            return
        attr_name = args[2]
        attr_value = args[3]
        instance = storage.all()[key]
        try:
            attr_value = eval(attr_value)
            setattr(instance, attr_name, attr_value)
            instance.save()
        except Exception:
            print("** value missing **")

    def do_count(self, arg):
        """Prints the number of instances of a class"""

        try:
            if arg not in HBNBCommand.cls_map:
                raise NameError()
            else:
                class_instances = [i for i in storage.all().values() if type(
                    i) == HBNBCommand.cls_map[arg]]
                print(len(class_instances))
        except NameError:
            print("** class doesn't exist **")

    def command(self, args):
        """Seperates command from its arguments"""
        i = args.find("(")
        if i == -1:
            return args
        return args[:i]

    def tokenizer(self, args):
        """Splits args into tokens and cleans the code"""
        tokens = []
        tokens.append(args[0])
        try:
            my_dict = eval(
                    args[1][args[1].find('{'):args[1].find('}')+1])
        except Exception:
            my_dict = None
        if isinstance(my_dict, dict):
            tok_str = args[1][args[1].find('(')+1:args[1].find(')')]
            tokens.append(((tok_str.split(", "))[0]).strip('"'))
            tokens.append(my_dict)
            return tokens

        tok_str = args[1][args[1].find('(')+1:args[1].find(')')]
        tokens.append(" ".join(tok_str.split(", ")))
        return " ".join(i for i in tokens).strip()

    def default(self, line):
        """Handles the <class name>.<method>(arg) syntax"""
        methods = {
                "all": self.do_all,
                "count": self.do_count,
                "update": self.do_update,
                "destroy": self.do_destroy,
                "show": self.do_show
                }
        cmd_list = line.split('.')

        if len(cmd_list) >= 2:
            command = self.command(cmd_list[1])
            if command not in methods:
                cmd.Cmd.default(self, line)
                return

            if command in ("all", "count"):
                methods[command](cmd_list[0])
            elif command == "update":
                args = self.tokenizer(cmd_list)
                if isinstance(args, list):
                    key = args[0] + ' ' + args[1]
                    for k, v in args[2].items():
                        self.do_update(key + ' "{}" "{}"'.format(k, v))
                else:
                    self.do_update(args)
            else:
                methods[command](self.tokenizer(cmd_list))
        else:
            cmd.Cmd.default(self, line)


if __name__ == '__main__':
    HBNBCommand().cmdloop()

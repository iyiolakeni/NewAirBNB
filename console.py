#!/usr/bin/python3
"""entry point of the command interpreter"""
import cmd
import ast
import shlex
from models.base_model import BaseModel
from models.user import User
from models import storage
from shlex import split
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review

class HBNBCommand(cmd.Cmd):
    """Beginning of the command interpreter"""

    prompt = "(hbnb) "
    __classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
    }

    def emptyline(self):
        """Does nothing on ENTER."""
        pass

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, arg):
        """Exit the console with Ctrl-D (EOF)"""
        print("")
        return True

    def default(self, args):
        """Default behavior for cmd module when input is invalid"""
        subArgs = self.stripper(args)
        str_list = list(shlex.shlex(args, posix=True))
        if str_list[0] not in HBNBCommand.__classes:
            print("*** Unknown syntax: {}".format(args))
            return
        if str_list[2] == "all":
            self.do_all(str_list[0])
        elif str_list[2] == "count":
            count = 0
            for obj in storage.all().values():
                if str_list[0] == type(obj).__name__:
                    count += 1
            print(count)
            return
        elif str_list[2] == "show":
            key = str_list[0] + " " + subArgs[0]
            self.do_show(key)
        elif str_list[2] == "destroy":
            key = str_list[0] + " " + subArgs[0]
            self.do_destroy(key)
        elif str_list[2] == "update":
            newdict = self.dict_strip(args)
            if type(newdict) is dict:
                for key, val in newdict.items():
                    key_val = str_list[0] + " " + subArgs[0]
                    self.do_update(key_val + ' "{}" "{}"'.format(key, val))
            else:
                key = str_list[0]
                for arg in subArgs:
                    key = key + " " + '"{}"'.format(arg)
                self.do_update(key)
        else:
            print("*** Unknown syntax: {}".format(args))
            return

    def do_create(self, args):
        """Creates an object"""
        if not len(args):
            print("** class name missing **")
        elif args not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            cre_obj = eval(args)()
            print(cre_obj.id)
            cre_obj.save()

    def do_show(self, args):
        """Shows the string representation of a class instance."""
        if not len(args):
            print("** class name missing **")
            return
        str_list = split(args)
        if str_list[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return
        if len(str_list) == 1:
            print("** instance id missing **")
            return
        key_val = "{}.{}".format(str_list[0], str_list[1])
        if key_val not in storage.all().keys():
            print("** no instance found **")
        else:
            print(storage.all()[key_val])

    def do_destroy(self, args):
        """Delete a class instance of a given id"""
        if not len(args):
            print("** class name missing **")
            return
        str_list = split(args)
        if str_list[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return
        if len(str_list) == 1:
            print("** instance id missing **")
            return
        key_val = "{}.{}".format(str_list[0], str_list[1])
        if key_val not in storage.all().keys():
            print("** no instance found **")
            return
        del storage.all()[key_val]
        storage.save()

    def do_all(self, args):
        """Prints string representations of all instances of a class"""
        if not len(args):
            print([obj for obj in storage.all().values()])
            return
        str_list = split(args)
        if str_list[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return
        print([obj for obj in storage.all().values()
               if str_list[0] == type(obj).__name__])

    def do_update(self, args):
        """Updates a class instance of a given id"""
        if not len(args):
            print("** class name missing **")
            return
        str_list = split(args)
        for string in str_list:
            if string.startswith('"') and string.endswith('"'):
                string = string[1:-1]
        if str_list[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return
        if len(str_list) == 1:
            print("** instance id missing **")
            return
        key_val = str_list[0] + '.' + str_list[1]
        if key_val not in storage.all().keys():
            print("** no instance found **")
            return
        if len(str_list) == 2:
            print("** attribute name missing **")
            return
        if len(str_list) == 3:
            print("** value missing **")
            return
        try:
            setattr(storage.all()[key_val], str_list[2], eval(str_list[3]))
        except ValueError:
            setattr(storage.all()[key_val], str_list[2], str_list[3])

    def stripper(self, st):
        """Strips that line"""
        new_string = st[st.find("(")+1:st.rfind(")")]
        new_string = shlex.shlex(new_string, posix=True)
        new_string.whitespace += ','
        new_string.whitespace_split = True
        return list(new_string)

    def dict_strip(self, st):
        """Tries to find a dict while stripping"""
        new_str = st[st.find("(")+1:st.rfind(")")]
        try:
            new_dict = new_str[new_str.find("{")+1:new_str.rfind("}")]
            return eval("{" + new_dict + "}")
        except ValueError:
            return None

if __name__ == '__main__':
    HBNBCommand().cmdloop()


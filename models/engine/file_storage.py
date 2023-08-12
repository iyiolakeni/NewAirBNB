#!/usr/bin/python3
"""Script for FileStorage class"""

import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class FileStorage:
    """Beginning for storage engine"""

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """returns the dictionary objects"""
        return FileStorage.__objects

    def new(self, obj):
        """Sets new obj to __objects with key"""
        if obj:
            okey = "{}.{}".format(type(obj).__name__, obj.id)
            FileStorage.__objects[okey] = obj

    def save(self):
        """Saves objects to the JSON file"""
        jDict = {}
        for k, v in FileStorage.__objects.items():
            jDict[k] = v.to_dict()
        with open(FileStorage.__file_path, 'w') as f:
            json.dump(jDict, f)

    def reload(self):
        """Reloads objects in JSON"""
        try:
            with open(FileStorage.__file_path, 'r') as f:
                objdict = json.load(f)
                for key, obj in objdict.items():
                    newObj = eval(obj['__class__'])(**obj)
                    FileStorage.__objects[key] = newObj
        except FileNotFoundError:
            pass


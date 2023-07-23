#!/usr/bin/python3
"""module for FileStorage class"""


import collections.abc
import models.engine.storage
import models
import os.path
import json


def key(cls, id):
    """Convenience function to return a "Class.1234" key"""

    if isinstance(cls, type):
        cls = cls.__name__
    return str(cls) + '.' + str(id)


class FileStorage (models.engine.storage.Storage):
    """class used to store and retrieve data model instances using JSON"""

    __file_path = "storage.json"
    __objects = {}

    def __contains__(self, obj):
        """Check if an object is in storage"""

        if isinstance(obj, str):
            return obj in FileStorage.__objects
        return key(type(obj), obj.id) in FileStorage.__objects

    def all(self, cls=None):
        """Return all instances"""

        if cls is None:
            return FileStorage.__objects
        else:
            return {
                name: obj
                for name, obj in FileStorage.__objects.items()
                if name.startswith(key(cls, ''))
            }

    def close(self):
        """Reload the file"""

        self.reload()

    def delete(self, obj, id=None):
        """Delete an object from storage"""

        if isinstance(obj, models.base_model.BaseModel):
            del FileStorage.__objects[key(type(obj), obj.id)]
            return
        if id is None:
            raise TypeError(
                'obj argument is not an instance and object ID not given'
            )
        del FileStorage.__objects[key(cls, id)]

    def get(self, cls, id):
        """Retrieve an object from storage"""

        return FileStorage.__objects[key(cls, id)]

    def new(self, obj):
        """add dictionary rep of obj to dictionary __objects"""

        FileStorage.__objects[key(type(obj), obj.id)] = obj

    def reload(self):
        """retreive repr of objects from JSON file and store in __objects"""

        if not os.path.exists(FileStorage.__file_path):
            return
        with open(FileStorage.__file_path, 'rt') as file:
            toLoad = json.load(file)
        if not isinstance(toLoad, collections.abc.Mapping):
            raise ValueError('value in JSON file is not an object')
        FileStorage.__objects = {
            key: models.classes[key.partition('.')[0]](**obj)
            for key, obj in toLoad.items()
        }

    def save(self):
        """save the instances to the storage file"""

        toStore = {
            key: obj.to_dict()
            for key, obj in FileStorage.__objects.items()
        }
        with open(FileStorage.__file_path, 'wt') as file:
            json.dump(toStore, file)

    def tryGet(self, cls, id, default):
        """Try to retrieve an object, instead returning default if not found"""

        k = key(cls, id)
        if k in FileStorage.__objects:
            return FileStorage.__objects[k]
        return default

#!/usr/bin/python3
"""Module for database storage engine"""


import models
import models.base_model
import models.engine.storage
import os
import sqlalchemy
import sqlalchemy.orm


class DBStorage (models.engine.storage.Storage):
    """Store AirBnB clone data model objects in an SQL database"""

    __engine = None
    __session = None
    __sessionMaker = None

    def __contains__(self, obj):
        """Check if an object exists in storage"""

        return obj in DBStorage.__session

    def __init__(self):
        """Initialize the database storage engine (use like a singleton)"""

        DBStorage.__engine = sqlalchemy.create_engine(
            'mysql+mysqldb://{}:{}@{}/{}'.format(
                os.getenv('HBNB_MYSQL_USER'),
                os.getenv('HBNB_MYSQL_PWD'),
                os.getenv('HBNB_MYSQL_HOST'),
                os.getenv('HBNB_MYSQL_DB')
            ),
            pool_pre_ping=True
        )
        if os.getenv('HBNB_ENV') == 'test':
            models.base_model.Base.metadata.drop_all(DBStorage.__engine)

    def all(self, cls=None):
        """Return a collection of objects, optionally filtered by class"""

        ret = {}
        if cls is None:
            for name, cls in models.classes.items():
                if issubclass(cls, models.base_model.Base):
                    for record in DBStorage.__session.query(cls):
                        key = name + '.' + record.id
                        ret[key] = record
        else:
            if not isinstance(cls, type):
                cls = models.classes[cls]
            for record in DBStorage.__session.query(cls):
                key = cls.__name__ + '.' + record.id
                ret[key] = record
        return ret

    def close(self):
        """Remove the session and create a new one"""

        DBStorage.__sessionMaker.remove()
        DBStorage.__session = None
        self.reload()

    def delete(self, obj=None):
        """Delete obj from the database"""

        DBStorage.__session.delete(obj)

    def get(self, cls, id):
        """Retrieve an object from storage"""

        if not isinstance(cls, type):
            cls = models.classes[cls]
        obj = DBStorage.__session.query(cls).filter(cls.id == str(id)).first()
        if obj is None:
            raise KeyError('object with given class and ID not found')
        return obj

    def new(self, obj):
        """Save a new object to the database"""

        DBStorage.__session.add(obj)

    def reload(self):
        """Open a new MySQL session and create tables if necessary"""

        models.base_model.Base.metadata.create_all(self.__engine)
        if DBStorage.__sessionMaker is None:
            DBStorage.__sessionMaker = sqlalchemy.orm.scoped_session(
                sqlalchemy.orm.sessionmaker(bind=self.__engine)
            )
        if DBStorage.__session is None:
            DBStorage.__session = \
                DBStorage.__sessionMaker(expire_on_commit=False)

    def save(self):
        """commit all current pending changes to the database"""

        DBStorage.__session.commit()

    def tryGet(self, cls, id, default):
        """Try to get an object with a fallback value"""

        if not isinstance(cls, type):
            cls = models.classes[cls]
        obj = DBStorage.__session.query(cls).filter(cls.id == str(id)).first()
        if obj is None:
            return default
        return obj

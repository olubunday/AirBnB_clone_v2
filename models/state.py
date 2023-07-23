#!/usr/bin/python3
"""This is the state class"""


import models
import models.base_model
import sqlalchemy
import sqlalchemy.orm
import os


class State(models.base_model.BaseModel, models.base_model.Base):
    """This is the class for State"""

    __tablename__ = "states"
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        name = sqlalchemy.Column(
            'name',
            sqlalchemy.String(128),
            nullable=False
        )
        cities = sqlalchemy.orm.relationship("City", back_populates="state")
    else:
        name = ""

        @property
        def cities(self):
            """Return all the cities"""

            ret = [
                city
                for city in models.storage.all('City').values()
                if city.state_id == self.id
            ]
            return ret

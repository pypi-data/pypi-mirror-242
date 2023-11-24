import json
from uuid import UUID
from datetime import date as Date, datetime as DateTime
from pydantic import BaseModel, UUID4


class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, BaseModel):
            return obj.__dict__
        if isinstance(obj, (UUID, UUID4)):
            # if the obj is uuid, we simply return the value of uuid
            return str(obj)
        if isinstance(obj, (Date, DateTime)):
            return obj.isoformat()

        return json.JSONEncoder.default(self, obj)

from dataclasses import dataclass

from marshmallow_dataclass import class_schema

from semantha_sdk.model.semantha_entity import SemanthaModelEntity, SemanthaSchema



@dataclass
class Area(SemanthaModelEntity):
    """ author semantha, this is a generated class do not change manually! """
    x: float
    y: float
    width: float
    height: float

AreaSchema = class_schema(Area, base_schema=SemanthaSchema)

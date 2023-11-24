
from dataclasses import dataclass

from marshmallow_dataclass import class_schema

from semantha_sdk.model.semantha_entity import SemanthaModelEntity, SemanthaSchema



@dataclass
class CustomField(SemanthaModelEntity):
    """ author semantha, this is a generated class do not change manually! """
    name: str
    value: str
    type: str

CustomFieldSchema = class_schema(CustomField, base_schema=SemanthaSchema)

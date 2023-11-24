
from dataclasses import dataclass

from marshmallow_dataclass import class_schema

from semantha_sdk.model.semantha_entity import SemanthaModelEntity, SemanthaSchema



@dataclass
class Metadata(SemanthaModelEntity):
    """ author semantha, this is a generated class do not change manually! """
    name: str
    value: str

MetadataSchema = class_schema(Metadata, base_schema=SemanthaSchema)

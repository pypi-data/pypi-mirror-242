
from dataclasses import dataclass

from marshmallow_dataclass import class_schema

from semantha_sdk.model.semantha_entity import SemanthaModelEntity, SemanthaSchema

from typing import Optional


@dataclass
class Difference(SemanthaModelEntity):
    """ author semantha, this is a generated class do not change manually! """
    operation: Optional[str] = None
    text: Optional[str] = None

DifferenceSchema = class_schema(Difference, base_schema=SemanthaSchema)

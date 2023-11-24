
from dataclasses import dataclass

from marshmallow_dataclass import class_schema

from semantha_sdk.model.semantha_entity import SemanthaModelEntity, SemanthaSchema

from typing import Optional


@dataclass
class ModelMetadata(SemanthaModelEntity):
    """ author semantha, this is a generated class do not change manually! """
    name: str
    type: str
    id: Optional[str] = None
    read_only: Optional[bool] = None

ModelMetadataSchema = class_schema(ModelMetadata, base_schema=SemanthaSchema)

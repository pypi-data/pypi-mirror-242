import time

from pydantic import BaseModel
from pydantic import Field
from pydantic import PrivateAttr

from amsdal_utils.models.data_models.address import Address
from amsdal_utils.models.data_models.reference import Reference
from amsdal_utils.models.enums import SchemaTypes
from amsdal_utils.models.enums import Versions
from amsdal_utils.models.utils.reference_builders import build_reference


class Metadata(BaseModel):
    _is_frozen: bool = PrivateAttr(False)

    """The address of the object/record."""
    address: Address
    """The reference to class schema"""
    class_schema_reference: Reference
    """The type of class schema"""
    class_schema_type: SchemaTypes = SchemaTypes.USER
    """Flag to indicate if the object/record is deleted"""
    is_deleted: bool = False
    """The next version of the object/record"""
    next_version: str | None = None
    """The previous version of the object/record"""
    prior_version: str | None = None
    """The list of references to other objects/records"""
    reference_to: list[Reference] = Field(default_factory=list)
    """The list of references from other objects/records"""
    referenced_by: list[Reference] = Field(default_factory=list)
    """The timestamp when the object/record was created"""
    created_at: float = Field(default_factory=lambda: round(time.time() * 1000))
    """The timestamp when the object/record was last updated"""
    updated_at: float = Field(default_factory=lambda: round(time.time() * 1000))

    @property
    def is_latest(self) -> bool:
        """
        Flag to indicate if the object/record is the latest version

        :rtype: bool
        """
        return self.next_version is None

    @property
    def reference(self) -> Reference:
        """
        Reference of the object/record. If the object/record is not frozen, the version of object is pinned. Otehrwise,
        it will store the latest version.

        :rtype: Reference
        """
        reference_address = self.address

        if not self._is_frozen:
            reference_address = self.address.model_copy(update={'object_version': Versions.LATEST})

        return build_reference(
            resource=reference_address.resource,
            class_name=reference_address.class_name,
            object_id=reference_address.object_id,
            class_version=reference_address.class_version,
            object_version=reference_address.object_version,
        )

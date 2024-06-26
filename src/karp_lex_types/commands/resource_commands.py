"""Commands for lex resources."""

from typing import Generic, Literal, TypeVar

import pydantic

from karp_lex_types.value_objects.unique_id import (
    UniqueId,
    UniqueIdPrimitive,
    make_unique_id,
)

from .base import Command

T = TypeVar("T")


class EntityOrResourceIdMixin(Command):  # noqa: D101
    resource_id: str | None = None
    id: UniqueId | None = None

    @pydantic.field_serializer("id")
    def serialize_id(self, id: UniqueId, _info) -> str:  # noqa: PLR6301, A002
        """Serialize id as string."""
        return str(id)

    @pydantic.model_validator(mode="before")
    @classmethod
    def resource_id_or_id(cls, values) -> dict:  # noqa: D102
        resource_id = values.get("resourceId", None)
        if "id" in values and resource_id:
            raise ValueError("Can't give both 'id' and 'resourceId'")

        if resource_id:
            return dict(values) | {
                "id": None,
                "resourceId": resource_id,
            }
        if "id" in values:
            return dict(values) | {
                "resourceId": None,
            }
        raise ValueError("Must give either 'id' or 'resourceId'")


class GenericCreateResource(Command, Generic[T]):  # noqa: D101
    id: UniqueId = pydantic.Field(default_factory=make_unique_id)
    resource_id: str
    name: str
    config: T
    entry_repo_id: UniqueId
    cmdtype: Literal["create_resource"] = "create_resource"

    @pydantic.field_serializer("id")
    def serialize_id(self, id: UniqueId, _info) -> str:  # noqa: PLR6301, A002
        """Serialize id as string."""
        return str(id)

    @pydantic.field_serializer("entry_repo_id")
    def serialize_entry_repo_id(self, entry_repo_id: UniqueId, _info) -> str:  # noqa: PLR6301
        """Serialize id as string."""
        return str(entry_repo_id)


class CreateResource(GenericCreateResource[dict]):
    """Command to create a resource."""

    @classmethod
    def from_dict(  # noqa: D102
        cls,
        data: dict,
        entry_repo_id: UniqueIdPrimitive,
        user: str | None = None,
        message: str | None = None,
    ) -> "CreateResource":
        try:
            resource_id = data.pop("resource_id")
        except KeyError as exc:
            raise ValueError("'resource_id' is missing") from exc
        try:
            name = data.pop("resource_name")
        except KeyError as exc:
            raise ValueError("'resource_name' is missing") from exc

        return cls(
            resourceId=resource_id,
            name=name,
            config=data,
            entryRepoId=entry_repo_id,
            user=user or "Unknown user",
            message=message or f"Resource '{resource_id}' created.",
        )


class GenericUpdateResource(EntityOrResourceIdMixin, Command, Generic[T]):
    """Generic command for updating a resource."""

    version: int
    name: str
    config: T
    cmdtype: Literal["update_resource"] = "update_resource"


class UpdateResource(GenericUpdateResource[dict]):
    """Command for updating a resource."""


class PublishResource(EntityOrResourceIdMixin, Command):  # noqa: D101
    version: int
    cmdtype: Literal["publish_resource"] = "publish_resource"


class DeleteResource(EntityOrResourceIdMixin, Command):  # noqa: D101
    #    version: int
    cmdtype: Literal["delete_resource"] = "delete_resource"


class SetEntryRepoId(EntityOrResourceIdMixin, Command):  # noqa: D101
    entry_repo_id: UniqueId
    version: int
    cmdtype: Literal["set_entry_repo_id"] = "set_entry_repo_id"

    @pydantic.field_serializer("entry_repo_id")
    def serialize_entry_repo_id(self, entry_repo_id: UniqueId, _info) -> str:  # noqa: PLR6301
        """Serialize id as string."""
        return str(entry_repo_id)

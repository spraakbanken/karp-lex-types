import pytest

from karp_lex_types.commands.resource_commands import (
    CreateResource,
    EntityOrResourceIdMixin,
)


class TestEntityOrResourceIdMixin:
    def test_given_both_raises_value_error(self):
        with pytest.raises(ValueError):  # noqa: PT011
            EntityOrResourceIdMixin(
                resource_id="abc", id="01GSAHD0K063FBMFE19BFDM4E9", user="test"
            )

    def test_given_either_raises_value_error(self):
        with pytest.raises(ValueError):  # noqa: PT011
            EntityOrResourceIdMixin(user="test")

    def test_both_given_none_raises_value_error(self):
        with pytest.raises(ValueError):  # noqa: PT011
            EntityOrResourceIdMixin(resource_id=None, user="test")


class TestCreateResource:
    def test_from_dict_works(self) -> None:
        cmd = CreateResource.from_dict(
            {
                "resource_id": "abc",
                "resource_name": "Abc",
            },
        )
        assert cmd.cmdtype == "create_resource"

import pytest
from karp_lex_types.commands.resource_commands import (
    CreateResource,
    EntityOrResourceIdMixin,
)


class TestEntityOrResourceIdMixin:
    def test_given_both_raises_value_error(self):  # noqa: PLR6301
        with pytest.raises(ValueError):  # noqa: PT011
            EntityOrResourceIdMixin(
                resourceId="abc",
                id="01GSAHD0K063FBMFE19BFDM4E9",
            )

    def test_given_either_raises_value_error(self):  # noqa: PLR6301
        with pytest.raises(ValueError):  # noqa: PT011
            EntityOrResourceIdMixin()

    def test_both_given_none_raises_value_error(self):  # noqa: PLR6301
        with pytest.raises(ValueError):  # noqa: PT011
            EntityOrResourceIdMixin(
                resourceId=None,
                entityId=None,
            )


class TestCreateResource:
    def test_from_dict_works(self) -> None:  # noqa: PLR6301
        cmd = CreateResource.from_dict(
            {
                "resource_id": "abc",
                "resource_name": "Abc",
            },
            entry_repo_id="01GSAHD0K063FBMFE19BFDM4E9",
        )
        assert cmd.cmdtype == "create_resource"

from datetime import datetime

import pytest

from karp_lex_types.value_objects import UniqueId, make_unique_id


def test_unique_ids_are_sortable():
    assert make_unique_id() > make_unique_id(datetime(1999, 12, 31))


class TestUniqueId:
    def test_bad_input_raises_value_error(self) -> None:
        with pytest.raises(ValueError):  # noqa: PT011
            UniqueId("not-an-ulid")  # ty: ignore[invalid-argument-type]

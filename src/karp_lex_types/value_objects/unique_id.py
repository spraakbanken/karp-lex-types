"""Handle of unique ids."""

import datetime

import ulid

UniqueId = ulid.ULID


def make_unique_id(
    t: float | datetime.datetime | None = None,
) -> UniqueId:
    """Generate an UniqueId that are sortable.

    >>> from karp_lex_types.value_objects import make_unique_id
    >>> from datetime import datetime
    >>> old_id = make_unique_id(datetime(1999,12,31,23,59,59))
    >>> make_unique_id() > old_id
    True:w

    """
    val = t.timestamp() if isinstance(t, datetime.datetime) else t
    return ulid.ULID() if val is None else ulid.ULID.from_timestamp(val)


LEN_OF_ULID: int = 26

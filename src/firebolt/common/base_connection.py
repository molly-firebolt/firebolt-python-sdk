from typing import Any, List

from firebolt.common.base_cursor import BaseCursor
from firebolt.utils.exception import ConnectionClosedError


class BaseConnection:
    def __init__(self) -> None:
        self._cursors: List[Any] = []
        self._is_closed = False

    def _remove_cursor(self, cursor: BaseCursor) -> None:
        # This way it's atomic
        try:
            self._cursors.remove(cursor)
        except ValueError:
            pass

    @property
    def _is_system(self) -> bool:
        """`True` if connection is a system engine connection; `False` otherwise."""
        return self._system_engine_connection is None  # type: ignore

    @property
    def closed(self) -> bool:
        """`True` if connection is closed; `False` otherwise."""
        return self._is_closed

    def commit(self) -> None:
        """Does nothing since Firebolt doesn't have transactions."""

        if self.closed:
            raise ConnectionClosedError("Unable to commit: Connection closed.")

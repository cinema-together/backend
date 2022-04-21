from typing import Any

import bugbear


class Extension(object):
    """Разрешает использовать Depends в значении параметра."""

    name = 'bugbear_fastapi_depends'
    version = 1

    def __init__(self, noqa: Any) -> None:
        super().__init__()


bugbear.B008.immutable_calls.update([
    'fastapi.Depends',
    'fastapi.params.Depends',
    'Depends',
])

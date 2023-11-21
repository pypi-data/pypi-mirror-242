from typing import Optional, Dict

import polars as pl


@dataclass(frozen=True)
class Key:
    dim: str
    key: str


class StarFrame:
    facts: Optional[pl.DataFrame] = None
    dims: Dict[str, pl.DataFrame] = {}
    keys: Dict[str, Key] = {}
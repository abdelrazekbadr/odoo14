from typing import Any, Optional

unsafe_eval = eval
_logger: Any

class ormcache_counter:
    __slots__: Any = ...
    hit: int = ...
    miss: int = ...
    err: int = ...
    def __init__(self) -> None: ...
    @property
    def ratio(self): ...

STAT: Any

class ormcache:
    args: Any = ...
    skiparg: Any = ...
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
    method: Any = ...
    def __call__(self, method: Any): ...
    key: Any = ...
    def determine_key(self): ...
    def lru(self, model: Any): ...
    def lookup(self, method: Any, *args: Any, **kwargs: Any): ...
    def clear(self, model: Any, *args: Any) -> None: ...

class ormcache_context(ormcache):
    keys: Any = ...
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
    key: Any = ...
    def determine_key(self) -> None: ...

class ormcache_multi(ormcache):
    multi: Any = ...
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
    key_multi: Any = ...
    multi_pos: Any = ...
    def determine_key(self) -> None: ...
    def lookup(self, method: Any, *args: Any, **kwargs: Any): ...

class dummy_cache:
    def __init__(self, *l: Any, **kw: Any) -> None: ...
    def __call__(self, fn: Any): ...
    def clear(self, *l: Any, **kw: Any) -> None: ...

def log_ormcache_stats(sig: Optional[Any] = ..., frame: Optional[Any] = ...): ...
def get_cache_key_counter(bound_method: Any, *args: Any, **kwargs: Any): ...
cache = ormcache

from functools import lru_cache
from typing import TYPE_CHECKING, Callable, Type, TypeVar

from httpx import URL

T = TypeVar("T")


def cached_property(func: Callable[..., T]) -> T:
    """cached_property implementation for 3.7 backward compatibility.

    Args:
        func (Callable): Property getter

    Returns:
        T: Property of type, returned by getter
    """
    return property(lru_cache()(func))  # type: ignore


def prune_dict(d: dict) -> dict:
    """Prune items from dictionaries where value is None.

    Args:
        d (dict): Dict to prune

    Returns:
        dict: Pruned dict
    """
    return {k: v for k, v in d.items() if v is not None}


TMix = TypeVar("TMix")


def mixin_for(baseclass: Type[TMix]) -> Type[TMix]:
    """Define mixin with baseclass typehint.

    Should be used as a mixin base class to fix typehints.

    Args:
        baseclass (Type[TMix]): Class which mixin will be made for

    Returns:
        Type[TMix]: Mixin type to inherit from

    Examples:
        ```
        class ReadonlyMixin(mixin_for(BaseClass))):
            ...
        ```

    """
    if TYPE_CHECKING:
        return baseclass
    return object


def fix_url_schema(url: str) -> str:
    """Add schema to URL if it's missing.

    Args:
        url (str): URL to check

    Returns:
        str: URL with schema present

    """
    return url if url.startswith("http") else f"https://{url}"


def get_auth_endpoint(api_endpoint: URL) -> URL:
    """Create auth endpoint from api endpoint.

    Args:
        api_endpoint (URL): provided API endpoint

    Returns:
        URL: authentication endpoint
    """
    return api_endpoint.copy_with(
        host=".".join(["id"] + api_endpoint.host.split(".")[1:])
    )


def merge_urls(base: URL, merge: URL) -> URL:
    """Merge a base and merge urls.

    If merge is not a relative url, do nothing

    Args:
        base (URL): Base URL to merge to
        merge (URL): URL to merge

    Returns:
        URL: Resulting URL
    """
    if merge.is_relative_url:
        merge_raw_path = base.raw_path + merge.raw_path.lstrip(b"/")
        return base.copy_with(raw_path=merge_raw_path)
    return merge

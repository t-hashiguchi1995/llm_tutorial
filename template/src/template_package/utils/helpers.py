"""Utility helper functions."""

import json
from collections.abc import Mapping
from pathlib import Path
from typing import TypeVar

from ..types import JSONObject, JSONValue
from ..utils.logging_config import get_logger

T = TypeVar("T")

# モジュールレベルのロガー
logger = get_logger(__name__)


def load_json_file(filepath: str | Path) -> JSONObject:
    """Load JSON data from a file.

    Parameters
    ----------
    filepath : str | Path
        Path to JSON file

    Returns
    -------
    JSONObject
        Loaded JSON data as a dictionary

    Raises
    ------
    FileNotFoundError
        If file doesn't exist
    ValueError
        If file contains invalid JSON
    """
    path = Path(filepath)
    logger.debug(f"Loading JSON file from: {path}")

    if not path.exists():
        logger.error(f"File not found: {path}")
        raise FileNotFoundError(f"File not found: {path}")

    try:
        logger.debug(f"Opening file: {path}")
        with path.open("r", encoding="utf-8") as f:
            result = json.load(f)
            logger.debug(f"Successfully loaded JSON data from {path}")

            # json.load returns Any, but we expect dict[str, Any]
            if not isinstance(result, dict):
                type_name = type(result).__name__
                logger.error(
                    f"Invalid JSON structure in {path}: expected object, "
                    f"got {type_name}"
                )
                raise ValueError(f"Expected JSON object in {path}, got {type_name}")

            logger.debug(f"JSON object contains {len(result)} keys")
            return result
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON from {path}: {e}")
        raise ValueError(f"Invalid JSON in {path}: {e}") from e


def save_json_file(
    data: JSONObject,
    filepath: str | Path,
    *,
    indent: int = 2,
    ensure_ascii: bool = False,
) -> None:
    """Save data to a JSON file.

    Parameters
    ----------
    data : JSONObject
        JSON-compatible dictionary to save
    filepath : str | Path
        Path to save to
    indent : int
        JSON indentation level
    ensure_ascii : bool
        Whether to escape non-ASCII characters
    """
    path = Path(filepath)
    logger.debug(
        f"Saving JSON data to: {path} (indent={indent}, ensure_ascii={ensure_ascii})"
    )

    # ディレクトリが存在しない場合は作成
    if not path.parent.exists():
        logger.debug(f"Creating directory: {path.parent}")
    path.parent.mkdir(parents=True, exist_ok=True)

    logger.debug(f"Writing {len(data)} keys to {path}")
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=indent, ensure_ascii=ensure_ascii)
    logger.info(f"Successfully saved JSON file to {path}")


def chunk_list(items: list[T], chunk_size: int) -> list[list[T]]:
    """Split a list into chunks of specified size.

    Parameters
    ----------
    items : list[T]
        Items to chunk
    chunk_size : int
        Size of each chunk

    Returns
    -------
    list[list[T]]
        List of chunks

    Raises
    ------
    ValueError
        If chunk_size is not positive

    Examples
    --------
    >>> chunk_list([1, 2, 3, 4, 5], 2)
    [[1, 2], [3, 4], [5]]
    """
    logger.debug(
        f"Chunking list of {len(items)} items into chunks of size {chunk_size}"
    )

    if chunk_size <= 0:
        logger.error(f"Invalid chunk_size: {chunk_size}")
        raise ValueError(f"chunk_size must be positive, got {chunk_size}")

    chunks = [items[i : i + chunk_size] for i in range(0, len(items), chunk_size)]
    logger.debug(f"Created {len(chunks)} chunks from {len(items)} items")

    return chunks


def flatten_dict(
    nested_dict: Mapping[str, JSONValue],
    *,
    separator: str = ".",
    prefix: str = "",
) -> Mapping[str, JSONValue]:
    """Flatten a nested dictionary.

    Parameters
    ----------
    nested_dict : dict[str, JSONValue]
        Dictionary with JSON-compatible values to flatten
    separator : str
        Separator for keys
    prefix : str
        Prefix for all keys

    Returns
    -------
    Mapping[str, JSONValue]
        Flattened dictionary with dot-notation keys

    Examples
    --------
    >>> flatten_dict({"a": {"b": 1, "c": 2}})
    {"a.b": 1, "a.c": 2}
    """
    logger.debug(
        f"Flattening dictionary with {len(nested_dict)} keys, "
        f"separator={separator!r}, prefix={prefix!r}"
    )

    items: list[tuple[str, JSONValue]] = []

    for key, value in nested_dict.items():
        new_key = f"{prefix}{separator}{key}" if prefix else key
        logger.debug(f"Processing key: {key!r} -> {new_key!r}")

        if isinstance(value, dict):
            logger.debug(f"Key {key!r} contains nested dict with {len(value)} keys")
            items.extend(
                flatten_dict(value, separator=separator, prefix=new_key).items()
            )
        else:
            items.append((new_key, value))

    result = dict(items)
    logger.debug(f"Flattened dictionary: {len(nested_dict)} keys -> {len(result)} keys")

    return result

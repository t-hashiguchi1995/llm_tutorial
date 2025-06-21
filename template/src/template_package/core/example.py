"""Example module demonstrating best practices."""

from dataclasses import dataclass
from typing import Any, Protocol

from ..types import ItemDict
from ..utils.logging_config import get_logger

# モジュールレベルのロガー
logger = get_logger(__name__)


class DataProcessor(Protocol):
    """Protocol for data processors."""

    def process(self, data: list[ItemDict]) -> list[ItemDict]:
        """Process a list of data items."""
        ...


@dataclass
class ExampleConfig:
    """Configuration for ExampleClass."""

    name: str
    max_items: int = 100
    enable_validation: bool = True

    def __post_init__(self) -> None:
        """Validate configuration after initialization."""
        logger.debug(
            f"Initializing ExampleConfig with name={self.name!r}, "
            f"max_items={self.max_items}"
        )
        if self.max_items <= 0:
            logger.error(f"Invalid max_items value: {self.max_items}")
            raise ValueError(f"max_items must be positive, got {self.max_items}")
        logger.debug("ExampleConfig validation completed successfully")


class ExampleClass:
    """Example class demonstrating type hints and documentation.

    This class shows how to properly structure a Python class with:
    - Type hints for all methods
    - Comprehensive docstrings
    - Proper error handling

    Attributes
    ----------
    config : ExampleConfig
        Configuration for this instance
    data : list[dict[str, Any]]
        Internal data storage

    Examples
    --------
    >>> config = ExampleConfig(name="test", max_items=50)
    >>> example = ExampleClass(config)
    >>> example.add_item({"id": 1, "value": "test"})
    >>> len(example)
    1
    """

    def __init__(self, config: ExampleConfig) -> None:
        """Initialize ExampleClass with configuration.

        Parameters
        ----------
        config : ExampleConfig
            Configuration object
        """
        logger.debug(f"Creating ExampleClass instance with config: {config}")
        self.config = config
        self.data: list[ItemDict] = []
        logger.info(
            f"ExampleClass initialized with name={config.name!r}, "
            f"max_items={config.max_items}"
        )

    def add_item(self, item: ItemDict) -> None:
        """Add an item to the internal storage.

        Parameters
        ----------
        item : dict[str, Any]
            Item to add

        Raises
        ------
        ValueError
            If max_items limit is reached or validation fails
        """
        logger.debug(f"Adding item: {item}")

        if len(self.data) >= self.config.max_items:
            logger.warning(
                f"Cannot add item: max_items limit ({self.config.max_items}) "
                f"reached. Current items: {len(self.data)}"
            )
            raise ValueError(
                f"Cannot add item: max_items limit ({self.config.max_items}) reached"
            )

        if self.config.enable_validation:
            logger.debug("Validation enabled, validating item")
            self._validate_item(item)

        self.data.append(item)
        logger.debug(f"Item added successfully. Total items: {len(self.data)}")

    def _validate_item(self, item: ItemDict) -> None:
        """Validate an item before adding.

        Parameters
        ----------
        item : dict[str, Any]
            Item to validate

        Raises
        ------
        ValueError
            If item is invalid
        """
        logger.debug(f"Validating item: {item}")

        # Validate required fields
        required_fields = {"id", "name", "value"}
        missing_fields = required_fields - set(item.keys())
        if missing_fields:
            logger.error(
                f"Missing required fields: {missing_fields}. "
                f"Item keys: {list(item.keys())}"
            )
            raise ValueError(f"Missing required fields: {missing_fields}")

        # Check if all required fields have truthy values
        if not all(item.get(field) is not None for field in required_fields):
            logger.error("One or more required fields have None values")
            raise ValueError("Required fields cannot be None")

        logger.debug("Item validation passed")

    def get_items(
        self,
        *,
        filter_key: str | None = None,
        filter_value: Any | None = None,
    ) -> list[ItemDict]:
        """Get items with optional filtering.

        Parameters
        ----------
        filter_key : str | None
            Key to filter by
        filter_value : Any | None
            Value to filter by

        Returns
        -------
        list[dict[str, Any]]
            Filtered items
        """
        logger.debug(
            f"Getting items with filter_key={filter_key!r}, "
            f"filter_value={filter_value!r}"
        )

        if filter_key is None or filter_value is None:
            logger.debug(f"No filter applied, returning all {len(self.data)} items")
            return self.data.copy()

        filtered = [item for item in self.data if item.get(filter_key) == filter_value]
        logger.debug(f"Filter applied: found {len(filtered)} items matching criteria")
        return filtered

    def __len__(self) -> int:
        """Return the number of items."""
        return len(self.data)

    def __repr__(self) -> str:
        """Return string representation."""
        return (
            f"ExampleClass(name={self.config.name!r}, "
            f"items={len(self)}/{self.config.max_items})"
        )


def process_data(
    data: list[ItemDict],
    processor: DataProcessor,
    *,
    validate: bool = True,
) -> list[ItemDict]:
    """Process data using a processor.

    Parameters
    ----------
    data : list[dict[str, Any]]
        Data to process
    processor : DataProcessor
        Processor to use
    validate : bool
        Whether to validate data before processing

    Returns
    -------
    list[dict[str, Any]]
        Processed data

    Raises
    ------
    ValueError
        If validation fails
    """
    logger.debug(f"Processing data with {len(data)} items, validate={validate}")

    if validate and not data:
        logger.error("Data validation failed: empty data provided")
        raise ValueError("Data cannot be empty")

    logger.debug(f"Calling processor: {processor}")
    result = processor.process(data)
    logger.info(
        f"Data processing completed. Input: {len(data)} items, "
        f"Output: {len(result)} items"
    )

    return result

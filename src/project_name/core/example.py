"""Example module with basic functionality."""

import logging
from dataclasses import dataclass
from typing import Any, Protocol

logger = logging.getLogger(__name__)


@dataclass
class ExampleConfig:
    """Configuration for example functionality."""

    name: str
    max_items: int = 100
    enable_validation: bool = True

    def __post_init__(self) -> None:
        """Validate configuration after initialization."""
        if self.max_items <= 0:
            raise ValueError("max_items must be positive")


class DataProcessor(Protocol):
    """Protocol for data processors."""

    def process(self, data: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Process data and return processed result."""
        ...


class ExampleClass:
    """Example class demonstrating the project structure."""

    def __init__(self, config: ExampleConfig) -> None:
        """Initialize with configuration."""
        self.config = config
        self._items: list[dict[str, Any]] = []
        logger.info(f"ExampleClass initialized with config: {config.name}")

    def add_item(self, item: dict[str, Any]) -> None:
        """Add an item to the collection."""
        logger.debug(f"Adding item: {item}")

        if len(self._items) >= self.config.max_items:
            raise ValueError("max_items limit exceeded")

        if self.config.enable_validation:
            required_fields = {"id", "name", "value"}
            if not all(field in item for field in required_fields):
                raise ValueError("Missing required fields: id, name, value")
            if not item.get("name"):
                raise ValueError("name cannot be empty")

        self._items.append(item)
        logger.debug(f"Item added successfully. Total items: {len(self._items)}")

    def get_items(
        self,
        filter_key: str | None = None,
        filter_value: Any = None,
    ) -> list[dict[str, Any]]:
        """Get items with optional filtering."""
        logger.debug(f"Getting items with filter: {filter_key}={filter_value}")

        if filter_key is None:
            return self._items.copy()

        filtered = [
            item for item in self._items if item.get(filter_key) == filter_value
        ]
        logger.debug(f"Filtered {len(self._items)} items to {len(filtered)}")
        return filtered

    def __len__(self) -> int:
        """Return number of items."""
        return len(self._items)

    def __repr__(self) -> str:
        """Return string representation."""
        return (
            f"ExampleClass(name='{self.config.name}', "
            f"items={len(self._items)}/{self.config.max_items})"
        )


def process_data(
    data: list[dict[str, Any]],
    processor: DataProcessor,
    validate: bool = True,
) -> list[dict[str, Any]]:
    """Process data using the provided processor."""
    logger.info(f"Processing {len(data)} items with validation={validate}")

    if validate and not data:
        raise ValueError("Data cannot be empty when validation is enabled")

    result = processor.process(data)
    logger.info(f"Processing completed. {len(result)} items returned")
    return result

"""Logging configuration module with dynamic level switching."""

import logging
import os
import sys
from pathlib import Path
from typing import Any


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance with the specified name.

    Parameters
    ----------
    name : str
        Name of the logger (typically __name__)

    Returns
    -------
    logging.Logger
        Configured logger instance
    """
    return logging.getLogger(name)


def setup_logging(
    *,
    level: str | int = "INFO",
    format_string: str | None = None,
    log_file: str | Path | None = None,
    force: bool = False,
) -> None:
    """Setup logging configuration for the entire application.

    Parameters
    ----------
    level : str | int
        Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        Can also be set via LOG_LEVEL environment variable
    format_string : str | None
        Custom format string for log messages
        If None, uses default format with timestamp, level, name, and message
    log_file : str | Path | None
        Optional file path to write logs to
    force : bool
        Force reconfiguration even if logging is already configured
    """
    # 環境変数からログレベルを取得(優先)
    env_level = os.environ.get("LOG_LEVEL", "").upper()
    if env_level and env_level in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
        level = env_level

    # レベルを正規化
    if isinstance(level, str):
        level = getattr(logging, level.upper(), logging.INFO)

    # デフォルトフォーマット
    if format_string is None:
        format_string = "[%(asctime)s] [%(levelname)8s] [%(name)s] %(message)s"

    # ハンドラーの設定
    handlers: list[logging.Handler] = []

    # コンソールハンドラー
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(logging.Formatter(format_string))
    handlers.append(console_handler)

    # ファイルハンドラー(指定された場合)
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_path, encoding="utf-8")
        file_handler.setLevel(level)
        file_handler.setFormatter(logging.Formatter(format_string))
        handlers.append(file_handler)

    # ロギング設定
    logging.basicConfig(
        level=level,
        format=format_string,
        handlers=handlers,
        force=force,
    )

    # サードパーティライブラリのログレベルを調整
    if level > logging.DEBUG:
        # DEBUG以外の場合は、外部ライブラリのログを抑制
        logging.getLogger("urllib3").setLevel(logging.WARNING)
        logging.getLogger("asyncio").setLevel(logging.WARNING)
        logging.getLogger("filelock").setLevel(logging.WARNING)


def set_log_level(level: str | int, logger_name: str | None = None) -> None:
    """Dynamically change the log level for a specific logger or all loggers.

    Parameters
    ----------
    level : str | int
        New logging level
    logger_name : str | None
        Name of the logger to update. If None, updates root logger
    """
    if isinstance(level, str):
        level = getattr(logging, level.upper(), logging.INFO)

    if logger_name:
        logger = logging.getLogger(logger_name)
        logger.setLevel(level)
        # ハンドラーのレベルも更新
        for handler in logger.handlers:
            handler.setLevel(level)
    else:
        # ルートロガーとすべてのハンドラーを更新
        root_logger = logging.getLogger()
        root_logger.setLevel(level)
        for handler in root_logger.handlers:
            handler.setLevel(level)


def log_function_call(logger: logging.Logger) -> Any:
    """Decorator to log function calls with arguments and return values.

    Parameters
    ----------
    logger : logging.Logger
        Logger instance to use

    Returns
    -------
    Callable
        Decorated function
    """

    def decorator(func: Any) -> Any:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # 関数呼び出しをログ
            func_name = func.__name__
            logger.debug(f"Calling {func_name} with args={args!r}, kwargs={kwargs!r}")

            try:
                # 関数実行
                result = func(*args, **kwargs)
                # 戻り値をログ
                logger.debug(f"{func_name} returned: {result!r}")
                return result
            except Exception as e:
                # エラーをログ
                logger.error(
                    f"{func_name} raised {type(e).__name__}: {e}", exc_info=True
                )
                raise

        return wrapper

    return decorator


# 開発時のデフォルト設定(環境変数で上書き可能)
if os.environ.get("PROJECT_ENV") == "development":
    setup_logging(level="DEBUG")

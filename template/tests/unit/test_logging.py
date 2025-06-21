"""Unit tests for logging functionality."""

import logging
from typing import Any

import pytest
from template_package.core.example import ExampleClass, ExampleConfig
from template_package.utils.helpers import (
    chunk_list,
    flatten_dict,
    load_json_file,
    save_json_file,
)
from template_package.utils.logging_config import get_logger


class TestLogging:
    """Test logging functionality."""

    def test_正常系_ログレベルをDEBUGに設定できる(
        self,
        capture_logs: pytest.LogCaptureFixture,
        set_test_log_level: Any,
    ) -> None:
        """ログレベルをDEBUGに設定してメッセージが記録されることを確認。"""
        # ログレベルをDEBUGに設定
        set_test_log_level("DEBUG")

        # テスト用のロガーを取得
        logger = get_logger("test_logger")

        # 各レベルのログを出力
        logger.debug("Debug message")
        logger.info("Info message")
        logger.warning("Warning message")
        logger.error("Error message")

        # すべてのログが記録されていることを確認
        assert len(capture_logs.records) >= 4
        messages = [r.message for r in capture_logs.records]
        assert "Debug message" in messages
        assert "Info message" in messages
        assert "Warning message" in messages
        assert "Error message" in messages

    def test_正常系_ログレベルをINFOに設定できる(
        self,
        capture_logs: pytest.LogCaptureFixture,
        set_test_log_level: Any,
    ) -> None:
        """ログレベルをINFOに設定してDEBUGメッセージが記録されないことを確認。"""
        # ログレベルをINFOに設定
        set_test_log_level("INFO")

        # テスト用のロガーを取得
        logger = get_logger("test_logger")

        # 各レベルのログを出力
        logger.debug("Debug message")
        logger.info("Info message")
        logger.warning("Warning message")

        # DEBUGログは記録されないことを確認
        messages = [r.message for r in capture_logs.records if r.name == "test_logger"]
        assert "Debug message" not in messages
        assert any("Info message" in msg for msg in messages)
        assert any("Warning message" in msg for msg in messages)

    def test_正常系_ExampleClassのログが記録される(
        self,
        capture_logs: pytest.LogCaptureFixture,
        example_config: ExampleConfig,
    ) -> None:
        """ExampleClassの操作でDEBUGログが記録されることを確認。"""
        # DEBUGレベルで記録
        capture_logs.set_level(logging.DEBUG)

        # ExampleClassのインスタンスを作成
        instance = ExampleClass(example_config)

        # アイテムを追加
        item = {"id": 1, "name": "test", "value": 100}
        instance.add_item(item)

        # ログメッセージを確認
        log_messages = [r.message for r in capture_logs.records]

        # 初期化ログ
        assert any("Creating ExampleClass instance" in msg for msg in log_messages)
        assert any("ExampleClass initialized" in msg for msg in log_messages)

        # アイテム追加ログ
        assert any("Adding item:" in msg for msg in log_messages)
        assert any("Item added successfully" in msg for msg in log_messages)

    def test_正常系_helpersモジュールのログが記録される(
        self,
        capture_logs: pytest.LogCaptureFixture,
        temp_dir: Any,
    ) -> None:
        """helpersモジュールの関数でDEBUGログが記録されることを確認。"""
        # DEBUGレベルで記録
        capture_logs.set_level(logging.DEBUG)

        # JSONファイルの保存と読み込み
        test_data = {"key": "value", "number": 42}
        json_path = temp_dir / "test.json"

        save_json_file(test_data, json_path)
        _ = load_json_file(json_path)

        # ログメッセージを確認
        log_messages = [r.message for r in capture_logs.records]

        # 保存ログ
        assert any("Saving JSON data to:" in msg for msg in log_messages)
        assert any("Successfully saved JSON file" in msg for msg in log_messages)

        # 読み込みログ
        assert any("Loading JSON file from:" in msg for msg in log_messages)
        assert any("Successfully loaded JSON data" in msg for msg in log_messages)

    def test_正常系_エラー時のログが記録される(
        self,
        capture_logs: pytest.LogCaptureFixture,
        example_config: ExampleConfig,
    ) -> None:
        """エラー発生時に適切なログが記録されることを確認。"""
        # DEBUGレベルで記録
        capture_logs.set_level(logging.DEBUG)

        # 最大数を1に設定
        example_config.max_items = 1
        instance = ExampleClass(example_config)

        # 1つ目のアイテムを追加(成功)
        instance.add_item({"id": 1, "name": "item1", "value": 10})

        # 2つ目のアイテムを追加(失敗)
        with pytest.raises(ValueError):
            instance.add_item({"id": 2, "name": "item2", "value": 20})

        # エラーログを確認
        log_messages = [r.message for r in capture_logs.records]
        assert any("Cannot add item: max_items limit" in msg for msg in log_messages)

    def test_正常系_chunk_listのログが記録される(
        self,
        capture_logs: pytest.LogCaptureFixture,
    ) -> None:
        """chunk_list関数のDEBUGログが記録されることを確認。"""
        # DEBUGレベルで記録
        capture_logs.set_level(logging.DEBUG)

        # リストをチャンク化
        items = list(range(10))
        _ = chunk_list(items, 3)

        # ログメッセージを確認
        log_messages = [r.message for r in capture_logs.records]
        assert any("Chunking list of 10 items" in msg for msg in log_messages)
        assert any("Created 4 chunks" in msg for msg in log_messages)

    def test_正常系_flatten_dictのログが記録される(
        self,
        capture_logs: pytest.LogCaptureFixture,
    ) -> None:
        """flatten_dict関数のDEBUGログが記録されることを確認。"""
        # DEBUGレベルで記録
        capture_logs.set_level(logging.DEBUG)

        # 辞書をフラット化
        nested = {"a": {"b": 1, "c": {"d": 2}}}
        flattened = flatten_dict(nested)

        # ログメッセージを確認
        log_messages = [r.message for r in capture_logs.records]
        assert any("Flattening dictionary" in msg for msg in log_messages)
        assert any(
            "Flattened dictionary: 1 keys -> 2 keys" in msg for msg in log_messages
        )

        # 結果が正しいことも確認
        assert flattened == {"a.b": 1, "a.c.d": 2}

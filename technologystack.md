# **LLM機能モジュール開発 技術スタック (Hydra, .env, Flask WebSocket対応)**

## **コア技術**

* **プログラミング言語**: Python (バージョン 3.9 以降を推奨)  
* **主要LLM API**:  
  * OpenAI API (Chat Completions, Embeddings)  
    * gpt-4o-mini (推奨モデル例)  
    * text-embedding-3-small (推奨モデル例)  
  * Anthropic Claude API (Messages API)  
    * claude-3-opus-20240229 (推奨モデル例)  
    * API Version: 2023-06-01 (設計書記載の調査結果に基づく想定)  
  * Google Gemini API  
    * gemini-1.5-pro-latest (推奨モデル例)  
    * gemini-1.5-flash-latest (推奨モデル例)  
    * (Embeddingモデルも適宜追加: 例 text-embedding-004)  
  * Ollama API (generate, chat, embeddings)  
    * (ローカルで利用するモデルに依存)

## **主要ライブラリ**

* **Webフレームワーク / WebSocket**:  
  * Flask  
  * Flask-SocketIO (FlaskでWebSocketを扱うための推奨ライブラリ)  
* **設定管理**:  
  * hydra-core (パラメータ管理用)  
  * python-dotenv (APIキーなどの秘匿情報管理用)  
* **HTTP通信**: requests (バージョン 2.25.1 以降)  
* **Google API Client Library (Gemini用)**: google-generativeai (推奨)  
* **数値計算 (ベクトル演算など)**: numpy  
* **(オプション) 非同期処理**: asyncio, aiohttp (Flask-SocketIOは eventlet や gevent との組み合わせも一般的です)

## **開発・テストツール**

* **パッケージ管理・仮想環境**: uv  
* **テストフレームワーク**: pytest  
* **リンター・フォーマッター**: ruff (または flake8, black, isort など)

## **モジュール構成とバージョン管理**

### **重要な制約事項**

* **LLM APIクライアントの一元管理**:  
  * 各LLMプロバイダーとの通信は、llm\_router.core.clients 配下の専用クライアントモジュール (openai\_client.py, anthropic\_client.py, gemini\_client.py, ollama\_client.py) で一元的に処理します。  
  * これらのクライアントは、llm\_router.core.clients.base\_client.py を基底とし、共通処理を継承します (Gemini Clientは公式ライブラリ利用も検討)。  
* **設定情報の管理**:  
  * **パラメータ管理 (Hydra)**: モデル名、エンドポイントURL、サーバー設定、各種処理の挙動を制御するパラメータ等は、Hydraを用いてYAMLファイル (llm\_router/config/hydra\_conf/ 配下) で管理します。Hydraの構造化設定 (Structured Configs) の利用を推奨します。  
  * **秘匿情報管理 (.env)**: APIキー、データベース接続情報、Flaskの SECRET\_KEY などの秘匿情報は、プロジェクトルートの .env ファイルで管理し、python-dotenv を使って読み込みます。  
  * **設定アクセス**: llm\_router.config.settings.py は、Hydraによってロードされた設定オブジェクトや、.env から読み込まれた秘匿情報への統一的なアクセスポイントを提供する役割を担うことができます。  
* **スキーマ定義の一元管理**:  
  * 各モジュールで使用するデータ構造（メッセージ、ツール定義、RAGドキュメント、リアルタイム通信メッセージなど）は、各サブパッケージ内の schemas.py ファイルで dataclasses や TypedDict を用いて定義します。  
  * 例: llm\_router.core.schemas.common.py, llm\_router.rag.schemas.py, llm\_router.core.schemas.gemini\_schemas.py, llm\_router.realtime.schemas.py  
* **変更管理**:  
  * 以下のコアファイル群の変更には、慎重なレビューと承認プロセスを推奨します。  
    * app.py (Flaskアプリケーションエントリポイント、Hydra初期化を含む可能性)  
    * llm\_router/core/clients/base\_client.py (全APIクライアントの基礎)  
    * llm\_router/config/settings.py (設定情報へのアクセサー)  
    * llm\_router/config/hydra\_conf/ 内の主要な設定ファイル  
    * 各 schemas.py ファイル (モジュール間インターフェースの基礎)  
    * llm\_router/realtime/routes.py (WebSocketイベントハンドラ定義)

### **実装規則**

* **LLM APIのバージョンとモデル**:  
  * 利用するLLMのモデル名やAPIバージョンに関する情報は、原則としてHydraの設定ファイル (llm\_router/config/hydra\_conf/) で管理し、各クライアントはこれらの設定値を参照して動作します。  
  * 特定のAPIバージョンに依存する処理が必要な場合は、クライアントモジュール内で適切に分岐・処理します。  
* **型定義の参照**:  
  * モジュール間でデータをやり取りする際は、必ず共有された schemas.py 内の型定義を利用します。  
* **設定値の利用**:  
  * パラメータはHydraを通じて取得します。  
  * APIキーなどの秘匿情報は、.env からロードされた値を llm\_router.config.settings.py などを経由して安全に取得します。コード内への直接埋め込みは禁止します。
* **DocStringと可読性**:
  * 実装する関数やクラスには必ず日本語でDocStringを記入すること。また、コードの処理は可能な限り複雑化させず、可読性を持たせること。処理を複雑化せざるを得ない場合は、必ずコードのディレクトリ直下にReadmeを作成し、処理のフローチャートを記入すること。参考にしている実装があれば、必ずコメントに入れること。
* **既存のLLMラッパーのモジュールの禁止**:
  * 実装にあたって、既存のLLMラッパーのモジュールを利用することを禁止します。（langchainやlitellmなど）
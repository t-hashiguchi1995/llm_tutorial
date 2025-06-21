# **LLM機能モジュール開発 ディレクトリ構成 (Hydra, .env, Flask WebSocket対応)**

以下のディレクトリ構造に従って実装を行ってください。

/  
├── app.py                        \# Flaskアプリケーションのエントリポイント (Hydra初期化もここで行う想定)  
├── llm\_router/                   \# Pythonモジュールのルートディレクトリ  
│   ├── \_\_init\_\_.py               \# llm\_routerパッケージの初期化ファイル  
│   ├── facade.py                 \# アプリケーション向け統一インターフェース  
│   │  
│   ├── core/                     \# LLMコア機能  
│   │   ├── \_\_init\_\_.py  
│   │   ├── clients/              \# 各LLM APIクライアント  
│   │   │   ├── \_\_init\_\_.py  
│   │   │   ├── base\_client.py    \# 全APIクライアントの基底クラス  
│   │   │   ├── openai\_client.py  \# OpenAI APIクライアント  
│   │   │   ├── anthropic\_client.py \# Anthropic APIクライアント  
│   │   │   ├── gemini\_client.py  \# Google Gemini APIクライアント  
│   │   │   └── ollama\_client.py  \# Ollama APIクライアント  
│   │   ├── templating/           \# プロンプトテンプレートエンジン  
│   │   │   ├── \_\_init\_\_.py  
│   │   │   └── engine.py  
│   │   └── schemas/              \# コア機能関連のスキーマ定義  
│   │       ├── \_\_init\_\_.py  
│   │       ├── common.py         \# 共通スキーマ (Message, Roleなど)  
│   │       ├── openai\_schemas.py  
│   │       ├── anthropic\_schemas.py  
│   │       ├── gemini\_schemas.py  
│   │       └── ollama\_schemas.py  
│   │  
│   ├── memory/                   \# 会話メモリ管理機能  
│   │   ├── \_\_init\_\_.py  
│   │   ├── buffer.py             \# 会話バッファ  
│   │   ├── window\_manager.py     \# コンテキストウィンドウ管理  
│   │   ├── summarizer.py         \# 会話要約機能 (オプション)  
│   │   └── schemas.py            \# 会話メモリ関連のスキーマ定義  
│   │  
│   ├── rag/                      \# RAG (Retrieval Augmented Generation) パイプライン  
│   │   ├── \_\_init\_\_.py  
│   │   ├── loaders/              \# ドキュメントローダー  
│   │   │   ├── \_\_init\_\_.py  
│   │   │   └── text\_loader.py  
│   │   ├── splitters/            \# テキストスプリッター  
│   │   │   ├── \_\_init\_\_.py  
│   │   │   └── recursive\_splitter.py  
│   │   ├── embeddings.py         \# 埋め込み生成ラッパー  
│   │   ├── vector\_stores/        \# ベクトルストア  
│   │   │   ├── \_\_init\_\_.py  
│   │   │   └── in\_memory\_store.py  
│   │   ├── retriever.py          \# リトリーバー  
│   │   ├── augmenter.py          \# プロンプトオーグメンタ  
│   │   └── schemas.py            \# RAG関連のスキーマ定義  
│   │  
│   ├── agents/                   \# エージェントフレームワーク  
│   │   ├── \_\_init\_\_.py  
│   │   ├── react\_loop.py         \# ReActループ実装  
│   │   ├── tools/                \# ツール定義・ディスパッチ  
│   │   │   ├── \_\_init\_\_.py  
│   │   │   ├── definition.py     \# ツールスキーマ定義  
│   │   │   └── dispatcher.py     \# ツール実行ディスパッチャ  
│   │   ├── parsers/              \# LLM出力パーサー  
│   │   │   ├── \_\_init\_\_.py  
│   │   │   └── output\_parser.py  
│   │   └── schemas.py            \# エージェント関連のスキーマ定義  
│   │  
│   ├── protocols/                \# MCP/A2Aプロトコル連携  
│   │   ├── \_\_init\_\_.py  
│   │   ├── mcp/                  \# Model Context Protocol  
│   │   │   ├── \_\_init\_\_.py  
│   │   │   ├── client.py  
│   │   │   ├── server.py  
│   │   │   └── schemas.py  
│   │   └── a2a/                  \# Agent-to-Agent Protocol  
│   │       ├── \_\_init\_\_.py  
│   │       ├── client.py  
│   │       ├── server.py  
│   │       └── schemas.py  
│   │  
│   ├── realtime/                 \# WebSocketリアルタイム処理機能 (Flask連携)  
│   │   ├── \_\_init\_\_.py  
│   │   ├── routes.py             \# Flask BlueprintやSocket.IOイベントハンドラ  
│   │   ├── manager.py            \# 接続管理、ブロードキャストなど  
│   │   ├── processor.py          \# リアルタイム処理ロジック  
│   │   └── schemas.py            \# リアルタイム通信用メッセージスキーマ  
│   │  
│   ├── utils/                    \# 共通ユーティリティ  
│   │   ├── \_\_init\_\_.py  
│   │   ├── http\_utils.py         \# HTTP通信補助  
│   │   ├── error\_handling.py     \# エラーハンドリング  
│   │   └── token\_utils.py        \# トークンカウント補助  
│   │  
│   └── config/                   \# ★ 設定管理 (Hydra \+ .env)  
│       ├── \_\_init\_\_.py  
│       ├── settings.py           \# ★ Hydra設定オブジェクトや.env値へのアクセサー  
│       └── hydra\_conf/           \# ★ Hydra設定ファイルディレクトリ  
│           ├── config.yaml       \# ★ Hydraのメイン設定ファイル  
│           ├── llm/              \# LLM関連設定の例  
│           │   ├── openai.yaml  
│           │   ├── anthropic.yaml  
│           │   ├── gemini.yaml  
│           │   └── ollama.yaml  
│           ├── server/           \# サーバー関連設定の例  
│           │   └── flask.yaml  
│           └── rag/              \# RAG関連設定の例  
│               └── default.yaml  
│  
├── tests/                        \# テストコード  
│   ├── \_\_init\_\_.py  
│   ├── conftest.py               \# pytest共通設定・フィクスチャ  
│   ├── core/  
│   │   ├── \_\_init\_\_.py  
│   │   ├── clients/  
│   │   │   ├── \_\_init\_\_.py  
│   │   │   ├── test\_base\_client.py  
│   │   │   ├── test\_openai\_client.py  
│   │   │   \# ... 他のクライアントテスト  
│   │   └── templating/  
│   │       ├── \_\_init\_\_.py  
│   │       └── test\_engine.py  
│   ├── memory/  
│   │   ├── \_\_init\_\_.py  
│   │   ├── test\_buffer.py  
│   │   ├── test\_window\_manager.py  
│   │   └── test\_summarizer.py  
│   ├── rag/  
│   │   ├── \_\_init\_\_.py  
│   │   ├── loaders/  
│   │   │   └── test\_text\_loader.py  
│   │   ├── splitters/  
│   │   │   └── test\_recursive\_splitter.py  
│   │   ├── test\_embeddings.py  
│   │   ├── vector\_stores/  
│   │   │   └── test\_in\_memory\_store.py  
│   │   ├── test\_retriever.py  
│   │   └── test\_augmenter.py  
│   ├── agents/  
│   │   ├── \_\_init\_\_.py  
│   │   ├── test\_react\_loop.py  
│   │   ├── tools/  
│   │   │   ├── test\_definition.py  
│   │   │   └── test\_dispatcher.py  
│   │   └── parsers/  
│   │       └── test\_output\_parser.py  
│   ├── protocols/  
│   │   ├── \_\_init\_\_.py  
│   │   ├── mcp/  
│   │   │   ├── \_\_init\_\_.py  
│   │   │   ├── test\_mcp\_client.py  
│   │   │   └── test\_mcp\_server.py  
│   │   └── a2a/  
│   │       ├── \_\_init\_\_.py  
│   │       ├── test\_a2a\_client.py  
│   │       └── test\_a2a\_server.py  
│   ├── realtime/  
│   │   ├── \_\_init\_\_.py  
│   │   ├── test\_realtime\_routes.py  
│   │   ├── test\_realtime\_manager.py  
│   │   └── test\_realtime\_processor.py  
│   └── utils/  
│       ├── \_\_init\_\_.py  
│       ├── test\_http\_utils.py  
│       └── test\_error\_handling.py  
│  
├── examples/                     \# 利用例を示すサンプルコード  
│   ├── \_\_init\_\_.py  
│   ├── simple\_chat\_example.py  
│   ├── rag\_pipeline\_example.py  
│   ├── basic\_agent\_example.py  
│   ├── mcp\_tool\_usage\_example.py  
│   ├── a2a\_collaboration\_example.py  
│   └── websocket\_client\_example.py  
│  
├── static/                       \# Flask用静的ファイル (オプション)  
│   └── style.css  
├── templates/                    \# Flask用テンプレート (オプション)  
│   └── index.html  
├── pyproject.toml                \# プロジェクト設定ファイル (依存関係、ビルド情報など)  
├── README.md                     \# プロジェクトの説明ファイル  
├── .gitignore                    \# Gitで無視するファイルを指定  
├── .env.example                  \# ★ APIキーなどの秘匿情報用テンプレート  
└── .env                          \# ★ APIキーなどの秘匿情報ファイル (Git管理外)

### **★ Hydra および .env 関連の主な変更点・追加点**

* **llm\_router/config/ ディレクトリの変更**:  
  * settings.py: Pydanticモデルによる設定管理から、Hydraによってロードされた設定オブジェクト (DictConfig) や、python-dotenv で読み込まれた環境変数へのアクセスを提供するモジュールに変更。  
  * hydra\_conf/: Hydraの設定ファイル（.yaml形式）を格納する専用ディレクトリを新設。  
    * config.yaml: Hydraのメインとなる設定ファイル。他の設定ファイルをインクルードしたり、デフォルト値を定義したりします。  
    * サブディレクトリ（例: llm/, server/, rag/）を作成し、関連する設定をグループ化できます。  
* **プロジェクトルートの .env ファイル**:  
  * APIキー、データベース認証情報、Flaskの SECRET\_KEY など、Gitで管理すべきでない秘匿情報を格納します。  
  * .env.example をテンプレートとして提供します。  
* **app.py (Flaskアプリケーションエントリポイント)**:  
  * python-dotenv を使って .env ファイルをロードします。  
  * Hydraの初期化処理（@hydra.main() デコレータなどを使用）をここで行い、設定オブジェクトをアプリケーション全体や各モジュールに渡す起点となります。

### **配置ルール (主要なもの) \- Hydra, .env 関連追記**

* **Flaskアプリケーションエントリーポイント**: プロジェクトルートに app.py を配置。.env のロードとHydraの初期化を含む。  
* **パラメータ設定ファイル (Hydra)**: llm\_router/config/hydra\_conf/ 配下にYAMLファイルとして配置。  
* **秘匿情報設定ファイル**: プロジェクトルートに .env ファイルを配置 (Git管理外)。.env.example をテンプレートとして提供。  
* **設定情報へのアクセス**: llm\_router/config/settings.py を通じて、Hydraの設定オブジェクトや環境変数にアクセスするインターフェースを提供することを検討。  
* **LLM APIクライアント**: llm\_router/core/clients/ 配下に各プロバイダー専用のクライアントを配置。  
* **スキーマ定義**: 各機能モジュール（core, memory, rag, agents, protocols, realtime）の直下に schemas/ ディレクトリを作成し、関連するデータ構造を定義。共通スキーマは llm\_router/core/schemas/common.py に配置。  
* **WebSocket処理ロジック (Flaskベース)**:  
  * ルート/イベントハンドラ: llm\_router/realtime/routes.py  
  * 接続管理・メッセージ送信: llm\_router/realtime/manager.py (Flask-SocketIOの機能を利用)  
  * ビジネスロジック: llm\_router/realtime/processor.py  
* **ユーティリティ関数**: 特定のモジュールに依存しない共通関数は llm\_router/utils/ に配置。  
* **テストコード**: プロジェクトルートの tests/ ディレクトリ以下に、モジュール構造に対応する形で配置。各サブディレクトリにも \_\_init\_\_.py を配置し、テストパッケージとして認識させます。conftest.py に共通のフィクスチャや設定を記述します。  
* **サンプルコード**: プロジェクトルートの examples/ ディレクトリに、モジュールの利用方法を示すサンプルを配置。各サンプルファイルは具体的な機能を示す名称に変更しました。
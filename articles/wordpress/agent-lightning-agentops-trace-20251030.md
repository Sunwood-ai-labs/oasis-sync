---
title: Agent-lightning、AgentOpsでトレース可視化：uv実行クイックスタート
post_status: publish
post_excerpt: Sunwood-ai-labs/agent-lightning の APO サンプルを使い、uv で環境構築して room_selector_apo.py
  を実行し、AgentOps でトレース可視化するまでを最短手順で解説。クローン、依存同期、.env 設定、実行、ダッシュボード確認の流れをシンプルにまとめます。
featured_image: https://raw.githubusercontent.com/Sunwood-ai-labs/oasis-sync/main/images/thumbnails/agent-lightning-agentops-trace-20251030.png
taxonomy:
  category:
  - ai
  - developer-tools
  post_tag:
  - Agent-lightning
  - AgentOps
  - APO
  - uv
  - OpenAI
custom_fields:
  lead: リポジトリのクローンから uv による依存同期、.env 設定、room_selector_apo.py の実行、AgentOps ダッシュボードでの可視化までを最短ルートで案内します。
---

本記事は **Agent-lightning** の APO サンプルを **uv** で実行し、**AgentOpsでトレース可視化** するための最短手順です。クローン → 依存同期 → `.env` 設定 → 実行 → ダッシュボード確認の流れだけに絞っています。

https://x.com/hAru_mAki_ch/status/1983577952731460049

---

## 前提

- **リポジトリ**：<https://github.com/Sunwood-ai-labs/agent-lightning.git>  
- **必須**：`OPENAI_API_KEY`（OpenAI互換API）  
- **推奨**：`AGENTOPS_API_KEY`（AgentOps ダッシュボード可視化）

> `examples/apo/room_selector_apo.py` は **同階層の `.env`** を自動読み込み、AgentOps にトレースを送信します。

---

## クローン

```bash
git clone https://github.com/Sunwood-ai-labs/agent-lightning.git
cd agent-lightning
# 既存クローンは最新化
# git pull --rebase
````

---

## uv で依存関係を同期

`uv sync` はルートの `pyproject.toml` を自動検出します。

```bash
uv sync --extra apo
```

> `uv` 未導入なら `pip install uv`。

---

##  .env を用意（API キー設定）

```bash
cp examples/apo/.env.example examples/apo/.env
```

`examples/apo/.env` を編集：

```env
OPENAI_API_KEY=sk-...      # 必須
AGENTOPS_API_KEY=ao-...    # 推奨（可視化）
```

> **重要**：`.env` は `examples/apo/`（`room_selector_apo.py` と同階層）に置くこと。

---

##  実行（uv 経由）

`examples/apo/` へ移動して実行します。

```bash
cd examples/apo
uv run python room_selector_apo.py
```

実行時の挙動（抜粋）：

* スクリプトの絶対パスを表示
* **10 秒待機**（ログ/環境確認のため）
* `room_tasks.jsonl` を訓練/検証に分割して APO を実行
* `.env` に `AGENTOPS_API_KEY` があれば、**セッションURL** を出力

---

##  AgentOpsでトレース可視化

1. AgentOps にサインインし **API キー** を取得
2. `.env` の `AGENTOPS_API_KEY` に設定済みで再実行
3. 出力された **Session Replay**（セッションURL）を開き、**メッセージ/コスト/ステップ** を確認

---

## 参考コマンド（まとめ）

```bash
# クローン
git clone https://github.com/Sunwood-ai-labs/agent-lightning.git
cd agent-lightning

# 依存同期
uv sync --extra apo

# .env 作成と編集
cp examples/apo/.env.example examples/apo/.env

# 実行
cd examples/apo
uv run python room_selector_apo.py
```

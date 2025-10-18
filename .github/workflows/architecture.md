![Architecture Diagram](./architecture.svg)

## 🏗️ アーキテクチャとワークフロー詳細

このドキュメントは、リポジトリ内の GitHub Actions と補助スクリプトの役割を俯瞰し、モジュールごとの責務とデータフローを整理したものです。トップレベルの概要は `README.md` を参照し、本書では各ワークフローやスクリプトの関係、必要な Secrets/Variables を掘り下げます。

### 全体像

- 上図（[architecture.svg](./architecture.svg)）は「**リリース起点での Gemini 生成パイプライン**」と「**Issue/コメント起点での Oasis 配信パイプライン**」の両輪を示します。
- `docs/flow.dio` には詳細図面（tldraw形式）が含まれており、必要に応じて編集できます。

### モジュール構成

| モジュール | 目的 | 主な責務 |
|------------|------|----------|
| 🟨 **Gemini Actions Labs** | AI を利用した生成・レビュー・周辺自動化 | リリースノート生成、ヘッダー画像生成、ハイブリッド記事生成、PRレビュー、Issue triage、Hugging Face Space へのデプロイ等 |
| 🟧 **Oasis Sync** | Oasis ソースを各配信先に展開 | Issue フォームからの記事・サムネイル生成、Gemini によるメタデータ生成、Zenn/Qiita/WordPress への同期、Qiita CLI 連携 |

---

## 📋 ワークフロー詳細

### 🟨 Gemini Actions Labs Module

#### 📝 `gemini-release-notes.yml`
- **トリガー**: Release Tag (`on: push tags`)
- **役割**:
  1. 差分統計・コード diff・コミット・貢献者情報を収集
  2. Imagen 4 MCP サーバーでヘッダー画像を生成し、リポジトリへコミット
  3. Gemini で Markdown リリースノートを作成し、GitHub Release を更新
  4. 生成画像を Release アセットへアップロード
- **ポイント**:
  - `MAX_DIFF_LINES` / `MAX_DIFF_CHARS` でプロンプト入力を制限
  - 画像生成に失敗した場合でも Release 更新は継続

#### 📰 `gemini-release-articles.yml`
- **トリガー**: `gemini-release-notes.yml` 完了後 (`workflow_run`)
- **役割**:
  1. 生成済みリリースノートと画像 URL を取得
  2. Gemini に Oasis ハイブリッド記事の生成を依頼
  3. `articles/oasis/` に記事をコミット（差分がある場合のみ）
- **出力**: `zenn` / `qiita` / `wordpress` セクション付き front matter と本文の単一 Markdown

#### 💬 `no_workflows/gemini-actions-labs/gemini-cli.yml`
- **トリガー**: Issue/PR コメントで `@gemini-cli`
- **役割**: コメントの意図を解析し、Gemini CLI による回答やコード変更を実行する万能アシスタントワークフロー
- **ポイント**:
  - GitHub App トークン（`vars.APP_ID` + `secrets.APP_PRIVATE_KEY`）を優先利用
  - `build_reviewer_prompt.py` でペルソナ別の応答テンプレートを構築
  - 日本語特化版は `gemini-jp-cli.yml`

#### 🧐 `no_workflows/gemini-actions-labs/pr-review-*.yml`
- **トリガー**: PR Open / Ready for review
- **役割**: 狐崎・鬼塚・雪村といった Persona に合わせたレビューコメントを PR へ投稿
- **ポイント**:
  - `gh pr diff` の抜粋（最大600行）とファイル一覧を Gemini に渡す
  - Persona ごとに専用 PAT (`GH_PAT_KOZAKI` 等) を利用し、投稿者を明確化

#### 🏷️ `no_workflows/gemini-actions-labs/gemini-issue-automated-triage.yml`
- **トリガー**: Issue オープン／再オープン
- **役割**: Issue 本文から推奨ラベルを Gemini が選定し、自動で付与
- **ポイント**: ラベルが存在しない場合は API で作成し、フォールバックとして `status/needs-triage` を付与

#### 🗓️ `no_workflows/gemini-actions-labs/gemini-issue-scheduled-triage.yml`
- **トリガー**: 毎時の cron もしくは手動実行
- **役割**: ラベル未設定／`status/needs-triage` の Issue を一括で再評価
- **ポイント**: Gemini 出力トラブルに備え、JSON パースを多段で保護

#### 🎨 Imagen 生成 (`imagen4-generate-and-commit.yml` / `imagen4-issue-trigger-and-commit.yml`)
- **トリガー**:
  - 手動ディスパッチ（固定プロンプト）
  - Issue/コメントで `/imagen4` コマンド
- **役割**: Imagen MCP サーバーで画像を生成し、`generated-images/` 以下に保存・コミット
- **ポイント**: 成功時/失敗時に Issue やコメントへリアクションを付与し、生成結果を Markdown で通知

#### 🚀 `huggingface-space-deploy.yml`
- **トリガー**: 手動ディスパッチ
- **役割**: Hugging Face API で Space の存在を確認・作成し、指定ディレクトリを Force Push
- **ポイント**: `.github/scripts/ensure_hf_space.py` が Space 情報を `GITHUB_OUTPUT` に書き込む

#### 🌐 `static-site.yml`
- **トリガー**: `main` push / workflow_dispatch
- **役割**: GitHub Pages への静的サイトデプロイ（リポジトリ全体）

---

### 🟧 Oasis Sync Module

#### 🗂️ `oasis-issue-intake.yml`
- **トリガー**: Issue フォーム（`oasis-article` ラベル or `[Oasis]` タイトル）
- **役割**:
  1. ラベルの存在チェック・付与
  2. Issue 本文から front matter と本文、画像を抽出
  3. `articles/oasis/` と `generated-images/issue-<number>-<timestamp>/` へ書き込み
  4. 必要に応じてコミット・pushし、Issue をコメント付きでクローズ
- **使用スクリプト**: `.github/scripts/ingest_oasis_issue.py`

#### 🪄 `oasis-sync.yml`
- **トリガー**: `articles/oasis/**/*.md` の push / 手動実行
- **役割**:
  1. GitHub API で変更ファイルを収集
  2. `process_oasis_articles.py prepare` で Gemini 入力 JSON を生成
  3. Gemini CLI で欠損メタデータを補完（不足時のみ）
  4. `process_oasis_articles.py apply` で Zenn / Qiita / WordPress 形式へ展開
  5. 変更があればコミット・push
- **ポイント**:
  - 既存 front matter に `zenn:` / `qiita:` / `wordpress:` が揃っている場合は Gemini をスキップ
  - WordPress 向け本文はリード画像を除去し、Git it Write 用に整形

#### 📘 `oasis-zenn-sync.yml` / 📗 `oasis-qiita-sync.yml` / 📙 `oasis-wordpress-sync.yml`
- **トリガー**:
  - 各派生ディレクトリへの push
  - `oasis-sync.yml` 完了後 (`workflow_run`)
- **役割**: 各配信先リポジトリに同期 (`TARGET_REPOSITORY`, `TARGET_PATH`, `TARGET_BRANCH`)
- **ポイント**: `.github/scripts/sync_platform.sh` が共通ロジック（clone → copy → commit → push）を担当

#### 🖼️ `thumbnail_ingest_experimental.yml`
- **トリガー**: サムネイル Issue フォーム（`thumbnail-upload` ラベル or `[Thumb]` タイトル）
- **役割**:
  - 添付ファイル、URL、`<img>` タグから画像を取得
  - 任意のリサイズ・レターボックス設定を適用し PNG で保存
  - コミット・pushを実行し、Issue をコメント付きでクローズ
- **使用スクリプト**: `.github/scripts/ingest_thumbnail_issue.py`、`.github/scripts/write_thumbnail_comment.py`

#### 📦 `qiita/publish.yml`
- **トリガー**: `main` / `master` への push、または手動実行
- **役割**: 変更された Qiita 記事のみ `npx qiita publish` で反映
- **ポイント**: 差分検出に `--diff-filter=ACMR` を使用し、credentials.json をその場で生成

---

## 🔗 補助スクリプト / プロンプト

| ファイル | 概要 |
|----------|------|
| `.github/scripts/process_oasis_articles.py` | Oasis 記事のペイロード生成・メタデータ適用。`prepare` と `apply` サブコマンドを提供。 |
| `.github/scripts/ingest_oasis_issue.py` | Issue Body から front matter / 画像を抽出し、Oasis 記事を生成。 |
| `.github/scripts/ingest_thumbnail_issue.py` | 添付・URL 画像を収集して PNG 変換・保存。 |
| `.github/scripts/sync_platform.sh` | 任意の配信先リポジトリへミラーリング。 |
| `.github/scripts/build_reviewer_prompt.py` | PR 情報とペルソナプロンプトを連結。Gemini Reviewer ワークフローで利用。 |
| `.github/prompts/*` | Gemini CLI / Reviewer / Imagen で使用するテンプレート。 |

---

## 🔄 データフロー

### 1️⃣ リリースドリブン生成フロー

```
Tag Push
  ↓
📝 gemini-release-notes.yml
  • 差分取得 & Imagen 生成
  • リリースノートを Release に反映
  ↓
📰 gemini-release-articles.yml (workflow_run)
  • Oasis リリース記事を生成
  • articles/oasis/ にコミット
  ↓
🪄 oasis-sync.yml (push trigger)
  • メタデータ補完 & 分岐
  ↓
📘📗📙 Oasis Zenn / Qiita / WordPress Sync
  • 各ターゲットリポジトリに同期
```

### 2️⃣ Issue ベースの記事生成フロー

```
Issue Submission (📰 Oasis ハイブリッド記事登録)
  ↓
🗂️ oasis-issue-intake.yml
  • front matter / 画像抽出
  • articles/oasis/ + generated-images/ へ保存
  ↓
🪄 oasis-sync.yml
  • Gemini メタデータ補完
  • Zenn / Qiita / WordPress 記事を生成
  ↓
📘📗📙 Sync workflows
  • 各配信先リポジトリへ反映
```

### 3️⃣ サムネイル自動保存フロー

```
Issue Submission (🚧 サムネイル登録)
  ↓
🚧 thumbnail_ingest_experimental.yml
  • 添付/URL/HTML から画像収集
  • リサイズ/レターボックス → PNG 書き出し
  • Issue コメントで結果共有 & クローズ
```

---

## ⏱️ トリガー一覧

| ワークフロー | push | workflow_run | Issue / コメント | manual |
|--------------|------|--------------|-----------------|--------|
| gemini-release-notes.yml | tags | - | - | - |
| gemini-release-articles.yml | - | ✅ | - | - |
| gemini-cli.yml / gemini-jp-cli.yml | - | - | ✅ | - |
| gemini-pr-review-*.yml | ✅ | - | - | - |
| gemini-issue-automated-triage.yml | - | - | ✅ | - |
| gemini-issue-scheduled-triage.yml | - | - | - | ✅ |
| imagen4-generate-and-commit.yml | - | - | - | ✅ |
| imagen4-issue-trigger-and-commit.yml | - | - | ✅ | - |
| huggingface-space-deploy.yml | - | - | - | ✅ |
| static-site.yml | ✅ | - | - | ✅ |
| oasis-issue-intake.yml | - | - | ✅ | - |
| thumbnail_ingest_experimental.yml | - | - | ✅ | - |
| oasis-sync.yml | ✅ (`articles/oasis/**`) | - | - | ✅ |
| oasis-zenn-sync.yml / oasis-qiita-sync.yml / oasis-wordpress-sync.yml | ✅ | ✅ | - | - |
| qiita/publish.yml | ✅ (`main`/`master`) | - | - | ✅ |

---

## 🔐 Secrets & Variables

| キー | タイプ | 用途 | 関連モジュール |
|------|--------|------|----------------|
| `GH_PAT` | Secret | push / Issue 操作用 PAT | 全般 |
| `GEMINI_API_KEY` | Secret | Gemini CLI / Imagen | Gemini Actions Labs |
| `QIITA_TOKEN` | Secret | Qiita CLI 認証 | Oasis Sync |
| `HUGGINGFACE_TOKEN` | Secret | Hugging Face Space API | Gemini Actions Labs |
| `vars.GCP_WIF_PROVIDER`, `vars.GOOGLE_CLOUD_PROJECT`, `vars.GOOGLE_CLOUD_LOCATION`, `vars.SERVICE_ACCOUNT_EMAIL` | Variable | Gemini CLI / Vertex AI 設定 | Gemini Actions Labs |
| `vars.*_TARGET_REPOSITORY`, `vars.*_TARGET_PATH`, `vars.*_TARGET_BRANCH` | Variable | 各配信先リポジトリ設定 | Oasis Sync |
| `GH_PAT_KOZAKI`, `GH_PAT_ONIZUKA`, `GH_PAT_YUKIMURA` | Secret | Persona レビューボット用 PAT | Gemini Actions Labs |

> Secrets / Variables のセットアップ手順は README の「Required Secrets & Variables」を参照してください。

---

## 📌 運用上のヒント

- **リトライ戦略**: 生成系ワークフローは idempotent な作りになっており、失敗時は同じトリガーを再実行すれば安全に再生成できます。
- **front matter の手動編集**: 既存記事を手で調整した場合は、Gemini 再生成を避けるため `zenn:` / `qiita:` / `wordpress:` セクションを残してください。
- **Persona レビュー**: PR レビュー結果はコメントのみの投稿です。必要に応じてレビューボットの権限を `Read & Write` に設定してください。
- **Space デプロイ**: Hugging Face Space へのデプロイは force push を行うため、Git LFS の大容量ファイルは除外してください。

---

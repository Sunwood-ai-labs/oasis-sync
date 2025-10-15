
![Architecture Diagram](./architecture.svg)

## 🏗️ アーキテクチャとワークフロー詳細

このドキュメントは、リポジトリ内のGitHub Actionsワークフローの全体像と詳細仕様をまとめたものです。トップレベルの概要は `README.md` を参照し、ここでは各ワークフローの目的・トリガー・実装上のポイントを詳述します。

### 全体像

上記の構成図（[architecture.svg](./architecture.svg)）をご参照ください。

### アーキテクチャの目的

このリポジトリは、**2つの主要モジュール**で構成されています：

#### 🟨 Gemini Actions Labs Module
- **目的**: AIを活用したコンテンツ生成
- **機能**:
  - リリースノートの自動生成
  - Imagen APIによるヘッダー画像生成
  - 複数プラットフォーム対応のハイブリッド記事作成

#### 🟧 Oasis Sync Module
- **目的**: コンテンツの変換と配信
- **機能**:
  - Oasisハイブリッド記事のプラットフォーム別分割
  - Geminiによるメタデータ生成
  - 各プラットフォームリポジトリへの自動同期

---

## 📋 ワークフロー詳細

### 🟨 Gemini Actions Labs Module

#### 📝 `gemini-release-notes.yml`
- **トリガー**: Release tag作成 (`on: push tags`)
- **役割**:
  1. 前回リリースとの差分を収集（コミット、変更ファイル、コントリビューター、コード差分）
  2. Imagen 4でヘッダー画像を生成
  3. Geminiでリリースノートを生成（Markdown形式）
  4. GitHub Releaseを作成/更新
  5. ヘッダー画像をReleaseアセットとしてアップロード
- **出力**:
  - `generated-images/release-{TAG}-{TIMESTAMP}/` にヘッダー画像
  - GitHub Releaseページに公開
- **実装ポイント**:
  - 環境変数で制御可能な最大値（`MAX_COMMITS`, `MAX_FILES`, `MAX_DIFF_LINES`等）
  - pre-releaseタグの自動検出（`-alpha`, `-beta`, `-rc`）
  - コード差分を含めた詳細な分析

#### 📰 `gemini-release-articles.yml`
- **トリガー**: `gemini-release-notes.yml` 完了後 (`workflow_run`)
- **役割**:
  1. トリガーしたリリースタグを特定
  2. リリースノート本文とヘッダー画像URLを取得
  3. サンプル記事（`.github/prompts/git-it-write-guide-*.md`）を参考にGeminiでOasis形式の記事を生成
  4. `articles/oasis/` にコミット
- **生成記事の構造**:
  ```yaml
  ---
  zenn:
    title: "【リリースノート】{project} {tag} - {summary}"
    emoji: "🎉"
    type: "tech"
    topics: ["tag1", "tag2", "tag3", "tag4"]
    published: true
  qiita:
    title: "{同じタイトル}"
    tags: ["Tag1", "Tag2", "Tag3", "Tag4", "Tag5"]
    private: false
    updated_at: null
    id: "{slug}-{timestamp}"
    organization_url_name: null
    slide: false
    ignorePublish: false
  wordpress:
    title: "{同じタイトル}"
    post_status: "publish"
    post_excerpt: "{2-3文の要約}"
    featured_image: "{ヘッダー画像URL}"
    taxonomy:
      category: ["category1", "category2"]
      post_tag: ["tag1", "tag2", "tag3", "tag4", "tag5"]
    custom_fields:
      lead: "{リード文}"
  ---
  
  ![{image_name}]({image_url})
  
  ## はじめに
  ...
  ```
- **実装ポイント**:
  - ファイル名は `{YYYYMMDD}-{repo_name}-{tag}-release.md` 形式
  - Qiita IDには末尾にタイムスタンプを付与
  - front matterと本文を一体化したハイブリッド形式

---

### 🟧 Oasis Sync Module

#### 🪄 `oasis-sync.yml`
- **トリガー**: 
  - `articles/oasis/**/*.md` へのpush
  - 手動実行（`workflow_dispatch`）
- **役割**:
  1. 新規追加/変更されたOasis記事を検出
  2. Geminiで各プラットフォーム用のメタデータを生成
  3. 記事をZenn、Qiita、WordPress形式に分割
  4. 各ディレクトリにコミット:
     - `articles/zenn/`
     - `articles/qiita/`
     - `articles/wordpress/`
- **処理フロー**:
  ```python
  1. collect: 変更ファイル検出
  2. prepare: ペイロード準備
  3. gemini: メタデータ生成
  4. apply: 記事分割・出力
  5. commit: 変更をコミット
  ```
- **実装ポイント**:
  - Pythonスクリプト（`.github/scripts/process_oasis_articles.py`）で記事処理
  - 既存メタデータは保持、不足分のみGeminiで補完
  - YAML形式のメタデータを安全にパース

#### 📘 `oasis-zenn-sync.yml`
- **トリガー**:
  - `articles/zenn/*.md` へのpush
  - `oasis-sync.yml` 完了後（`workflow_run`）
- **役割**: Zenn記事をターゲットリポジトリに同期
- **ターゲット**: `Sunwood-ai-labs/Zenn` (`./articles`)
- **実装ポイント**:
  - 差分検出により新規/変更記事のみを同期
  - `.github/scripts/sync_platform.sh` スクリプトを使用
  - GH_PAT（Personal Access Token）で認証

#### 📗 `oasis-qiita-sync.yml`
- **トリガー**:
  - `articles/qiita/*.md` へのpush
  - `oasis-sync.yml` 完了後（`workflow_run`）
- **役割**: Qiita記事をターゲットリポジトリに同期
- **ターゲット**: `Sunwood-ai-labs/qiita-article` (`./public`)
- **実装ポイント**:
  - Zenn同期と同じ仕組みを利用
  - Qiita CLIが期待するディレクトリ構造に対応

#### 📙 `oasis-wordpress-sync.yml`
- **トリガー**:
  - `articles/wordpress/*.md` へのpush
  - `oasis-sync.yml` 完了後（`workflow_run`）
- **役割**: WordPress記事をターゲットリポジトリに同期
- **ターゲット**: `Sunwood-ai-labs/WP-dev` (`./docs`)
- **実装ポイント**:
  - WordPress側のGitHub Actionsが記事を検出して自動投稿
  - front matterのメタデータをWordPress APIに渡す

---

## 🔄 データフロー

### 1️⃣ リリース時の自動フロー

```
Release Tag Created
  ↓
📝 gemini-release-notes.yml
  • コード差分分析
  • Imagen 4でヘッダー画像生成
  • Geminiでリリースノート生成
  • GitHub Releaseに公開
  ↓
📰 gemini-release-articles.yml (workflow_run)
  • リリースノート取得
  • Oasisハイブリッド記事生成
  • articles/oasis/ にコミット
  ↓
🪄 oasis-sync.yml (push trigger)
  • Geminiでメタデータ生成
  • プラットフォーム別に分割
  • articles/zenn/、qiita/、wordpress/ にコミット
  ↓
📘📗📙 Platform-specific sync (push/workflow_run)
  • oasis-zenn-sync.yml → Zennリポジトリ
  • oasis-qiita-sync.yml → Qiitaリポジトリ
  • oasis-wordpress-sync.yml → WordPressリポジトリ
  ↓
各プラットフォームで自動検出・投稿
```

### 2️⃣ トリガータイプ

| ワークフロー | push | workflow_run | manual |
|-------------|------|--------------|--------|
| gemini-release-notes.yml | tags | - | - |
| gemini-release-articles.yml | - | ✅ | - |
| oasis-sync.yml | articles/oasis/** | - | ✅ |
| oasis-zenn-sync.yml | articles/zenn/** | ✅ | - |
| oasis-qiita-sync.yml | articles/qiita/** | ✅ | - |
| oasis-wordpress-sync.yml | articles/wordpress/** | ✅ | - |

---

## 🎯 主要な設計原則

### 1. **責任分離**
- **Gemini Actions Labs**: コンテンツ生成に特化
- **Oasis Sync**: コンテンツ変換・配信に特化

### 2. **ハイブリッド形式**
- 単一ソース（Oasis記事）から複数プラットフォームへ配信
- プラットフォーム固有のメタデータをfront matterで管理

### 3. **イベント駆動**
- `workflow_run`で連鎖的に実行
- 各ワークフローは独立して動作可能

### 4. **拡張性**
- 新しいプラットフォーム追加が容易
- 環境変数とスクリプトで柔軟に設定変更可能

---


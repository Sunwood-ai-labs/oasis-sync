---
zenn:
  title: Git it Write の設定と使い方完全ガイド
  emoji: 🪄
  type: tech
  topics:
  - wordpress
  - git
  - markdown
  - plugin
  - automation
  published: true
qiita:
  title: Git it Write の設定と使い方完全ガイド
  tags:
  - WordPress
  - Git
  - Markdown
  - Plugin
  - Automation
  private: false
  updated_at: null
  id: git-it-write-guide-20251012
  organization_url_name: null
  slide: false
  ignorePublish: false
wordpress:
  title: Git it Write の設定と使い方完全ガイド
  post_status: publish
  post_excerpt: GitHub の Markdown ファイルを push するだけで WordPress に自動投稿できるプラグイン「Git it
    Write」の導入と設定方法を詳しく解説。Webhook やトークン設定、トラブル対処まで完全ガイドします。
  featured_image: _images/git-it-write-setup.jpg
  taxonomy:
    category:
    - wordpress
    - github
    - automation
    post_tag:
    - WordPress
    - Git
    - Markdown
    - Plugin
    - Automation
  custom_fields:
    lead: GitHub の Markdown を WordPress 投稿へ自動反映するプラグイン「Git it Write」。本記事では導入から設定、Webhook
      連携までをわかりやすくまとめました。
---

# Git it Write の設定と使い方完全ガイド

GitHub の Markdown ファイルを push するだけで、WordPress の投稿に自動反映できる神プラグインが **「[Git it Write](https://ja.wordpress.org/plugins/git-it-write/)**」です。

この記事では、Git it Write の導入から Webhook の設定まで、手順をステップごとに丁寧に紹介します。

---

## 🧩 Git it Write とは？

**Git it Write** は、GitHub のリポジトリと WordPress を連携し、Markdown 形式の記事を自動で投稿・更新できるプラグインです。

例えば、`README.md` や `docs/` フォルダにある記事をそのまま WordPress 投稿として公開できます。  
技術ブログやドキュメントサイト運用に最適です。

---

## ⚙️ 導入手順

### 1. プラグインをインストール

1. WordPress 管理画面 → **プラグイン → 新規追加**
2. 「**Git it Write**」で検索
3. 「今すぐインストール」→「有効化」

---

### 2. GitHub 側で Personal Access Token を作成

1. GitHub → 右上アイコン → **Settings → Developer settings → Personal access tokens**
2. 「Generate new token (classic)」をクリック
3. スコープは **`repo` → `public_repo`** にチェック
4. トークンを生成してコピー（後で WordPress に貼り付けます）

---

### 3. WordPress 側の設定

**設定 → Git it Write** を開いて、以下を入力します。

| 項目 | 入力内容 |
|------|-----------|
| GitHub Username | あなたの GitHub ユーザー名 |
| GitHub Access token | さきほど生成したトークン |
| Webhook secret | 任意の文字列（例：`GiW_2024_hamaruki`）|

最後に「**Save settings**」をクリック。

---

### 4. リポジトリを追加

同じ画面で「**Add a new repository to publish posts from**」をクリック。

| 項目 | 入力例 |
|------|--------|
| Owner | Sunwood-ai-labs |
| Repository | WP-dev |
| Path | （ルートなら空欄） |
| Post Type | post |

→ 保存すると、連携リポジトリ一覧に追加されます。

---

### 5. GitHub に Webhook を設定

ここが一番重要なポイントです。

GitHub → 対象リポジトリ → **Settings → Webhooks → Add webhook**

| 項目 | 入力内容 |
|------|-----------|
| **Payload URL** | `https://hamaruki.com/wp-json/giw/v1/publish` |
| **Content type** | `application/json` ✅ |
| **Secret** | WordPress 側と同じ文字列（例：`GiW_2024_hamaruki`） |
| **Which events...** | 「Just the push event」 |
| **Active** | ✅ チェックのまま |

💡 **ポイント:**  
Content type を `application/x-www-form-urlencoded` のままにすると、WordPress 側が 500 エラーを返すので必ず JSON に変更してください。

---

### 6. 動作確認

1. GitHub で `.md` ファイルを push  
2. 数秒後、WordPress 管理画面 → **Git it Write → Logs** を確認  
3. 「Received push event...」と出ていれば成功🎉  
4. 投稿一覧に記事が自動追加されているはずです。

---

## 📝 Markdown の書き方

ファイル名が投稿のスラッグになります。

```

docs/
├── getting-started.md
└── tips/
└── index.md

````

- `index.md` はそのフォルダのメイン記事として扱われます。
- フロントマターでタイトルやカテゴリを指定可能。

```md
---
title: はじめての Git it Write
post_status: publish
taxonomy:
  category:
    - WordPress
  post_tag:
    - Git
    - 自動化
---

# Git it Write 入門

この記事では、GitHub の Markdown を WordPress に自動投稿する方法を解説します。
````

---

## 💡 よくあるトラブルと解決法

| 症状               | 原因                                         | 対処                                 |
| ---------------- | ------------------------------------------ | ---------------------------------- |
| 500 エラーになる       | Content type が `x-www-form-urlencoded` のまま | `application/json` に変更             |
| 401 Unauthorized | Secret が不一致                                | WordPress と GitHub の Secret を同じにする |
| 投稿されない           | Path や Post Type が間違い                      | 設定画面を再確認                           |
| 画像が表示されない        | `_images` フォルダに配置していない                     | `/_images` に入れて push               |

---

## 🎯 まとめ

| ステップ | 内容                              |
| ---- | ------------------------------- |
| 1️⃣  | GitHub Token 作成                 |
| 2️⃣  | WordPress 側に設定                  |
| 3️⃣  | Webhook 登録 (`application/json`) |
| 4️⃣  | `.md` を push                    |
| ✅    | 自動で WordPress 投稿に反映！            |

---

## 🚀 おわりに

「Git it Write」を使えば、GitHub のワークフローをそのまま WordPress に繋げられます。
開発者にとって理想的なコンテンツ管理の形です。

🧡 この記事が役に立ったら、ぜひ [Git it Write の公式ページ](https://ja.wordpress.org/plugins/git-it-write/) に 5⭐ レビューを！

---

*作成者: Sunwood AI Labs*



---
zenn:
  title: 🪄 Oasis Sync v0.1.0 リリース！ Gemini と GitHub Actions でブログのマルチプラットフォーム配信を自動化
  emoji: 🚀
  type: tech
  topics:
    - oasis
    - github-actions
    - gemini
    - automation
  published: true
qiita:
  title: 🪄 Oasis Sync v0.1.0 リリース！ Gemini と GitHub Actions でブログのマルチプラットフォーム配信を自動化
  tags:
    - Oasis
    - GitHubActions
    - Gemini
    - Automation
  private: false
  updated_at: ''
  id: ''
  organization_url_name: sunwood-ai-labs
  slide: false
  ignorePublish: false
---

# 🪄 Oasis Sync v0.1.0 リリース！ Gemini と GitHub Actions でブログのマルチプラットフォーム配信を自動化

![Whisk_3ce8177c2d232e9af9c4ab32cb887f82dr](https://github.com/user-attachments/assets/e0e7992e-ebd2-4938-a711-08f5a50543c0)


本日、コンテンツクリエイターやデベロッパーの皆さまに向けて、画期的なツール **Oasis Sync v0.1.0** をリリースしました！このバージョンでは、**Google の Gemini と GitHub Actions を活用し、Zenn や Qiita など複数のプラットフォームへの記事配信を全自動化する**、強力なワークフローが導入されています。

---

## 📖 Oasis Sync とは？

Oasis Sync は、「一度書けば、どこへでも (Write Once, Publish Anywhere)」の思想を実現するためのツールです。`articles/oasis/` という単一のディレクトリをコンテンツの「信頼できる唯一の情報源（Single Source of Truth）」とし、そこに追加された Markdown 記事を、各技術ブログプラットフォーム（現在は Zenn と Qiita に対応）に特化した形式へ自動的に変換・同期します。

---

## ✨ v0.1.0 の主な新機能

今回のアップデートでは、コンテンツ配信の手間を劇的に削減するための、3つのコアなワークフローが導入されました。

### 1. 🪄 **Oasis Article Sync (oasis-sync.yml)**
本リリースの心臓部です。`articles/oasis/` ディレクトリへの変更を検知すると、以下の処理を自動で実行します。
- **Gemini によるメタデータ生成**: フロントマターが存在しない記事に対し、Gemini API を呼び出して Zenn と Qiita に最適化されたタイトル、タグ、絵文字などを自動で生成します。
- **記事の派生生成**: Python スクリプト (`process_oasis_articles.py`) が、元の記事と生成されたメタデータを結合し、`articles/zenn/` と `articles/qiita/` にそれぞれのプラットフォーム用の記事を生成します。
- **自動コミット**: 生成された記事をリポジトリに自動でコミット＆プッシュし、コンテンツを最新の状態に保ちます。

### 2. 📜 **Platform Sync (oasis-zenn-sync.yml / oasis-qiita-sync.yml)**
`Oasis Article Sync` の完了後、または `articles/zenn/`, `articles/qiita/` ディレクトリへの直接のプッシュをトリガーとして起動します。
- `sync_platform.sh` スクリプトを使用し、派生した記事をそれぞれの配信用 GitHub リポジトリ（例: Zenn 用の `Sunwood-ai-labs/Zenn`、Qiita 用の `Sunwood-ai-labs/qiita-article`）へ自動で同期（プッシュ）します。

---

## 🧱 新しいワークフローの仕組み

1.  **記事の執筆**: ユーザーは `articles/oasis/` ディレクトリに新しい Markdown 記事を追加します。  
2.  **プッシュと起動**: `main` ブランチにプッシュすると、`oasis-sync.yml` ワークフローが自動的に起動します。  
3.  **メタデータ生成**: `process_oasis_articles.py` がフロントマターの有無を確認。なければ、記事本文を Gemini に送信し、Zenn/Qiita 用のメタデータ（YAML 形式）を受け取ります。  
4.  **記事の結合・生成**: 受け取ったメタデータと本文を結合し、`articles/zenn/` と `articles/qiita/` に新しい記事ファイルが生成されます。  
5.  **配信リポジトリへの同期**: 最後に `oasis-zenn-sync.yml` と `oasis-qiita-sync.yml` が起動し、生成された記事を各プラットフォームの公開用リポジトリにプッシュします。  

---

## 🚀 今すぐ始めよう！

Oasis Sync はテンプレートリポジトリとして提供されており、誰でもすぐにこの強力な自動化ワークフローを利用開始できます。セットアップは README をご覧ください。

- **[GitHub リポジトリはこちら](https://github.com/Sunwood-ai-labs/oasis-sync.git)**

この v0.1.0 が、皆さまのコンテンツ制作と配信の効率を飛躍的に向上させる一助となることを願っています。ぜひフィードバックをお寄せください！

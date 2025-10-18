---
zenn:
  title: 【リリースノート】Oasis Sync v0.4.0 - GitHub Issueによる記事とサムネイルの自動登録
  emoji: 🚀
  type: tech
  topics:
  - github
  - github-actions
  - automation
  - python
  - contents-management
  published: true
qiita:
  title: 【リリースノート】Oasis Sync v0.4.0 - GitHub Issueによる記事とサムネイルの自動登録
  tags:
  - GitHub
  - GitHubActions
  - Automation
  - Python
  - CMS
  private: false
  updated_at: null
  id: null
  organization_url_name: null
  slide: false
  ignorePublish: false
wordpress:
  title: 【リリースノート】Oasis Sync v0.4.0 - GitHub Issueによる記事とサムネイルの自動登録
  post_status: publish
  post_excerpt: Oasis Sync v0.4.0をリリースしました。本バージョンでは、GitHub Issueを通じて記事やサムネイルを自動でリポジトリに登録する機能が追加され、コンテンツ管理が大幅に効率化されています。
  featured_image: https://raw.githubusercontent.com/Sunwood-ai-labs/oasis-sync/main/generated-images/release-v0.4.0-20251017_165817/imagen-4-ultra_2025-10-17T16-59-41-056Z_A_mesmerizing_and_vivid_digital_painting_featuring_1.png
  taxonomy:
    category:
    - release-note
    - github
    - automation
    post_tag:
    - GitHub
    - GitHubActions
    - Automation
    - Python
    - OasisSync
  custom_fields:
    lead: GitHub Issueをトリガーに、記事やサムネイルを自動でリポジトリ登録する新機能を追加した Oasis Sync v0.4.0 をリリース。GitHub
      Actionsを活用したコンテンツ管理の効率化について解説します。
---

![imagen-4-ultra_2025-10-17T16-59-41-056Z_A_mesmerizing_and_vivid_digital_painting_featuring_1.png](https://raw.githubusercontent.com/Sunwood-ai-labs/oasis-sync/main/generated-images/release-v0.4.0-20251017_165817/imagen-4-ultra_2025-10-17T16-59-41-056Z_A_mesmerizing_and_vivid_digital_painting_featuring_1.png)

## はじめに
Oasis Sync v0.4.0 をリリースしました。このバージョンでは、コンテンツ管理を大幅に効率化する2つの主要な自動化機能を追加しました。GitHub Issue を利用して、記事の投稿やサムネイルの登録といった作業を完全に自動化し、リポジトリへの反映をシームレスに行えるようになります。

## 主な変更点
本リリースのハイライトは以下の通りです。

- **GitHub Issueによる記事投稿**: 新しいIssueテンプレート `📰 Oasis ハイブリッド記事登録` を通じて、記事のfront matterと本文を投稿するだけで、記事ファイル（`.md`）とヘッダー画像がリポジトリに自動で追加されます。
- **GitHub Issueによるサムネイル登録**: 実験的な機能として `🚧🖼️ サムネイル登録` Issueフォームから画像を添付またはURLを指定するだけで、サムネイルが自動でリサイズ・変換（PNG）され、指定ディレクトリに保存されます。

これらのワークフローはGitHub Actionsによって完全に自動化されており、ファイルの生成、コミット、Issueへの結果報告、そしてIssueのクローズまでを一貫して行います。

## 技術的な詳細
### 新機能
#### GitHub Issueによる記事投稿
Issueテンプレート `oasis-article.yml` を利用して、必要な情報をフォームに入力するだけで記事を投稿できるようになりました。

このワークフローは、`oasis-issue-intake.yml` によって実行され、`ingest_oasis_issue.py` スクリプトがIssueの内容を解析します。front matterと本文からMarkdownファイルを生成し、指定されたヘッダー画像をリポジトリに追加後、自動でコミットします。これにより、コンテンツ作成者はGit操作を意識することなく記事を投稿できます ([bef76da](https://github.com/Sunwood-ai-labs/oasis-sync/commit/bef76da))。

#### GitHub Issueによるサムネイル登録（実験的）
サムネイル管理を効率化するため、Issue経由で画像を登録する実験的な機能を追加しました。`thumbnail-upload-experimental.yml` テンプレートから画像をアップロードするか、URLを指定すると、GitHub Actionsワークフロー `thumbnail_ingest_experimental.yml` が起動します。

`ingest_thumbnail_issue.py` スクリプトが画像をダウンロードし、リサイズとPNG形式への変換を行った上で `images/thumbnails/` ディレクトリに保存します。処理完了後、`write_thumbnail_comment.py` スクリプトがIssueに結果をコメントし、生成されたファイルへのリンクを通知します ([37b2e61](https://github.com/Sunwood-ai-labs/oasis-sync/commit/37b2e61), [94cc18d](https://github.com/Sunwood-ai-labs/oasis-sync/commit/94cc18d))。

### 改善点
- サムネイルのファイル名を決めるスラッグの生成ロジックを改善し、より予測可能で一貫性のあるファイル名が付けられるようになりました ([a354c99](https://github.com/Sunwood-ai-labs/oasis-sync/commit/a354c99))。
- Issueの備考欄に貼り付けられた `<img>` タグの `src` 属性からも画像を収集する実験的なサポートを追加し、柔軟な画像指定が可能になりました ([61f91a5](https://github.com/Sunwood-ai-labs/oasis-sync/commit/61f91a5))。
- ワークフロー内のコメントフォーマットを改善し、可読性を向上させました ([2dd745b](https://github.com/Sunwood-ai-labs/oasis-sync/commit/2dd745b))。

### バグ修正
- サムネイル登録ワークフローの安定性を向上させるための修正を行いました ([7c1844d](https://github.com/Sunwood-ai-labs/oasis-sync/commit/7c1844d))。

## まとめ
v0.4.0では、GitHub Issueをインターフェースとして活用し、コンテンツ管理のワークフローを自動化する強力な機能が追加されました。

| 機能 | 概要 | 関連コンポーネント |
|:---|:---|:---|
| 記事の自動登録 | Issueフォームから記事のfront matterと本文を投稿 | `oasis-issue-intake.yml`, `ingest_oasis_issue.py` |
| サムネイル自動登録 | Issueフォームから画像をアップロードまたはURL指定 | `thumbnail_ingest_experimental.yml`, `ingest_thumbnail_issue.py` |

これにより、開発者やコンテンツ作成者はGitHub上での操作に集中でき、手動でのファイル追加やコミット作業から解放されます。

---
### 📚 参考リンク
- **GitHub Repository**: [Sunwood-ai-labs/oasis-sync](https://github.com/Sunwood-ai-labs/oasis-sync)
- **Release Page**: [v0.4.0 Release](https://github.com/Sunwood-ai-labs/oasis-sync/releases/tag/v0.4.0)
- **Full Changelog**: [Compare v0.3.7...v0.4.0](https://github.com/Sunwood-ai-labs/oasis-sync/compare/v0.3.7...v0.4.0)

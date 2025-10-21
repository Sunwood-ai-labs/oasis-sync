---
title: 【リリースノート】oasis-sync v0.6.0 - 外部リポジトリへの記事投稿機能とドキュメント改善
post_status: publish
post_excerpt: oasis-sync v0.6.0 がリリースされました。このバージョンでは、生成されたリリース記事を指定した外部リポジトリに直接プッシュする機能が追加され、記事管理と運用リポジトリの分離が可能になりました。また、プロジェクトの理解を深めるためのアーキテクチャ図もドキュメントに導入されています。
featured_image: https://raw.githubusercontent.com/Sunwood-ai-labs/oasis-sync/main/generated-images/release-v0.6.0-20251021_150745/imagen-4-ultra_2025-10-21T15-08-57-125Z_A_mesmerizing_and_vivid_digital_painting_featuring_1.png
taxonomy:
  category:
  - リリースノート
  - GitHub
  - CI-CD
  post_tag:
  - GitHubActions
  - CICD
  - Automation
  - ReleaseNote
  - GitHub
custom_fields:
  lead: oasis-sync v0.6.0 では、リリース記事を外部リポジトリへ直接プッシュする新機能が導入されました。本記事では、この変更の詳細とドキュメント改善について解説します。
---

## はじめに
`oasis-sync` v0.6.0 がリリースされました。このバージョンでは、リリース記事の管理をより柔軟にするための外部リポジトリ連携機能が追加されたほか、プロジェクトの全体像を把握しやすくするためのドキュメント改善が行われています。

## 主な変更点
- **外部リポジトリへの記事投稿**: 生成されたリリース記事を、指定した外部リポジトリに直接プッシュできるようになりました。
- **アーキテクチャ図の追加**: `README.md` にワークフローのアーキテクチャ図を追加し、プロジェクトの全体像を把握しやすくなりました。

## 技術的な詳細
### 新機能
#### 外部リポジトリへの記事投稿機能
`gemini-release-articles.yml` ワークフローが強化され、リリース記事を任意のターゲットリポジトリおよびブランチにプッシュする機能が追加されました (000efd9)。

この機能は、以下の環境変数を設定することで利用できます。
- `OASIS_ARTICLE_REPOSITORY`: 記事をプッシュしたい外部リポジトリ（例: `owner/article-repo`）
- `OASIS_ARTICLE_REPOSITORY_REF`: プッシュ先のブランチ（例: `main`）

これにより、`oasis-sync` を運用するリポジトリと、生成された記事を管理するリポジトリを完全に分離でき、より柔軟なコンテンツ管理が可能になります。

また、Oasis 記事フォーマットを生成するためのアシスタントシステムプロンプト v1.2 も追加されています (4a096ba)。

### 改善点
#### ドキュメントの視覚化
プロジェクトのワークフローの全体像を直感的に理解できるよう、`README.md` にアーキテクチャ図を追加しました (4affda5)。これにより、新規コントリビューターや利用者がシステムの動作を素早く把握できるようになります。

## まとめ
v0.6.0 の主要なアップデートは以下の通りです。

| 機能 | 概要 |
|---|---|
| **外部リポジトリへの記事投稿** | `gemini-release-articles` ワークフローで、生成記事を別リポジトリにプッシュ可能に。 |
| **ドキュメント改善** | `README.md` にアーキテクチャ図を追加し、プロジェクトの理解を促進。 |

今回のリリースにより、コンテンツ管理の柔軟性が向上し、プロジェクトの透明性も高まりました。

---
📚 参考リンク
- **GitHub Repository**: [Sunwood-ai-labs/oasis-sync](https://github.com/Sunwood-ai-labs/oasis-sync)
- **Release Page**: [v0.6.0 Release](https://github.com/Sunwood-ai-labs/oasis-sync/releases/tag/v0.6.0)
- **Comparison**: [v0.5.0...v0.6.0](https://github.com/Sunwood-ai-labs/oasis-sync/compare/v0.5.0...v0.6.0)

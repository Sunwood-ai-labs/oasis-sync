---
title: 【リリースノート】Oasis Sync v0.2.0 - WordPress連携とリリース記事の自動生成
tags:
- GitHub
- Actions
- WordPress
- Automation
- Gemini
private: false
updated_at: null
id: oasis-sync-v0-2-0-release
organization_url_name: null
slide: false
ignorePublish: false
---

![imagen-4-ultra_2025-10-14T14-33-34-241Z_A_mesmerizing_and_vivid_digital_painting_featuring_1.png](https://raw.githubusercontent.com/Sunwood-ai-labs/oasis-sync/main/generated-images/release-v0.2.0-20251014_143214/imagen-4-ultra_2025-10-14T14-33-34-241Z_A_mesmerizing_and_vivid_digital_painting_featuring_1.png)

# 【リリースノート】Oasis Sync v0.2.0 - WordPress連携とリリース記事の自動生成

Oasis Sync v0.2.0をリリースしました。このバージョンでは、コンテンツ配信の自動化をさらに推し進めるため、WordPressとの連携機能や、Geminiを活用したリリース記事の自動生成ワークフローが導入されています。

---

## ## はじめに

Oasis Syncは、Markdownで管理された技術記事を複数のプラットフォームへ自動同期するためのリポジトリです。今回のアップデートでは、特にWordPressユーザーにとって価値のある機能と、開発プロセスを効率化する仕組みが追加されました。

---

## ## 主な変更点

v0.2.0の主要なハイライトは以下の通りです。

-   **WordPressへの記事自動同期**: `articles/oasis/` ディレクトリ内の記事を、指定のWordPressサイトへ自動で投稿・更新する機能を追加しました。
-   **リリース記事の自動生成**: GitHubリリースノートの内容を基に、GeminiがOasisフォーマットの技術記事を自動で生成し、リポジトリにコミットするワークフローを導入しました。
-   **「Git it Write」ガイド記事の追加**: WordPressとGitHubを連携させるためのプラグイン「Git it Write」の導入から設定までを網羅したガイド記事を新たに追加しました。

---

## ## 技術的な詳細

### ### 新機能

#### WordPress連携ワークフローの追加

新たに `.github/workflows/oasis-wordpress-sync.yml` を導入しました。このワークフローは、`articles/oasis/` 内のMarkdownファイルに記述されたWordPress用のfront matterを解析し、対象のリポジトリへファイルを同期します。

これにより、Gitベースの執筆フローを維持したまま、WordPressへのコンテンツ展開を完全に自動化できます。

#### リリース記事の自動生成

`.github/workflows/gemini-release-articles.yml` ワークフローが追加されました。このワークフローは、新しいリリースが作成されると自動的にトリガーされます。

1.  リリースノートの本文を取得します。
2.  Gemini APIを呼び出し、リリースノートの内容を基にしたOasisフォーマットの技術記事を生成します。
3.  生成された記事をリポジトリに自動でコミットします。

この仕組みにより、リリース情報の二次展開にかかる手間を大幅に削減します。

### ### 改善点

#### ワークフローの責務分離

従来 `gemini-release-notes.yml` に含まれていたZenn記事生成のロジックを、新設された `gemini-release-articles.yml` へと分離しました。これにより、各ワークフローの責務が明確になり、メンテナンス性が向上しました。

### ### 注意点（Breaking Changes）

-   **一部ワークフローの一時的な無効化**: `oasis-qiita-sync.yml` と `oasis-zenn-sync.yml` のワークフローは、今後の改修を見据えて `.github/no_workflows/` ディレクトリに移動され、一時的に無効化されました。

---

## ## まとめ

| カテゴリ | 内容 |
| :--- | :--- |
| ✨ **新機能** | WordPressへの記事同期ワークフローを追加 |
| ✨ **新機能** | Geminiによるリリース記事の自動生成ワークフローを追加 |
| 📚 **ドキュメント** | 「Git it Write」のセットアップガイド記事を追加 |
| 🔧 **リファクタ** | ワークフローの責務を分離し、メンテナンス性を向上 |
| 💥 **破壊的変更** | QiitaおよびZennの同期ワークフローを一時的に無効化 |

---

📚 参考リンク
-   **GitHub Repository**: [Sunwood-ai-labs/oasis-sync](https://github.com/Sunwood-ai-labs/oasis-sync)
-   **Release Page**: [v0.2.0 Release](https://github.com/Sunwood-ai-labs/oasis-sync/releases/tag/v0.2.0)
-   **Compare URL**: [v0.1.0...v0.2.0](https://github.com/Sunwood-ai-labs/oasis-sync/compare/v0.1.0...v0.2.0)


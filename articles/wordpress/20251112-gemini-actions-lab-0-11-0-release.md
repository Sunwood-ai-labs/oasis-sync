---
title: 【リリースノート】gemini-actions-lab v0.11.0 - Discord Botの機能強化とコマンド刷新
post_status: publish
post_excerpt: gemini-actions-lab v0.11.0をリリースしました。本バージョンでは、Discord Botの機能が大幅に強化され、リポジトリの初期設定を効率化する新コマンドが追加されました。また、レガシーなテキストコマンドを廃止し、スラッシュコマンドへ統一しています。
featured_image: https://raw.githubusercontent.com/Sunwood-ai-labsII/gemini-actions-lab/main/generated-images/release-v0.11.0-20251112_165119/imagen-4-ultra_2025-11-12T16-52-17-481Z_Create_a_minimalist_typographic_illustration_displ_1.png
taxonomy:
  category:
  - リリースノート
  - Discord
  - CI/CD
  post_tag:
  - GitHub Actions
  - Discord Bot
  - Python
  - 自動化
  - v0.11.0
custom_fields:
  lead: gemini-actions-labの最新バージョンv0.11.0がリリースされました。このアップデートでは、Discord Botにリポジトリ設定を自動化する新コマンドが追加され、開発体験が大きく向上しています。また、従来のテキストコマンドを廃止し、より直感的なスラッシュコマンド体系へと刷新されました。
---

## はじめに
gemini-actions-lab v0.11.0へようこそ！このリリースでは、開発ワークフローをさらに加速させるため、Discord Botの機能を大幅に強化・刷新しました。リポジトリのセットアップを自動化する新コマンドの追加や、従来のテキストコマンドの廃止など、より使いやすく、モダンな体験を提供します。

## 主な変更点
- **Discord Botの機能強化**: リポジトリの初期設定やワークフロー管理を効率化する3つの新しいスラッシュコマンド (`/repo_setup`, `/workflow_preset`, `/list_presets`) を追加しました。
- **コマンド体系の刷新**: 従来のテキストベース `!issue` コマンドを完全に廃止し、操作性の高いスラッシュコマンドに統一しました。これにより、Discordの特権インテント（Message Content Intent）も不要になります。
- **開発プロセスの改善**: PyPIへのリリースプロセスを自動化するため、`pyproject.toml`のバージョンを更新するPythonスクリプトを導入しました。

## 技術的な詳細
### 新機能
#### 1. リポジトリセットアップの自動化 (`/repo_setup`)
新コマンド `/repo_setup` は、GitHubリポジトリの初期設定をDiscordから一括で行うためのものです。ワークフローの同期と、`.env`ファイルに基づいたシークレットの同期を一度に実行し、手動でのセットアップ作業を大幅に削減します。

#### 2. ワークフロープリセットの適用 (`/workflow_preset`)
`/workflow_preset` コマンドを使用すると、あらかじめ定義されたワークフローのプリセットをリポジトリに簡単に適用できます。これにより、プロジェクトの種類に応じたCI/CDパイプラインを迅速に構築できます。

#### 3. プリセット一覧の表示 (`/list_presets`)
利用可能なワークフロープリセットの一覧をDiscord上で確認できる `/list_presets` コマンドを追加しました。どのプリセットが利用可能か、コマンド一つで簡単に把握できます。

#### 4. PyPIリリースプロセスの自動化
CI/CDプロセスを強化するため、`pyproject.toml`内のバージョン番号を自動で更新するPythonスクリプト (`.github/scripts/update_version.py`) を導入しました。これにより、PyPIへのパッケージリリースがよりスムーズになります。

### 改善点
#### コマンド体系のモダン化
レガシーな `!issue` テキストコマンドを廃止し、すべての操作をスラッシュコマンドに統一しました。これにより、Discord上でのコマンド入力が直感的になり、ユーザー体験が向上します。また、この変更に伴い、Discord Botが特権インテントである「Message Content Intent」を要求しなくなりました。

#### ドキュメントの更新
新しいスラッシュコマンドの導入と `!issue` コマンドの廃止に伴い、`discord-issue-bot/README.md` のドキュメントを更新しました。最新の利用方法が反映されています。

## 破壊的変更
### `!issue` テキストコマンドの廃止
v0.11.0より、従来の `!issue` コマンドは完全に削除されました。今後は、GitHub Issueを作成・管理するために `/issue` や `/issue_quick` などのスラッシュコマンドをご利用ください。

## まとめ
v0.11.0では、Discord Botを中心とした開発体験の向上に注力しました。新しいスラッシュコマンドにより、リポジトリのセットアップがこれまで以上に簡単かつ迅速になります。ぜひ新しいコマンドをお試しいただき、フィードバックをお寄せください。

---
📚 **参考リンク**
- **GitHubリポジトリ**: [Sunwood-ai-labsII/gemini-actions-lab](https://github.com/Sunwood-ai-labsII/gemini-actions-lab)
- **リリースページ**: [v0.11.0 Release](https://github.com/Sunwood-ai-labsII/gemini-actions-lab/releases/tag/v0.11.0)
- **変更点の比較**: [v0.10.3...v0.11.0](https://github.com/Sunwood-ai-labsII/gemini-actions-lab/compare/v0.10.3...v0.11.0)

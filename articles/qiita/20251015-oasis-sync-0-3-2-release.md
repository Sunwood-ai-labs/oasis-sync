---
title: 【リリースノート】Oasis Sync v0.3.2 - アーキテクチャ刷新とリリースノート生成の強化
tags:
- GitHubActions
- Gemini
- Automation
- ReleaseNote
- CICD
private: false
updated_at: null
id: oasis-sync-v0-3-2-release-20251015111741
organization_url_name: null
slide: false
ignorePublish: false
---

![imagen-4-ultra_2025-10-15T11-18-40-617Z_A_mesmerizing_and_vivid_digital_painting_featuring_1.png](https://raw.githubusercontent.com/Sunwood-ai-labs/oasis-sync/main/generated-images/release-v0.3.2-20251015_111741/imagen-4-ultra_2025-10-15T11-18-40-617Z_A_mesmerizing_and_vivid_digital_painting_featuring_1.png)

## はじめに

Oasis Sync v0.3.2をリリースしました。このバージョンでは、プロジェクトの構造を明確にするためのアーキテクチャ刷新と、開発ワークフローを効率化するためのリリースノート生成機能の強化が中心となります。本記事では、これらの変更点の技術的な詳細を解説します。

## 主な変更点

v0.3.2の主要なハイライトは以下の通りです。

-   **アーキテクチャドキュメントの全面刷新**: リポジトリの役割を「Gemini Actions Labs（コンテンツ生成）」と「Oasis Sync（コンテンツ配信）」の2大モジュールとして再定義し、ドキュメントを更新しました。
-   **リリースノート生成機能の強化**: コード差分を取得する際に、行数だけでなく文字数でも上限を設定可能にし、バイナリファイルを除外することで、より精度の高いリリースノートを生成します。
-   **ワークフローの整理と有効化**: これまで無効化されていたワークフローを整理し、QiitaとZennへの記事同期ワークフローを有効化しました。

## 技術的な詳細

### 新機能

#### 差分取得ロジックの強化

リリースノート生成時に参照する `git diff` の取得ロジックを改善しました。

-   **差分サイズの上限設定**: 巨大な差分によって処理が失敗するのを防ぐため、取得するコード差分のサイズを最大行数と最大文字数で制限する機能を追加しました。
-   **バイナリファイルの除外**: 差分収集の際に、画像やPDFなどのバイナリファイルを自動的に除外するようになりました。これにより、テキストベースの変更点のみを抽出し、ノイズの少ないリリースノートを生成できます。

### 改善点

#### ワークフローの再編成と有効化

開発の効率性と透明性を高めるため、GitHub Actionsワークフローを見直しました。

-   **無効なワークフローの整理**: 従来 `.github/no_workflows` に配置されていたワークフローファイルを、役割に応じて `.github/no_workflows/gemini-actions-labs/` へと再編成しました。
-   **Qiita/Zenn同期の有効化**: `oasis-qiita-sync.yml` と `oasis-zenn-sync.yml` のワークフローを有効化し、Oasisフォーマットの記事を各プラットフォームへ自動で配信するパイプラインを構築しました。
-   **差分切り詰め処理のスクリプト化**: リリースノート生成時の差分切り詰め処理を、再利用可能なPythonスクリプト (`.github/scripts/clamp_diff.py`) として分離し、メンテナンス性を向上させました。

### ドキュメント

プロジェクトの全体像を理解しやすくするため、ドキュメントを全面的に刷新しました。

-   **アーキテクチャドキュメントの更新**: `architecture.md` を全面的に書き直し、リポジトリの2つの主要モジュール（Gemini Actions Labs, Oasis Sync）の役割と連携について詳細に解説しました。
-   **アーキテクチャ図の追加**: 新しいアーキテクチャ図 (`architecture.svg`) を追加し、ワークフロー間の連携を視覚的に分かりやすくしました。
-   **READMEの更新**: `README.md` を更新し、新しいアーキテクチャの概要と関連ドキュメントへのリンクを記載しました。

## まとめ

本リリースでは、プロジェクトの基盤となるアーキテクチャを整理し、コンテンツ生成から配信までのパイプラインを強化しました。

| 変更カテゴリ | 内容 |
| :--- | :--- |
| 🏛️ アーキテクチャ | 「コンテンツ生成」と「コンテンツ配信」の2大モジュールとして再定義 |
| 📝 リリースノート | 差分取得のロジックを改善し、生成精度を向上 |
| 🚀 ワークフロー | Qiita/Zennへの記事同期を有効化し、配信パイプラインを強化 |
| 📚 ドキュメント | アーキテクチャ図を含むドキュメントを全面的に刷新 |

これらの変更により、Oasis Syncはより堅牢でスケーラブルなコンテンツ管理ハブへと進化しました。

---

### 📚 参考リンク

-   **GitHubリポジトリ**: [Sunwood-ai-labs/oasis-sync](https://github.com/Sunwood-ai-labs/oasis-sync)
-   **リリースページ**: [v0.3.2 Release](https://github.com/Sunwood-ai-labs/oasis-sync/releases/tag/v0.3.2)
-   **変更差分**: [Compare v0.2.5...v0.3.2](https://github.com/Sunwood-ai-labs/oasis-sync/compare/v0.2.5...v0.3.2)

---
zenn:
  title: 【リリースノート】Oasis Sync v0.3.3 - Qiitaへの差分自動公開ワークフローを追加
  emoji: 🚀
  type: tech
  topics:
  - github-actions
  - qiita
  - automation
  - cli
  - git
  published: true
qiita:
  title: 【リリースノート】Oasis Sync v0.3.3 - Qiitaへの差分自動公開ワークフローを追加
  tags:
  - GitHubActions
  - Qiita
  - Automation
  - CLI
  - Git
  private: false
  updated_at: null
  id: oasis-sync-v0-3-3-release-20251015130000
  organization_url_name: null
  slide: false
  ignorePublish: false
wordpress:
  title: 【リリースノート】Oasis Sync v0.3.3 - Qiitaへの差分自動公開ワークフローを追加
  post_status: publish
  post_excerpt: Oasis Sync v0.3.3をリリースしました。このバージョンでは、変更があったMarkdownファイルのみを自動でQiitaに投稿・更新するGitHub
    Actionsワークフローが追加され、コンテンツの公開がより効率的になりました。
  featured_image: https://raw.githubusercontent.com/Sunwood-ai-labs/oasis-sync/main/generated-images/release-v0.3.3-20251015_123446/imagen-4-ultra_2025-10-15T12-36-03-293Z_A_mesmerizing_and_vivid_digital_painting_featuring_1.png
  taxonomy:
    category:
    - release-note
    - github-actions
    - automation
    post_tag:
    - Oasis Sync
    - GitHubActions
    - Qiita
    - Automation
    - ReleaseNote
  custom_fields:
    lead: Oasis Sync v0.3.3では、`git diff` を活用して変更されたMarkdownファイルのみをQiitaに自動公開する新しいワークフローを導入しました。本記事では、この機能の詳細とその他の改善点について解説します。
---

![imagen-4-ultra_2025-10-15T12-36-03-293Z_A_mesmerizing_and_vivid_digital_painting_featuring_1.png](https://raw.githubusercontent.com/Sunwood-ai-labs/oasis-sync/main/generated-images/release-v0.3.3-20251015_123446/imagen-4-ultra_2025-10-15T12-36-03-293Z_A_mesmerizing_and_vivid_digital_painting_featuring_1.png)

## はじめに
Oasis Sync v0.3.3をリリースしました。このアップデートの最大の目玉は、変更があったMarkdownファイルのみを自動でQiitaに投稿・更新するGitHub Actionsワークフローの追加です。これにより、コンテンツ管理の効率が大幅に向上します。

## 主な変更点
- **Qiitaへの差分公開ワークフローを追加**: `git diff` を利用して変更があった記事のみを検出し、自動でQiitaに公開する仕組みを導入しました。
- **コンテンツの整理**: 過去のリリースノート記事を追加し、古くなった、あるいは重複した記事ファイルをリポジトリから削除しました。
- **メタデータ自動更新**: ボットにより、各記事のフロントマター（Zenn & Qiitaメタデータ）が自動で更新されました。

## 技術的な詳細
### 新機能
#### Qiitaへの差分自動公開ワークフロー
今回のリリースで、`.github/qiita/publish.yml` に新しいGitHub Actionsワークフローを追加しました。

このワークフローは、`git diff` コマンドを使って前回のコミットから変更があったMarkdownファイル（`public/*.md`）を特定し、Qiita CLI (`npx qiita publish`) を通じて自動で投稿・更新します。

**主なメリット:**
- **効率化**: 変更のない記事に対して不要なAPIリクエストを送ることを防ぎます。
- **高速化**: 差分のみを処理するため、ワークフローの実行時間が短縮されます。
- **確実性**: 手動での公開漏れやミスを防ぎ、変更が確実に反映されます。

### 改善点
#### コンテンツの拡充と整理
- v0.3.2およびv0.2.4のリリースノート記事をOasis, WordPress, Zennの各プラットフォーム向けに追加しました。
- リポジトリ内に存在した古い、あるいは重複した記事ファイルを削除し、コンテンツの整合性を高めました。

#### メンテナンス
- `oasis-sync[bot]` が各記事のフロントマターを自動更新し、メタデータ管理を効率化しました。
- フロントマター内の不要なクォーテーションを削除し、コードのクリーンアップを行いました。

## まとめ
Oasis Sync v0.3.3は、特にQiitaへのコンテンツ展開を自動化する上で大きな一歩となるリリースです。差分検知による効率的な公開ワークフローは、今後の運用をよりスムーズにします。

| 機能 | 詳細 |
| :--- | :--- |
| 🚀 **Qiita差分公開** | `git diff` を利用し、変更があった記事のみを自動でQiitaに投稿・更新するワークフローを追加しました。 |
| 📚 **コンテンツ整理** | 過去のリリースノートを追加し、不要なファイルをクリーンアップしました。 |
| 🔧 **自動メンテナンス** | ボットによるフロントマターの自動更新とコードの微修正を行いました。 |

---
📚 参考リンク
- **GitHub Repository**: [Sunwood-ai-labs/oasis-sync](https://github.com/Sunwood-ai-labs/oasis-sync)
- **Release Page**: [v0.3.3 Release](https://github.com/Sunwood-ai-labs/oasis-sync/releases/tag/v0.3.3)
- **Compare URL**: [v0.3.2...v0.3.3](https://github.com/Sunwood-ai-labs/oasis-sync/compare/v0.3.2...v0.3.3)

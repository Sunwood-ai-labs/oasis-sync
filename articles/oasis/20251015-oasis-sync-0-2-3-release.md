---
zenn:
  title: "【リリースノート】Oasis Sync v0.2.3 - WordPress連携強化とCIワークフロー整理"
  emoji: "✨"
  type: "tech"
  topics:
    - github-actions
    - wordpress
    - ci-cd
    - automation
    - python
  published: true
qiita:
  title: "【リリースノート】Oasis Sync v0.2.3 - WordPress連携強化とCIワークフロー整理"
  tags:
    - GitHubActions
    - WordPress
    - CI
    - Automation
    - Python
  private: false
  updated_at: null
  id: "oasis-sync-v0-2-3-release"
  organization_url_name: null
  slide: false
  ignorePublish: false
wordpress:
  title: "【リリースノート】Oasis Sync v0.2.3 - WordPress連携強化とCIワークフロー整理"
  post_status: "publish"
  post_excerpt: "Oasis Sync v0.2.3をリリースしました。本バージョンではWordPress連携を強化し、アイキャッチ画像と本文画像の重複表示を自動で防ぐ機能を追加しました。また、CI/CDの効率化のため、未使用のGitHub Actionsワークフローを整理しています。"
  featured_image: "https://raw.githubusercontent.com/Sunwood-ai-labs/oasis-sync/main/generated-images/release-v0.2.3-20251015_074758/imagen-4-ultra_2025-10-15T07-48-55-327Z_A_mesmerizing_and_vivid_digital_painting_featuring_1.png"
  taxonomy:
    category:
      - release-note
      - github-actions
      - wordpress
    post_tag:
      - OasisSync
      - WordPress
      - GitHubActions
      - CI
      - Automation
  custom_fields:
    lead: "Oasis Sync v0.2.3では、WordPressへの記事投稿フローが改善され、アイキャッチ画像の重複表示が自動で解消されます。本記事では、新機能の詳細やCIワークフローの整理内容について解説します。"
---

![imagen-4-ultra_2025-10-15T07-48-55-327Z_A_mesmerizing_and_vivid_digital_painting_featuring_1.png](https://raw.githubusercontent.com/Sunwood-ai-labs/oasis-sync/main/generated-images/release-v0.2.3-20251015_074758/imagen-4-ultra_2025-10-15T07-48-55-327Z_A_mesmerizing_and_vivid_digital_painting_featuring_1.png)

## はじめに

Oasis Sync `v0.2.3` をリリースしました。このバージョンでは、WordPressへの記事投稿体験を向上させるための機能改善と、CI/CDの運用効率を高めるためのワークフロー整理に焦点を当てています。

## 主な変更点

- **WordPress投稿の画像重複防止**: 記事本文の先頭にあるヘッダー画像が自動で削除され、アイキャッチ画像との重複表示を防ぎます。
- **アイキャッチ画像の安定性向上**: アイキャッチ画像の設定に完全なURL (`raw_url`) を使用することで、画像の表示をより確実にしました。
- **CIワークフローの整理**: 現在使用されていないGitHub Actionsワークフローを無効化し、リポジトリをクリーンな状態に保ちます。

## 技術的な詳細

### 新機能

#### WordPress投稿時のヘッダー画像自動削除

WordPress向けの記事を処理する際、本文の先頭に配置されたMarkdown形式の画像を自動で削除する機能を追加しました。

これまで、Oasisフォーマットの記事にヘッダー画像を含めると、WordPress側でアイキャッチ画像として設定されると同時に、本文の冒頭にも画像が表示されてしまい、重複感がありました。今回の改善により、投稿プロセスで本文側の画像が除去され、アイキャッチ画像のみがスマートに表示されるようになります。

この処理は `.github/scripts/process_oasis_articles.py` に実装されています (コミット: `1559ff8`)。

### バグ修正

#### アイキャッチ画像URLの確実な設定

WordPressのアイキャッチ画像を設定する際、これまでのファイル名ベースの指定から、GitHubの `raw.githubusercontent.com` を指す完全なURL (`raw_url`) を使用するように修正しました。

これにより、画像の参照がより安定的になり、テーマや環境に依存せずアイキャッチ画像が確実に表示されるようになります (コミット: `a8528be`)。

### 改善点

#### CIワークフローの整理

リポジトリのメンテナンス性を向上させるため、現在使用されていない、あるいは将来的に見直しを予定している複数のGitHub Actionsワークフローを無効化しました。

具体的には、対象のワークフローファイルを `.github/no_workflows` ディレクトリへ移動しています。これにより、Actionsタブのノイズが減り、現在アクティブなワークフローの管理が容易になります (コミット: `e77109a`, `2f12246`)。

## まとめ

Oasis Sync `v0.2.3` では、特にWordPressを利用するユーザーにとって、より快適なコンテンツ管理体験を提供するための改善を行いました。

| 分類 | 変更内容 | メリット |
|:---|:---|:---|
| **新機能** | WordPress投稿時に本文先頭の画像を自動削除 | アイキャッチ画像との重複表示を解消 |
| **バグ修正** | アイキャッチ画像に完全なURL (`raw_url`) を使用 | 画像表示の安定性と確実性が向上 |
| **改善点** | 未使用のCIワークフローを無効化 | CI/CDの運用効率と可読性が向上 |

今後の開発においても、各プラットフォームとの連携を強化し、自動化によるコンテンツ運用の効率化を推進していきます。

---

### 📚 参考リンク

- **GitHubリポジトリ**: [Sunwood-ai-labs/oasis-sync](https://github.com/Sunwood-ai-labs/oasis-sync)
- **リリースページ**: [v0.2.3 Release](https://github.com/Sunwood-ai-labs/oasis-sync/releases/tag/v0.2.3)
- **変更差分**: [Compare v0.2.2...v0.2.3](https://github.com/Sunwood-ai-labs/oasis-sync/compare/v0.2.2...v0.2.3)

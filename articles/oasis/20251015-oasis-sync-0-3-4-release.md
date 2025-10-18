---
zenn:
  title: 【リリースノート】Oasis Sync v0.3.4 - Qiita連携の改善とコンテンツ整理
  emoji: 📝
  type: tech
  topics:
  - github-actions
  - qiita
  - automation
  - ci-cd
  - release-note
  published: true
qiita:
  title: 【リリースノート】Oasis Sync v0.3.4 - Qiita連携の改善とコンテンツ整理
  tags:
  - GitHubActions
  - Qiita
  - Automation
  - CI
  - ReleaseNote
  private: false
  updated_at: null
  id: oasis-sync-v0-3-4-release-20251015125254
  organization_url_name: null
  slide: false
  ignorePublish: false
wordpress:
  title: 【リリースノート】Oasis Sync v0.3.4 - Qiita連携の改善とコンテンツ整理
  post_status: publish
  post_excerpt: Oasis Sync v0.3.4をリリースしました。本バージョンではQiita連携ワークフローを改善し、記事IDの自動採番に対応したほか、コンテンツの整理を行いました。
  featured_image: https://raw.githubusercontent.com/Sunwood-ai-labs/oasis-sync/main/generated-images/release-v0.3.4-20251015_125254/imagen-4-ultra_2025-10-15T12-53-58-148Z_A_mesmerizing_and_vivid_digital_painting_featuring_1.png
  taxonomy:
    category:
    - release-note
    - automation
    - github
    post_tag:
    - OasisSync
    - GitHubActions
    - Qiita
    - Automation
    - ReleaseNote
  custom_fields:
    lead: Oasis Sync v0.3.4では、Qiitaへの新規投稿時にIDが自動採番されるよう連携を改善しました。本記事では、変更点の技術的な詳細と背景を解説します。
---

![imagen-4-ultra_2025-10-15T12-53-58-148Z_A_mesmerizing_and_vivid_digital_painting_featuring_1.png](https://raw.githubusercontent.com/Sunwood-ai-labs/oasis-sync/main/generated-images/release-v0.3.4-20251015_125254/imagen-4-ultra_2025-10-15T12-53-58-148Z_A_mesmerizing_and_vivid_digital_painting_featuring_1.png)

## はじめに
Oasis Sync v0.3.4をリリースしました。このバージョンでは、Qiitaへの記事投稿ワークフローを改善し、より安全に新規投稿が行えるように修正しました。また、リポジトリ内のコンテンツ整理も行っています。

## 主な変更点
本リリースにおける主な変更点は以下の通りです。

- **Qiita連携の改善**: 新規投稿時に記事IDを`null`に設定し、Qiita側でIDが自動採番されるようにしました。
- **コンテンツ更新**: v0.3.3のリリースノート記事を追加しました。
- **リポジトリ整理**: 不要になった古いバージョンの記事ファイルを削除しました。

## 技術的な詳細
### バグ修正
#### Qiita投稿時のID自動採番への対応
これまで、Oasis SyncからQiitaへ新しい記事を投稿する際、フロントマターに `id` が設定されていると、そのIDを持つ既存の記事を意図せず上書きしてしまう可能性がありました。

今回の修正では、新規投稿と判断された場合にフロントマターの `id` を強制的に `null` に設定する処理をワークフローに追加しました。

```yaml
# 修正前のフロントマター例
qiita:
  id: "some-preset-id-..."
```

```yaml
# 修正後のフロントマター（新規投稿時）
qiita:
  id: null
```

これにより、Qiita APIが記事IDを自動で採番するため、既存記事との競合を防ぎ、安全に新規投稿を行えるようになります。

### メンテナンス
リポジトリの可読性を保つため、以下のコンテンツ整理を行いました。

- **v0.3.3リリースノートの追加**: 各プラットフォーム（Oasis, Qiita, WordPress, Zenn）向けに前回のリリースノート記事を追加しました。
- **古いファイルの削除**: `git-it-write-guide-20251012-V5.md` など、現在使われていない古い記事ファイルをリポジトリから削除しました。

## まとめ
Oasis Sync v0.3.4では、特にQiita連携の安定性向上に焦点を当てた改善を行いました。

| 変更カテゴリ | 内容 |
| :--- | :--- |
| **バグ修正** | Qiitaへの新規投稿時に`id`を`null`に設定し、IDの自動採番を有効化 |
| **ドキュメント** | v0.3.3のリリースノート記事を追加 |
| **メンテナンス** | 古いバージョンの記事ファイルをリポジトリから削除 |

この改善により、コンテンツ管理者はより安心して記事投稿の自動化ワークフローを利用できます。

---
### 📚 参考リンク
- **GitHubリポジトリ**: [Sunwood-ai-labs/oasis-sync](https://github.com/Sunwood-ai-labs/oasis-sync)
- **リリースページ**: [v0.3.4 Release](https://github.com/Sunwood-ai-labs/oasis-sync/releases/tag/v0.3.4)
- **変更差分**: [Compare v0.3.3...v0.3.4](https://github.com/Sunwood-ai-labs/oasis-sync/compare/v0.3.3...v0.3.4)

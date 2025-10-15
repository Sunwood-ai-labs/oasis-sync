---
zenn:
  title: "【リリースノート】Oasis Sync v0.2.2 - リリース記事生成ワークフローの堅牢性向上"
  emoji: ✨
  type: tech
  topics:
    - github-actions
    - automation
    - ai
    - gemini
    - markdown
  published: true
qiita:
  title: "【リリースノート】Oasis Sync v0.2.2 - リリース記事生成ワークフローの堅牢性向上"
  tags:
    - GitHubActions
    - Automation
    - AI
    - Gemini
    - Markdown
  private: false
  updated_at: null
  id: "oasis-sync-v0-2-2-release"
  organization_url_name: null
  slide: false
  ignorePublish: false
wordpress:
  title: "【リリースノート】Oasis Sync v0.2.2 - リリース記事生成ワークフローの堅牢性向上"
  post_status: "publish"
  post_excerpt: "Oasis Sync v0.2.2をリリースしました。本バージョンでは、AIによるリリース記事生成ワークフローが改善され、Markdownコードブロックの自動整形機能が追加されました。これにより、手動での修正作業が不要になり、コンテンツ生成の堅牢性が向上しています。"
  featured_image: "imagen-4-ultra_2025-10-15T07-14-25-675Z_A_mesmerizing_and_vivid_digital_painting_featuring_1.png"
  taxonomy:
    category:
      - release-note
      - automation
      - github
    post_tag:
      - GitHubActions
      - Automation
      - AI
      - Gemini
      - Markdown
  custom_fields:
    lead: "Oasis Sync v0.2.2では、AIを活用したリリース記事生成ワークフローの堅牢性を向上させました。生成されたMarkdownの自動整形機能やプロンプトの改善により、より高品質なコンテンツを安定して生成できるようになりました。"
---

![imagen-4-ultra_2025-10-15T07-14-25-675Z_A_mesmerizing_and_vivid_digital_painting_featuring_1.png](https://raw.githubusercontent.com/Sunwood-ai-labs/oasis-sync/main/generated-images/release-v0.2.2-20251015_071338/imagen-4-ultra_2025-10-15T07-14-25-675Z_A_mesmerizing_and_vivid_digital_painting_featuring_1.png)

## はじめに
Oasis Sync v0.2.2 をリリースしました。このバージョンでは、AIによるリリース記事生成の自動化ワークフローをより堅牢にするための改善に焦点を当てています。手動での修正作業を削減し、コンテンツ生成の信頼性を高めるための機能が追加されました。

## 主な変更点
今回のリリースにおける主な変更点は以下の通りです。

- **AI生成Markdownの自動整形機能**: AIが生成したMarkdownコンテンツがコードブロックで囲まれていても、自動的にクリーンアップする処理を追加しました。
- **プロンプトの改善**: リリース記事とヘッダー画像を生成するためのプロンプトを更新し、より高品質で安定したコンテンツ生成を目指しました。

## 技術的な詳細
### 新機能
#### AI生成Markdownの自動整形
これまで、AIが生成するリリース記事の本文が稀にMarkdownのコードブロック（` ```markdown` ... ````）で囲まれてしまうケースがありました。この場合、手動でコードブロックを削除する必要があり、完全な自動化の妨げとなっていました。

今回のアップデートで、`.github/workflows/gemini-release-articles.yml` ワークフローに以下の処理を追加しました。

- AIが生成したコンテンツをチェックし、Markdownコードブロックで囲まれている場合は自動的に除去する。

この改善により、ワークフローの堅牢性が向上し、手動での介入なしに整形された記事を生成できるようになりました。

### 改善点
#### プロンプトの品質向上
コンテンツ生成の品質をさらに高めるため、AIへの指示（プロンプト）を以下のように見直しました。

1.  **記事生成プロンプトの厳密化**:
    - 見出しに番号を付けないようにするルールを追加し、記事フォーマットの統一性を高めました。

2.  **画像生成プロンプトの可読性向上**:
    - `.github/prompts/release-image.en.txt` のプロンプトを複数行に整形し、どのような指示で画像が生成されているかを人間が理解しやすくしました。

これらの変更により、生成されるコンテンツの品質と一貫性が向上します。

## まとめ
Oasis Sync v0.2.2 は、AIを活用したコンテンツ生成ワークフローの信頼性と自律性を高めるための重要なアップデートです。Markdownの自動整形機能とプロンプトの改善により、開発者は手動での修正作業から解放され、より安定したリリースプロセスを実現できます。

---

### 📚 参考リンク
- **GitHub Repository**: [Sunwood-ai-labs/oasis-sync](https://github.com/Sunwood-ai-labs/oasis-sync)
- **Release Page**: [v0.2.2](https://github.com/Sunwood-ai-labs/oasis-sync/releases/tag/v0.2.2)
- **Full Changelog**: [Compare v0.2.1...v0.2.2](https://github.com/Sunwood-ai-labs/oasis-sync/compare/v0.2.1...v0.2.2)

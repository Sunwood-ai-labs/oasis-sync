```markdown
---
zenn:
  title: "【リリースノート】oasis-sync v0.2.1 - ワークフロー改善とメタデータ修正"
  emoji: "✨"
  type: "tech"
  topics:
    - github-actions
    - workflow
    - automation
    - ci-cd
    - oasis-sync
  published: true
qiita:
  title: "【リリースノート】oasis-sync v0.2.1 - ワークフロー改善とメタデータ修正"
  tags:
    - GitHubActions
    - Workflow
    - Automation
    - CICD
    - OasisSync
  private: false
  updated_at: null
  id: "oasis-sync-v0-2-1-release"
  organization_url_name: null
  slide: false
  ignorePublish: false
wordpress:
  title: "【リリースノート】oasis-sync v0.2.1 - ワークフロー改善とメタデータ修正"
  post_status: "publish"
  post_excerpt: "oasis-sync v0.2.1をリリースしました。本バージョンでは、リリース記事を自動生成するワークフローのプロンプト改善や、Oasis記事同期ワークフローの実行トリガー修正など、CI/CDの安定性向上に焦点を当てた改善が含まれています。"
  featured_image: "imagen-4-ultra_2025-10-14T15-03-21-072Z_A_mesmerizing_and_vivid_digital_painting_featuring_1.png"
  taxonomy:
    category:
      - release-note
      - github-actions
      - automation
    post_tag:
      - OasisSync
      - GitHubActions
      - Workflow
      - Automation
      - CICD
  custom_fields:
    lead: "Oasis-sync v0.2.1では、GitHub Actionsワークフローの改善と記事メタデータの修正を行いました。本記事では、プロンプトの調整や実行トリガーの限定など、技術的な変更点を詳しく解説します。"
---

![imagen-4-ultra_2025-10-14T15-03-21-072Z_A_mesmerizing_and_vivid_digital_painting_featuring_1.png](https://raw.githubusercontent.com/Sunwood-ai-labs/oasis-sync/main/generated-images/release-v0.2.1-20251014_150210/imagen-4-ultra_2025-10-14T15-03-21-072Z_A_mesmerizing_and_vivid_digital_painting_featuring_1.png)

## はじめに
Oasis-sync v0.2.1をリリースしました。このバージョンでは、主にリポジトリの運用を効率化するためのGitHub Actionsワークフロー改善と、既存記事のメタデータ修正に焦点を当てています。本記事では、これらの技術的な変更点について詳しく解説します。

## 主な変更点
今回のリリースに含まれる主な変更点は以下の通りです。

- **リリース記事生成ワークフローの改善**: AIが生成するMarkdownの品質を向上させるため、プロンプトを調整しました。
- **Oasis記事同期トリガーの限定**: ワークフローが意図しないタイミングで実行されるのを防ぐため、トリガーを`main`ブランチへのpushに限定しました。
- **記事メタデータの修正**: 既存記事のQiita連携用IDのフォーマットを修正し、一貫性を保つようにしました。

## 技術的な詳細
### 改善点
#### 1. リリース記事生成ワークフローのプロンプト改善
**コミット:** `e2f7d69`

これまで、リリースノートから記事を自動生成するワークフロー (`.github/workflows/gemini-release-articles.yml`) では、生成されるMarkdownに不要なタイトル行が含まれることがありました。

今回の更新では、プロンプトをより厳密に調整し、出力形式を細かく指定することで、手修正が不要な、より正確なOasisフォーマットの記事が生成されるように改善しました。

```yaml:gemini-release-articles.yml
# .github/workflows/gemini-release-articles.yml (抜粋)
# ...
      - name: Generate Release Articles
        id: generate_articles
        uses: google-gemini/gemini-release-notes-to-articles@v0
        with:
          # ...
          prompt: |
            あなたはOasisフォーマットの技術記事作成のエキスパートです。
            以下の情報を基に、GitHubリリースノートを題材とした技術記事を生成してください。
            # ... (改善されたプロンプト)
# ...
```

#### 2. Oasis記事同期トリガーの限定
**コミット:** `e2f7d69`

Oasis記事同期ワークフロー (`.github/workflows/oasis-sync.yml`) は、これまでブランチを問わずpushイベントでトリガーされていました。

開発ブランチでのpushでも実行されると思わぬ記事同期が発生する可能性があるため、トリガーを`main`ブランチへのpushに限定しました。これにより、本番環境への同期プロセスがより安全かつ予測可能になります。

```yaml:oasis-sync.yml
# .github/workflows/oasis-sync.yml (抜粋)
on:
  push:
    branches:
      - main # mainブランチへのpush時のみ実行
```

### バグ修正
#### 3. 記事メタデータの修正
**コミット:** `6758534`, `6ce9f0c`, `9ab212c`, `207ccff`

`git-it-write-guide`関連の記事において、Qiita連携用のID (`id`) のフォーマットに一貫性がありませんでした。今回の修正で、リポジトリの命名規則に沿ったフォーマット (`{リポジトリ名}-{tag}-release`) に統一しました。

これにより、IDの予測可能性が向上し、将来的なメンテナンス性が改善されます。

## まとめ
v0.2.1では、CI/CDプロセスの安定性と品質を向上させるための内部的な改善を中心に行いました。

| 変更カテゴリ | 内容 | 目的 |
| :--- | :--- | :--- |
| **ワークフロー改善** | リリース記事生成プロンプトの調整 | 生成される記事の品質向上 |
| **ワークフロー改善** | Oasis記事同期トリガーを`main`に限定 | 意図しない実行の防止と安全性向上 |
| **メタデータ修正** | Qiita連携IDのフォーマット統一 | メンテナンス性の向上 |

このリリースには破壊的変更は含まれておらず、すべてのユーザーが安全にアップデートできます。

---
📚 **参考リンク**
- **GitHubリポジトリ:** [Sunwood-ai-labs/oasis-sync](https://github.com/Sunwood-ai-labs/oasis-sync)
- **リリースページ:** [v0.2.1 Release](https://github.com/Sunwood-ai-labs/oasis-sync/releases/tag/v0.2.1)
- **変更差分:** [Compare v0.2.0...v0.2.1](https://github.com/Sunwood-ai-labs/oasis-sync/compare/v0.2.0...v0.2.1)
```

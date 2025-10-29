---
zenn:
  title: "【リリースノート】harina-v3-webui v0.3.0 - 重複チェック機能と高度なフィルタリングを追加"
  emoji: "✨"
  type: "tech"
  topics:
    - nextjs
    - react
    - typescript
    - docker
    - ai
  published: true
qiita:
  title: "【リリースノート】harina-v3-webui v0.3.0 - 重複チェック機能と高度なフィルタリングを追加"
  tags:
    - Next.js
    - React
    - TypeScript
    - Docker
    - AI
  private: false
  updated_at: null
  id: null
  organization_url_name: null
  slide: false
  ignorePublish: false
wordpress:
  title: "【リリースノート】harina-v3-webui v0.3.0 - 重複チェック機能と高度なフィルタリングを追加"
  post_status: "publish"
  post_excerpt: "v0.3.0では、レシートの重複チェック機能や一覧ページの高度なフィルタリングなど、データ管理を効率化する新機能を多数追加しました。設定ページも拡充され、カテゴリの動的同期やAIへのカスタム指示が可能になり、より柔軟な運用を実現します。"
  featured_image: "https://raw.githubusercontent.com/Sunwood-ai-labs/harina-v3-webui/main/generated-images/release-v0.3.0-20251029_081513/imagen-4-ultra_2025-10-29T08-16-14-819Z_A_clean__photorealistic_miniature_scene_inside_a_w_1.png"
  taxonomy:
    category:
      - リリースノート
      - Next.js
    post_tag:
      - Next.js
      - React
      - TypeScript
      - Docker
      - AI
  custom_fields:
    lead: "v0.3.0では、レシートの重複チェック機能や一覧ページの高度なフィルタリングなど、データ管理を効率化する新機能を多数追加しました。設定ページも拡充され、カテゴリの動的同期やAIへのカスタム指示が可能になり、より柔軟な運用を実現します。"
---

![imagen-4-ultra_2025-10-29T08-16-14-819Z_A_clean__photorealistic_miniature_scene_inside_a_w_1.png](https://raw.githubusercontent.com/Sunwood-ai-labs/harina-v3-webui/main/generated-images/release-v0.3.0-20251029_081513/imagen-4-ultra_2025-10-29T08-16-14-819Z_A_clean__photorealistic_miniature_scene_inside_a_w_1.png)

## はじめに
v0.3.0では、レシートの重複チェック機能や一覧ページの高度なフィルタリングなど、データ管理を効率化するための新機能を多数追加しました。また、設定ページを拡充し、カテゴリの動的同期やAIへのカスタム指示が可能になり、より柔軟な運用を実現します。

## 主な変更点
- **重複チェック機能**: 同一店舗・日付・金額のレシートを自動で検出し、専用ページで確認・削除できます。
- **高度なフィルタリング**: レシート一覧で、キーワード、カテゴリ、店舗、アップロード者、期間を指定して絞り込みが可能になりました。
- **一括カテゴリ更新**: 複数のレシートを選択し、カテゴリとサブカテゴリを一括で変更できるようになりました。
- **設定ページの拡充**: カテゴリ定義の同期機能や、レシート解析時にAIへ追加の指示（プロンプト）を送る機能を追加しました。
- **使用モデルの追跡**: レシート解析に使用されたAIモデル（例: `gemini/gemini-1.5-flash`）が記録・表示されるようになりました。

## 技術的な詳細

### 新機能
#### 重複チェック機能
同一店舗・日付・合計金額のレシートを重複として検出し、`/duplicates` ページで一覧表示する機能を新設しました。グループごとに内容を比較し、不要なレシートを選択して一括で削除できます。これにより、データの精度を高く保つことができます。

#### レシート一覧の機能強化
- **高度なフィルタリング**: キーワード、カテゴリ、店舗名、アップロード者、期間を指定してレシートを絞り込むためのパネルを追加しました。複雑な条件でのデータ検索が容易になります。
- **一括カテゴリ更新**: 一覧で選択した複数のレシート品目に対し、カテゴリとサブカテゴリを一括で設定する機能を追加しました。データ整理の効率が大幅に向上します。

#### 設定ページの拡充
- **カテゴリマスター同期**: Harinaサーバーで定義されたカテゴリ情報をUIに同期するための「カテゴリマスター更新」機能を追加しました。
- **カスタムプロンプト**: レシート解析時に使用するAIへの指示をカスタマイズできる「追加プロンプト」設定機能を追加しました。よりドメインに特化した解析が可能になります。

#### データ管理とその他
- **使用モデルの追跡**: レシート解析に使用したAIモデルをデータベースに保存し、各ページで表示するようにしました。これにより、どのモデルがどのような結果を出力したかを後から追跡できます。
- **CSVエクスポート**: エクスポートされるCSVデータに「使用モデル」列を追加しました。
- **カテゴリ追加**: 「外食」カテゴリと、そのサブカテゴリ（レストラン、カフェ等）を新たに追加しました。
- **APIキーのフォールバック**: Gemini APIのFreeキーが利用できない場合に、本命キーへ自動でフォールバックする機能を追加し、安定性を向上させました。

### 改善点
- **スキーママイグレーション**: データベース起動時に `model_used` カラムなどが存在しない場合、自動で追加するマイグレーション機能を実装しました。
- **環境変数**: Docker環境変数に `GEMINI_API_KEY_FREE` を追加しました。
- **Discordボット**: ボットの通知メッセージに、使用したモデルやAPIキーの種類が表示されるように改善しました。
- **リポジトリ設定**: `.gitignore` に `*.png` ファイルを追加し、不要な画像ファイルがコミットされるのを防ぎます。

### バグ修正
このリリースに分類されるバグ修正はありません。

## まとめ
v0.3.0では、データ管理の効率性と柔軟性を大幅に向上させる機能を追加しました。特に重複チェックと高度なフィルタリングは、多くのユーザーにとって強力なツールとなるはずです。今後のアップデートでは、さらなる分析機能の強化を予定していますので、ご期待ください。

---

📚 **参考リンク**
- **GitHubリポジトリ**: [https://github.com/Sunwood-ai-labs/harina-v3-webui](https://github.com/Sunwood-ai-labs/harina-v3-webui)
- **リリースページ**: [https://github.com/Sunwood-ai-labs/harina-v3-webui/releases/tag/v0.3.0](https://github.com/Sunwood-ai-labs/harina-v3-webui/releases/tag/v0.3.0)
- **比較URL**: [https://github.com/Sunwood-ai-labs/harina-v3-webui/compare/v0.2.0...v0.3.0](https://github.com/Sunwood-ai-labs/harina-v3-webui/compare/v0.2.0...v0.3.0)


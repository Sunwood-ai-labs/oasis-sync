---
title: 【リリースノート】Bookshelf v0.3.0 - 漫画個別ページの追加とUI/UXの大幅改善
post_status: publish
post_excerpt: Bookshelf v0.3.0をリリースしました。本バージョンでは、待望の漫画個別ページ機能を追加し、UIデザインを全面的に刷新するなど、ユーザー体験を大幅に向上させるアップデートが含まれています。
featured_image: https://raw.githubusercontent.com/Sunwood-ai-labs/bookshelf/main/generated-images/release-v0.3.0-20251130_161323/imagen-4-ultra_2025-11-30T16-14-17-522Z_A_micro_book_terrarium_scene_featuring_a_tiny_clay_1.png
taxonomy:
  category:
  - リリースノート
  - フロントエンド
  post_tag:
  - Bookshelf
  - React
  - TypeScript
  - UI/UX
  - HuggingFace
custom_fields:
  lead: Bookshelf v0.3.0がついに登場！本バージョンでは、待望の漫画個別ページ機能の追加や、より直感的に使えるトップナビゲーションへのUI刷新など、使いやすさを大きく向上させる改善が満載です。この記事では、v0.3.0の技術的な詳細と変更のポイントを分かりやすく解説します。
---

```yaml
---
zenn:
  title: "【リリースノート】Bookshelf v0.3.0 - 漫画個別ページの追加とUI/UXの大幅改善"
  emoji: "✨"
  type: "tech"
  topics:
    - react
    - typescript
    - ui-ux
    - huggingface
    - vite
  published: true
qiita:
  title: "【リリースノート】Bookshelf v0.3.0 - 漫画個別ページの追加とUI/UXの大幅改善"
  tags:
    - React
    - TypeScript
    - UI
    - UX
    - HuggingFace
  private: false
  updated_at: null
  id: null
  organization_url_name: null
  slide: false
  ignorePublish: false
wordpress:
  title: "【リリースノート】Bookshelf v0.3.0 - 漫画個別ページの追加とUI/UXの大幅改善"
  post_status: "publish"
  post_excerpt: "Bookshelf v0.3.0をリリースしました。本バージョンでは、待望の漫画個別ページ機能を追加し、UIデザインを全面的に刷新するなど、ユーザー体験を大幅に向上させるアップデートが含まれています。"
  featured_image: "https://raw.githubusercontent.com/Sunwood-ai-labs/bookshelf/main/generated-images/release-v0.3.0-20251130_161323/imagen-4-ultra_2025-11-30T16-14-17-522Z_A_micro_book_terrarium_scene_featuring_a_tiny_clay_1.png"
  taxonomy.category:
    - リリースノート
    - フロントエンド
  taxonomy.post_tag:
    - Bookshelf
    - React
    - TypeScript
    - UI/UX
    - HuggingFace
  custom_fields.lead: "Bookshelf v0.3.0がついに登場！本バージョンでは、待望の漫画個別ページ機能の追加や、より直感的に使えるトップナビゲーションへのUI刷新など、使いやすさを大きく向上させる改善が満載です。この記事では、v0.3.0の技術的な詳細と変更のポイントを分かりやすく解説します。"
---

![imagen-4-ultra_2025-11-30T16-14-17-522Z_A_micro_book_terrarium_scene_featuring_a_tiny_clay_1.png](https://raw.githubusercontent.com/Sunwood-ai-labs/bookshelf/main/generated-images/release-v0.3.0-20251130_161323/imagen-4-ultra_2025-11-30T16-14-17-522Z_A_micro_book_terrarium_scene_featuring_a_tiny_clay_1.png)

## はじめに
Bookshelf v0.3.0をリリースしました。今回のアップデートでは、ユーザーの皆様からご要望の多かった漫画の個別ページ機能を追加し、UI/UXを全面的に刷新しました。より快適に、そして直感的に作品を楽しめるようになった本バージョンの主な変更点と技術的な詳細について解説します。

## 主な変更点
v0.3.0のハイライトは以下の通りです。

- **📖 漫画の個別ページを追加**: 表紙をクリックすると、作品の詳細情報や全ページが一覧できる専用ページに移動できるようになりました ([cced929](https://github.com/Sunwood-ai-labs/bookshelf/commit/cced929))。
- **🎨 UIデザインを刷新**: サイドバーを廃止し、ヘッダーに機能を集約したトップナビゲーションUIに変更しました ([de80160](https://github.com/Sunwood-ai-labs/bookshelf/commit/de80160))。
- **🎞️ リッチなローディングアニメーション**: 本棚や個別ページの読み込み中に、本がパラパラとめくれるような新しいアニメーションを表示します ([c6f917f](https://github.com/Sunwood-ai-labs/bookshelf/commit/c6f917f), [c8196ed](https://github.com/Sunwood-ai-labs/bookshelf/commit/c8196ed))。
- **👤 著者アイコンの表示**: 著者名の横にX (旧Twitter) のプロフィール画像を表示し、視認性を向上させました ([3e87e55](https://github.com/Sunwood-ai-labs/bookshelf/commit/3e87e55))。

## ⚠️ 破壊的変更
### 環境変数の変更
Hugging Faceリポジトリを指定する環境変数が `VITE_HF_TOKEN` から `VITE_REPO` に変更されました。v0.3.0へアップデートする際は、`.env` ファイルの更新が必要です。

- **旧:** `VITE_HF_TOKEN=hf_xxxxxxxx`
- **新:** `VITE_REPO=datasets/username/repo-name`

この変更 ([c8196ed](https://github.com/Sunwood-ai-labs/bookshelf/commit/c8196ed)) により、Hugging Faceのトークンではなく、データセットリポジトリのパスを直接指定する形となり、設定がより直感的になりました。

## 技術的な詳細
### 新機能
#### 漫画個別ページのルーティング
これまで本棚表示のみでしたが、本バージョンから各漫画作品の詳細ページを追加しました。React Routerを利用し、`/manga/:title` というパスで各ページにアクセスできます。これにより、特定の作品をブックマークしたり、URLを共有したりすることが容易になりました。

#### トップナビゲーションレイアウトへの刷新
従来のサイドバーレイアウトを廃止し、画面上部に検索機能などを集約したトップナビゲーションレイアウトへ全面的に刷新しました ([de80160](https://github.com/Sunwood-ai-labs/bookshelf/commit/de80160))。これにより、特にモバイルデバイスでの操作性が向上し、よりシンプルなUIを実現しています。

### 改善点
#### アスペクト比に応じた画像幅の調整
表紙画像の視認性を高めるため、正方形に近いアスペクト比の画像を検出して、表示幅を自動的に1.5倍に拡大する処理を追加しました ([4692778](https://github.com/Sunwood-ai-labs/bookshelf/commit/4692778))。これにより、縦長の表紙と横長の表紙が混在していても、レイアウトのバランスが保たれます。

#### サイトタイトルとファビコンの導入
アプリケーションのアイデンティティを明確にするため、サイトタイトルを「Bookshelf」に設定し、新しいSVGファビコンを導入しました ([be8005b](https://github.com/Sunwood-ai-labs/bookshelf/commit/be8005b), [ec0a764](https://github.com/Sunwood-ai-labs/bookshelf/commit/ec0a764))。

### バグ修正
#### URLエンコードの問題修正
`#` などの特殊文字をタイトルに含む作品の場合、URLが正しく機能しない問題がありました。これを解決するため、URLのパスには作品タイトルではなく、作品が格納されているフォルダ名を `encodeURIComponent` でエンコードして使用するように修正しました ([41f2cdc](https://github.com/Sunwood-ai-labs/bookshelf/commit/41f2cdc))。

## まとめ
Bookshelf v0.3.0は、個別ページの追加とUIの全面的な刷新により、機能性と使いやすさを大きく向上させたメジャーアップデートです。特にトップナビゲーションへの変更は、今後の機能拡張を見据えた重要な基盤となります。

今後もコミュニティからのフィードバックを反映し、より良い読書体験を提供できるよう開発を進めていきます。ぜひ新しいBookshelfをお試しください。

---
📚 参考リンク
- **GitHubリポジトリ**: [https://github.com/Sunwood-ai-labs/bookshelf](https://github.com/Sunwood-ai-labs/bookshelf)
- **変更点の比較**: [https://github.com/Sunwood-ai-labs/bookshelf/compare/v0.2.0...v0.3.0](https://github.com/Sunwood-ai-labs/bookshelf/compare/v0.2.0...v0.3.0)
- **v0.3.0 リリースページ**: [https://github.com/Sunwood-ai-labs/bookshelf/releases/tag/v0.3.0](https://github.com/Sunwood-ai-labs/bookshelf/releases/tag/v0.3.0)
```

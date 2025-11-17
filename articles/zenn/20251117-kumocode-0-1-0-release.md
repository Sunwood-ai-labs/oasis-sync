---
title: 【リリースノート】KumoCode v0.1.0 - Next.jsベースの静的サイトジェネレーターとして刷新
emoji: ✨
type: tech
topics:
- nextjs
- react
- ssg
- typescript
- markdown
published: true
---

![imagen-4-ultra_2025-11-17T13-37-40-348Z_A_stylized_sculpture_of_a_drifting_cloud_woven_wit_1.png](https://raw.githubusercontent.com/Sunwood-ai-labs/KumoCode/main/generated-images/release-v0.1.0-20251117_133650/imagen-4-ultra_2025-11-17T13-37-40-348Z_A_stylized_sculpture_of_a_drifting_cloud_woven_wit_1.png)

## はじめに
この度、Next.jsベースの新しい静的サイトジェネレーター「KumoCode」の最初のバージョンv0.1.0をリリースしました。本バージョンは、システム全体をNext.js (App Router + SSG) へと刷新し、パフォーマンスと開発者体験の向上を実現しています。動的なテーマシステムや豊富な埋め込み機能など、コンテンツ制作を強力にサポートする新機能が多数搭載されました。

## 主な変更点
v0.1.0の主要なアップデートは以下の通りです。

- **Next.jsへの移行**: システム全体をNext.js (App Router + SSG) ベースに刷新し、パフォーマンスと開発者体験を大幅に向上させました。
- **動的テーマシステム**: JSONファイルベースのテーマシステムを導入し、環境変数でデフォルトテーマを指定できるようになりました。`default`, `ocean`, `sunset`, `cyberpunk` の4つのテーマを同梱しています。
- **豊富な埋め込み機能**: Mermaid.jsによるダイアグラム描画、YouTubeやX (旧Twitter) などのURLを自動でカード形式や埋め込みコンテンツに変換する機能を実装しました。
- **UI/UXの改善**: 記事の左側に追従サイドバー型の目次(TOC)を追加し、スクロールに合わせて現在位置がハイライトされるようになりました。

## 技術的な詳細
本リリースにおける主要な機能や改善点について、技術的な背景を解説します。

### 新機能
#### Next.js (App Router + SSG) への移行
プロジェクトの基盤をNext.jsに移行しました (a3408fe)。App Routerと静的サイト生成（SSG）を組み合わせることで、高速なページ表示と優れたSEOパフォーマンスを実現しています。これにより、開発者はReactのモダンなエコシステムを活用しながら、効率的に開発を進めることができます。

#### 動的テーマシステム
JSONファイルでサイトの配色を定義できる、柔軟なテーマシステムを実装しました (ae12464)。
```json:themes/default.json
{
  "colors": {
    "primary": "#3498db",
    "background": "#ffffff",
    "text": "#333333",
    "header": "#2c3e50",
    "accent": "#e74c3c"
  }
}
```
デフォルトテーマは環境変数 `DEFAULT_THEME` で指定可能で (94abe26)、`default`, `ocean`, `sunset`, `cyberpunk` の4種類が標準で利用できます。

#### 豊富な埋め込み機能
Markdownの表現力を高めるため、複数の埋め込み機能を導入しました。

- **Mermaidダイアグラム**: `mermaid` コードブロック内に記述されたテキストを、自動的にダイアグラムとして描画します (b9cf59e)。
- **URLカードと自動埋め込み**: 記事内のURLを自動で解析し、リッチなカード形式に変換したり (cfc301a)、YouTubeやXなどの対応サービスの場合はコンテンツを直接埋め込んだりします (7857ef5)。

#### 追従サイドバー型目次 (TOC)
長文コンテンツの可読性を向上させるため、追従型の目次をサイドバーに実装しました (609e637)。スクロール位置に応じて現在のセクションが自動でハイライトされ、ユーザーは記事全体の構造を把握しやすくなります (4286c68, 2ec5d24)。

### 改善点
#### remarkプラグインの実行順序最適化
URLカードのレンダリングが他のMarkdown変換処理と競合しないよう、remarkプラグインの実行順序を修正しました (b44ed5d, 422a031)。これにより、埋め込みコンテンツが安定して表示されるようになりました。

#### デプロイメントの安定化
`package-lock.json` をリポジトリに追加し、依存関係を固定しました (89d22fc)。これにより、GitHub Actionsを用いたCI/CD環境でのデプロイメントが安定し、環境差異によるエラーを防ぎます。

### バグ修正
- 動画やソーシャルメディアの埋め込みコードが正しいHTMLフォーマットで出力されるように修正しました (5784294, 2e69e4d)。
- `marked` ライブラリのv4以上に対応するため、非推奨となったAPIを利用していた見出しのレンダリング処理を更新しました (bb99efb)。
- MarkdownファイルのFrontmatterが出力後のHTMLに含まれてしまう問題を修正しました (de0fca0)。

## まとめ
KumoCode v0.1.0は、Next.jsというモダンな技術基盤の上に、開発者とコンテンツ制作者双方にとって使いやすい機能を提供することを目指した重要な第一歩です。パフォーマンス、拡張性、そして表現力を兼ね備えた静的サイトジェネレーターとして、今後の機能追加にもご期待ください。

---
📚 **参考リンク**
- **GitHubリポジトリ**: [https://github.com/Sunwood-ai-labs/KumoCode](https://github.com/Sunwood-ai-labs/KumoCode)
- **リリースページ**: [https://github.com/Sunwood-ai-labs/KumoCode/releases/tag/v0.1.0](https://github.com/Sunwood-ai-labs/KumoCode/releases/tag/v0.1.0)
- **Full Changelog**: [https://github.com/Sunwood-ai-labs/KumoCode/commits/v0.1.0](https://github.com/Sunwood-ai-labs/KumoCode/commits/v0.1.0)

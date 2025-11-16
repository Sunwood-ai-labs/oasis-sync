```yaml
---
zenn:
  title: "【リリースノート】Jupytext-Web v0.0.1 - ブラウザでJupyter Notebookとテキストを相互変換"
  emoji: "📝"
  type: "tech"
  topics:
    - "jupyter"
    - "jupytext"
    - "javascript"
    - "web"
    - "converter"
  published: true
qiita:
  title: "【リリースノート】Jupytext-Web v0.0.1 - ブラウザでJupyter Notebookとテキストを相互変換"
  tags:
    - "Jupyter"
    - "Jupytext"
    - "JavaScript"
    - "Web"
    - "Frontend"
  private: false
  updated_at: null
  id: null
  organization_url_name: null
  slide: false
  ignorePublish: false
wordpress:
  title: "【リリースノート】Jupytext-Web v0.0.1 - ブラウザでJupyter Notebookとテキストを相互変換"
  post_status: "publish"
  post_excerpt: "Jupytext-Webの最初のリリースです。このバージョンでは、ファイルアップロードまたはテキスト入力によるJupyter Notebookと各種テキストフォーマットの相互変換、ライブプレビューなど、基本的な機能を実装しました。"
  featured_image: "https://raw.githubusercontent.com/Sunwood-ai-labs/Jupytext-Web/main/generated-images/release-v0.0.1-20251116_130903/imagen-4-ultra_2025-11-16T13-09-55-700Z_A_Celestial_Clockwork_Dreamscape_featuring_a_ringe_1.png"
  taxonomy:
    category:
      - "リリースノート"
      - "フロントエンド"
    post_tag:
      - "Jupyter"
      - "Jupytext"
      - "JavaScript"
      - "Web"
      - "Converter"
  custom_fields:
    lead: "Jupytext-Webの記念すべき最初のバージョンv0.0.1がリリースされました！本バージョンでは、ブラウザ上でJupyter Notebookとテキストファイルをシームレスに相互変換する基本機能を提供します。この記事では、その主な機能と技術的な詳細について解説します。"
---

![imagen-4-ultra_2025-11-16T13-09-55-700Z_A_Celestial_Clockwork_Dreamscape_featuring_a_ringe_1.png](https://raw.githubusercontent.com/Sunwood-ai-labs/Jupytext-Web/main/generated-images/release-v0.0.1-20251116_130903/imagen-4-ultra_2025-11-16T13-09-55-700Z_A_Celestial_Clockwork_Dreamscape_featuring_a_ringe_1.png)

## はじめに
Jupytext-Webの記念すべき最初のバージョンv0.0.1がリリースされました！本バージョンでは、ブラウザ上でJupyter Notebookとテキストファイルをシームレスに相互変換する基本機能を提供します。この記事では、その主な機能と技術的な詳細について解説します。

## 主な変更点
v0.0.1は初回リリースであり、Jupytext-Webのコアとなる機能を実装しました。

- **Jupytext Web Converter**: ブラウザ上でJupyter Notebook (`.ipynb`) とテキストファイル（Markdown, Pythonスクリプトなど）を相互に変換するコア機能を実装しました。
- **多彩な入力方法**: ファイルのドラッグ＆ドロップ、またはエディタへの直接テキスト入力に対応しています。
- **ライブプレビュー**: 入力内容をリアルタイムでプレビューし、変換結果を即座に確認できます。`.ipynb`ファイルはビジュアル表示にも対応。
- **高機能エディタ**: ACEエディタを統合し、シンタックスハイライトや自動補完機能を提供します。
- **UI/UXの改善**: モダンなデザイン、日英言語切り替え、GitHubリボン、ファビコンなどを追加し、使いやすさを向上させました。

## 技術的な詳細
### 新機能
本リリースで実装された主要な機能は以下の通りです。

- **テキスト入力モードとACEエディタの導入**
  - ファイルアップロードに加え、エディタに直接テキストを貼り付けて変換できるモードを追加しました。(cdaae35)
  - 高機能なACEエディタを統合し、主要な言語のシンタックスハイライトや自動補完が利用可能になりました。(0a46fed)

- **`.ipynb`ファイルのビジュアルプレビュー**
  - アップロードまたは入力された`.ipynb`ファイルの内容を、ノートブック形式で視覚的にプレビューする機能を追加しました。これにより、変換前に内容を簡単に確認できます。(01650c9)

- **UI/UXの強化**
  - サイト全体のUIを刷新し、モダンなデザインとアンビエントエフェクトを導入しました。(36c2bff)
  - 日本語と英語の言語切り替え機能を実装し、より多くのユーザーが利用しやすくなりました。(07c841c)
  - ダウンロードファイル名にタイムスタンプを含めるかを選択できるオプションを追加しました。(645220a)
  - 画面右上にGitHubリポジトリへのリンクを常時表示するリボンを設置しました。(81fe4e3)

### 改善点
初回リリースに伴い、コードベースの整理やドキュメントの整備も行いました。

- **コードの分離とレイアウト整理**
  - メンテナンス性向上のため、CSSとJavaScriptをHTMLファイルから個別のファイルに分離しました。(b7074a2)
  - プレビューのネスト構造をフラット化し、よりクリーンなレイアウトに整理しました。(b42e8e1, 3ba3df0)

- **ドキュメントの更新**
  - プロジェクトの概要や利用方法を記載した`README.md`を更新し、フォーマットを改善しました。(60e29e8, 92eb36e)

### バグ修正
開発過程で発見されたいくつかの不具合を修正しました。

- ACEエディタの自動補完オプションが有効にならない問題を修正しました。(a3cf6fb)
- タイムスタンプラベルの`for`属性が欠落していた問題を修正しました。(f0f0a64)
- ノートブックプレビュー機能におけるJSONパースエラーや、ネスト表示に関する不具合を修正しました。(0a3de54, b9edcbf)
- プレビューパネルのMarkdownシンタックスハイライトが正しく適用されるように修正しました。(06d7fc6)

## まとめ
Jupytext-Web v0.0.1は、ブラウザ上で手軽にJupyter Notebookとテキストファイルの相互変換を実現するための第一歩です。基本的な変換機能に加え、高機能エディタやライブプレビューなど、開発体験を向上させるための多くの機能を盛り込みました。ぜひお試しいただき、フィードバックをお寄せください。

---
📚 参考リンク
- **GitHubリポジトリ**: [https://github.com/Sunwood-ai-labs/Jupytext-Web](https://github.com/Sunwood-ai-labs/Jupytext-Web)
- **リリースページ**: [https://github.com/Sunwood-ai-labs/Jupytext-Web/releases/tag/v0.0.1](https://github.com/Sunwood-ai-labs/Jupytext-Web/releases/tag/v0.0.1)
- **比較URL**: [https://github.com/Sunwood-ai-labs/Jupytext-Web/compare/v0.0.1...v0.0.1](https://github.com/Sunwood-ai-labs/Jupytext-Web/compare/v0.0.1...v0.0.1)
```

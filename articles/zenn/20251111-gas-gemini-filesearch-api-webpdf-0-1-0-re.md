---
title: gemini-filesearch-api - Google Driveファイル検索APIの初期リリース
emoji: 🔍
type: tech
topics:
- google-apps-script
- gas
- gemini-api
- google-drive
- api
published: true
---

![imagen-4-ultra_2025-11-11T17-39-36-555Z_A_soft_polymer_clay_cloud_dragon_figurine_with_rou_1.png](https://raw.githubusercontent.com/Sunwood-ai-labs/gas-gemini-filesearch-api-webpdf/main/generated-images/release-v0.1.0-20251111_173830/imagen-4-ultra_2025-11-11T17-39-36-555Z_A_soft_polymer_clay_cloud_dragon_figurine_with_rou_1.png)

## はじめに
この度、Google Drive内のファイルを横断的に検索するAPI `gas-gemini-filesearch-api-webpdf` の初期バージョンv0.1.0をリリースしました。本プロジェクトはGoogle Apps Script（GAS）をベースに構築されており、Web APIとして外部から簡単に利用できます。

今回のリリースでは、Gemini Pro Visionとの連携により、テキストファイルだけでなくPDFや画像ファイルの内容もテキスト化して検索対象に含めることが可能になりました。

## 主な変更点
v0.1.0の主なハイライトは以下の通りです。

- **Google Driveファイル検索API**: 指定したフォルダ配下のファイルをキーワードで横断的に検索するAPIを実装しました。
- **Webアプリとしてのデプロイ**: GASのWebアプリとしてデプロイすることで、外部アプリケーションからHTTPリクエストを通じて検索機能を利用できます。
- **Gemini Pro Vision連携**: PDFや画像ファイルの内容をテキスト化し、全文検索の対象に含める機能を搭載しました。
- **シンプルなフロントエンド**: APIの動作をすぐに確認できる、基本的なHTMLフロントエンドを同梱しています。

## 技術的な詳細
### 新機能
今回のリリースは初期バージョンであり、すべての変更が新機能となります。

#### 1. Google Driveファイル検索API (`code.gs`)
プロジェクトの中核となるファイル検索APIを実装しました。GASの `doGet` 関数を利用して、HTTP GETリクエストを受け付けます。以下のパラメータを指定することで、柔軟な検索が可能です。

- `query`: 検索キーワード
- `folderId`: 検索対象のGoogle DriveフォルダID
- `maxResults`: 最大取得件数

APIは検索結果をJSON形式で返し、ファイル名、URL、ファイル内容の抜粋などを含みます。

#### 2. 動作確認用フロントエンド (`index.html`)
APIの基本的な動作を手軽に試せるように、シンプルなHTMLファイルを用意しました。フォームに検索キーワードとフォルダIDを入力して実行すると、APIから返された検索結果を画面に表示します。

```html
<!-- index.html の抜粋 -->
<form id="searchForm">
  <input type="text" id="query" placeholder="検索キーワード">
  <input type="text" id="folderId" placeholder="フォルダID">
  <button type="submit">検索</button>
</form>
<div id="results"></div>
```

#### 3. ドキュメントとワークフローの整備
開発者がスムーズにプロジェクトを理解し、貢献できるようにドキュメントを刷新しました。

- **README.md**: プロジェクトの概要、デプロイ手順、APIの使用方法などを網羅的に記載しました。
- **GitHub Actions**: リリースノートの自動生成やPull Requestのレビューを自動化するワークフローを導入し、開発プロセスを効率化しました。

## まとめ
`gas-gemini-filesearch-api-webpdf` v0.1.0は、Google Driveの検索性を飛躍的に向上させるための第一歩です。特に、Gemini Pro Visionを活用して画像やPDFの内容まで検索対象とすることで、これまで見つけにくかった情報へのアクセスを容易にします。

今後、より高度な検索オプションの追加や、パフォーマンスの改善を進めていく予定です。ぜひ一度お試しいただき、フィードバックをお寄せください。

---
📚 参考リンク
- **GitHubリポジトリ**: [Sunwood-ai-labs/gas-gemini-filesearch-api-webpdf](https://github.com/Sunwood-ai-labs/gas-gemini-filesearch-api-webpdf)
- **v0.1.0 リリースページ**: [https://github.com/Sunwood-ai-labs/gas-gemini-filesearch-api-webpdf/releases/tag/v0.1.0](https://github.com/Sunwood-ai-labs/gas-gemini-filesearch-api-webpdf/releases/tag/v0.1.0)
```

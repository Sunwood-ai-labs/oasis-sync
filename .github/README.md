# `.github` ディレクトリ概要

このディレクトリには、GitHub Actions のワークフロー定義や補助スクリプト、Issue テンプレートなど、リポジトリ運用を自動化するための資材がまとまっています。  
プロジェクト全体の仕組みを俯瞰したい場合は、`.SourceSageAssets/DOCUMIND/Repository_summary.md` も併せて参照してください。

## ワークフロー一覧

- **Gemini Actions Labs グループ** `workflows/` + `no_workflows/gemini-actions-labs/`
  - リリースノート生成（`gemini-release-notes.yml`）と派生記事生成（`gemini-release-articles.yml`）
  - Persona 別 PR レビュー、Issue トリアージ、Imagen による画像生成 など
- **Oasis Sync 系** `workflows/` + `no_workflows/oasis/`
  - Issue フォーム経由で記事・サムネイルを取り込むフロー（`oasis-issue-intake.yml`, `oasis-article-thumbnail_experimental.yml`, `thumbnail_intake_experimental.yml`）
  - Oasis 記事を Zenn / Qiita / WordPress 向けに展開する同期フロー（`oasis-sync.yml` ほか）
- **その他**
  - Hugging Face Space へのデプロイ（`huggingface-space-deploy.yml`）
  - 静的サイト公開（`static-site.yml`）
  - PyPI / TestPyPI へのリリース（`pypi-release.yml`）

## スクリプト

`scripts/` 配下（Actions からは `.github/scripts/` として参照）には、ワークフローから呼び出される実行ファイルがまとまっています。主なものは次の通りです。

- `ingest_oasis_issue.py` / `ingest_thumbnail_issue.py`  
  Issue フォームの本文を解析し、記事ファイルや画像を生成します。`article_slug` の自動補完や画像のダウンロードもここで処理します。
- `process_oasis_articles.py`  
  Oasis 記事を解析して Gemini への入力を生成し、戻ってきたメタデータを Zenn / Qiita / WordPress 用に反映します。
- `sync_platform.sh`  
  生成された記事を各配信先リポジトリへ同期する共通シェルスクリプトです。
- `write_oasis_article_thumbnail_comment.py` / `write_thumbnail_comment.py`  
  ワークフローの結果を Issue へ報告する Markdown コメントを生成します。

Python スクリプトは基本的に 3.11 で実行される想定です。依存はワークフロー側で `pip install` されます。

## Issue テンプレート

`ISSUE_TEMPLATE/` には、Oasis 記事登録・サムネイル登録用の Issue Forms が配置されています。  
`oasis-article-thumbnail-experimental.yml` では front matter 内の `article_slug` を参照するようになっているため、フォームのスラッグを空欄にしても意図したファイル名で記事を生成できます。

## Secrets / Variables の目安

詳しい一覧は `workflows/architecture.md` にまとまっていますが、主に次の値が必要です。

- `GEMINI_API_KEY`：Gemini CLI / Imagen 系ワークフロー共通
- `GH_PAT`（および Persona 用 PAT）：リポジトリへの push や Issue へのコメントに使用
- `QIITA_TOKEN`：`qiita/publish.yml` で利用
- Hugging Face 関連 (`HUGGINGFACE_TOKEN`)、GCP Workload Identity 設定 など

Secrets や Variables を更新した際は、関連するワークフローを手動実行して疎通確認することを推奨します。

## ドキュメントの参照先

- `workflows/architecture.md`：パイプライン全体の図解と詳細な解説
- `prompts/`：Gemini CLI / Reviewer / Imagen 用のプロンプトテンプレート
- `.SourceSageAssets/DOCUMIND/Repository_summary.md`：ファイル構成サマリー（IDE 用補助ドキュメント）

これらの資料を併用すると、`.github` 配下の管理対象を素早く把握できます。***

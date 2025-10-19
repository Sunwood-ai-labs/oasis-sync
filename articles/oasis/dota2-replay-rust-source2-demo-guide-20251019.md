---
article_slug: dota2-replay-rust-source2-demo-guide-20251019
zenn:
  title: 🎮 Dota 2 のリプレイを Rust で解析する完全ガイド
  emoji: 🎮
  type: tech
  topics:
  - rust
  - dota2
  - source2-demo
  - replay
  - windows
  published: true
qiita:
  title: 🎮 Dota 2 のリプレイを Rust で解析する完全ガイド
  tags:
  - Rust
  - Dota2
  - Source2-demo
  - Replay
  - Windows
  private: false
  updated_at: null
  id: null
  organization_url_name: null
  slide: false
  ignorePublish: false
wordpress:
  title: 🎮 Dota 2 のリプレイを Rust で解析する完全ガイド
  post_status: publish
  post_excerpt: Windows上でRust製の`source2-demo`を用い、Dota 2のリプレイ（.dem）を解析するまでの手順を、実際のPowerShell出力とコマンド例で解説。環境構築、リプレイ取得、ビルドと実行、各サンプルの使い方まで網羅します。
  featured_image: https://raw.githubusercontent.com/Sunwood-ai-labs/oasis-sync/main/images/thumbnails/dota2-replay-rust-source2-demo-guide-20251019.png
  taxonomy:
    category:
    - rust
    - dota-2
    - windows
    post_tag:
    - Rust
    - Dota2
    - Source2-demo
    - Replay
    - Windows
  custom_fields:
    lead: RustとGitの導入から`source2-demo`のビルド、`.dem`の配置と実行までをWindows向けに実践解説。Elapsed表示で動作確認し、combatlog等の応用にも触れます。
---

![dota2-replay-rust-source2-demo-guide-20251019](https://raw.githubusercontent.com/Sunwood-ai-labs/oasis-sync/main/images/thumbnails/dota2-replay-rust-source2-demo-guide-20251019.png)

https://x.com/hAru_mAki_ch/status/1979882175513362631

## 🧭 はじめに

Dota 2 のリプレイファイル（`.dem`）には、
**全プレイヤーの位置・行動・イベント**がすべて記録されています。

この記事では、Rust 製パーサー **[`source2-demo`](https://github.com/Rupas1k/source2-demo)** を使って、
実際に自分の試合を解析できる環境を Windows 上で構築する方法を解説します。



---

## 🧩 Rust と Git をインストールする

### ▶ Rust の導入

PowerShell で以下を実行：

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
````

Windows の場合は、インストーラ（`rustup-init.exe`）を使うのが簡単です。
完了したら、新しいターミナルで確認：

```bash
rustc --version
cargo --version
```

出力例：

```
rustc 1.90.0 (1159e78c4 2025-09-14)
cargo 1.90.0
```

### ▶ Git の確認

```bash
git --version
```

もし入っていなければ、[Git for Windows](https://git-scm.com/download/win) をインストール。

---

## 📦 `source2-demo` をクローンする

リポジトリを取得して、Dota 2 用サンプルがあるフォルダへ移動します。

```bash
git clone https://github.com/Rupas1k/source2-demo
cd source2-demo/d2-examples
```

---

## ⚙️ Rust を最新版にアップデート

古いバージョン（1.80 など）だと依存関係の `indexmap` が対応していないため、更新します。

```bash
rustup target remove wasm32-wasi
rustup toolchain install stable --profile minimal
rustup default stable
rustc --version
```

✅ 出力例

```
rustc 1.90.0 (1159e78c4 2025-09-14)
```

これでOK！

---

## 🎮 自分のリプレイ（.dem）を取得する

### ▶ Dota 2 クライアントから

1. Dota 2 を起動
2. **「Watch（観戦）」→「Your Matches」** へ
3. 試合を選んで **「Download Replay」** をクリック

### ▶ ファイルの場所

通常は以下に保存されています：

```
C:\Program Files (x86)\Steam\steamapps\common\dota 2 beta\dota\replays
```

リプレイファイルの拡張子は `.dem`
例）`auto-20251019-2017-start-maki.dem`

---

## 📂 リプレイをプロジェクトに置く

あなたの環境ではすでに以下のように配置できています 👇

```powershell
PS C:\Prj\source2-demo\d2-examples> ls
...
-a---- 47397110 auto-20251019-2017-start-maki.dem
```

この `.dem` がリプレイデータです。

---

## 🚀 サンプルをビルド＆実行する

### ▶ ビルド

```bash
cargo clean
cargo build --release
```

### ▶ 実行

```bash
cargo run --release --bin chat -- "auto-20251019-2017-start-maki.dem"
```

出力例：

```
Elapsed: 279.5053ms
```

これでリプレイ解析が成功 🎉
（チャットメッセージが無ければログ出力は空のままでOK）

---

## 🧩 他のサンプルを試す

より出力が見やすい解析もあります。

| サンプル名         | コマンド                                                    | 内容                  |
| ------------- | ------------------------------------------------------- | ------------------- |
| **combatlog** | `cargo run --release --bin combatlog -- "auto-....dem"` | 戦闘ログ（ダメージ、キル、スキル発動） |
| **lifestate** | `cargo run --release --bin lifestate -- "auto-....dem"` | 死亡・復活イベント           |
| **wards**     | `cargo run --release --bin wards -- "auto-....dem"`     | ワード設置・破壊            |

---

## 🧠 成功のサイン

出力に「Elapsed: xxx ms」が出てエラーがなければ、
**Rust の環境・依存・ファイル読み込みがすべて正しく動いている**証拠です。


---

## ✅ まとめ

| ステップ     | 内容                               | 結果               |
| -------- | -------------------------------- | ---------------- |
| Rust環境構築 | rustup & git                     | 最新版でOK           |
| リポジトリ取得  | `git clone`                      | d2-examples 準備完了 |
| リプレイ入手   | Dota 2クライアント                     | `.dem` ファイル取得    |
| 実行       | `cargo run --release --bin chat` | 正常解析（Elapsed表示）  |
| 次の一歩     | combatlog・位置情報抽出                 | より詳細な解析へ         |

---

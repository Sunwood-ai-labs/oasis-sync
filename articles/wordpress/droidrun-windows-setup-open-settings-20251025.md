---
title: 【実践ログ】Windowsで DroidRun をセットアップして「Open the settings app」まで動かしてみた！
post_status: publish
post_excerpt: DroidRunは、AIを使ってAndroidやiOSデバイスを自然言語で操作できるオープンソースフレームワークです。本記事では、Windows
  11環境でADB設定からDroidRun v0.4.0のインストール、Portalアプリ導入、そして「Open the settings app」で設定アプリを自動起動するまでの手順を実践形式で解説します。
featured_image: https://raw.githubusercontent.com/Sunwood-ai-labs/oasis-sync/main/images/thumbnails/droidrun-windows-setup-open-settings-20251025.png
taxonomy:
  category:
  - android
  - ai
  - windows
  post_tag:
  - DroidRun
  - Android
  - ADB
  - AI
  - Windows
custom_fields:
  lead: Windows上でDroidRunを導入し、「Open the settings app」で実際にスマホ設定を開くまでの手順を記録しました。ADBセットアップからPortal導入、AI操作の動作確認までを詳しく解説します。
---

## 💡 DroidRunとは

[DroidRun](https://github.com/droidrun/droidrun) は、AI（LLM）を使って **Android／iOS デバイスを自然言語で操作できる** オープンソースフレームワーク。
英語で「Open the settings app」と指示するだけで、実際にスマホの設定アプリを開いてくれます。

https://x.com/hAru_mAki_ch/status/1982070673985179790

---

## 🧰 検証環境

| 項目       | 内容                             |
| -------- | ------------------------------ |
| OS       | Windows 11                     |
| Python   | 3.13.3（uv経由の仮想環境）              |
| DroidRun | v0.4.0                         |
| ADB      | v1.0.41（platform-tools 36.0.0） |
| デバイス     | Android（USB接続）                 |

---

## ⚙️ ステップ1：ADBを準備する

### 1️⃣ ADBとは？

**Android Debug Bridge（ADB）** は、パソコンからスマホを操作するためのコマンドラインツール。
DroidRunも内部でADBを使って端末を制御します。

### 2️⃣ ダウンロード

👉 [Android Platform Tools（公式）](https://developer.android.com/tools/releases/platform-tools?hl=ja)

ダウンロードしたZIPを解凍して、
`C:\Users\<あなたの名前>\Downloads\platform-tools-latest-windows\platform-tools\adb.exe`
などに配置します。

### 3️⃣ 環境変数PATHに追加

1. Windows検索 → 「環境変数」と入力 → 「環境変数の編集」を開く
2. 「Path」に platform-tools のフォルダパスを追加
3. 再起動後、PowerShellで確認：

```powershell
adb version
````

出力例：

```
Android Debug Bridge version 1.0.41
Version 36.0.0-13206524
```

✅ これが出れば準備OK！

---

## 📱 ステップ2：スマホ側の設定

1. 「設定」→「デバイス情報」→「ビルド番号」を7回タップして開発者モードをON
2. 「設定」→「システム」→「開発者向けオプション」→「USBデバッグ」をON
3. スマホをUSBでPCに接続し、表示された「このパソコンを許可しますか？」に「許可」

---

## 📁 ステップ3：作業ディレクトリを作成

```powershell
PS C:\Prj> mkdir drun-demo
PS C:\Prj> cd .\drun-demo\
```

---

## 🐍 ステップ4：仮想環境を作成（uv使用）

```powershell
uv venv
.venv\Scripts\activate
```

---

## 📦 ステップ5：DroidRunをインストール

```powershell
uv pip install droidrun
```

出力に

```
+ droidrun==0.4.0
Successfully installed ...
```

と出れば成功です。

---

## 🔌 ステップ6：デバイス接続確認

```powershell
uv run droidrun devices
```

初回は「No devices connected」と出ることもあります。
もう一度試すと……

```
Found 1 connected device(s):
  • d7b42150
```

✅ 接続完了！

---

## 🧩 ステップ7：Portalアプリをインストール

DroidRunがスマホのUIを操作するためには Portal アプリが必要です。

🔗 [DroidRun Portal v0.4.0 ダウンロード](https://github.com/droidrun/droidrun-portal/releases/tag/v0.4.0)

1. ダウンロードした `droidrun-portal.apk` をADBでインストール

   ```powershell
   adb install droidrun-portal.apk
   ```
2. スマホ側で「設定 → アクセシビリティ → DroidRun Portal」をONにします。

---

## 🚀 ステップ8：実行してみる！

```powershell
uv run droidrun "Open the settings app"
```

出力例：

```
🚀 Running DroidAgent to achieve goal: Open the settings app
💻 Executing action code
open_app("Settings")
✅ Task completed: Successfully opened the settings app.
🎉 Goal achieved!
```

✨ **設定アプリが自動で開く！**

まさにAIがスマホを直接操作してくれる瞬間です。

---

## 🔁 （補足）スマホ画面をPCにリアルタイム表示したい人へ

DroidRunのデバッグや発信用に、**画面ミラーリング**をしたい場合は
[Genymobile / scrcpy](https://github.com/Genymobile/scrcpy/releases) が超おすすめ。

* 🔗 最新版（v3.3.3）：
  [scrcpy-win64-v3.3.3.zip](https://github.com/Genymobile/scrcpy/releases/download/v3.3.3/scrcpy-win64-v3.3.3.zip)

使い方は簡単：

```
1. ZIPを展開 → scrcpy.exe を実行
2. スマホをUSB接続
3. すぐにミラーリング開始！
```

---

## ✅ まとめ

ここまでで実施したこと：

1. ADBをセットアップ（PATH登録・USBデバッグON）
2. DroidRunを仮想環境にインストール
3. Portalアプリを導入
4. 実際に「Open the settings app」で動作確認
5. （希望者向け）scrcpyでミラーリング

これで、AIによるAndroid操作環境が完全に整いました！

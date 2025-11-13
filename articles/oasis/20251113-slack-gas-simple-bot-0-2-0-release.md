```---
zenn:
  title: "【リリースノート】Slack GAS Simple Bot v0.2.0 - スレッド返信対応とUI改善"
  emoji: "✨"
  type: "tech"
  topics:
    - "slack"
    - "gas"
    - "google-apps-script"
    - "bot"
    - "javascript"
  published: true
qiita:
  title: "【リリースノート】Slack GAS Simple Bot v0.2.0 - スレッド返信対応とUI改善"
  tags:
    - "Slack"
    - "GAS"
    - "GoogleAppsScript"
    - "Bot"
    - "JavaScript"
  private: false
  updated_at: null
  id: null
  organization_url_name: null
  slide: false
  ignorePublish: false
wordpress:
  title: "【リリースノート】Slack GAS Simple Bot v0.2.0 - スレッド返信対応とUI改善"
  post_status: "publish"
  post_excerpt: "Slack GAS Simple Bot v0.2.0がリリースされました。このバージョンでは、Slackのスレッドへの返信機能が追加され、メッセージ投稿時のUIが改善され、より円滑なコミュニケーションが可能になりました。"
  featured_image: "https://raw.githubusercontent.com/Sunwood-ai-labs/slack-gas-simple-bot/main/generated-images/release-v0.2.0-20251113_184707/imagen-4-ultra_2025-11-13T18-48-05-180Z_A_Bioluminescent_Forest_Reverie_featuring_a_radian_1.png"
  taxonomy:
    category:
      - "リリースノート"
      - "Google Apps Script"
  taxonomy:
    post_tag:
      - "Slack"
      - "GAS"
      - "GoogleAppsScript"
      - "Bot"
      - "JavaScript"
  custom_fields:
    lead: "SlackとGoogle Apps Scriptを連携させるシンプルなBotプロジェクトのv0.2.0が公開されました。本記事では、スレッド返信対応やUI改善といった主要な変更点について、技術的な背景を交えて解説します。"
---

![imagen-4-ultra_2025-11-13T18-48-05-180Z_A_Bioluminescent_Forest_Reverie_featuring_a_radian_1.png](https://raw.githubusercontent.com/Sunwood-ai-labs/slack-gas-simple-bot/main/generated-images/release-v0.2.0-20251113_184707/imagen-4-ultra_2025-11-13T18-48-05-180Z_A_Bioluminescent_Forest_Reverie_featuring_a_radian_1.png)

## はじめに
SlackとGoogle Apps Script（GAS）を連携させるシンプルなBotプロジェクト「Slack GAS Simple Bot」のv0.2.0がリリースされました。このアップデートでは、ユーザーからのフィードバックを反映し、より円滑なコミュニケーションを実現するための機能強化が行われています。

本記事では、v0.2.0での主要な変更点である「スレッド返信対応」と「UI改善」について、その技術的な詳細とメリットを解説します。

## 主な変更点
今回のリリースに含まれる主な変更点は以下の通りです。

- **✨ Slackスレッドへの返信機能:** 特定のメッセージに対して、スレッド内で返信できるようになりました。
- **✨ メッセージ投稿UIの改善:** より直感的で使いやすいインターフェースに更新しました。
- **🔧 メンテナンス:** v0.1.0のリリースイメージを追加しました。

## 技術的な詳細
### 新機能
#### Slackスレッドへの返信対応
これまでBotからの返信は、常に新しいメッセージとしてチャンネルに投稿されていました。v0.2.0からは、元の投稿のタイムスタンプ（`thread_ts`）を識別し、それに対して返信することで、会話の文脈を維持できるようになりました。

具体的には、Slackから送られてくるイベントペイロードに `thread_ts` が含まれている場合、それをGAS側で取得し、Slack APIの `chat.postMessage` メソッドの引数に含めるように `code.gs` を変更しました。

```javascript
// code.gs の変更（イメージ）
function replyToSlack(e) {
  const postData = {
    channel: e.parameter.channel_id,
    text: "こちらが返信です。",
    thread_ts: e.parameter.thread_ts // thread_tsをペイロードに追加
  };
  
  // ... UrlFetchAppでSlack APIを呼び出す処理
}
```
この改修により、関連するやり取りが一つのスレッドにまとまり、チャンネルが散らかるのを防ぎます。

#### メッセージ投稿UIの改善
メッセージ投稿時のUI（`index.html`）を見直し、操作性を向上させました。モーダルダイアログのデザインを調整し、テキストエリアを広げることで、長文のメッセージも入力しやすくなっています。また、送信ボタンの視認性を高め、より直感的な操作が可能になりました。

### 改善点
今回のリリースでは、主に新機能の追加に焦点を当てており、既存機能の大きな改善点はありません。

### バグ修正
今回のリリースでは、主要なバグ修正はありません。

## まとめ
v0.2.0では、スレッド返信機能の実装とUIの改善により、Slack GAS Simple Botがより実用的で使いやすいツールへと進化しました。特にスレッド返信は、複数人でのコミュニケーションを円滑にするための重要な機能です。

ぜひ新しいバージョンをお試しいただき、フィードバックをお寄せください。

---
📚 **参考リンク**
- **GitHubリポジトリ:** [Sunwood-ai-labs/slack-gas-simple-bot](https://github.com/Sunwood-ai-labs/slack-gas-simple-bot)
- **v0.2.0リリースページ:** [Release v0.2.0](https://github.com/Sunwood-ai-labs/slack-gas-simple-bot/releases/tag/v0.2.0)
- **v0.1.0との比較:** [Compare v0.1.0...v0.2.0](https://github.com/Sunwood-ai-labs/slack-gas-simple-bot/compare/v0.1.0...v0.2.0)
```

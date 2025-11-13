---
title: 【リリースノート】Slack GAS Simple Bot v0.1.0 - Slackオウム返しボットの初期リリース
emoji: 🤖
type: tech
topics:
- gas
- slack
- google-apps-script
- bot
- javascript
published: true
---

![imagen-4-ultra_2025-11-13T16-22-36-320Z_A_Bioluminescent_Forest_Reverie_featuring_a_radian_1.png](https://raw.githubusercontent.com/Sunwood-ai-labs/slack-gas-simple-bot/main/generated-images/release-v0.1.0-20251113_162136/imagen-4-ultra_2025-11-13T16-22-36-320Z_A_Bioluminescent_Forest_Reverie_featuring_a_radian_1.png)

## はじめに
この度、Google Apps Script（GAS）で動作するシンプルなSlackボット「Slack GAS Simple Bot」の最初のバージョンv0.1.0をリリースしました。このプロジェクトは、GASを手軽に利用してSlackとの連携を実現することを目的としています。本記事では、v0.1.0の主な変更点や技術的な詳細について解説します。

## 主な変更点
- **オウム返しボットの基本機能**: Slackに投稿されたメッセージをそのまま返信するコア機能を実装しました。
- **ランディングページ**: プロジェクトの概要を紹介するためのシンプルなWebページを追加しました。
- **信頼性の向上**: メッセージ処理に関するバグ修正とリファクタリングを行い、安定性を高めました。
- **ドキュメントの充実**: `README.md`にスクリーンショットや詳細な説明を追加し、導入しやすくなるよう改善しました。

## 技術的な詳細
### 新機能
#### 1. Slackオウム返し機能 (a8ed0e4)
GASの`doPost(e)`関数をトリガーとして、Slackからのイベントを受け取ります。受け取ったメッセージは`processMessage`関数に渡され、投稿されたテキストをそのままJSONペイロードとしてSlack APIに送り返すことで、オウム返しを実現しています。

```javascript:code.gs
function doPost(e) {
  const verificationToken = PropertiesService.getScriptProperties().getProperty('VERIFICATION_TOKEN');
  if (e.parameter.token !== verificationToken) {
    throw new Error('Invalid token');
  }

  const event = JSON.parse(e.postData.contents).event;
  if (event.type === 'message' && !event.subtype) {
    processMessage(event.text, event.channel);
  }
}

function processMessage(text, channel) {
  const slackApp = SlackApp.create(PropertiesService.getScriptProperties().getProperty('SLACK_ACCESS_TOKEN'));
  slackApp.postMessage(channel, text);
}
```

#### 2. プロジェクト紹介用ランディングページ (2bc3245)
GASの`doGet(e)`関数を利用して、プロジェクトを紹介する簡単なHTMLページを公開する機能を追加しました。これにより、ボットのURLにアクセスしたユーザーがプロジェクトの概要を把握できるようになります。

```html:index.html
<!DOCTYPE html>
<html>
  <head>
    <base target="_top">
    <title>Slack GAS Simple Bot</title>
  </head>
  <body>
    <h1>Slack GAS Simple Bot</h1>
    <p>This is a simple Slack bot powered by Google Apps Script that echoes messages.</p>
  </body>
</html>
```

### 改善点
#### `processMessage`関数のリファクタリング (d7cf593)
初期実装からコードを整理し、`processMessage`関数を独立させることで、メッセージ処理ロジックの保守性と可読性を向上させました。

### バグ修正
#### メッセージ処理の信頼性向上 (d7cf593)
`processMessage`関数内のバグを修正し、特定の条件下でメッセージが正しく処理されなかった問題を解決しました。これにより、ボットの応答信頼性が向上しています。

## まとめ
v0.1.0では、Slack GAS Simple Botの基本的な骨格が完成しました。メッセージのオウム返しというシンプルな機能ですが、GASとSlack連携の第一歩として重要なリリースです。今後は、より複雑な対話機能や外部APIとの連携などを視野に入れて開発を進めていく予定です。

---
📚 参考リンク
- **GitHubリポジトリ**: [Sunwood-ai-labs/slack-gas-simple-bot](https://github.com/Sunwood-ai-labs/slack-gas-simple-bot)
- **リリースページ**: [v0.1.0 Release](https://github.com/Sunwood-ai-labs/slack-gas-simple-bot/releases/tag/v0.1.0)
- **比較URL**: [v0.1.0...v0.1.0](https://github.com/Sunwood-ai-labs/slack-gas-simple-bot/compare/v0.1.0...v0.1.0)

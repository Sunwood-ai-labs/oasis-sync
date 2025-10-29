---
title: Colabで「Agent Lightning / examples/apo」を動かす
emoji: ⚡
type: tech
topics:
- agent-lightning
- apo
- colab
- prompt-optimization
- openai
published: true
---

![run-agent-lightning-examples-apo-on-colab-20251029](https://raw.githubusercontent.com/Sunwood-ai-labs/oasis-sync/main/images/thumbnails/run-agent-lightning-examples-apo-on-colab-20251029.png)

— 5つのセルで体験する“自動プロンプト最適化（APO）”

AIエージェントを**ほぼゼロ改変**で“育てる”。Microsoftの**Agent Lightning**は、実行ログと報酬から学んで**プロンプトを自動改善（APO）**したり、RLやSFTへ広げられる実験フレームワークです。ここでは公式サンプル `examples/apo` の**Room Selector**（会議室を選ぶエージェント）を**Google Colab**で再現します。セットアップ、実行、ハマりやすい点、次の一歩までをまとめました。



https://x.com/hAru_mAki_ch/status/1983520643774836955

## 何をやるか

* `examples/apo/room_selector_apo.py` を**Colabで手早く実行**
* APO（自動プロンプト最適化）の**流れ**と**見るべきログ**を把握
* **エラー対処**や**コスト/時間のコントロール**を理解

## 事前準備

* **OpenAI APIキー**（課金/利用制限に注意）
* **環境**：Colab（Linux）。Python 3.10+を想定
* **モデル**：スクリプト内の既定モデルが使えない場合は、手持ちで使える軽量モデルに差し替え（例：`gpt-4o-mini` など）

## クイックスタート（Colab用コピペ）

### ライブラリのインストール

```python
!pip -q install --upgrade agentlightning "openai>=1.100.0" uv
````

```python
!pip -q install -U poml openai
```

### リポジトリを取得

```python
!git clone --depth=1 https://github.com/microsoft/agent-lightning.git
%cd agent-lightning/examples/apo
```

### OpenAI APIキーを設定

```python
import os
from google.colab import userdata


os.environ["OPENAI_API_KEY"] = userdata.get('OPENAI_API_KEY')
```

### サンプルを実行（Room Selector / APO）

```python
!python room_selector_apo.py
```

## 実行すると何が起きる？（APOの概略）

`room_selector_apo.py` を実行すると、単にエージェントが動くだけでなく、その裏で**プロンプトを自動的に改善する**ための学習サイクルが回り始めます。この中核技術が **APO（Automatic Prompt Optimization）** です。

一言で言えば、「**エージェントの失敗から学び、より賢い指示文（プロンプト）をAI自身が考える**」仕組みです。

### APOの学習サイクル：失敗から学ぶ3ステップ

APOは、以下の3つのステップを自動で繰り返すことで、エージェントの性能を向上させます。

#### ステップ1：実行 → 評価 (Execution → Evaluation)

まず、エージェントは現在のプロンプト（指示文）を使って、与えられたタスク（「〇〇な会議室を探して」）を実行します。その後、**Judge（評価者）** と呼ばれる別のAIが、その結果を「正解」と比較し、厳密にスコアリングします。

**成功例（スコア: 1.0）**

ユーザーの要求に完璧に応えられたケースです。

**ユーザーからの指示 (User Message)**

```
Find a room on 2025-10-13 at 12:30 for 60 minutes, 10 attendees. Needs: ['projector', 'whiteboard']. Accessible required: True.
```

**[日本語訳]**
2025年10月13日 12:30から60分間、10名で利用できる部屋を探してください。必須要件: プロジェクター、ホワイトボード。アクセシビリティ対応: 必要。

**エージェントの回答 (Final Assistant Message)**

```
However, since you need 10 attendees, the suitable options are:
- Lyra (capacity 10)
- Nova (capacity 12)
```

**[日本語訳]**
10名の参加者が必要とのことですので、最適な選択肢は以下の通りです。

* Lyra（定員10名）
* Nova（定員12名）

エージェントは人数、設備、利用可能性の全てを満たす候補を正しく提示しました。そのため、Judgeは満点の評価を与えます。

**Judgeの評価 (Judge / Judge Score)**

```json
{
 "reason": "Chosen room matches capacity requirement exactly.",
 "score": 1
}
```

**[日本語訳]**

```json
{
 "理由": "選択された部屋が定員の要件に正確に一致しています。",
 "スコア": 1
}
```

**スコア: 1.0**

---

**失敗例（スコア: 0.0）**

エージェントが要求を見落とし、間違った回答をしたケースです。

**ユーザーからの指示 (User Message)**

```
Find a room on 2025-10-13 at 09:15 for 30 minutes, 6 attendees. Needs: ['projector', 'whiteboard']. Accessible required: True.
```

**[日本語訳]**
2025年10月13日 09:15から30分間、6名で利用できる部屋を探してください。必須要件: プロジェクター、ホワイトボード。アクセシビリティ対応: 必要。

**エージェントの回答 (Final Assistant Message)**

```
Rooms that meet all your criteria are Nova and Pulse.
```

**[日本語訳]**
あなたの基準をすべて満たす部屋はNovaとPulseです。

この提案は誤りです。`Nova` には `ledwall` はあっても `projector` はありません。Judgeはこの致命的な見落としを検出し、スコア0.0（完全な失敗）と評価します。

**Judgeの評価 (Judge / Judge Score)**

```json
{
 "reason": "Suggested Nova has ledwall, not projector as required.",
 "score": 0
}
```

**[日本語訳]**

```json
{
 "理由": "提案されたNovaには要求されたプロジェクターではなく、ledwallが備わっています。",
 "スコア": 0
}
```

**スコア: 0.0**

#### ステップ2：批評 → 書き換え (Critique → Rewrite)

スコアが低かった実行ログ（特に失敗例）は、プロンプトを改善するための**貴重な学習データ**になります。

APOアルゴリズムは、失敗ログ（ユーザー指示、エージェントの誤答、Judgeの評価理由）をまとめて分析AIに渡し、「**なぜこのエージェントは失敗したのか？**」という**批評（Critique）**を生成させます。

例えば、「エージェントは必須の設備要件を無視している」といった批評が生まれます。

次に、その批評に基づき、「次こそは成功するように」と、元のプロンプトを**複数のパターンで書き換え**、改善案を生成します。例えば、以下のような指示がプロンプトに追記されるかもしれません。

* 「ユーザーが要求した設備は、**絶対に**含まれている必要があります。」
* 「提案する前に、各部屋の設備リストをもう一度確認してください。」

#### ステップ3：改善案プロンプトで再評価 (Re-evaluation)

新しく作られたプロンプト候補たちが本当に優れているかを検証します。

各候補プロンプトをエージェントに渡し、再度タスクを実行させてJudgeがスコアリングします。この試行（ロールアウト）を複数回行い、**最も平均スコアが高かったプロンプト**を探し出します。

### ログの見どころ：学習の成果を確認する

この一連のサイクルが回っている証拠は、実行ログの最後に集約されています。

* **候補プロンプトのスコア推移**
  ログの `Evaluated ... rollouts.` の行に、あるプロンプト候補（例：`Prompt v6`）を試した結果の平均スコアが表示されます。ここを見れば、プロンプトの性能が数値で分かります。

  ```
  [Round 02 | Prompt v6] Evaluated 29 rollouts. ... Rewards: [1.0, 1.0, 1.0, 0.0, ...], average is 0.603
  ```

  **[日本語訳]**

  ```
  [ラウンド02 | プロンプトv6] 29回の試行を評価しました。... 報酬: [1.0, 1.0, 1.0, 0.0, ...], 平均スコアは0.603です
  ```

* **最終的に選ばれたベストプロンプト**
  `Best prompt not updated.` や `New best prompt saved!` といったメッセージで、改善案が採用されたかどうかが分かります。以下のログは、「新しいプロンプト（スコア0.603）は、過去最高（0.631）を超えなかったので、採用を見送った」という賢明な判断が下されたことを示しています。

  ```
  [WARNING] ... [Round 02 | Prompt v6] Best prompt not updated. Current score: 0.603 vs. history best: 0.631)
  ```

  **[日本語訳]**

  ```
  [警告] ... [ラウンド02 | プロンプトv6] 最良プロンプトは更新されませんでした。現在のスコア: 0.603に対し、過去の最高スコア: 0.631)
  ```

このように、Agent Lightningは「実行・評価・改善」のループを自動で回し続けることで、人間が手作業で調整するよりも効率的に、エージェントを賢く育てていくのです。

## よくあるつまずき

* **APIキー**：`OPENAI_API_KEY` が空/権限不足だと失敗
* **openai のバージョン**：`openai>=1.100.0` を推奨（内部アダプタの要件）
* **モデル名**：利用可能なモデルに差し替え
* **Colab無料枠**：並列度や探索幅を詰めすぎると時間切れになりやすい

## コストと時間を抑えるコツ

* **探索幅を小さく**：ビーム幅/分岐数/ラウンド数を控えめに
* **検証バッチを縮小**：`val_batch_size` を下げる
* **小さなデータセット**から始める
* **軽量モデル**で当たりを付け、良さそうなら強いモデルで仕上げ

> `room_selector_apo.py` をベースに、露出しているパラメータを小さめに設定すると効果的です。

## 背景の仕組み（軽く理解）

* **Tracer**：プロンプト・ツール呼び出し・報酬などのイベントを収集
* **Store**：タスク/リソース/トレースを一元管理
* **Algorithm**（APO/RL/SFT）：データを読み、**プロンプト/ポリシー**を改良
* **Trainer**：学習を回し、改善を推論側へ反映
  → 既存エージェントへの変更は最小限で、**回すほど良くなる**ループを構築できます。

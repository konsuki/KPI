---

## 📁 ファイル名

このドキュメントは以下の名前で保存してください：

```
initial_chart_data_explained.md
```

---

## 🔰 はじめに

`initial_chart_data` は、**組織図（Org Chart）に表示する情報**を表現するためのリスト（配列）です。

* 各要素は「1つのノード（＝チームや役職など）」の情報を表しています。
* このデータを使って、**Google Charts の OrgChart** をHTML上に描画できます。

---

## 🔎 ざっくり構造

```python
initial_chart_data = [
    { ... },  # ノード1
    { ... },  # ノード2
    { ... },  # ノード3
    ...
]
```

各 `{ ... }` の中に、\*\*そのノードが持つ情報（ID、名前、親ノード、目標など）\*\*が入っています。

---

## 🧩 各ノードのデータ構造（1件分の例）

```python
{
    "id": "team_a",
    "parent": "ceo",
    "cssClass": "team-a-content",
    "title": "Aチーム",
    "rinen": "予算達成はマスト...",
    "mokuhyo": "年間粗利1~3億円",
    "kpi": "年間粗利1~3億円",
    "tasseiRitsu": 25,
    "tooltip": ""
}
```

| 項目名           | 型   | 説明                             |
| ------------- | --- | ------------------------------ |
| `id`          | 文字列 | ノードの一意なID（他と被らない名前）            |
| `parent`      | 文字列 | 上の階層のノードのID（""ならトップ）           |
| `cssClass`    | 文字列 | HTML/CSSの見た目に使うクラス名            |
| `title`       | 文字列 | ノードに表示されるタイトル（チーム名など）          |
| `rinen`       | 文字列 | 理念・ビジョンの文章                     |
| `mokuhyo`     | 文字列 | 目標（数値など）                       |
| `kpi`         | 文字列 | KPI（Key Performance Indicator） |
| `tasseiRitsu` | 数値  | 達成率（プログレスバーに表示）                |
| `tooltip`     | 文字列 | ツールチップの内容（マウスホバー時の補足）          |

---

## 🏗️ ノードの関係性（親子関係）

```
[代表（ceo）]
 ├── Aチーム（team_a）
 │    ├── YouTube広告（yt_ads）
 │    ├── Instagram（insta）
 │    └── 広告（ad）
 ├── マーケチーム（team_b）
 │    └── TikTok（tiktok）
 ├── セールスチーム（team_c）
 │    └── 広告運用チーム（ad_ops）
 ├── ECチーム（team_d）
 │    ├── Amazon（amazon_ec）
 │    ├── Yahoo!（yahoo_ec）
 │    └── eBay（ebay_ec）
 └── ライターチーム（team_e）
      ├── Amazon（amazon_writer）
      ├── アップル（apple_writer）
      └── eBay（ebay_writer）
```

* `parent` が `ceo` なら「代表の部下」
* `parent` が `team_a` なら「Aチームの子チーム」

---

## 🎨 cssClass の使い方

* 見た目を変えるための**スタイル用クラス名**です。
* HTML内の `.node-content.XYZ` として定義されていて、チームごとに色を変えられます。

例：

```css
.node-content.team-a-content {
  border-color: #4CAF50; /* 緑色の枠 */
}
```

---

## 📊 tasseiRitsu（達成率）

* 0〜100の数値。
* HTML側で**プログレスバーの長さに反映**されます。

例：

```html
<div class="progress-bar" style="width: 25%;"></div>
```

---

## 🧠 補足：Flask × Google Chartの連携ポイント

* `initial_chart_data` は Python 側で定義
* HTMLでは `{{ chart_data | tojson | safe }}` によってJavaScript側に渡される
* JS側では `drawChartWithData()` 関数内で HTML化 → 表示される

---

## ✅ まとめ

* `initial_chart_data` は、**組織図の各ノードの情報を定義したリスト**
* 各要素は、`id`, `parent`, `title`, `rinen`, `mokuhyo`, `kpi`, `tasseiRitsu`, `tooltip`, `cssClass` などの情報を持つ
* Flask → Jinja2 → JS → Google Charts で連携して表示される

---

## 📎 おすすめ活用法

* **データの更新**： `/update` にPOSTすればリアルタイムで書き換え可能
* **DB連携**：このデータをDBに保存しておけば、管理画面なども作成可能
* **デザイン変更**：CSSの `.node-content` を調整することでカスタマイズ自在

---

## まとめ


obsidinian



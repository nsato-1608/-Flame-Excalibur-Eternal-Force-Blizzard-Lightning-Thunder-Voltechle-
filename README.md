*This project has been created as part of the 42 curriculum by nsato, tenomoto*.

## 📖*Content*

1. [💡Description](README.md#💡Description)
2. [✅Instructions](README.md#✅Instructions)
3. [⛏Technologies](README.md#⛏*Technologies)
5. [🌈Resources](#🌈Resources)

## 💡Description

## ✅Instructions
1. 仮想環境の構築  
`python3 -m venv .venv`
2. 仮想環境のアクティベート  
`source .venv/bin/activate`
3. パッケージのインストール  
`make install`
4. プログラムの実行  
`make run`
5. デバッグ  
`make debug`
6. ランプチェック  
`make lint`
7. ランプチェック（厳格）  
`make lint-strict`
8. ビルド  
`make build`

## ⛏Additional sections

### 1. 設定ファイルの完全な構造とフォーマット
|Key|Description|
|---|---|
|WIDTH|迷路の幅（セル数）|
|HEIGHT|迷路の高さ（セル数）|
|ENTRY|入口の座標（x, y）|
|EXIT|出口の座標（x, y）|
|OUTPUT_FILE|出力ファイル名|
|PERFECT|完全迷路にするか|
|SEED|迷路の生成を固定|
|PATTERN|迷路の真ん中に42スタンプを生成(9×7以上の時のみ)|

### 2. 選択した迷路生成アルゴリズム
迷路生成  
>棒倒し法(バイナリツリー法)  

最短経路探索  
>幅優先探索

### 3. このアルゴリズムを選択した理由
迷路生成  ->  生成方法が直感的に理解しやすく、配列を使った迷路生成と相性が良かったため
最短経路探索  ->  

### 4. コードのどの部分が再利用可能か、およびその方法
./mazegen/generator.pyのMazeGeneratorクラス
### 5. チーム構成とプロジェクト管理：
#### 各チームメンバーの役割
<details open>
	<summary>nsato</summary>
	configファイルからのパース
	README.md雛形作成。
</details>

<details open>
	<summary>tenomoto</summary>
	
</details>

+ 当初の計画と最終段階までの変更経緯  
目標スケジュール
	+ 2月24日(火) チーム結成。スケジュール整理。
	+ 2月25日(水) スタート。迷路生成アルゴリズムの決定。
	+ 2月26日(木) 迷路生成、ターミナルに出力する。
	+ 2月27日(金) ターミナルに出力する。
	+ 2月28日(土) 迷路調整、完全迷路化、Perfectフラグ対応。
	+ 3月1日(日)
	+ 3月2日(月) README.md, Makefile作成
	+ 3月3日(火) 最終チェック。提出。
	+ 3月4日(水) 提出バッファ。

完遂スケジュール  
最終提出  ->  3月6日(金)

#### 成功した点と改善点

#### 特定ツールの使用有無（使用した場合はその名称）
+ Discord
+ Notion
+ [Git hub](https://github.com/nsato-1608/-Flame-Excalibur-Eternal-Force-Blizzard-Lightning-Thunder-Voltechle-/tree/main)

### 6. 高度な機能（複数アルゴリズム、表示オプションなど）実装について
今回は未実装

## 🌈Resources
[Python Documentation contents](https://docs.python.org/3/library/index.html)  
[迷路生成・棒倒し法](https://algoful.com/Archive/Algorithm/MazeBar)  
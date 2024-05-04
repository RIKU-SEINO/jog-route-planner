# Share Jog
## WEBアプリの概要
### アクセス先
https://share-jog.onrender.com/home/
こちらから開発中のWEBアプリにアクセスすることができます。
（無料プランを使っているので起動にやや時間がかかる可能性があります。）

### 素敵なランニングコースに出会おう
このWEBアプリは、自分のお気に入りのジョギングコースを管理したり、投稿することができるSNSサービスです。
自分のとっておきのジョギングコースを広く知ってもらうことができるだけでなく、自分の知らないジョギングコースに出会うことができるかもしれません。

全国のランナーが投稿したジョギングコースをエリアや走行距離などの条件で絞り込み、あなたにピッタリのジョギングコースを検索することができます。（開発途中です）

また、オリジナルのジョギングコースを作成することもできます。スタート地点とゴール地点、走行距離を指定することで、あなたにおすすめのジョギングコースを自動的に作成してくれます。

## 外観
### ホーム画面
<img width="1435" alt="スクリーンショット 2024-04-14 19 49 35" src="https://github.com/RIKU-SEINO/share-jog/assets/102781001/03295274-5ed5-4683-aa02-eb7bdf93fbf4">

### ユーザー新規登録画面
<img width="1436" alt="スクリーンショット 2024-04-14 19 54 20" src="https://github.com/RIKU-SEINO/share-jog/assets/102781001/456abd9e-6bdb-4095-938e-fd813fd478bf">

### ジョギングコース検索画面
<img width="1438" alt="スクリーンショット 2024-04-14 19 50 15" src="https://github.com/RIKU-SEINO/share-jog/assets/102781001/d459d971-9e58-47f8-87ed-a4bb781328e0">

### マイページ画面
<img width="1253" alt="スクリーンショット 2024-05-03 20 04 35" src="https://github.com/RIKU-SEINO/share-jog/assets/102781001/796e8dbc-8f3e-4bb2-8b60-459cfc7c4cc0">

## 使用技術
- Python 3.9.6
    - Flask
- HTML
- CSS
- JavaScript
    - Leaflet.js
    - Chart.js
- SQLite 3.39.5
- AWS (今後こちらにデプロイする予定ですが、現在はRender.comを使っています。)
- OpenStreetMap API

## 機能一覧
### 実装済みの機能
- ユーザー新規登録
    - ユーザー名
    - メールアドレス
    - パスワード
    - アイコン画像
- ログイン
    - メールアドレス
    - パスワード
- ログアウト
- ジョギングコース自動作成機能
    - スタート地点とゴール地点の指定
        - マップ上のクリックした位置にピンを立てる
        - フリーワードで検索した位置にピンを立てる
    - コースの自動作成

### これから実装予定の機能
- ユーザープロフィール設定
- コースをお気に入りに追加する機能
- ジョギングコース検索機能
    - フリーワード検索
    - 特定の条件による検索
        - エリア
        - 走行距離
- フォロー機能
- エラーハンドリング
# Share Jog

## アクセスはこちらから
https://share-jog.onrender.com/

## WEBアプリケーションの概要
こちらは、ランニングやジョギングを趣味とする方向けに、ランニングコースの検索と作成を支援するSNS形式のWEBアプリケーションです。

ランニングを趣味とする方にとって課題となるのが、「どこを走るか？」だと思います。

GoogleMapのような通常の経路案内サービスは、移動に最適なルートを提案するだけで、走行距離などを指定したジョギングルートを作成することはできません。

そこで、ランニングコースを自動的に作成することで、ユーザーがランニングコース作成にかける時間を削減するソフトウェアがあれば良いなと思い、「Share-Jog」の開発に至りました。

また、他のユーザーが走ったコースを検索・ブックマークすることもできるため、自分が今まで知らなかった素敵なランニングコースに出会うことができるかもしれません。

## ローカルで使いたい方向け
1. Pythonの環境構築
- Windows: https://prog-8.com/docs/python-env-win
- macOS: https://prog-8.com/docs/python-env

2. お使いの環境にクローンし、作業ディレクトリに移動
```
git clone https://github.com/RIKU-SEINO/share-jog
cd share-jog
```

3. 仮想環境の構築
https://qiita.com/shun_sakamoto/items/7944d0ac4d30edf91fde

3. 必要なライブラリをインストール
```
pip install -r requirements.txt
```
4. データベースの作成
```
python -m flask db init
python -m flask db migrate
python -m flask db upgrade
```
5. 初期データの投入
```
chmod +x import_data.sh
./import_data.sh
```
6. ローカルホストでアプリケーションを実行
```
python -m flask run
```

## 使用技術
- バックエンド
    - Python 3.9.6
- フレームワーク
    - Flask
- フロントエンド
    - HTML
    - CSS
    - JavaScript
        - jQuery
- データベース
    - SQLite 3
- インフラ
    - Render.com
- 外部サービス
    - OpenStreetMap API
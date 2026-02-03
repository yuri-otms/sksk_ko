# 韓国語学習アプリ「サクッと作文　韓国語」
![toppage](https://github.com/yuri-otms/sksks_ko/assets/75471760/657f1e02-6572-40a9-946e-ed5c192c2bfe)
URL
https://ko.skskfun.com
(2025/11/30 ko.sksk.funよりドメイン変更)

## アプリの概要
簡単な日本語を韓国語作文することで韓国語を学習するアプリケーションです。
![sksk_ko_問題を解く](https://github.com/yuri-otms/sksks_ko/assets/75471760/565cabcf-54ab-4b0a-a2fd-724bb5598439)


## 使用技術
- [Python](https://www.python.org/) 3.9.16
- [Flask](https://flask.palletsprojects.com/en/2.3.x/) 2.2.3
- [MySQL](https://www.mysql.com/) 8.0
- HTML/CSS/JavaScript
- [jQuery](https://jquery.com/) 3.7.8
- [Bootstrap](https://getbootstrap.com/) 5.2.3
- [Docker](https://www.docker.com/) 23.0.3/[Docker Compose](https://docs.docker.com/compose/) 1.29.2
- [Gunicorn](https://gunicorn.org/) 20.1.0
- [nginx](https://www.nginx.com/) 1.23
- [さくらのVPS](https://vps.sakura.ad.jp/)

## 機能一覧

### 問題出題機能
- 文法項目の選択
- 単語のヒント表示
- 音声再生

### 認証機能
- ユーザー登録
- ログイン・ログアウト
- アカウント情報の変更
- パスワード再設定
- アカウント削除

### 問題編集機能
- 問題の属性（級・グループ・項目）編集
- 問題作成・編集・削除
- ヒント（単語）の作成・編集・削除

### 管理機能
- ユーザー編集（名前編集・パスワード再設定・削除）
- ユーザーへの権限（問題編集・確認依頼・公開設定・管理）付与・削除
- 編集履歴の表示

## インフラ構成図
<img width="1385" height="749" alt="sksk_ko_インフラ構成図" src="https://github.com/user-attachments/assets/a55d6919-6f0e-42c2-bd3b-0a0e6dd5f4e2" />

## ER図
![sksk_ko_er](https://github.com/yuri-otms/sksks_ko/assets/75471760/6727546a-6898-4436-a013-6e7fb4222c4a)



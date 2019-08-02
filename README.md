## Johnny's_classifier概要
   顔写真からジャニーズ系かどうか判定するアプリケーションです。

### 使い方


### 機能
- 学習用の画像をスクレイピングで収集
- 顔写真のアップロード
- アップロード写真を分類
   - モデルはSVMを仕様しています。(CNNなど他のモデルも比較検討しました。)
   - ジャニーズタレントを１０人選抜し、顔写真を機会学習に使用しました。
- 結果はHTMLで出力

### 残課題
- エラー処理(アップロードされた画像に顔が含まれているかなど)
- サーバーに上げる

###参考
「AIを使って自分の顔がジャニーズ系かどうかを判定するWebサービスを作ってみた」
https://qiita.com/gold-kou/items/e1a96657a63b043c4564
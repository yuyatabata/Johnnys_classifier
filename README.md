## Johnny's_classifier概要
   顔写真からジャニーズ系かどうか判定するアプリケーションです。

### 使い方

1. 「ファイルを選択」ボタンを押す

![スクリーンショット 2019-08-02 15 31 25](https://user-images.githubusercontent.com/27131456/62350628-3f882e80-b53e-11e9-945f-f400ebd620b2.png)


2. 手元の顔写真を選択

![スクリーンショット 2019-08-02 15 32 17](https://user-images.githubusercontent.com/27131456/62350667-5fb7ed80-b53e-11e9-947e-e4b636d14246.png)

3. ジャニーズ係数と共に判別結果が表示
![スクリーンショット 2019-08-02 15 32 41](https://user-images.githubusercontent.com/27131456/62350687-752d1780-b53e-11e9-8644-cfb20f3398ac.png)

4. ジャニーズ系ではなかったパターン 
![スクリーンショット 2019-08-02 15 33 03](https://user-images.githubusercontent.com/27131456/62350702-81b17000-b53e-11e9-908d-990f30c4fb8b.png)


### 機能
- 学習用の画像をスクレイピングで収集
- 顔写真のアップロード
- アップロード写真を分類
   - モデルはSVMを仕様しています。(CNNなど他のモデルも比較検討しました。)
   - ジャニーズタレントを１０人選抜し、顔写真を機会学習に使用しました。
- 結果はHTMLで出力


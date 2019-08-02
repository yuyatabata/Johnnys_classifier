import argparse
import json
import os
import urllib

from bs4 import BeautifulSoup
import requests #HTTPリクエスト用

class Google:
    def __init__(self):
        self.GOOGLE_SERCH_URL = "https://www.google.co.jp/search"
        self.session = requests.session() #HTTPリクエスト/レスポンスで、Cookieやカスタムヘッダーなどを使い回す
        self.session.headers.update(
            {
                "User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:10.0) \
                    Gecko/20100101 Firefox/10.0"
            }
        )#ヘッダの設定

    #スクレイピングの検索行動まとめ
    def search(self, keyword, maximum):
        print(f"Begining search {keyword}")
        query = self.query_gen(keyword) #クエリ検索
        return self.image_search(query, maximum) #画像検索

    #検索クエリを付与したURLを生成
    def query_gen(self, keyword):
        page = 0
        while True:
            params = urllib.parse.urlencode(
                {"q": keyword, "tbm": "isch", "ijn":str(page)}
            )#Webサーバに送信するデータクエリ文字列パラメータの作成。tbmは検索の種類(ischで画像)。ijnはページ数のパラメータ

            yield self.GOOGLE_SERCH_URL + "?" + params #yieldで処理を止めずにurl＋パラメータを返す。
            page +=1

    #画像検索(クエリurlと画像取得枚数を指定)
    def image_search(self,query_gen,maximum):
        results = []
        total = 0
        while True:
            #検索
            html = self.session.get(next(query_gen)).text #GETリクエスト。.textでレスポンスボディをテキスト形式で取得
            soup = BeautifulSoup(html, "lxml") #BeautifulSoupを作成。HTMLファイルからデータを取得
            elements = soup.select(".rg_meta.notranslate") #CSSセレクタでタグ取得.rg_meta.notranslate
            jsons = [json.loads(e.get_text()) for e in elements] #elementのテキストのみを取得し、json→辞書形式に変換
            image_url_list = [js["ou"] for js in jsons] #画像のURLを取得

            #検索結果の追加
            if not len(image_url_list):
                print("-> No more image")
                break
            elif len(image_url_list) > maximum - total: #
                results += image_url_list[: maximum - total]
                break
            else:
                results += image_url_list
                total += len(image_url_list) #追加枚数

        print("-> Found", str(len(results)), "image")
        return results

    #実行
def main():
    parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS) #パーサを作る。main関数の引数(実行時にターミナルで与える)の解析
    parser.add_argument("-t", "--target", help="target name", type=str, required=True) #引数を追加。属性として使える。-で位置で決まらない引数を指定。
    parser.add_argument("-n", "--number", help="number of images", type=int, required=True) #helpで引数の説明。required=Trueで引数必須
    parser.add_argument("-d", "--directoty", help="download location", type=str, default="./j_data") #出力先の指定。defaultでコマンド引数がなかった場合の値を指定
    parser.add_argument("-f","--force",help="download overwrite existing file",type = bool,default = False)

    args = parser.parse_args() #コマンド引数のおぶジェクト

    data_dir = args.directoty #データを入れるディレクトリ
    target_name = args.target #target=検索クエリ(keyword)

    #保存先のディレクトリ
    os.makedirs(data_dir, exist_ok=True)
    # os.makedirs(os.path.join(data_dir, target_name), exist_ok=args.force)

    google = Google()

    results = google.search(target_name, maximum=args.number)

    download_errors = []
    for i, url in enumerate(results):
        print("-> Downloading image", str(i + 1).zfill(4), end=" ")
        try:
            urllib.request.urlretrieve(
                url,
                os.path.join(*[data_dir,target_name+str(i + 1).zfill(4)+".jpg"]),
            )#ダウンロードファイルの保存
            print("successful")
        except BaseException:
            print("failed")
            download_errors.append(i+1)
            continue

    print("-" * 50)
    print("Complete downloaded")
    print("├─ Successful downloaded", len(results) - len(download_errors), "images")
    print("└─ Failed to downloaded", len(download_errors), "images", *download_errors)

if __name__ == "__main__":
    main()
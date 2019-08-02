import os
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename

from keras.models import Sequential, load_model
import keras,sys
import numpy as np
from PIL import Image

classes = ["face_j","face_d"]
num_classes = len(classes)
image_size = 50

UPLOAD_FOLDER = "./uploads"
ALLOWED_EXTENTIONS = set(["png", "jpg", "gif"])

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

#ファイル名からアップロードの可否を判定
def allowed_file(filename):
    return "." in filename and filename.rsplit(".",1)[1].lower() in ALLOWED_EXTENTIONS #.拡張子あるか、指定された拡張子か。

#fileを受け取る
@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        if "file" not in request.files:#リクエストの中にfileが無いとき
            flash("ファイルはありません")
            return redirect(request.url)
        file = request.files["file"]#fileがある時、リクエストから取り出す。
        if file.filename == "":#fileに名前がない時
            flash("ファイルはありません")
            return redirect(request.url)
        if file and allowed_file(file.filename):#allowed_file関数でOKなら
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"],filename)) #サニタイズ処理
            #fileの識別
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)#画像fileのパスを作成

            model = load_model("./j_cnn.h5")#学習済みモデルの読み込み

            image = Image.open(filepath)#アップロードファイルの展開と以下予測用の加工
            image = image.convert("RGB")
            image = image.resize((image_size,image_size)) #多分なくても大丈夫
            data = np.asarray(image)
            X = []
            X.append(data)
            X = np.array(X)

            result = model.predict([X])[0]
            predicted = result.argmax() #最大値が入っている添字を返す
            percentage = int(result[predicted]*100)

            return "ラベル：" + classes[predicted] + ",確率：" + str(percentage) + "%"

    return '''
    <!doctype html>
    <html>
    <head>
    <meta charset="UTF-8">
    <title>写真をアップロードしてジャニーズ判定しよう</title> </head>
    <body>
    <h1>写真をアップロードしてジャニーズ判定しよう</h1>
    <form method = post enctype = multipart/form-data>
    <p><input type=file name=file>
    <input type=submit value=Upload>
    </form>
    </body>
    </html>
    '''
from flask import send_from_directory#ディレクトリ内の静的ファイルにアクセス
@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"],filename)#画像ファイル
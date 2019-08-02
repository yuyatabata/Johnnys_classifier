import os
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename
# from sklearn.externals import joblib
import numpy as np
from PIL import Image
import pickle
import joblib

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
            image = Image.open(filepath)#アップロードファイルの展開と以下予測用の加工
            print("image:",image)
            # print("shape:",image.shape)
            image = image.convert("RGB")
            print("imageRGB:",image)
            # print("shapeRGB:",image.shape)
            image = image.resize((image_size,image_size)) #多分なくても大丈夫
            print("resize:",image)
            # print("shaperesize:",image.shape)
            data = np.asarray(image)
            print("data:",data)
            print("shapedata:",data.shape)
            data = data.reshape(-1)
            print("data_reshape:",data)
            print("shape:",data.shape)
            X = []
            X.append(data)
            print("X:",X)
            # print("X.shape:",X.shape)
            X = np.array(X)
            print("X_array:",X)
            # print("X_array.shape:",X.shape)
            print("[X]_array:",[X])
            # print("X_array.shape:",[X].shape)
            print("[X][0]_array:",[X][0])
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

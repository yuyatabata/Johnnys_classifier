import os
from flask import Flask, request, redirect, url_for,render_template
from werkzeug.utils import secure_filename
from keras.models import Sequential, load_model
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
            image = image.convert("RGB")
            image = image.resize((image_size,image_size)) #多分なくても大丈夫
            data = np.asarray(image)

            #svm学習済みモデルの読み込みjoblib
            model = joblib.load("./j_svm.h5")
            #ベクトル化(SVM用)
            data = data/255
            data = data.reshape(-1)#多次元配列を一次元配列に変更
            data = data / np.linalg.norm(data, ord=2, keepdims=True)

            X = []
            X.append(data)
            X = np.array(X)

            result = model.predict([X][0])
            score = model.decision_function(X).ravel()#Xベクトルと識別境界の距離
            if score >0:
                predicted=1
            else:
                predicted=0
            return render_template("result.html", file=file.filename, predicted=predicted,score=score)

    return render_template("index.html")

from flask import send_from_directory#ディレクトリ内の静的ファイルにアクセス
@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"],filename)#画像ファイル
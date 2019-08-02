from PIL import Image
import os, glob
import numpy as np
from sklearn import model_selection

classes = ["face_j","face_d"]
num_classes = len(classes)
image_size = 50
num_testdata = 100

#読み込み画像のnumpy配列に変更用
X_train = []
X_test = []
Y_train = []
Y_test = []

#クラスを兼ねたディレクトリから画像を取り出す。
for index, classlabel in enumerate(classes):
    photos_dir = "./face_all/" + classlabel #画像のディレクトリ
    files = glob.glob(photos_dir + "/*.jpg") #画像データの取得
    for i, file in enumerate(files):
        if i > 300:
            break
        image = Image.open(file)
        image = image.convert("RGB")#3色の２５６階調の数字に変換
        image = image.resize((image_size,image_size)) #多分なくても大丈夫
        data = np.asarray(image)#イメージデータを数字の配列に変換

        #100枚をテストデータに残す
        if i < num_testdata:
            X_test.append(data)
            Y_test.append(index)
        else:
            for angle in range(-20,20,5):
                #回転
                img_r = image.rotate(angle)#PILのimageモジュールで回転
                data = np.asarray(img_r)
                X_train.append(data)
                Y_train.append(index)

                #反転
                img_trans = img_r.transpose(Image.FLIP_LEFT_RIGHT)#PILのimageモジュールで反転
                data = np.asarray(img_trans)
                X_train.append(data)
                Y_train.append(index)
X_train = np.array(X_train)
X_test = np.array(X_test)
y_train = np.array(Y_train)
y_test = np.array(Y_test)

xy = (X_train, X_test, y_train, y_test)
np.save("./j_aug2.npy", xy)
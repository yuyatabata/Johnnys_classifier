from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras.layers import np_utils
import keras
import numpy as np

classes = ["face_j","face_d"]
num_classes = len(classes)
image_size = 50

#実行用メインの関数を定義
def main():
    X_train, X_test, y_train, y_test = np.load("./j_aug2.npy", allow_pickle=True)#gen_data.pyで作ったファイルからデータを配列に読み込む
    X_train = X_train.astype("float")/256#データの正規化：最大値で割って0~1に
    X_test = X_test.astype("float")/256
    y_train = np_utils.to_categorical(y_train, num_classes)#正解値を1にするone-hotはto_categorical(ラベル,クラス数)
    y_test = np_utils.to_categorical(y_test,num_classes)

    #長くなるから学習と評価は別関数に分けて呼び出す
    model = model_train(X_train, y_train)
    model_eval(model, X_test, y_test)

#モデル関数。畳み込みNN
def model_train(X,y):
    model = Sequential()
    model.add(Conv2D(32,(3,3), padding="same",input_shape=X.shape[1:]))#１層目は畳み込み層。32個のフィルタでフィルタのサイズは3×3。

    model.add(Activation("relu"))#活性化
    model.add(Conv2D(32,(3,3)))
    model.add(Activation("relu"))
    model.add(MaxPooling2D(pool_size=(2,2)))#プーリング層でもとの画像を縮小。次元削減
    model.add(Dropout(0.25))#入力時に25%捨てて過学習を防ぐ

    model.add(Conv2D(64,(3,3),padding="same"))
    model.add(Activation("relu"))
    model.add(Conv2D(64,(3,3)))
    model.add(Activation("relu"))
    model.add(MaxPooling2D(pool_size=(2,2)))
    model.add(Dropout(0.25))

    model.add(Flatten())
    model.add(Dense(512))
    model.add(Activation("relu"))
    model.add(Dropout(0.5))
    model.add(Dense(2)) #最終出力。目的は２クラス分類
    model.add(Activation("softmax"))

    opt = keras.optimizers.rmsprop(lr=0.0001,decay=1e-6)#学習率
    model.compile(loss="categorical_crossentropy",optimizer=opt,metrics=["accuracy"])#モデルの最適化手法を宣言

    model.fit(X,y,batch_size=32,epochs=100)#epochs=100だからcolabで学習。手元なら20

    model.save("./j_cnn.h5")

    return model

def model_eval(model, X,y):
    scores = model.evaluate(X,y, verbose=1)
    print("Test Loss: ", scores[0])
    print("Test Accuracy: ", scores[1])

if __name__ == "__main__":
    main()



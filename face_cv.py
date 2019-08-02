import cv2, os, sys

def detect_face(each_img_path, cascade_path, img, image_size):

    #ファイルの読み込み
    image_gs = cv2.imread(each_img_path)
    # print("image:",image_gs.shape)

    re_file_name = "cv_"+ img
    # print("Detect face: ", re_file_name)

    #カスケード分類器の特徴量を取得
    cascade = cv2.CascadeClassifier(cascade_path)
    # print("cascade:",cascade)
    facerect = cascade.detectMultiScale(image_gs, scaleFactor=1.1, minNeighbors=1, minSize=(1,1)) #顔検出。矩形のリストを返す。(画像CV_8U型の行列,画像縮小量,近傍矩形数の閾値,識別サイズの最小閾値)
    # print("facerect:",facerect)

    if len(facerect) > 0:
        for rect in facerect:
            dst = image_gs[rect[1]:rect[1]+rect[3],rect[0]:rect[0]+rect[2]] #矩形をimageに当てはめる
            dst = cv2.resize(dst, dsize=(image_size, image_size)) #画像のリサイズ。(入力画像,出力サイズ)
            cv2.imwrite("./face_all/face_d/" + re_file_name, dst) #切り抜き画像の保存。(保存先(※jとdで変えること),切り抜き画像)

def main():
    image_size=50

    cascade_path = "./haarcascade_frontalface_alt.xml"

    org_img_path = "./d_data/" #元画像 ※jとdで変えること
    imgs = []
    for i in os.listdir(org_img_path):
        imgs.append(i)
    if len(imgs) == 0:
        print("not exist original image directory")
        sys.exit()
    # print("imgs:",imgs)

    for img in imgs:
        each_img_path = org_img_path + img
        # print("img:",img)
        # print("each_img_path:",each_img_path)
        #画像のループ処理
        detect_face(each_img_path, cascade_path, img, image_size)

    print("Finish detect face")

if __name__ == "__main__":
    main()
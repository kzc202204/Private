import cv2 as cv
import numpy as np
import os
import sys
import glob

# Define
COSINE_THRESHOLD = 0.363
NORML2_THRESHOLD = 1.128

#参考
#https://qiita.com/UnaNancyOwen/items/f3db189760037ec680f3
path = 'C:/Users/KZC202204-102/Desktop/Natsuki/python/OpenCV/'
directory = 'C:/Users/KZC202204-102/Desktop/Natsuki/python/OpenCV/data/'

# 特徴を辞書と比較してマッチしたユーザーとスコアを返す関数
def match(recognizer, feature1, dictionary):
    for element in dictionary:
        user_id, feature2 = element
        score = recognizer.match(feature1, feature2, cv.FaceRecognizerSF_FR_COSINE)
        if score > COSINE_THRESHOLD:
            return True, (user_id, score)
    return False, ("", 0.0)


# FaceDetectorYNの生成
face_detector = cv.FaceDetectorYN_create( path + "face_detection_yunet_2023mar.onnx", "", (320, 320), 0.6, 0.3, 5000, cv.dnn.DNN_BACKEND_DEFAULT, target_id=cv.dnn.DNN_TARGET_CPU)
#face_detector = cv.FaceDetectorYN.create( path + "face_detection_yunet_2023mar.onnx", "", (0, 0))
# FaceRecognizer
weights = os.path.join(path, "face_recognizer_fast.onnx")
face_recognizer = cv.FaceRecognizerSF_create(weights, "")


#カメラの準備
cap = cv.VideoCapture(0, cv.CAP_MSMF)

# 特徴を読み込む
dictionary = []
files = glob.glob(os.path.join(directory, "*.npy"))
for file in files:
    feature = np.load(file)
    user_id = os.path.splitext(os.path.basename(file))[0]
    dictionary.append((user_id, feature))

while(True):
    # ビデオキャプチャ
    ret, image = cap.read()

    # 画像サイズを設定する
    height, width, _ = image.shape
    face_detector.setInputSize((width, height))
    
    # 顔検出
    _, faces = face_detector.detect(image)
    faces = faces if faces is not None else []

    # 検出した顔のバウンディングボックスとランドマークを描画する
    for face in faces:

        # 顔を切り抜き特徴を抽出する
        aligned_face = face_recognizer.alignCrop(image, face)
        feature = face_recognizer.feature(aligned_face)

        # 辞書とマッチングする
        result, user = match(face_recognizer, feature, dictionary)

        # 顔の表示
        box = list(map(int, face[:4]))
        color = (0, 0, 255)
        thickness = 1
        cv.rectangle(image, box, color, thickness, cv.LINE_AA)
        
        # 認識の結果を描画する
        id, score = user if result else ("unknown", 0.0)
        text = "{0} ({1:.2f})".format(id, score)
        position = (box[0], box[1] - 10)
        font = cv.FONT_HERSHEY_SIMPLEX
        scale = 0.6
        cv.putText(image, text, position, font, scale, color, thickness, cv.LINE_AA)
    
    # 表示
    cv.imshow('frame', image)
    # qが押されたら終了
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
    
# カメラ終了
cap.release()
# ウィンドウ終了
cv.destroyAllWindows()

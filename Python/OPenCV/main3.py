import cv2 as cv
import numpy as np

#参考
#https://qiita.com/UnaNancyOwen/items/f3db189760037ec680f3
path = 'C:/Users/KZC202204-102/Desktop/Natsuki/python/OpenCV/'

# FaceDetectorYNの生成
face_detector = cv.FaceDetectorYN_create( path + "face_detection_yunet_2023mar.onnx", "", (320, 320), 0.6, 0.3, 5000, cv.dnn.DNN_BACKEND_DEFAULT, target_id=cv.dnn.DNN_TARGET_CPU)
#face_detector = cv.FaceDetectorYN.create( path + "face_detection_yunet_2023mar.onnx", "", (0, 0))


#画像の読み込む
image = cv.imread( path + 'img_01.jpg')

# 画像サイズを設定する
height, width, _ = image.shape
face_detector.setInputSize((width, height))

# 顔検出
_, faces = face_detector.detect(image)
faces = faces if faces is not None else []

# 検出した顔のバウンディングボックスとランドマークを描画する
for face in faces:
    # 顔の表示
    box = list(map(int, face[:4]))
    color = (0, 0, 255)
    thickness = 2
    cv.rectangle(image, box, color, thickness, cv.LINE_AA)

    # ランドマーク（右目、左目、鼻、右口角、左口角）
    landmarks = list(map(int, face[4:len(face)-1]))
    landmarks = np.array_split(landmarks, len(landmarks) / 2)
    for landmark in landmarks:
        radius = 2
        thickness = -1
        cv.circle(image, landmark, radius, color, thickness, cv.LINE_AA)

    # 信頼度
    confidence = face[-1]
    confidence = "{:.2f}".format(confidence)
    position = (box[0], box[1] - 10)
    font = cv.FONT_HERSHEY_SIMPLEX
    scale = 0.5
    thickness = 2
    cv.putText(image, confidence, position, font, scale, color, thickness, cv.LINE_AA)

# 表示
cv.imshow("Image", image)

# キー入力待ち(ここで画像が表示される)
cv.waitKey()


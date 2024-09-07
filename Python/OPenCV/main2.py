import cv2
from matplotlib import pyplot as plt

path = 'C:/Users/KZC202204-102/Desktop/Natsuki/python/OpenCV/'

#画像を読み込む
image = cv2.imread( path + 'img_01.jpg')

#グレースケールに変換
image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#顔検出
cascade = cv2.CascadeClassifier( path + 'haarcascade_frontalface_default.xml')
#scaleFactor – 各画像スケールにおける縮小量を表します(caleFactor=1.1)
#minNeighbors – 物体候補となる矩形は，最低でもこの数だけの近傍矩形を含む必要があります
#minSize – 物体が取り得る最小サイズ．これよりも小さい物体は無視されます
boxes = cascade.detectMultiScale(image_gray, minNeighbors=3, minSize=(20, 20))

#表示用画像のコピー
image_output = image.copy()

for x, y, w, h in boxes:
    face = image[y: y + h, x: x + w]
    cv2.rectangle(image_output, (x, y), (x + w, y + h), (0, 0, 255), 2)

#表示
plt.imshow(cv2.cvtColor(image_output, cv2.COLOR_BGR2RGB))
plt.show()

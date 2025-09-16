from tensorflow.keras.models import load_model
import numpy as np
import cv2


def initializePredictionModel():
    model = load_model('./model.h5')
    return model


def getPredection(boxes, model):
    result = []
    for image in boxes:
        img = np.asarray(image)
        countW = 0
        for i in range (28):
            for j in range (28):
                if img[i][j] > 127:
                    countW = countW + 1
        # print(countW/784)
        if(countW/784) > 0.01:
            img = img.reshape(1, 28, 28, 1)
            prediction = model.predict(img)
            classIndex = np.argmax(prediction, axis=-1)
            probabilityValue = np.amax(prediction)
#             print(classIndex[0], probabilityValue)
            if probabilityValue > 0.8:
                result.append(classIndex[0])
            else:
                result.append(0)
        else:
            result.append(0)
#             print(0)
        image = cv2.resize(image, (112, 112))
#         cv2.imshow("test", image)
#         cv2.waitKey(0)
    return result

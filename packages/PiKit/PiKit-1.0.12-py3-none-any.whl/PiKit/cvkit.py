# -*- coding:utf-8 -*-

import cv2 


class VideoCapture:
    def __init__(self,device_id=0) -> None: 
        self.cap = cv2.VideoCapture(device_id)
    def read(self): 
        _,frame = self.cap.read()
        return frame
    def release(self) -> None: 
        self.cap.release()

class Draw:
    def __init__(self,image) :
        self.image = image

    def paint_arrow(self, x0, y0, x1, y1, color, thickness=1, line_type=8, shift=0, tiplength=0.1):
        # 获取图片的尺寸
        height, width = self.shape[:2]
        # 检查color参数是否为三元素元组，且每个元素都在0到255范围内
        assert isinstance(color, tuple) and len(color) == 3, "ERROR: Color must be a tuple of three integers"
        assert all(isinstance(c, int) and 0 <= c <= 255 for c in color), "ERROR: Each element in color must be an integer between 0 and 255"
        # 检查坐标是否在图片大小范围内
        assert 0 <= x0 < width and 0 <= y0 < height, "ERROR: Starting point out of bounds"
        assert 0 <= x1 < width and 0 <= y1 < height, "ERROR: Ending point out of bounds"

        cv2.arrowedLine(self, (x0, y0), (x1, y1), color, thickness, line_type, shift, tiplength)



class Image:
    def __init__(self) :
        self.data = None
    def capyure_from_camera(self,device_id=0):
        cap = cv2.VideoCapture(device_id)
        ret,frame = cap.read()
        if ret:
            self.data = frame
        else:
            print("Failed to capture image")
        cap.release()

    def show(self,winname ="image"):
        if self.data is not None:
            cv2.imshow(winname, self.data)


def face_detetion():
    
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=2, minSize=(100, 100))

        # 存储筛选后的人脸框
        filtered_faces = []

        for (x, y, w, h) in faces:
            # 计算当前人脸框的中心点坐标
            center_x = x + w // 2
            center_y = y + h // 2

            # 检查当前人脸框是否被其他人脸框包含
            is_inside = False
            for (fx, fy, fw, fh) in faces:
                # 计算其他人脸框的中心点坐标
                face_center_x = fx + fw // 2
                face_center_y = fy + fh // 2

                # 检查小框的中心点是否被大框框住，并且小框相对于大框来说较小
                if (fx < center_x < fx + fw) and (fy < center_y < fy + fh) and (w * h < fw * fh):
                    is_inside = True
                    break

            # 如果当前人脸框不被其他人脸框包含，则将其添加到筛选后的人脸框列表中
            if not is_inside:
                filtered_faces.append((x, y, w, h))

        for (x, y, w, h) in filtered_faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
    
        cv2.imshow('Face Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def wait(stop_key):
    if cv2.waitKey(1) & 0xFF == ord(stop_key):
        return 1
    else:
        return 0
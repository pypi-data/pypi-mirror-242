import PiKit

cap = PiKit.VideoCapture()

while True:
    frame = cap.read()
    PiKit.imshow('test',frame)
    if PiKit.wait('q')==1:
        break
    
cap.release()
# PiKit.face_detetion()
import PiKit.cvkit as cvkit

cap = cvkit.VideoCapture()

while True:
    frame = cap.read()
    cvkit.imshow('test',frame)
    if cvkit.wait('q')==1:
        break
    
cap.release()
# PiKit.face_detetion()

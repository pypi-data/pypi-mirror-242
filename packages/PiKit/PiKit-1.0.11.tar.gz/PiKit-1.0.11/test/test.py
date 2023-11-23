import PiKit.cvkit as cvkit
cap = cvkit.VideoCapture()

while True:
    frame = cap.read()
    cvkit.imshow('test',frame)
    cvkit.paint_arrow(frame,0,0,20,20)
    if cvkit.wait('q')==1:
        break
    
cap.release()
# PiKit.face_detetion()

import PiKit.cvkit as cvkit
cap = cvkit.VideoCapture()

while True:
    frame = cap.read()
    
    cvkit.paint_arrow(frame,0,0,20,20,(0,0,0))
    cvkit.imshow('test',frame)
    if cvkit.wait('q')==1:
        break
    
cap.release()
# PiKit.face_detetion()

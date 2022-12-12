import os
import torch
from matplotlib import pyplot as plt
import numpy as np
import cv2
import depthai as dai


model = torch.hub.load('./yolov7', 'custom', path_or_model='./weights/best.pt', source='local', force_reload=True)

# Create pipeline
pipeline = dai.Pipeline()

# Define sources and outputs
monoLeft = pipeline.create(dai.node.MonoCamera)
xoutLeft = pipeline.create(dai.node.XLinkOut)
xoutLeft.setStreamName('left')

# monoRight = pipeline.create(dai.node.MonoCamera)
# xoutRight = pipeline.create(dai.node.XLinkOut)
# xoutRight.setStreamName('right')

# Properties
monoLeft.setBoardSocket(dai.CameraBoardSocket.LEFT)
monoLeft.setResolution(dai.MonoCameraProperties.SensorResolution.THE_720_P)
# monoRight.setBoardSocket(dai.CameraBoardSocket.RIGHT)
# monoRight.setResolution(dai.MonoCameraProperties.SensorResolution.THE_720_P)

# Linking
monoLeft.out.link(xoutLeft.input)
# monoRight.out.link(xoutRight.input)

#To rescale the frame of the video capture
def rescale_frame(frame, percent=75):
    width = int(frame.shape[1] * percent/ 100)
    height = int(frame.shape[0] * percent/ 100)
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation =cv2.INTER_AREA)


with dai.Device(pipeline) as device:
    qLeft = device.getOutputQueue(name="left", maxSize=4, blocking=False)
    # qRight = device.getOutputQueue(name="right", maxSize=4, blocking=False)
    print('Webcam Online ...')
    while True:      
        #Mono webcam feed
        inLeft = qLeft.get().getCvFrame()
        inLeft_Colour = cv2.cvtColor(inLeft, cv2.COLOR_GRAY2RGB)
        # inRight = qRight.get().getCvFrame()
        # inRight_Colour = cv2.cvtColor(inRight, cv2.COLOR_GRAY2RGB)
        
        # Make decisions
        results = model(inLeft_Colour)
        squeezed = np.squeeze(results.render())

        # Rescale the frame of the GUI
        # rescaled = rescale_frame(squeezed, percent=50)

        # Render to the screen
        cv2.imshow('Yolo',squeezed)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

inLeft.release()
cv2.destroyAllWindows()
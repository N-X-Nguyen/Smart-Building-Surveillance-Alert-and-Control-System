#thư viện:
import paho.mqtt.client as mqtt
import cv2
import numpy as np
# khai bao bien:

# cấu hình cv2:
counter = 0
flag = False
cap = cv2.VideoCapture(0)
whT = 320
confThershold = 0.5
nmsThreshold = 0.3
classesFile = 'coco.names'
classNames = []
with open(classesFile,'rt') as f:
    classNames = f.read().rstrip('\n').split('\n')
modelConfiguration = 'yolov3-tiny.cfg.txt'
modelWeight = 'yolov3-tiny.weights'
net = cv2.dnn.readNetFromDarknet(modelConfiguration,modelWeight)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
#---------------------------------------------------------------------------------------------
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    if rc == 0:
        print("connected")
        
    
def on_message(client, userdata, message):
    print("")

def main():
    timer = 300
    counter = 0
    flag = False
#---------------------------------------------------------------------------------------------
# Connect to the MQTT server and process messages in a background thread.
    mqtt_client = mqtt.Client(client_id ="camera2")
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.connect('192.168.0.185', 1883, 60)
    mqtt_client.loop_start() 
#---------------------------------------------------------------------------------------------
#vòng lặp để sử dụng camera: 
    while True:
        success, img = cap.read()
        blob = cv2.dnn.blobFromImage(img, 1/255,(whT,whT),[0,0,0],1,crop=False)
        net.setInput(blob)
        layerNames = net.getLayerNames()
        outputNames = [layerNames[i-1] for i in net.getUnconnectedOutLayers()]
        outputs =  net.forward(outputNames)
        hT,wT,cT = img.shape
        bbox = []
        classIds = []
        confs = []
        for output in outputs:
            for det in output:
                scores = det[5:]
                classId = np.argmax(scores)
                confidence = scores[classId]
                if confidence > confThershold:
                    w,h = int(det[2]*wT) , int(det[3]*hT)
                    x,y = int((det[0]*wT)-w/2) , int((det[1]*hT)-h/2)
                    bbox.append([x,y,w,h])
                    classIds.append(classId)
                    confs.append(float(confidence))
        indices = cv2.dnn.NMSBoxes(bbox,confs,confThershold,nmsThreshold)
        if counter == 1 and flag == False:
            mqtt_client.publish("camera2", "1")
            flag = True
        if counter == 1:
            timer -= 1
            if timer == 0 and flag == True:
                counter = 0
                mqtt_client.publish("camera2", "0")
                flag = False
                print(counter)
        for i in indices:
            box = bbox[i]
            x,y,w,h = box[0],box[1],box[2],box[3]
            if (classNames[classIds[i]].upper() == "PERSON"):
                if counter == 0:
                    timer = 300
                    counter = 1
                    print(counter)
                cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,255),2)
                cv2.putText(img,f'{classNames[classIds[i]].upper()}{counter}', (x,y-10),cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,0,255),2)
        cv2.imshow('cap',img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
#---------------------------------------------------------------------------------------------
if __name__ == '__main__':
    print('MQTT to InfluxDB bridge')
    main()

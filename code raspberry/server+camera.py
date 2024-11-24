#thư viện:
import paho.mqtt.client as mqtt
import json
import requests
import cv2
import numpy as np
import time 
#---------------------------------------------------------------------------------------------
#liên kết:
url = 'https://smarthome2000.000webhostapp.com/buttonstatus.php'
API_ENDPOINT = "https://smarthome2000.000webhostapp.com/data.php"
API_ENDPOINT1 = "https://smarthome2000.000webhostapp.com/buttonauto.php"
API_KEY = "tPmAT5Ab3j7F9"
#---------------------------------------------------------------------------------------------
#khai báo biến:
data1 = 0
flag1 = False
flag2 = False
flag3 = False
flag4 = False
flag5 = False
flag6 = False
flag7 = False
flag8 = False
flag9 = False
flag10 = False
flag11 = False
flag12 = False
flag13 = False
flag14 = False
flag15 = False
flag16 = False
counter = 0
counter_1 = 0
last_counter = 0
json_data1 = 0
json_data2 = 0
json_data3 = 0
json_data4 = 0
MQTT_Topic = "#"
last_temp1 = 0
last_humi1 = 0
last_amoni1 = 0
last_CO_1 = 0
last_CO2_1 = 0
last_Alcoho_1 = 0
last_lux1 = 0
#---------------------------------------------------------------------------------------------
last_temp2 = 0
last_humi2 = 0
last_amoni2 = 0
last_CO_2 = 0
last_CO2_2 = 0
last_Alcoho_2 = 0
last_lux2 = 0
#---------------------------------------------------------------------------------------------
last_temp3 = 0
last_humi3 = 0
last_amoni3 = 0
last_CO_3 = 0
last_CO2_3 = 0
last_Alcoho_3 = 0
#---------------------------------------------------------------------------------------------
last_temp4 = 0
last_humi4 = 0
last_amoni4 = 0
last_CO_4 = 0
last_CO2_4 = 0
last_Alcoho_4 = 0
#---------------------------------------------------------------------------------------------
# cấu hình cv2:
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
    client.subscribe(MQTT_Topic)
    
def on_message(client, userdata, message):
    global counter,counter_1,json_data1,json_data2,json_data3,json_data4,flag1,flag2,flag3,flag4,flag5,flag6,flag7,flag8,flag9,flag10,last_counter,flag11,flag12,flag13,flag14,flag15,flag16,data1
    global last_temp2, last_humi2, last_amoni2,last_CO_2,last_CO2_2,last_Alcoho_2,last_temp1,last_humi1,last_amoni1,last_CO_1,last_CO2_1,last_Alcoho_1,last_temp3,last_humi3,last_amoni3,last_CO_3,last_CO2_3,last_Alcoho_3,last_temp4,last_humi4,last_amoni4,last_CO_4,last_CO2_4,last_Alcoho_4,last_lux1,last_lux2
    topic = message.topic
#--------------------------------------------------------------------------------------------- 
    topic1 = "/PHONG1/relay/"
    topic2 = "/PHONG2/relay/"
    try:
#phong1:
        response = requests.get(url)
        status = response.text
        time.sleep(0.5)
        if status and status != "":
            if "o1" in status and flag1 == False:
                flag1 = True
            elif "o1" in status and flag1 == True:
                flag13 == False
                flag1 = False
            elif "f_1" in status and flag1 == False:
                flag1 = True
            elif "f_1" in status and flag1 == True:
                flag13 == False
                flag1 = False
            if "o2" in status and flag2 == False:
                flag2 = True
            elif "o2" in status and flag2 == True:
                flag13 == False
                flag2 = False
            elif "f_2" in status and flag2 == False:
                flag2 = True
            elif "f_2" in status and flag2 == True:
                flag13 == False
                flag2 = False
            if "o3" in status and flag3 == False:
                flag3 = True
            elif "o3" in status and flag3 == True:
                flag13 == False
                flag3 = False
            elif "f_3" in status and flag3 == False:
                flag3 = True
            elif "f_3" in status and flag3 == True:
                flag13 == False
                flag3 = False
            if "o4" in status and flag4 == False:
                flag4 = True
            elif "o4" in status and flag4 == True:
                flag13 == False
                flag4 = False
            elif "f_4" in status and flag4 == False:
                flag4 = True
            elif "f_4" in status and flag4 == True:
                flag13 == False
                flag4 = False
            if "o5" in status and flag5 == False:
                flag5 = True
            elif "o5" in status and flag5 == True:
                flag15 == False
                flag5 = False
            elif "f_5" in status and flag5 == False:
                flag5 = True
            elif "f_5" in status and flag5 == True:
                flag15 == False
                flag5 = False
            if "o1" in status or "f_1" in status or"o2" in status or"f_2" in status or"o3" in status or"f_3" in status or"o4" in status or"f_4" in status or"o5" in status or"f_5" in status:
                datastatus = {
                'api_key':API_KEY,
                'status1': "o1" if "o1" in status else "f1" if "f_1" in status else "",
                'status2': "o2" if "o2" in status else "f2" if "f_2" in status else "",
                'status3': "o3" if "o3" in status else "f3" if "f_3" in status else "",
                'status4': "o4" if "o4" in status else "f4" if "f_4" in status else "",
                'status5': "o5" if "o5" in status else "f5" if "f_5" in status else "",
                'statuss1':  "",
                'statuss2':  "",
                'statuss3':  "",
                'statuss4':  "",
                'statuss5':  "",}
                r = requests.post(url = API_ENDPOINT1, data = datastatus)
                data_json5 = json.dumps(datastatus)
                client.publish(topic1,payload=data_json5)
                # pastebin_url = r.text
                # print("The pastebin URL is:%s"%pastebin_url) 
#--------------------------------------------------------------------------------------------
#phong2:           
            if "on1" in status and flag6 == False:
                flag6 = True
            elif "on1" in status and flag6 == True:
                flag6 = False
                flag14 == False
            elif "off1" in status and flag6 == False:
                flag6 = True
            elif "off1" in status and flag6 == True:
                flag6 = False
                flag14 == False
            if "on2" in status and flag7 == False:
                flag7 = True
            elif "on2" in status and flag7 == True:
                flag7 = False
                flag14 == False
            elif "off2" in status and flag7 == False:
                flag7 = True
            elif "off2" in status and flag7 == True:
                flag7 = False
                flag14 == False
            if "on3" in status and flag8 == False:
                flag8 = True
            elif "on3" in status and flag8 == True:
                flag8 = False
                flag14 == False
            elif "off3" in status and flag8 == False:
                flag8 = True
            elif "off3" in status and flag8 == True:
                flag8 = False
                flag14 == False
            if "on4" in status and flag9 == False:
                flag9 = True
            elif "on4" in status and flag9 == True:
                flag9 = False
                flag14 == False
            elif "off4" in status and flag9 == False:
                flag9 = True
            elif "off4" in status and flag9 == True:
                flag9 = False
                flag14 == False
            if "on5" in status and flag10 == False:
                flag10 = True
            elif "on5" in status and flag10 == True:
                flag10 = False
                flag16 == False
            elif "off5" in status and flag10 == False:
                flag10 = True
            elif "off5" in status and flag10 == True:
                flag10 = False
                flag16 == False
            if "on1" in status or "off1" in status or"on2" in status or"off2" in status or"on3" in status or"off3" in status or"on4" in status or"off4" in status or"off5" in status or"on5" in status:
                datastatus1 = {
                'api_key':API_KEY,
                'status1':  "",
                'status2':  "",
                'status3':  "",
                'status4':  "",
                'status5':  "",
                'statuss1': "on1" if "on1" in status else "off1" if "off1" in status else "",
                'statuss2': "on2" if "on2" in status else "off2" if "off2" in status else "",
                'statuss3': "on3" if "on3" in status else "off3" if "off3" in status else "",
                'statuss4': "on4" if "on4" in status else "off4" if "off4" in status else "",
                'statuss5': "on5" if "on5" in status else "off5" if "off5" in status else "",}
                data_json6 = json.dumps(datastatus1)
                requests.post(url = API_ENDPOINT1 ,data = datastatus1) 
                client.publish(topic2,payload=data_json6)
#--------------------------------------------------------------------------------------------- 
# tự đông 1:
        if last_lux1 <200  and flag13 == False:
            flag12 = False
            flag13 = True
        elif last_lux1 >= 200:
            flag13 = False
        elif last_temp1 >=25 and flag15 == False:
            flag12 = False
            flag15 = True
            
        if (counter == 1 and flag12 == False) or (counter == 1 and last_lux1 < 200 and flag12 == False) or (counter == 1 and last_temp1 >=25 and flag12 == False ) :         
            flag12 = True
            datastatus = {
            'api_key':API_KEY,
            'status1': "o1" if  not flag1 and last_lux1 < 200  else "",
            'status2': "o2" if  not flag2 and last_lux1 < 200  else "",
            'status3': "o3" if  not flag3 and last_lux1 < 200  else "",
            'status4': "o4" if  not flag4 and last_lux1 < 200  else "",
            'status5': "o5" if  not flag5 and last_temp1 >= 25 else "",
            'statuss1': "",
            'statuss2': "",
            'statuss3': "",
            'statuss4': "",
            'statuss5': "",}
            r = requests.post(url = API_ENDPOINT1, data = datastatus)  
            data_json5 = json.dumps(datastatus)
            client.publish(topic1,payload =data_json5)
            # pastebin_url = r.text
            # print("The pastebin URL is:%s"%pastebin_url)
        elif counter == 0 and flag12 == True:
            flag12 = False
            datastatus = {
            'api_key':API_KEY,
            'status1': "f1" if not flag1 else "",
            'status2': "f2" if not flag2 else "",
            'status3': "f3" if not flag3 else "",
            'status4': "f4" if not flag4 else "",
            'status5': "f5" if not flag5 else "",
            'statuss1': "",
            'statuss2': "",
            'statuss3': "",
            'statuss4': "",
            'statuss5': "",}
            r = requests.post(url = API_ENDPOINT1, data = datastatus)
            data_json5 = json.dumps(datastatus)
            client.publish(topic1,payload=data_json5)  
            # pastebin_url = r.text
            # print("The pastebin URL is:%s"%pastebin_url)
#---------------------------------------------------------------------------------------------   
# tự động2:
        if last_lux2 <200  and flag14 == False:
            flag11 = False
            flag14 = True
        elif last_lux2 >= 200:
            flag14 = False
        elif last_temp2 >=25 and flag16 == False:
            flag11 = False
            flag16 = True
        if topic == "camera2":
            counter_1 = message.payload.decode()
            print(counter_1)
            if (counter_1 == "1" and flag11 == False) or (counter == 1 and last_lux2 < 200 and flag14 == False): 
                flag11 = True
                datastatus1 = {
                'api_key':API_KEY,
                'statuss1': "on1" if flag6 == False and last_lux2 < 200  else "",
                'statuss2': "on2" if flag7 == False and last_lux2 < 200  else "",
                'statuss3': "on3" if flag8 == False and last_lux2 < 200 else "",
                'statuss4': "on4" if flag9 == False and last_lux2 < 200 else "",
                'statuss5': "on5" if flag10 == False and last_temp2 >= 25 else "",
                'status1': "",
                'status2': "",
                'status3': "",
                'status4': "",
                'status5': "",}
                r = requests.post(url = API_ENDPOINT1, data = datastatus1)
                data_json6 = json.dumps(datastatus1)
                client.publish(topic2,payload=data_json6)  
            elif counter_1 == "0" and flag11 == True:
                flag11 = False
                datastatus1 = {
                'api_key':API_KEY,
                'statuss1': "off1" if flag6 == False  else "",
                'statuss2': "off2" if flag7 == False  else "",
                'statuss3': "off3" if flag8 == False  else "",
                'statuss4': "off4" if flag9 == False  else "",
                'statuss5': "off5" if flag10 == False else "",
                'status1': "",
                'status2': "",
                'status3': "",
                'status4': "",
                'status5': "",}
                r = requests.post(url = API_ENDPOINT1, data = datastatus1)
                data_json6 = json.dumps(datastatus1)
                client.publish(topic2,payload=data_json6)  
    except requests.exceptions.ConnectionError:
        print("Không thể kết nối đến server. Đang thử lại...")
        
    if(topic == "/PHONG1"):
        json_data1 = json.loads(message.payload.decode())
        print(json_data1)
        if "phong1" in json_data1 and json_data1.get("phong1") is not None:# and (json_data2 == 0 or json_data3 == 0 or json_data4 == 0):     
            temp1 = json_data1["temp1"]
            humi1 = json_data1["humi1"]
            amoni1 = json_data1["Nh31"]
            CO_1 = json_data1["1CO"]
            CO2_1 = json_data1["CO21"]
            Alcoho_1 = json_data1["Alcoho1"] 
            lux1 = json_data1["lux1"]
            if temp1 != last_temp1 or humi1 !=last_humi1 or amoni1 !=last_amoni1 or CO_1 !=last_CO_1 or CO2_1 != last_CO2_1 or Alcoho_1 != last_Alcoho_1:
                last_temp1 = temp1
                last_humi1 = humi1
                last_amoni1 = amoni1
                last_Alcoho_1 = Alcoho_1
                last_CO2_1 = CO2_1
                last_CO_1 = CO_1
                last_lux1 = lux1
                data1={'api_key':API_KEY,
                        'temp1':temp1,
                        'humi1':humi1,
                        'amoni1':amoni1,
                        'CO2_1':CO2_1,
                        'CO_1':CO_1,
                        'Alcoho1':Alcoho_1,
                        'lux1': lux1,
                        'temp2':last_temp2,
                        'humi2':last_humi2,
                        'amoni2':last_amoni2,
                        'CO2_2':last_CO2_2,
                        'CO_2':last_CO_2,
                        'Alcoho2':last_Alcoho_2,
                        'lux2': last_lux2,
                        'temp3':last_temp3,
                        'humi3':last_humi3,
                        'amoni3':last_amoni3,
                        'CO2_3':last_CO2_3,
                        'CO_3':last_CO_3,
                        'Alcoho3':last_Alcoho_3,
                        'temp4':last_temp4,
                        'humi4':last_humi4,
                        'amoni4':last_amoni4,
                        'CO2_4':last_CO2_4,
                        'CO_4':last_CO_4,
                        'Alcoho4':last_Alcoho_4}
                r = requests.post(url = API_ENDPOINT, data = data1)
                
#---------------------------------------------------------------------------------------------   
    elif(topic == "/PHONG2"):
        print(json_data2)
        json_data2 = json.loads(message.payload.decode())
        if "phong2" in json_data2 and json_data2.get("phong2") is not None:# and (json_data1 == 0 or json_data3 == 0 or json_data4 == 0):           
            temp2 = json_data2["temp2"]
            humi2 = json_data2["humi2"]
            amoni2 = json_data2["Nh32"]
            CO_2 = json_data2["2CO"]
            CO2_2 = json_data2["CO22"]
            Alcoho_2 = json_data2["Alcoho2"]
            lux2 = json_data2["lux2"]
            if temp2 != last_temp2 or humi2 !=last_humi2 or amoni2 !=last_amoni2 or CO_2 !=last_CO_2 or CO2_2 != last_CO2_2 or Alcoho_2 != last_Alcoho_2:
                last_temp2 = temp2
                last_humi2 = humi2
                last_amoni2 = amoni2
                last_Alcoho_2 = Alcoho_2
                last_CO2_2 = CO2_2
                last_CO_2 = CO_2
                last_lux2 = lux2
                data1={'api_key':API_KEY,
                        'temp1':last_temp1,
                        'humi1':last_humi1,
                        'amoni1':last_amoni1,
                        'CO2_1':last_CO2_1,
                        'CO_1':last_CO_1,
                        'Alcoho1':last_Alcoho_1,
                        'lux1': last_lux1,
                        'temp2':temp2,
                        'humi2':humi2,
                        'amoni2':amoni2,
                        'CO2_2':CO2_2,
                        'CO_2':CO_2,
                        'Alcoho2':Alcoho_2,
                        'lux2': lux2,
                        'temp3':last_temp3,
                        'humi3':last_humi3,
                        'amoni3':last_amoni3,
                        'CO2_3':last_CO2_3,
                        'CO_3':last_CO_3,
                        'Alcoho3':last_Alcoho_3,
                        'temp4':last_temp4,
                        'humi4':last_humi4,
                        'amoni4':last_amoni4,
                        'CO2_4':last_CO2_4,
                        'CO_4':last_CO_4,
                        'Alcoho4':last_Alcoho_4}
                r = requests.post(url = API_ENDPOINT, data = data1)
               # pastebin_url = r.text
                #print("The pastebin URL is:%s"%pastebin_url)      
#---------------------------------------------------------------------------------------------   
    elif(topic == "/PHONG3"):
        json_data3 = json.loads(message.payload.decode())
        print(json_data3)
        if "phong3" in json_data3 and json_data3.get("phong3") is not None:# and (json_data1 == 0 or json_data2 == 0 or json_data4 == 0):
            temp3 = json_data3["temp3"]
            humi3 = json_data3["humi3"]
            amoni3 = json_data3["Nh33"]
            CO_3 = json_data3["3CO"]
            CO2_3 = json_data3["CO23"]
            Alcoho_3 = json_data3["Alcoho3"]  
            if temp3 != last_temp3 or humi3 !=last_humi3 or amoni3 !=last_amoni3 or CO_3 !=last_CO_3 or CO2_3 != last_CO2_3 or Alcoho_3 != last_Alcoho_3:
                last_temp3 = temp3
                last_humi3 = humi3
                last_amoni3 = amoni3
                last_Alcoho_3 = Alcoho_3
                last_CO2_3 = CO2_3
                last_CO_3 = CO_3
                data1={'api_key':API_KEY,
                        'temp1':last_temp1,
                        'humi1':last_humi1,
                        'amoni1':last_amoni1,
                        'CO2_1':last_CO2_1,
                        'CO_1':last_CO_1,
                        'Alcoho1':last_Alcoho_1,
                        'lux1': last_lux1,
                        'temp2':last_temp2,
                        'humi2':last_humi2,
                        'amoni2':last_amoni2,
                        'CO2_2':last_CO2_2,
                        'CO_2':last_CO_2,
                        'Alcoho2':last_Alcoho_2,
                        'lux2': last_lux2,
                        'temp3':temp3,
                        'humi3':humi3,
                        'amoni3':amoni3,
                        'CO2_3':CO2_3,
                        'CO_3':CO_3,
                        'Alcoho3':Alcoho_3,  
                        'temp4':last_temp4,
                        'humi4':last_humi4,
                        'amoni4':last_amoni4,
                        'CO2_4':last_CO2_4,
                        'CO_4':last_CO_4,
                        'Alcoho4':last_Alcoho_4}
                r = requests.post(url = API_ENDPOINT, data = data1)
#---------------------------------------------------------------------------------------------   
    elif(topic == "/PHONG4"):
        json_data4 = json.loads(message.payload.decode())
        print(json_data4)
        if "phong4" in json_data4 and json_data4.get("phong4") is not None:# and (json_data1 == 0 or json_data2 == 0 or json_data3 == 0):      
            temp4 = json_data4["temp4"]
            humi4 = json_data4["humi4"]
            amoni4 = json_data4["Nh34"] 
            CO_4 = json_data4["4CO"]
            CO2_4 = json_data4["CO24"]
            Alcoho_4 = json_data4["Alcoho4"] 
            if temp4 != last_temp4 or humi4 !=last_humi4 or amoni4 !=last_amoni4 or CO_4 !=last_CO_4 or CO2_4 != last_CO2_4 or Alcoho_4 != last_Alcoho_4:
                last_temp4 = temp4
                last_humi4 = humi4
                last_amoni4 = amoni4
                last_Alcoho_4 = Alcoho_4
                last_CO2_4 = CO2_4
                last_CO_4 = CO_4
                data1={'api_key':API_KEY,
                        'temp1':last_temp1,
                        'humi1':last_humi1,
                        'amoni1':last_amoni1,
                        'CO2_1':last_CO2_1,
                        'CO_1':last_CO_1,
                        'Alcoho1':last_Alcoho_1,
                        'temp2':last_temp2,
                        'humi2':last_humi2,
                        'amoni2':last_amoni2,
                        'CO2_2':last_CO2_2,
                        'CO_2':last_CO_2,
                        'Alcoho2':last_Alcoho_2,
                        'temp3':last_temp3,
                        'humi3':last_humi3,
                        'amoni3':last_amoni3,
                        'CO2_3':last_CO2_3,
                        'CO_3':last_CO_3,
                        'Alcoho3':last_Alcoho_3,
                        'temp4':temp4,
                        'humi4':humi4,
                        'amoni4':amoni4,
                        'CO2_4':CO2_4,
                        'CO_4':CO_4,
                        'Alcoho4':Alcoho_4}
                r = requests.post(url = API_ENDPOINT, data = data1) 

#---------------------------------------------------------------------------------------------    
def main():
    global counter
    timer = 300
    counter = 0
#---------------------------------------------------------------------------------------------
# Connect to the MQTT server and process messages in a background thread.
    mqtt_client = mqtt.Client(client_id = "server" )
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.connect('localhost', 1883, 60)
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
        if counter == 1:
            timer -= 1
            if timer == 0 :
                counter = 0
        for i in indices:
            box = bbox[i]
            x,y,w,h = box[0],box[1],box[2],box[3]
            if (classNames[classIds[i]].upper() == "PERSON"):
                if counter == 0:
                    timer = 300
                    counter = 1
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
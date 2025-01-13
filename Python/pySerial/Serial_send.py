import os
import serial
import serial.tools.list_ports
import threading
import time


cmdStausList = [
    ('AT', 1)
    ,('ATE1', 1)
    ,('ATI', 1)
    ,('AT+GSN', 1)
]

cmdList = [
    ('AT+CFUN=0', 1)
    ,('AT+CGDCONT=1,"IP","soracom.io"', 1)
    ,('AT+CNCFG=0,1,"soracom.io"', 1)
    ,('AT+CFUN=1', 1)
    ,('AT+CGNAPN', 1)
    ,('AT+CMNB=1', 1)
    ,('AT+CPSI?', 1)
    ,('AT+CNACT=0,1', 1)
    ,('AT+CNACT?', 1)
    ,('AT+SHCONF="URL","http://uni.soracom.io"', 1)
    ,('AT+SHCONF="URL","http://uni.soracom.io"', 1)
    ,('AT+SHCONF="BODYLEN",1024', 1)
    ,('AT+SHCONF="HEADERLEN",350', 1)
    ,('AT+SHCONN', 1)
    ,('AT+SHSTATE?', 1)
    ,('AT+SHCHEAD', 1)
    ,('AT+SHAHEAD="User-Agent","CAT-M/NB-IoT+GNSS Unit w/ SIM7080G"', 1)
    ,('AT+SHAHEAD="Connection","close"', 1)
    ,('AT+SHAHEAD="Accept","*/*"', 1)
    ,('AT+SHAHEAD="Content-Type","text/plain"', 1)
    ,('AT+SHBOD=29,10000', 1)
    ,('{"title":"Hello http server"}', 1)
    ,('AT+SHREQ="/",3', 1)
    ,('AT+SHDISC', 1)
]

#----------------------
# データを送信
#----------------------
def serial_list_write():
    global Serial_Port
    
    if Serial_Port !='':
        for item in cmdList:
            cmd, tm = item
            data=cmd+'\r\n'
            data=data.encode('utf-8')
            Serial_Port.write(data)
            time.sleep(tm)

#----------------------
# データを送信
#----------------------
def serial_write():
    global Serial_Port
    
    while(1):
        if Serial_Port !='':
            data=input()+'\r\n'
            data=data.encode('utf-8')
            Serial_Port.write(data)

#----------------------
# データを受信
#----------------------
def serial_read():
    global Serial_Port

    while(1):
        if Serial_Port !='':
            #data=Serial_Port.read(1)
            data=Serial_Port.readline()
            data=data.strip()
            data=data.decode('utf-8')
            print(data)

# Main

Serial_Port=''
    
#port open
Serial_Port=serial.Serial('/dev/ttyAMA0', 115200, timeout=None)
    
thread_1 = threading.Thread(target=serial_list_write)
thread_2 = threading.Thread(target=serial_read)

thread_1.start()
thread_2.start()


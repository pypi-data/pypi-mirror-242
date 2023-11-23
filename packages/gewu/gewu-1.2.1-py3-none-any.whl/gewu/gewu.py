'''
# V0.1
* 优化了舵机的接口

# V0.2
* 修正了舵机部分错误

# V0.3
* 增加lcd显示的icon接口等

# V0.4
* 增加颜色传感器和超声波传感器的接口

# V0.5 
* 增加对码盘电机的支持
'''
import serial
import serial.tools.list_ports
from threading import Thread
import time

STEP_WAIT_AA = 0
STEP_WAIT_BB = 1
STEP_WAIT_CMD = 2
STEP_WAIT_LEN = 3
STEP_WAIT_DATA = 4
STEP_WAIT_BCC = 5
STEP_WAIT_AA1 = 10
STEP_WAIT_AA2 = 11
STEP_WAIT_BB1 = 12
STEP_WAIT_BB2 = 13

HEADA=0xF0
HEADB=0x0C

uartRxstep = STEP_WAIT_AA
datacmd = 0
uartRxindex = 0
datalen = 0
UART_BUFF_SIZE = 255
uartdata = bytearray(UART_BUFF_SIZE)

btn_a_state = 1
btn_b_state = 1
mic_value = 0
pin_1_input = 0
pin_2_input = 0
light_value = 0
acc_x = 0
acc_y = 0
acc_z = 0

dist_result = bytearray(4) #存储4个端口的超声波数据
color_result = bytearray(16) #[result,r,g,b]
motor_result = [0] * 20 #[state,car,power,speed,count]
motor_result_flag = 0

def get_serialport():
    # 获取所有串口设备实例。
    # 如果没找到串口设备，则输出：“无串口设备。”
    # 如果找到串口设备，则依次输出每个设备对应的串口号和描述信息。
    ports_list = list(serial.tools.list_ports.comports())
    gewu_port = ""
    if len(ports_list) <= 0:
        print("无串口设备。")
        return None
    else:
        print("可用的串口设备如下：")
        for comport in ports_list:
            print(list(comport)[0], list(comport)[1])
            if list(comport)[1].find('CH340') != -1:
                gewu_port = list(comport)[0]
    if gewu_port !="":
        print("Gewu Serial:" + gewu_port)
        return gewu_port
    else:
        return None

def open_serial_port():
    gewu_port = get_serialport()
    if gewu_port == None:
        print("搜索串口设备失败")
        return None
    try:
        ser = serial.Serial(gewu_port, 115200)    # 打开COM17，将波特率配置为115200，其余参数使用默认值
    except Exception as e:
        print('端口连接失败,错误原因：\n',e)
        return None
    if ser.isOpen():                        # 判断串口是否成功打开
        print("打开串口成功。")
        print(ser.name)    # 输出串口号
    else:
        print("打开串口失败。")
        return None
    ser.write(chr(0x03).encode("utf-8"))
    ser.write(chr(0x06).encode("utf-8")) #进入在线模式
    return ser

def getChecksum(cmd, data, len):
    checksum = 0
    checksum ^= cmd
    checksum ^= len
    for i in range (len):
        checksum ^= data[i]
    return checksum

def readCmd():
    global datacmd
    return datacmd

def readLen():
    global datalen
    return datalen

def readBytes(_len, index):
    global uartdata
    _data = []
    for i in range(_len):
        _data.append(uartdata[i+index])
    return _data

def recv_parse(_inByte):
    global uartRxstep, datacmd, uartRxindex, uartdata, datalen
    if uartRxstep == STEP_WAIT_AA:
        if _inByte == HEADA:
            uartRxstep = STEP_WAIT_BB
            #print("##A")
    elif uartRxstep == STEP_WAIT_BB:
        if _inByte == HEADB:
            uartRxstep = STEP_WAIT_CMD
        else:
            uartRxstep = STEP_WAIT_AA
    elif uartRxstep == STEP_WAIT_CMD:
        datacmd = _inByte
        uartRxstep = STEP_WAIT_LEN
    elif uartRxstep == STEP_WAIT_LEN:
        datalen = _inByte
        if datalen > 128: ##error
            uartRxstep = STEP_WAIT_AA
        uartRxindex = 0
        uartRxstep = STEP_WAIT_DATA
    elif uartRxstep == STEP_WAIT_DATA:
        uartdata[uartRxindex] = _inByte
        uartRxindex += 1
        if uartRxindex >= datalen:
            uartRxstep = STEP_WAIT_BCC
    elif uartRxstep == STEP_WAIT_BCC:
        uartRxstep = STEP_WAIT_AA
        if getChecksum(datacmd, uartdata, datalen) == _inByte:
            return True
        else:
            print('crc error')
    return False

def recv_serial_handler(serial_port):
    global btn_a_state,btn_b_state,mic_value,pin_2_input,light_value,acc_x,acc_y,acc_z,pin_1_input,dist_result,color_result,motor_result
    global motor_result_flag
    try:
        while True:
            count = serial_port.inWaiting()
            if count > 0:
                data = serial_port.read(count)
                #print(data)
                for ch in data:
                    if recv_parse(ch) == True:
                        cmd = readCmd()
                        if cmd == 0x01: #广播数据
                            [state] = readBytes(1, 0)
                            [btn] = readBytes(1, 1)
                            #print(btn)
                            btn_b_state = btn & 0x01
                            btn_a_state = (btn>>1) & 0x01
                            #print("BTN "+str(btn_a_state)+" "+str(btn_b_state))
                            [mic_value] = readBytes(1, 2)
                            [pin_2_input] = readBytes(1, 3)
                            [light_value] = readBytes(1, 4)
                            [acc_1,acc_2,acc_3,acc_4,acc_5,acc_6] = readBytes(6, 5)
                            acc_x = acc_1 |(acc_2<<8)
                            acc_y = acc_3 |(acc_4<<8)
                            acc_z = acc_5 |(acc_6<<8)
                            [pin_1_input] = readBytes(1, 11)

                        elif cmd == 0x0A: #超声波数据
                            [p,d1,d2] = readBytes(3, 0)
                            p = p - 0xE5
                            dist_result[p] = (int)((d1 | (d2<<8))/10)
                        elif cmd == 0x09: #颜色传感器
                            [p,a,b,c,d,e] = readBytes(6, 0)
                            p = p - 0xE5
                            color_result[4*p] = a
                            color_result[4*p+1] = b
                            color_result[4*p+2] = c
                            color_result[4*p+3] = d
                        elif cmd == 0x08: #电机参数
                            [p] = readBytes(1, 0) #端口
                            p = p - 0xE9
                            [motor_state] = readBytes(1, 1)
                            [deg1,deg2,deg3,deg4] = readBytes(4, 7)
                            deg = deg1 | (deg2<<8) |(deg3<<16)|(deg4<<24)
                            motor_result[5*p] = motor_state
                            if deg > 2147483647:
                                motor_result[5*p+4] = 4294967295 - deg
                            else:
                                motor_result[5*p+4] = deg
                            #print("deg "+ str(motor_result[5*p]) + " " + str(motor_result[5*p+4]))
                            motor_result_flag = 1

            time.sleep(0.01)
    except KeyboardInterrupt:
        if port != None:
            port.close()

class Button():
    def pressA(self):
        if btn_a_state:
            return False
        else:
            return True
        
    def pressB(self):
        if btn_b_state:
            return False
        else:
            return True

def hex2str(n):
    if n >=0 and n<=9:
        return 0x30 + n
    else:
        return 0x41+ (n-0x0A)

def pack_send_data(cmd, data, len):
    msg_send = bytearray(48)
    msg_send[0] = HEADA
    msg_send[1] = HEADB
    msg_send[2] = cmd
    msg_send[3] = len
    for i in range (len):
        msg_send[4 + i] = data[i]
    msg_send[4 + len] = getChecksum(cmd, data, len)

    for i in range (5 + len):
        port.write(chr(hex2str(msg_send[i]>>4)).encode("utf-8"))
        port.write(chr(hex2str(msg_send[i]&0x0f)).encode("utf-8"))


class OLED():
    def clear(self):
        _data = bytearray(2)
        _data[0] = 8
        _data[1] = 1
        pack_send_data(4, bytearray(_data), 2)

    def show(self):
        _data = bytearray(2)
        _data[0] = 9
        _data[1] = 1
        pack_send_data(4, bytearray(_data), 2)

    def text(self,x,y,font,data):
        _data = bytearray(128)
        _data[0] = 0
        _data[1] = x
        _data[2] = y
        pack_send_data(4, bytearray(_data), 3)

        _data[0] = 6
        # font_size = [6, 7, 11, 16]
        if font == 6:
            _data[1] = 0
        elif font == 7 :
            _data[1] = 1
        elif font == 11 :
            _data[1] = 2
        else:
            _data[1] = 3
        n = 2
        for i in str(data):
            _data[n] = ord(i)
            n = n + 1
        pack_send_data(4, bytearray(_data), n)
    # pic = [OLED.LOGO_S, OLED.LOVE, OLED.STONE, OLED.SCISSORS, OLED.CLOTH, OLED.ANGERE, OLED.SMILE, OLED.CRY,OLED.SUN,OLED.SUN,OLED.MOON,OLED.EYE]
    def get_icon_index(self,name):
        if name == "logo":
            return 0
        elif name == "sun":
            return 8
        elif name == "moon":
            return 9
        elif name == "love":
            return 1
        elif name == "eye":
            return 10
        elif name == "happy":
            return 6
        elif name == "sad":
            return 7
        elif name == "angry":
            return 5
        elif name == "stone":
            return 2
        elif name == "yeah":
            return 3
        elif name == "palm":
            return 4
        elif name == "fist":
            return 0
        elif name == "left":
            return 0
        elif name == "up":
            return 0
        elif name == "down":
            return 0
        elif name == "right":
            return 0
        else:
            return 0
        
    def icon(self,x,y,n):
        _data = bytearray(4)
        _data[0] = 7
        _data[1] = x
        _data[2] = y
        _data[3] = self.get_icon_index(n)
        pack_send_data(4, bytearray(_data), 4)

    def rect(self,x,y,l,w,type):
        _data = bytearray(6)
        if type == 0:#空心
            _data[0] = 2
        else:
            _data[0] = 3
        _data[1] = x
        _data[2] = y
        _data[3] = l
        _data[4] = w
        _data[5] = 1 #显示
        pack_send_data(4, bytearray(_data), 6)
    
    def clearRect(self,x,y,l,w,type):
        _data = bytearray(6)
        if type == 0:#空心
            _data[0] = 2
        else:
            _data[0] = 3
        _data[1] = x
        _data[2] = y
        _data[3] = l
        _data[4] = w
        _data[5] = 0 #
        pack_send_data(4, bytearray(_data), 6)

    def circle(self,x,y,r,type):
        _data = bytearray(5)
        if type == 0:#空心
            _data[0] = 4
        else:
            _data[0] = 5
        _data[1] = x
        _data[2] = y
        _data[3] = r
        _data[4] = 1 #显示
        pack_send_data(4, bytearray(_data), 5)
    def clearCircle(self,x,y,r,type):
        _data = bytearray(5)
        if type == 0:#空心
            _data[0] = 4
        else:
            _data[0] = 5
        _data[1] = x
        _data[2] = y
        _data[3] = r
        _data[4] = 0
        pack_send_data(4, bytearray(_data), 5)

class Servo():
    def __init__(self, r): 
       self.port = r - 2

    def angle(self,angle):
        if angle > 180:
            angle = 180
        if angle < 0:
            angle = 0
        _data = bytearray(3)
        _data[0] = self.port
        a = 0
        if angle == 90:
            a = 1500
        elif angle == 0:
            a = 1000
        elif angle == 180:
            a = 2000
        else:
            a = (int)(angle*5.5)+1000
        _data[1] = a & 0xff 
        _data[2] = a >> 8
        pack_send_data(2, bytearray(_data), 3)

    def speed(self,speed):
        if speed > 100:
            speed = 100
        if speed < -100:
            speed = -100
        if speed > 0 and speed < 25:
            speed = 25
        if speed < 0 and speed > -25:
            speed = -25

        _data = bytearray(3)
        _data[0] = self.port
        a = 5*speed +1500
        if a>2000:
            a = 2000
        _data[1] = a & 0xff 
        _data[2] = a >> 8
        pack_send_data(2, bytearray(_data), 3)

# -100 1000
#  100 2000
#
class Pin():
    def __init__(self, r): 
       self.port = r
    
    def getNum(self):
        if self.port == 1:
            return  0 if pin_1_input > 100 else 1
        else:
            return 0 if pin_2_input > 100 else 1
        
    def getCq(self):
        if self.port == 1:
            if pin_1_input < 20:
                return 0
            else:
                return pin_1_input
        else:
            if pin_2_input < 20:
                return 0
            else:
                return pin_2_input
    
class Audio():
    def play(self,name):
        _data = bytearray(3)
        _data[0] = 9
        _data[1] = self.get_sound_index(name)
        _data[2] = 1
        pack_send_data(1, bytearray(_data), 3)
    
    def get_sound_index(self,name):
        if name == "car":
            return 1
        elif name == "door":
            return 2
        elif name == "alert":
            return 3
        else:
            return 4

class Sensor():
    def __init__(self, r): 
       self.port = r

    def getDist(self):
        return dist_result[self.port - 5]
        
    def getColor(self):
        return color_result[4*(self.port - 5)]

    def getRgb(self):
        result = []
        result.append(color_result[4*(self.port - 5)+1])
        result.append(color_result[4*(self.port - 5)+2])
        result.append(color_result[4*(self.port - 5)+3])
        return result

class Motor():
    def __init__(self, r): 
       self.port = 0xE0 + r

    def speed(self,speed):
        if speed != 0:
            _data = bytearray(4)
            _data[0] = 0
            _data[1] = self.port
            _data[2] = speed
            _data[3] = speed >> 8
            pack_send_data(0x0A, bytearray(_data), 4) #设置速度

            _data[0] = 4
            _data[1] = self.port
            _data[2] = 0x01
            pack_send_data(0x0A, bytearray(_data), 3) #开始转动
        else:
            _data = bytearray(3)
            _data[0] = 1
            _data[1] = self.port
            _data[2] = 0x00
            pack_send_data(0x0A, bytearray(_data), 3) #STOP

    def degree(self,degree):
        global motor_result,motor_result_flag
        _data = bytearray(7)
        _data[0] = 0x0A
        _data[1] = self.port
        _data[2] = 1
        if degree < 0:
            _data[2] = 0
            degree = - degree
        _data[3] = (degree&0xff)
        _data[4] = (degree >> 8)&0xff
        _data[5] = (degree >> 16)&0xff
        _data[6] = (degree >> 24)&0xff
        pack_send_data(0x0A, bytearray(_data), 7)
        time.sleep(0.1)
        motor_result[5*(self.port -0xe0 - 9)] = 1
        while True:
            #print("### "+ str(motor_result[5*(self.port -0xe0 - 9)]))
            if motor_result[5*(self.port -0xe0 - 9)] == 0:
                break
            self.getMotorStatus()
            time.sleep(0.1)

    def setZero(self):
        global motor_result,motor_result_flag
        _data = bytearray(3)
        _data[0] = 5
        _data[1] = self.port
        _data[2] = 0x00
        pack_send_data(0x0A, bytearray(_data), 3)
        motor_result[5*(self.port -0xe0 - 9)+4] = 0

    def getMotorStatus(self):
        _data = bytearray(3)
        _data[0] = 7
        _data[1] = self.port
        _data[2] = 0x00
        pack_send_data(0x0A, bytearray(_data), 3)

    def getDegree(self):
        global motor_result,motor_result_flag
        _data = bytearray(3)
        _data[0] = 8
        _data[1] = self.port
        _data[2] = 0x00
        pack_send_data(0x0A, bytearray(_data), 3)
        motor_result_flag = 0
        count = 0
        while True:
            if motor_result_flag == 1:
                break
            time.sleep(0.01)
            count = count + 1
            if count > 500:
                print('error01 time out')
                break
        return motor_result[5*(self.port -0xe0 - 9)+4]

button = Button()
lcd = OLED()

p1 = Pin(1)
p2 = Pin(2)

p3 = Servo(3)
p4 = Servo(4)

p5 = Sensor(5)
p6 = Sensor(6)
p7 = Sensor(7)
p8 = Sensor(8)

p9 = Motor(9)
p10 = Motor(10)
p11 = Motor(11)
p12 = Motor(12)

sound = Audio()

# print(hex2str(0x05))
# print(hex2str(0x0F))

port = open_serial_port()
t = Thread(target=recv_serial_handler,args=(port,))
t.start()
#t.join()
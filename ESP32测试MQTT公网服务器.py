import time
import network
from umqtt.simple import MQTTClient

# 定义WiFi的SSID和密码变量
wifi_ssid = 'zhang'
wifi_password = '66886688abc'

# 定义MQTT服务器和认证信息
mqtt_server = "175.178.61.48"
mqtt_port = 1883
mqtt_username = "admin"
mqtt_password = "Zdc20031122"
mqtt_keepalive = 60

# 定义MQTT订阅的主题
mqtt_subscribe_topic = "my_esp8266"

#联网函数
def do_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(wifi_ssid, wifi_password)
        i = 1
        
        while not wlan.isconnected():
            print("正在链接...{}".format(i))
            i += 1
            time.sleep(1)
    print('network config:', wlan.ifconfig())

def sub_cb(topic, msg):
    print(topic, msg)

if __name__ == "__main__":
    #1.连接WiFi
    do_connect()
    
    #2. 创建mqtt客户端
    c = MQTTClient("MyESP8266", mqtt_server, mqtt_port, mqtt_username, mqtt_password, keepalive=mqtt_keepalive)
    c.set_callback(sub_cb)
    c.connect()
    c.subscribe(mqtt_subscribe_topic)
    
    for i in range(100):
        c.check_msg()
        time.sleep(0.5)
        c.publish("hello", "esp32...%d" % i)
        print("esp8266...%d" % i)
        time.sleep(0.5)

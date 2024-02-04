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

# 定义HA发送GPIO状态的主题
mqtt_control_GPIO1 = "ShuiChan/GPIO1/set"
mqtt_control_GPIO2 = "ShuiChan/GPIO2/set"
mqtt_control_GPIO3 = "ShuiChan/GPIO3/set"
mqtt_control_GPIO4 = "ShuiChan/GPIO4/set"

# 定义向Ha发送状态的主题
GPIO1_state_topic = "ShuiChan/GPIO1/state"
GPIO2_state_topic = "ShuiChan/GPIO2/state"
GPIO3_state_topic = "ShuiChan/GPIO3/state"
GPIO4_state_topic = "ShuiChan/GPIO4/state"
GPIO5_state_topic = "ShuiChan/GPIO5/state"

# 联网函数
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
    if topic == mqtt_control_GPIO1.encode():
        send_GPIO1_state_to_ha(msg)
    elif topic == mqtt_control_GPIO2.encode():
        send_GPIO2_state_to_ha(msg)
    elif topic == mqtt_control_GPIO3.encode():
        send_GPIO3_state_to_ha(msg)
    elif topic == mqtt_control_GPIO4.encode():
        send_GPIO4_state_to_ha(msg)


def send_GPIO1_state_to_ha(state):
    if state == b"ON":
        MQTT_CLIENT.publish(GPIO1_state_topic, b"ON")
    else:
        MQTT_CLIENT.publish(GPIO1_state_topic, b"OFF")


def send_GPIO2_state_to_ha(state):
    if state == b"ON":
        MQTT_CLIENT.publish(GPIO2_state_topic, b"ON")
    else:
        MQTT_CLIENT.publish(GPIO2_state_topic, b"OFF")

def send_GPIO3_state_to_ha(state):
    if state == b"ON":
        MQTT_CLIENT.publish(GPIO3_state_topic, b"ON")
    else:
        MQTT_CLIENT.publish(GPIO3_state_topic, b"OFF")

def send_GPIO4_state_to_ha(state):
    if state == b"ON":
        MQTT_CLIENT.publish(GPIO4_state_topic, b"ON")
    else:
        MQTT_CLIENT.publish(GPIO4_state_topic, b"OFF")

if __name__ == "__main__":
    # 1.连接WiFi
    do_connect()

    # 2. 创建mqtt客户端
    MQTT_CLIENT = MQTTClient("MyESP8266", mqtt_server, mqtt_port, mqtt_username, mqtt_password, keepalive=mqtt_keepalive)
    MQTT_CLIENT.set_callback(sub_cb)
    MQTT_CLIENT.connect()
    MQTT_CLIENT.subscribe(mqtt_control_GPIO1)
    MQTT_CLIENT.subscribe(mqtt_control_GPIO2)
    MQTT_CLIENT.subscribe(mqtt_control_GPIO3)
    MQTT_CLIENT.subscribe(mqtt_control_GPIO4)

    while 1:
        MQTT_CLIENT.check_msg()

        time.sleep(1)

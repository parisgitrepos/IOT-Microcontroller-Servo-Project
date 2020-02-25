from network_selection import Network_Selection
import network
import utime as time

wifi = network.WLAN(network.STA_IF)
wifi.activate(True)

while not wifi.isconnected():
    ssid_list = []
    for a in wifi.scan():
        ssid_list.append(a[0])

    configure_network = Network_Selection(ssid_list = ssid_list, ip = '', port = 25501, welcome_message = 'Welcome to the WiFi Configuration Portal!')
    ssid = configure_network.ssid
    password = configure_network.password

    wifi.connect(ssid, password)
    time.sleep(5)
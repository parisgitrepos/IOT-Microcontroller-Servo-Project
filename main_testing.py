class MainTesting:
    def __init__(self):
        from network_selection import NetworkSelection
        import network
        import time
        from mqtt import ServoStatusRequest

        wifi = network.WLAN(network.STA_IF)
        wifi.active(True)

        test = 0
        while test == 0:
            if wifi.isconnected():
                publish = ServoStatusRequest()
                publish.MQTT_publish(200)
                test+=1

            else:
                ssid_list = []
                wifi_scan_list = wifi.scan()
                for a in wifi_scan_list:
                    ssid_list.append(a[0])
                ap = network.WLAN(network.AP_IF)
                ap.active(True)
                ap.config(essid = 'ESP-Network-Config')
                NetworkSelection(ssid_list, '0.0.0.0', 11999, 'Welcome to the WiFi configuration portal!', wifi)
                ap.active(False)
                time.sleep(3)
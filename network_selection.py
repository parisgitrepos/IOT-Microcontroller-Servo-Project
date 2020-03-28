import usocket as socket
import time

class NetworkSelection:

    def __init__(self, ssid_list, ip, port, welcome_message, network_object):
        self.welcome_message = welcome_message
        self.ssid_list = ssid_list
        self.ssid_strings = ''
        for a in range(len(ssid_list)):
            value = str(a) + '.' + ' ' + str(ssid_list[a]) + '<br>'
            self.ssid_strings += value

        self.wifi = network_object
        self.ip = ip
        self.port = port
        self.wifi_connected = False

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_online = False
        while not server_online:
            try:
                self.server.bind((self.ip, self.port))
                self.server.listen(2)
                server_online = True
            except OSError:
                time.sleep(2)

        while self.wifi_connected is False:
            try:
                conn, addr = self.server.accept()
                self.client_handling(conn)
            except Exception as e:
                print(e)
                self.server.close()
                break

    def client_handling(self, conn):
        method = conn.recv(2048).decode()
        if 'GET' in method:
            max_list = len(self.ssid_list) - 1
            conn.send('HTTP/1.0 200 OK\n'.encode())
            conn.send('Content-Type: text/html\n\n'.encode())
            html = """
                    <html>
                    <h1>{welcome_message}</h1>
                    <br>
                    <h2>Please select your network from this list. If you do not see your network, try moving close to your router.</h2>
                    <h3>{ssid_strings}</h3>
                    <br>
                    <form method="post">
                    <h3>Number next to network:</h3><br>
                    <input type="number" name="SSID" min="0" max={max}>
                    <br><br>
                    <h3>Password:</h3>
                    <input type="password" name="password">
                    <br><br>
                    <input type="submit">
                    </form>
                    </html>
                    """.format(ssid_strings = self.ssid_strings, max = max_list, welcome_message = self.welcome_message)
            conn.sendall(html.encode())
        elif 'POST' in method:
            method += conn.recv(2048).decode()
            ssid = self.ssid_list[int(str(method.split('SSID=', 1)[1]).split('password=')[0][:-1])]
            password = method.split('password=')[1]
            self.wifi.connect(ssid, password)

            connecting = True
            while connecting:
                status = int(self.wifi.status())
                if status == 1:
                    pass
                else:
                    connecting = False

            if status == 5:
                status = 'Connected'
                self.wifi_connected = True
            elif status == 0:
                status = 'ERROR - No activity'
            elif status == 2:
                status = 'ERROR - Incorrect password'
            elif status == 3:
                status = 'ERROR - No AP replied'
            elif status == 4:
                status = 'ERROR - Unknown error'
            else:
                status = 'ERROR - Unknown error'

            html = """
                <html>
                <head>
                </head>
                <body>
                <h3>Status: {status}</h3>
                <h3>If your network connection resulted in an error, please refresh the page and try again.</h3>
                </body>
                </html>
                """.format(status = status).encode()
            conn.send('HTTP/1.0 200 OK\n'.encode())
            conn.send('Content-Type: text/html\n\n'.encode())
            conn.sendall(html)
import usocket as socket
import time

class NetworkSelection:

    def __init__(self, ssid_list, ip, port, welcome_message):
        self.welcome_message = welcome_message
        self.ssid_list = ssid_list
        self.ssid_strings = ''
        for a in range(len(ssid_list)):
            value = str(a) + '.' + ' ' + str(ssid_list[a]) + '<br>'
            self.ssid_strings += value

        self.ip = ip
        self.port = port
        self.ssid = None
        self.password = None

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_online = False
        while not server_online:
            try:
                self.server.bind((self.ip, self.port))
                self.server.listen(2)
                server_online = True
            except OSError:
                time.sleep(2)

        while self.ssid is None:
            try:
                conn, addr = self.server.accept()
                self.client_handling(conn)

            except Exception as e:
                self.server.close()
                break

    def client_handling(self, conn):
        method = conn.recv(1024).decode()
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
            self.ssid = int(str(method.split('SSID=', 1)[1]).split('password=')[0])
            self.ssid = self.ssid_list[self.ssid]
            self.password = method.split('password=')[1]
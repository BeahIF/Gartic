import socket
import json
import pickle


class Network:
    def __init__(self, name):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server = "localhost"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.name = name
        self.connect()

    def connect(self):
        try:
            self.client.connect(self.addr)
            self.client.sendall(self.name.encode())
            return json.loads(self.client.recv(2048))
        except Exception as e:
            # print(e)
            self.disconnect(e)

    def send(self, data):
        try:
            self.client.send(json.dumps(data).encode())
            d = ""
            
            while 1:
                last = self.client.recv(1024).decode()
                d += last
                try:
                    if last.count("}") == 1:
                        break
                except:
                    break

            return json.loads(d)
        except socket.error as e:
            print(e)

    def disconnect(self, msg):
        print("exception disconected from server", msg)
        # self.client.shutdown(socket.SHUT_RDWR)
        # try:
        #     self.send({10: []})
        # except:
        #     self.client.close()
        self.client.close()


n = Network("Finge que tem um nome interessante")
# print(n.connect())
print(n.send({3: []}))
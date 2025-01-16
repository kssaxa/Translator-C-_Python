from server import app
import socket
import json

if __name__ == "__main__":


    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    print("Локальный IP:", local_ip)

    local_ip_data = {
        "ip": local_ip
    }

    with open("./ip_address.json", "w") as file:
        json.dump(local_ip_data, file)

    app.run(host=local_ip, port=8888)

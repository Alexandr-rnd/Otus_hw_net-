import socket
import re
from http import HTTPStatus
import random


def random_port(): return random.randint(20000, 30000)


LOCALHOST = "127.0.0.1"
my_socket = socket.socket()
address_and_port = (LOCALHOST, random_port())
my_socket.bind(address_and_port)
my_socket.listen(10)
conn, addr = my_socket.accept()

print("Started socket on", address_and_port)
with open("request.txt", "w") as txt:  # вычитываем заголовки и тело
    data = conn.recv(1024).decode("utf-8")
    txt.writelines(data)
    cl_request = []
    for i in data.split('\n'):
        cl_request.append(i)
    status_code = "200 OK"
    if 'status' in cl_request[0]:  # проверяем параметр переданного статус кода
        result = re.search(r'\d{3}%20\w+', cl_request[0])
        status_mask = result[0].split('%20')
        if int(status_mask[0]) in list(HTTPStatus) and status_mask[1] in str(
                list(HTTPStatus)):  # проверяем валидность переданного статус кода
            status_code = f'{status_mask[0]} {status_mask[1]}'
        else:
            status_code = "499 invalid status code!!!"
with open("request.txt", "r") as txt:
    txt.readline()  # пропускаем уже переданные строки
    txt.readline()
    r = txt.readlines()
    HtmlString = ''
    for i in r:  # переписываем под HTML
        HtmlString += f'<p>{i}</p>'
    conn.send(f"HTTP/1.1 {status_code}\n Content-Length: 100\n Connection: close\n Content-Type:"
              f"text/html\n\n<p>Request Method:{cl_request[0].split('/')[0]}</p>"
              f"<p>Request Source:{cl_request[1][7:-1]}</p>"
              f"<p>Request Status:{status_code}</p>{HtmlString}".encode("utf-8"))

my_socket.close()

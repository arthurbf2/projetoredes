import socket

pageTemplate = '''
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
    <style>
        table, th, td {{
          border:2px solid black;
          background-color:#aa9825;
          text-align:center"
        }}
        </style>
<head>
    <meta charset="UTF-8">
    <title>Servidor WEB</title>
</head>
<body>
    <form action="" id="formulario"method="post">
        <input type="text" id="box1" name="box1" style="width:99%">
        <button type="submit" style="width:100%">Enviar</button>
    </form>
    <p> </p>
    <table id="myTable" style="width:100%">
        <div style="background-color:#a9abac;text-align:center; font-size:xx-large;"> Lista </div>
        <script>
            var itens = {tabela};
            for(var i=0; i < itens.length; i++) {{
                document.write('<tr id="' + itens[i] + '"><th>' + itens[i] + '<button onclick="deleta_item()"> \
                Delete</button></th></tr>');
            }}
        </script>
    </table>
</body>
<script>
    function deleta_item() {{
        var target = event.target.parentNode.parentNode;
        var id = target.id;
        deleted = id;
        console.log(deleted);
        fetch('/' + id, {{
            method: 'DELETE' 
        }})
    }}
</script>
</html>'''  # NEW note '{person}' two lines up

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind(('', 8000))
s.listen(10)
itens = []


def request_handler(req):
    req = req.split()
    tabela = []

    if req[0] == 'GET':
        contents = pageTemplate.format(**locals())
        resp = ('HTTP/1.1 200 OK\r\n' + 'Content-Type: text/html\r\n' + 'Content-Length: ' + str(
            len(contents)) + '\r\n\r\n' + contents)
    elif req[0] == 'POST':
        form = req[-1].split('=')[1]  # DADO DO FORMULÁRIO
        # print(form)
        itens.append(form)
        for item in itens:
            if item:
                #  tabela += f'<tr><th>{item}<button onclick="deleta_item()">Delete</button></th></tr>'
                tabela.append(item)
        contents = pageTemplate.format(**locals())
        resp = ('HTTP/1.1 200 Ok\r\n' + 'Content-Type: text/html\r\n' + 'Content-Length: ' + str(
            len(contents)) + '\r\n\r\n' + contents)
        # print(itens)
    elif req[0] == 'DELETE':
        deleted = req[1][1:]
        print(itens)
        print('DELETED = ' + deleted)
        itens.remove(deleted)
        tabela = []
        for item in itens:
            if item:
                tabela.append(item)
        print(tabela)
        contents = pageTemplate.format(**locals())
        resp = ('HTTP/1.1 200 Ok\r\n' + 'Content-Type: text/html\r\n' + 'Content-Length: ' + str(
            len(contents)) + '\r\n\r\n' + contents)
    return resp


while True:
    client_connection, client_address = s.accept()
    request = client_connection.recv(1024).decode()
    # print(request)
    response = request_handler(request)
    print(response)
    client_connection.sendall(response.encode())
    client_connection.close()

s.close()

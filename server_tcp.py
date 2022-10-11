from cmath import log
import json
import socket
import sys

# INÍCIO - MÉTODOS PRIVADOS SERVIDOR
aguardando_jogador = 0 # 0 false 1 True
aguardando_jogador_1 = 0
board = None


def verificar_tabuleiro(i, j, jogador, board):
    if verificar_linha(i, jogador_atual=jogador, board=board):
        return True
    if verificar_coluna(j, jogador_atual=jogador, board=board):
        return True
    if verificar_diagonal(jogador, board=board):
        return True

    return False

def verificar_linha(i, jogador_atual, board):
    b = 0;
    count = 0
    total = 14
    while b <= total:
        if board[i][b] == jogador_atual:
            count += 1
            if count == 5:
                return True
        else:
            count = 0
        b += 1

    return False

def verificar_coluna(j, jogador_atual, board):
    b = 0;
    count = 0
    total = 14
    while b <= total:
        if board[b][j] == jogador_atual:
            count += 1
            if count == 5:
                return True
        else:
            count = 0
        b += 1
    return False

def verificar_diagonal(jogador, board):
    max_col = len(board[0])
    max_row = len(board)
    fdiag = [[] for _ in range(max_row + max_col - 1)]
    bdiag = [[] for _ in range(len(fdiag))]
    min_bdiag = -max_row + 1

    for x in range(max_col):
        for y in range(max_row):
            fdiag[x + y].append(board[y][x])
            bdiag[x - y - min_bdiag].append(board[y][x])

    count = 0
    for vetor in bdiag:
        for item in vetor:
            if item == jogador:
                count += 1
                if count == 5:
                    return True
            else:
                count = 0

    for vetor in fdiag:
        for item in vetor:
            if item == jogador:
                count += 1
                if count == 5:
                    return True
            else:
                count = 0

    return False

# FIM - MÉTODOS PRIVADOS SERVIDOR

# INÍCIO - LÓGICA TCP SERVIDOR

if (len(sys.argv) != 2):
    print('%s <porta>' % (sys.argv[0]))
    sys.exit(0)

ip = '127.0.0.1' #localhost
porta = int(sys.argv[1])
nr_clientes = 0
id_clientes = []

soquete = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soquete.bind((ip, porta))
soquete.listen()

while True:
    s, cliente = soquete.accept()
    dados_recv = s.recv(1024)
    dados_recv = json.loads(dados_recv.decode())
    clientId = dados_recv.get("clientId")


    aguardando_message = dados_recv.get("message", None)

    if aguardando_message != None:
        dados = json.dumps({"board": board})
        dados = dados.encode()
        s.send(dados)


    if not clientId in id_clientes:
        nr_clientes+=1
        id_clientes.append(clientId)
        print(f"Cliente {clientId} conectado.")
        print("Clientes conectados:", nr_clientes)
        dados = json.dumps({"nro_jogador": nr_clientes})

    if nr_clientes <= 2:
        if nr_clientes >= 1:
            if dados_recv.get("message") == None:
                print(dados_recv)
                i = dados_recv.get("i")
                j = dados_recv.get("j")
                board = dados_recv.get("board")
                jogador = dados_recv.get("jogador")

                if (i != None):
                    if verificar_tabuleiro(i, j, jogador, board=board):
                        dados = json.dumps({"i": i, "j": j,  "response": True})
                    else:
                        dados = json.dumps({"i": i, "j": j, "response": False, "board": board, "jogador": jogador})

                if jogador == 1:
                    aguardando_jogador_2 = 1
                    aguardando_jogador_1 = 0
                else:
                    aguardando_jogador_2 = 0
                    aguardando_jogador_1 = 1

            elif dados_recv.get("message") == "leaving":
                nr_clientes-=1
                print(f'Cliente {clientId} desconectado.')
                print("Clientes conectados:", nr_clientes)
        else:
            if dados_recv.get("message") == "leaving":
                nr_clientes-=1
                print(f'Cliente {clientId} desconectado.')
                print("Clientes conectados:", nr_clientes)

        s.send(dados.encode())
        s.close()
    else:
        print('Número máximo de jogadores atingido para este servidor.')
        break

# FIM - LÓGICA TCP SERVIDOR
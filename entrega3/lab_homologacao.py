import socket
import threading
import time

ESCOPO_AUTORIZADO = {
    "alvo": "127.0.0.1",
    "ambiente": "Homologacao Local (Laboratorio UNIT)",
    "portas_simuladas": [2222, 5432, 8080, 9090],
    "responsavel": "Thiago"
}

BANNERS = {
    2222: b"SSH-2.0-OpenSSH_9.5\r\n",
    5432: b"PostgreSQL 15.4 Homologacao\r\n",
    8080: b"HTTP/1.1 200 OK\r\nServer: Werkzeug/3.0.1 Python/3.12\r\nContent-Length: 18\r\n\r\nHomologacao Portal",
    9090: b"HTTP/1.1 200 OK\r\nServer: DebugAdminPanel/1.0\r\nContent-Length: 16\r\n\r\nAdmin Debug Mode"
}

servidor_ativo = True


def tratar_conexao(conn, porta):
    try:
        conn.settimeout(2.0)
        try:
            conn.recv(1024)
        except socket.timeout:
            pass
        conn.sendall(BANNERS[porta])
    except OSError:
        pass
    finally:
        conn.close()


def iniciar_servico(porta):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1.0)
    sock.bind(("127.0.0.1", porta))
    sock.listen(5)

    while servidor_ativo:
        try:
            conn, _ = sock.accept()
            t = threading.Thread(target=tratar_conexao, args=(conn, porta), daemon=True)
            t.start()
        except socket.timeout:
            continue
        except OSError:
            break
    sock.close()


def main():
    global servidor_ativo
    print("=== LABORATORIO DE HOMOLOGACAO - ENTREGA 3 ===")
    print(f"Alvo Autorizado : {ESCOPO_AUTORIZADO['alvo']}")
    print(f"Ambiente        : {ESCOPO_AUTORIZADO['ambiente']}")
    print(f"Portas Ativas   : {ESCOPO_AUTORIZADO['portas_simuladas']}")
    print("\nSubindo servicos simulados em 127.0.0.1...")

    threads = []
    for porta in ESCOPO_AUTORIZADO["portas_simuladas"]:
        t = threading.Thread(target=iniciar_servico, args=(porta,), daemon=True)
        t.start()
        threads.append(t)

    print("[ATIVO] Servicos aguardando varredura Nmap.")
    print("Abra outro terminal (PowerShell) e execute:")
    print("nmap -sV -sC -p 2222,5432,8080,9090 127.0.0.1")
    print("\nPressione Ctrl+C para encerrar o laboratorio.\n")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nEncerrando servicos do laboratorio...")
        servidor_ativo = False
        for t in threads:
            t.join(timeout=2.0)
        print("Laboratorio encerrado com seguranca.")


if __name__ == "__main__":
    main()
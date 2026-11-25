# Entrega 3 — Varredura de Portas e Serviços com Nmap

**Vídeo de Demonstração:** [https://drive.google.com/file/d/1AvZvcucM75BBpHbA08Z5Diqf9JLe5TBR/view?usp=drivesdk]

## 1. Requisitos Atendidos
- Montagem de laboratório local controlado (`lab_homologacao.py`) simulando serviços expostos em ambiente de homologação.
- Registro de autorização e escopo isolado (`127.0.0.1` — portas TCP `2222`, `5432`, `8080` e `9090`).
- Descoberta controlada de portas, protocolos e serviços utilizando **Nmap** (`-sV -sC`).
- Comparação entre necessidade operacional e exposição com matriz de riscos e recomendações.
- Análise de endurecimento (*hardening*) de **SSH** e plano de redução da superfície de ataque.

## 2. Escopo e Matriz de Riscos

- **Alvo Autorizado:** `127.0.0.1` (interface *loopback* local — Windows)
- **Portas Avaliadas:** `2222`, `5432`, `8080`, `9090` (TCP)
- **Comando Executado:** `nmap -sV -sC -p 2222,5432,8080,9090 127.0.0.1`

| Porta | Protocolo | Serviço / Versão | Necessidade vs. Exposição | Risco | Recomendação Técnica |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **2222** | TCP | SSH (`OpenSSH 9.5`) | Necessário para administração remota, porém exposto sem restrição de origem. | **Médio** | Restringir por firewall a IPs administrativos/VPN; exigir chaves Ed25519 e desativar login `root` e por senha. |
| **5432** | TCP | PostgreSQL `15.4` | Necessário apenas localmente para a aplicação; exposição externa é indevida. | **Alto** | Vincular o banco apenas a `127.0.0.1` (`listen_addresses = 'localhost'`) e bloquear a porta no firewall. |
| **8080** | TCP | HTTP (`Werkzeug 3.0.1`) | Necessário para testes web, mas trafega sem criptografia (TLS) e expõe banner de desenvolvimento. | **Médio** | Encapsular atrás de proxy reverso (Nginx) com HTTPS/TLS, suprimir banner `Server` e restringir à VPN. |
| **9090** | TCP | HTTP (`DebugAdminPanel 1.0`) | Desnecessário em exposição de rede; interface administrativa de depuração. | **Crítico** | Desativar o painel imediatamente ou vincular exclusivamente a `127.0.0.1` com acesso via túnel SSH. |

## 3. SSH e Redução da Superfície de Ataque
1. **Autenticação por Chaves Assimétricas:** Desabilitar login por senha (`PasswordAuthentication no`) e exigir chaves **Ed25519** ou RSA-4096.
2. **Bloqueio de Login Root:** Configurar `PermitRootLogin no`, exigindo autenticação nominal auditável antes da elevação de privilégios.
3. **Bloqueio Padrão (*Default Deny*) e Isolamento:** Negar conexões de entrada no firewall por padrão, restringir o SSH a IPs administrativos/VPN (`AllowUsers` + Fail2Ban) e vincular serviços internos (`5432` e `9090`) exclusivamente a `127.0.0.1`.

## 4. Como Executar (Windows)

### Pré-requisitos
- **Python 3.10+** instalado no Windows (com *"Add Python to PATH"* marcado).
- **Nmap** instalado no Windows (`winget install Insecure.Nmap` ou via `nmap.org/download.html`).

### Passo a Passo no PowerShell ou Prompt de Comando (CMD)

1. Acesse a pasta da entrega:
```powershell
cd entrega3
```

2. Inicie o laboratório local (Terminal 1):
```powershell
python lab_homologacao.py
```

3. Em um segundo terminal (Terminal 2), execute a varredura com Nmap:
```powershell
nmap -sV -sC -p 2222,5432,8080,9090 127.0.0.1
```

4. Pressione **`Ctrl + C`** no Terminal 1 para encerrar o laboratório ao concluir.

## 5. Referências Consultadas
- **ABNT NBR ISO/IEC 27002:2022 (Controles de Segurança da Informação):** https://www.abntcatalogo.com.br/
- **Documentação Oficial do Nmap:** https://nmap.org/book/man.html
- **NIST Special Publication 800-115 (Information Security Testing and Assessment):** https://csrc.nist.gov/publications/detail/sp/800-115/final
- **Manual Oficial OpenSSH (`sshd_config`):** https://man.openbsd.org/sshd_config
- **OWASP Attack Surface Analysis Cheat Sheet:** https://cheatsheetseries.owasp.org/cheatsheets/Attack_Surface_Analysis_Cheat_Sheet.html
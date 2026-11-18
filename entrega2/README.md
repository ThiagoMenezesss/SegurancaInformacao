# Entrega 2 — Hash e Autenticação Segura

**Vídeo de Demonstração:** [https://drive.google.com/file/d/1oEr6m4xi2cKbgUxAhsXg0Vl5icmp-i8d/view?usp=drivesdk] 

## 1. Requisitos Atendidos
- Cadastro e autenticação de usuários com **Argon2id** (`argon2-cffi`).
- Geração automática de **Salt** criptográfico aleatório de 16 bytes por usuário.
- Armazenamento estruturado no formato **PHC** (algoritmo, versão, custo de memória, iterações, paralelismo, salt e hash).
- Verificação de senha utilizando comparação segura em tempo constante (`ph.verify()`).
- Demonstração automatizada e interativa de login válido, login inválido e inspeção do registro protegido.

## 2.Parâmetros Técnicos Adotados (OWASP)
- **Algoritmo:** `Argon2id`
- **Memória (`memory_cost`):** `65536 KiB` (64 MiB)
- **Iterações (`time_cost`):** `3`
- **Paralelismo (`parallelism`):** `4` threads
- **Tamanho do Salt (`salt_len`):** `16 bytes` (128 bits)
- **Tamanho do Hash (`hash_len`):** `32 bytes` (256 bits)

## 3. Por que SHA-256 isolado NÃO é adequado para senhas?
Embora o **SHA-256** seja uma função de hash criptográfica segura para verificação de integridade de arquivos e assinaturas digitais, seu uso isolado para armazenar senhas é considerado inseguro pelos seguintes motivos:
1. **Velocidade Extrema (Baixo Custo Computacional):** O SHA-256 foi projetado para ser rápido. GPUs modernas calculam bilhões de hashes SHA-256 por segundo, tornando ataques de força bruta e dicionário trivialmente rápidos.
2. **Ausência de Fator de Trabalho (*Work Factor*) e Dureza de Memória:** O SHA-256 não possui parâmetros configuráveis de custo de CPU ou memória para desacelerar o atacante. Algoritmos como o **Argon2id** exigem uma quantidade significativa de memória RAM e tempo por tentativa, inviabilizando o paralelismo massivo em placas de vídeo.
3. **Falta de *Salting* Nativo:** Usado de forma isolada, senhas iguais geram exatamente o mesmo digest SHA-256, permitindo que um atacante identifique usuários com senhas idênticas e utilize tabelas pré-computadas (*Rainbow Tables*) para reverter múltiplas credenciais simultaneamente.

## 4. Como Executar (Windows)

### Pré-requisitos
- **Python 3.10+** instalado no Windows (com a opção *"Add Python to PATH"* marcada na instalação).

### Passo a Passo no PowerShell ou Prompt de Comando (CMD)

1. Acesse a pasta da entrega:
```powershell
cd entrega2
```

2. Crie e ative o ambiente virtual:
```powershell
python -m venv venv
.\venv\Scripts\activate
```
*(Caso o PowerShell bloqueie a execução de scripts, utilize o Prompt de Comando `cmd` ou execute `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` antes de ativar).*

3. Instale a dependência necessária:
```powershell
pip install -r requirements.txt
```

4. Execute a aplicação:
```powershell
python auth_segura.py
```

5. No menu exibido, digite **`4`** e pressione **Enter** para executar a bateria automática de testes (cadastro com Argon2id, inspeção do salt/hash gerado, login válido e rejeição de senha incorreta).

> **Nota sobre a entrada de senha:** Para facilitar a visualização durante os testes e a demonstração em terminal CLI, a digitação da senha nas opções interativas (`1` e `2`) é exibida na tela via `input()`, enquanto o armazenamento em disco (`usuarios_db.json`) permanece estritamente protegido apenas pelo hash Argon2id e seu respectivo salt.

## 5. Referências Consultadas
- **OWASP Password Storage Cheat Sheet:** https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html
- **OWASP Application Security Verification Standard (ASVS):** https://owasp.org/www-project-application-security-verification-standard/
- **NIST Special Publication 800-63B (Digital Identity Guidelines):** https://pages.nist.gov/800-63-3/sp800-63b.html
- **Documentação Oficial `argon2-cffi`:** https://argon2-cffi.readthedocs.io/
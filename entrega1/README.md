## ENTREGA 1 - Criptografia Assimétrica e Confiança

**Vídeo de Demonstração (Execução no Terminal):** [https://drive.google.com/file/d/1u6cprpSZrARMJOev1UhysfllF5DUorv0/view?usp=drivesdk]

### 1. Problema e Objetivo
O objetivo deste projeto é simular o envio seguro de dados entre dois sistemas, usando criptografia híbrida para garantir que ninguém leia o conteúdo e assinatura digital para confirmar quem enviou.


### 2. Ambiente e Tecnologias
* **Linguagem:** Python 3 (Solução multiplataforma: compatível com Windows e Linux)
* **Biblioteca Criptográfica:** "cryptography" (Biblioteca oficial e auditada da comunidade Python)


### 3. Algoritmos e Justificativa Técnica
* **RSA-OAEP (2048 bits):** Usado para encapsular a chave simétrica com segurança (previne ataques de Padding Oracle).
* **AES-256-GCM:** Usado para cifrar a mensagem. O modo GCM garante sigilo e integridade ao mesmo tempo.
* **RSA-PSS:** Usado para a assinatura digital do pacote junto com SHA-256.


### 4. Sigilo (Confidencialidade) vs. Autenticidade
* **Sigilo (Confidencialidade):** Garante que apenas o destinatário autorizado (possuidor da chave privada correspondente) consiga ler o conteúdo da mensagem. A cifragem oculta o texto de terceiros.
* **Autenticidade:** Comprova a identidade do remetente e garante que a informação não foi alterada. É alcançada assinando o hash da mensagem com a chave privada do remetente.


### 5. Função dos Certificados Digitais e Infraestrutura de Chaves Públicas (PKI)
Para resolver o problema da distribuição de chaves públicas em ambientes não confiáveis (prevenindo ataques de Man-in-the-Middle):

* **Certificados Digitais (Padrão X.509):** Vinculam uma chave pública a uma identidade verificada (como o domínio de um site, CNPJ ou CPF).
* **Autoridade Certificadora (CA):** Entidade de confiança responsável por validar a identidade e assinar digitalmente o certificado.
* **PKI (Public Key Infrastructure):** Estrutura completa de hardware, software, políticas e CAs responsável pela emissão, distribuição, validação e revogação (listas CRL / protocolo OCSP) de certificados digitais.


### 6. Instalação e Execução

#### Requisitos
Instale a biblioteca oficial no terminal / prompt de comando: 
``` bash
pip install cryptography

```
### 7. Testes e Evidências de Execução

Ao executar a aplicação no terminal, a saída gerada confirma o sucesso da cifragem/assinatura e a detecção das falhas nos testes negativos:

```text
[1] Gerando chaves RSA...
-> OK: Chaves geradas!

[Mensagem Original]: 'Transacao bancaria confidencial: Enviar R$ 5.000,00 para Conta X.'

[2] Cifrando mensagem (RSA-OAEP + AES-256-GCM)...
-> Chave AES Encapsulada: 3b0c9de7a2885136adecaa2fe096f435...
-> Texto Cifrado: 3d9b3a9e2ee7e039326be4b6ca7a9580...

[3] Teste Positivo: Decifrando...
-> Sucesso: 'Transacao bancaria confidencial: Enviar R$ 5.000,00 para Conta X.'

[4] Teste Negativo: Tentando decifrar pacote alterado...
-> OK: Adulteracao detectada com sucesso! Erro: InvalidTag

[5] Gerando assinatura digital...
-> Assinatura: 6bf6786ea7ba6eab5d4e3d86edf1128b...

[6] Teste Positivo: Validando assinatura...
-> Assinatura valida? True

[7] Teste Negativo: Validando assinatura com mensagem alterada...
-> Assinatura alterada valida? False
-> OK: Alteracao detectada, assinatura recusada!
```

### 8. Riscos, Limitações e Melhorias
Gestão de Chaves: As chaves estão na memória RAM por ser um protótipo. Em produção, devem ser guardadas em cofres como AWS KMS ou HashiCorp Vault.

Algoritmos: Em novos projetos, vale migrar para curvas elípticas (Ed25519) pelo desempenho e tamanho menor de chave.

### 9. Mapeamento de Riscos e Controles
OWASP Top 10 (2025): A04 - Falhas Criptográficas

OWASP ASVS 5.0: Capítulo V11 - Criptografia (Requisito 11.4.1 L1)

ISO/IEC 27002:2022: Controle 8.24 - Uso de Criptografia

### 10. Referências Consultadas
OWASP Foundation. OWASP Top 10:2025 / ASVS 5.0.

ISO/IEC 27002:2022. Information security, cybersecurity and privacy protection — Information security controls.

Python Cryptography Authority (PyCA). Cryptography Documentation. https://cryptography.io/



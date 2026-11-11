import os
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

def gerar_chaves_rsa():
  
    chave_privada = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    chave_publica = chave_privada.public_key()
    return chave_privada, chave_publica

def cifrar_hibrido(chave_publica, mensagem_bytes):
   
    chave_simetrica = AESGCM.generate_key(bit_length=256)
    aesgcm = AESGCM(chave_simetrica)
    nonce = os.urandom(12)
    
    texto_cifrado = aesgcm.encrypt(nonce, mensagem_bytes, associated_data=None)

    chave_simetrica_encapsulada = chave_publica.encrypt(
        chave_simetrica,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    
    return {
        "chave_encapsulada": chave_simetrica_encapsulada,
        "nonce": nonce,
        "texto_cifrado": texto_cifrado
    }

def decifrar_hibrido(chave_privada, pacote_cifrado):

    chave_simetrica = chave_privada.decrypt(
        pacote_cifrado["chave_encapsulada"],
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    
    aesgcm = AESGCM(chave_simetrica)
    mensagem_decifrada = aesgcm.decrypt(
        pacote_cifrado["nonce"],
        pacote_cifrado["texto_cifrado"],
        associated_data=None
    )
    return mensagem_decifrada

def assinar_mensagem(chave_privada, mensagem_bytes):
    # Assinatura digital RSA-PSS com SHA256
    assinatura = chave_privada.sign(
        mensagem_bytes,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return assinatura

def verificar_assinatura(chave_publica, mensagem_bytes, assinatura):
    try:
        chave_publica.verify(
            assinatura,
            mensagem_bytes,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except Exception:
        return False

if __name__ == "__main__":
    print("==================================================================")
    print("  ENTREGA 1 - CRIPTOGRAFIA ASSIMETRICA E CONFIANCA")
    print("==================================================================\n")

    print("[1] Gerando chaves RSA...")
    priv_key, pub_key = gerar_chaves_rsa()
    print("-> OK: Chaves geradas!\n")

    mensagem_original = "Transacao bancaria confidencial: Enviar R$ 5.000,00 para Conta X."
    bytes_msg = mensagem_original.encode('utf-8')
    print(f"[Mensagem Original]: '{mensagem_original}'\n")

    print("[2] Cifrando mensagem (RSA-OAEP + AES-256-GCM)...")
    pacote = cifrar_hibrido(pub_key, bytes_msg)
    print(f"-> Chave AES Encapsulada: {pacote['chave_encapsulada'][:16].hex()}...")
    print(f"-> Texto Cifrado: {pacote['texto_cifrado'][:16].hex()}...\n")

    print("[3] Teste Positivo: Decifrando...")
    msg_decifrada = decifrar_hibrido(priv_key, pacote).decode('utf-8')
    print(f"-> Sucesso: '{msg_decifrada}'\n")

    print("[4] Teste Negativo: Tentando decifrar pacote alterado...")
    pacote_adulterado = {
        "chave_encapsulada": pacote["chave_encapsulada"],
        "nonce": pacote["nonce"],
        "texto_cifrado": pacote["texto_cifrado"][:-1] + b'\x00'
    }
    try:
        decifrar_hibrido(priv_key, pacote_adulterado)
        print("-> ERRO: Adulteracao nao detectada!")
    except Exception as e:
        print(f"-> OK: Adulteracao detectada com sucesso! Erro: {type(e).__name__}\n")

    print("[5] Gerando assinatura digital...")
    assinatura = assinar_mensagem(priv_key, bytes_msg)
    print(f"-> Assinatura: {assinatura[:16].hex()}...\n")

    print("[6] Teste Positivo: Validando assinatura...")
    valido = verificar_assinatura(pub_key, bytes_msg, assinatura)
    print(f"-> Assinatura valida? {valido}\n")

    print("[7] Teste Negativo: Validando assinatura com mensagem alterada...")
    msg_adulterada_bytes = "Transacao bancaria confidencial: Enviar R$ 50.000,00 para Conta X.".encode('utf-8')
    valido_adulterado = verificar_assinatura(pub_key, msg_adulterada_bytes, assinatura)
    print(f"-> Assinatura alterada valida? {valido_adulterado}")
    if not valido_adulterado:
        print("-> OK: Alteracao detectada, assinatura recusada!")
    
    print("\n==================================================================")
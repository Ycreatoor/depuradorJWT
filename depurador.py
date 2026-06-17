import base64
import json
import os

def decodificar_base64url(base64_url):
    """Corrige o padding do Base64Url e decodifica para dicionário JSON."""
    base64_url = base64_url.strip()
    padding = len(base64_url) % 4
    if padding:
        base64_url += '=' * (4 - padding)
    dados_bytes = base64.urlsafe_b64decode(base64_url)
    return json.loads(dados_bytes.decode('utf-8'))

def depurar_jwt(token):
    """Separa e decodifica as partes do JWT com validações extras."""
    try:
        token = token.strip()
        partes = token.split('.')
        if len(partes) != 3:
            return {"Erro": f"Formato JWT inválido. O token deve ter 3 partes, mas encontramos {len(partes)}."}
        
        header_b64 = partes[0]
        payload_b64 = partes[1]
        
        resultado = {}
        
        # Decodifica o Header
        if header_b64:
            resultado["Header (Cabeçalho)"] = decodificar_base64url(header_b64)
        else:
            resultado["Header (Cabeçalho)"] = "⚠️ Parte ausente no token"
            
        # Decodifica o Payload
        if payload_b64:
            payload_b64 = payload_b64.replace(" ", "")
            resultado["Payload (Carga Útil)"] = decodificar_base64url(payload_b64)
        else:
            resultado["Payload (Carga Útil)"] = "⚠️ Alerta: O Payload deste token está VAZIO (ausente)."
            
        return resultado
        
    except Exception as e:
        return {"Erro": f"Falha crítica ao decodificar: {str(e)}"}

def limpar_tela():
    """Limpa o terminal para a próxima consulta."""
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    while True:
        limpar_tela()
        print("\n" + "="*40)
        print("           DEPURADOR JWT CLI            ")
        print("="*40)
        
        token = input("Cole o seu token JWT aqui e aperte Enter:\n> ")
        
        if token.strip():
            resultado = depurar_jwt(token)
            
            print("\n" + "="*40)
            print("       RESULTADO DA DEPURAÇÃO JWT       ")
            print("="*40)
            print(json.dumps(resultado, indent=4, ensure_ascii=False))
            print("="*40 + "\n")
        else:
            print("❌ Nenhum token inserido.")

        # Pergunta se quer continuar
        continuar = input("\nDeseja fazer outra consulta? (S/N): ").strip().upper()
        if continuar != 'S':
            break  # Sai do loop infinito

    # Trava final antes de fechar a janela
    print("\nEncerrando o depurador...")
    input("Pressione Enter para sair...")

if __name__ == "__main__":
    main()
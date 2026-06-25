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
    """Limpa o terminal."""
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    # Inicializa o estilo Matrix no terminal do Windows (Fundo Preto '0', Letras Verdes 'a')
    if os.name == 'nt':
        os.system('color 0a')
        
    # Limpa o terminal uma única vez na inicialização para começar o histórico do zero
    limpar_tela()
    
    print("\n" + "="*45)
    print("         SYSTEM DEPURADOR JWT - Ycreatoor        ")
    print("="*45)
        
    while True:
        token = input("\nCole a sequência do token JWT e aperte Enter:\n> ")
        
        if token.strip():
            resultado = depurar_jwt(token)
            
            print("\n" + "="*45)
            print("          SISTEMA DE LEITURA COMPLETO        ")
            print("="*45)
            print(json.dumps(resultado, indent=4, ensure_ascii=False))
            print("="*45 + "\n")
        else:
            print("❌ Nenhuma sequência detectada.")

        # Pergunta se quer continuar (sem limpar a tela atual)
        continuar = input("Deseja decodificar outra sequência? (S/N): ").strip().upper()
        if continuar != 'S':
            break  # Quebra o loop principal e vai para a finalização
            
        print("\n" + "-"*45)
        print("          PRÓXIMA CONSULTA DO HISTÓRICO        ")
        print("-"*45)

    # Limpa todos os tokens exibidos da tela antes de fechar por segurança
    limpar_tela()
    print("\nDesconectando da Matrix... Dados limpos com sucesso.")
    input("Pressione Enter para fechar o terminal...")

if __name__ == "__main__":
    main()
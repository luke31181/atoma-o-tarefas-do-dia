import os
import shutil
from datetime import datetime
import requests
from plyer import notification

# ------------------------------------------------------------
# 1. organizador e renomeador da pasta downloads
# ------------------------------------------------------------

def organizar_e_renomear_downloads():
    # caminho da pasta downloads do meu windows 
    caminho_downloads = os.path.expanduser('~/DownLoads')

    # Mapeamento de pastas por extensao 
    extensoes_pastas = {

        'Imagens': ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg', 'psd'],
        'videos': ['.mp4', '.mov', '.avi', '.mkv', '.flv', '.wmv'],
        'Audios': ['.mp3', '.wav', '.flac', '.aac', '.ogg'],
        'Documentos': ['.pdf', '.docx', '.txt', '.xlsx', '.csv', ".pptx", '.web', '.html', '.css'],
        'Instaladores': ['.exe', 'msi'],
        'Compactados': ['.zip', '.rar', '.7z']
    }

    data_hoje = datetime.now().strftime("%y-%m-%d")     
    arquivos_movidos = 0

    for arquivo in os.listdir(caminho_downloads):
        caminho_completo = os.path.join(caminho_downloads, arquivo)

        # Ignorar se for uma pasta
        if os.path.isdir(caminho_completo):
            continue

        nome, extensao_arquivo = os.path.splitext(arquivo)
        extensao_arquivo = extensao_arquivo.lower()

        #descobrir a pasta de destino
        pasta_destino = None
        for pasta, lista_extensao in extensoes_pastas.items():
            if extensao_arquivo in lista_extensao:
                pasta_destino = pasta
                break

        # se encontrou uma cadegoria valida
        if pasta_destino:
            caminho_destino_pasta = os.path.join(caminho_downloads, pasta_destino)
            os.makedirs(caminho_destino_pasta, exist_ok=True)

            # renomear arquivo addicionado a data de hoje se ainda não tiver
            novo_nome = arquivo
            if not nome.startswith(data_hoje):
                novo_nome = f'{data_hoje}_{arquivo}'

            caminho_destino_final = os.path.join(caminho_destino_pasta, novo_nome)

            #mover e renomear 
            shutil.move(caminho_completo, caminho_destino_final)
            arquivos_movidos += 1

            
    return arquivos_movidos

# ------------------------------------------------------------
# Web scraping: Buscar cotacoes do dolar
# ------------------------------------------------------------

def obter_cotacao_dolar():
    try:
        url = 'https://economia.awesomeapi.com.br/Last/USD-BRL'
        resposta = requests.get(url, timeout=5)
        dados = resposta.json()
        cotacao = float(dados['USDBRL']['bid'])

        # salvar relatorio em arquivo txt
        caminho_relatorio = os.path.expanduser('~/DownLoads/relatorio_cotacao.txt')
        with open(caminho_relatorio, 'a', encoding='utf-8') as arquivo:
            arquivo.write(f'A cotação do dólar em [{datetime.now().strftime("%y-%m-%d %H:%M")}] é: R$ {cotacao}')

        return f'cotação do dólar: R$ {cotacao:.2f}'
    except Exception as e:
        return 'indisponível'

# ------------------------------------------------------------
# notificação na tela
# ------------------------------------------------------------

def enviar_notificacao(total_arquivos, cotacao):

    if isinstance(cotacao, (int, float)):
        cotacao_formatada = f'R${cotacao:.2f}'
    else:
        cotacao_formatada = cotacao
    notification.notify(
        title= 'Automação concluído',
        message = f"{total_arquivos} arquivos organizados em downloads. \nCotação do dólar: R$ {cotacao_formatada}",
        app_name='Central Python',
        timeout=10
    )

# ------------------------------------------------------------
# executando automação
# ------------------------------------------------------------
if __name__ == "__main__":
    print('executando automação...')

    total = organizar_e_renomear_downloads()
    cotacao = obter_cotacao_dolar()
    enviar_notificacao(total, cotacao)

    print('Processo concluído com sucesso!')

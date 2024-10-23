from telethon import TelegramClient,sync,events
from time import sleep
import requests
from senhas import api_hash,api_id
import asyncio
from telethon.tl.types import MessageEntityTextUrl

sessao = 'Repassar Mensagem'

async def enviar_mensagem(client, event):
    destinos = [-1002150341373, -1002158564635, -1001989422050, -1002219750316,
        -1002227444305, -1002355680111, -1002425763410, -1002221610832,
        -1002309650852, -1002480613056, -1002207091923, -1002268389774,
        -1002154184872, -1002481709435, -1002393885001, -1002152467453,
        -1002210146747, -1002167843303, -1002190499684, -1002294147510,
        -1002277522695]  # IDs de destino

    # Captura a mensagem original
    mensagem_original = event.message.message
    print(f"Mensagem original para envio: {mensagem_original}")  # Debug: Imprime a mensagem original

    # Inicializa a mensagem formatada como a mensagem original
    formatted_message = mensagem_original
    
    # Verifica se a mensagem contém links formatados
    if event.message.entities:
        for entity in event.message.entities:
            if isinstance(entity, MessageEntityTextUrl):
                print("A mensagem contém um link formatado.")
                # Obtem o link e o texto
                link_text = mensagem_original[entity.offset:entity.offset + entity.length]
                url = entity.url
                formatted_message = formatted_message.replace(link_text, f'<a href="{url}">{link_text}</a>')
    
    for destino in destinos:
        try:
            # Tenta obter a entidade
            entity = await client.get_input_entity(destino)
            print(f"Enviando para: {destino}")  # Debug: Mostra o destino

            if event.media:
                # Envia a mídia com a legenda original
                await client.send_file(entity, file=event.media, caption=mensagem_original, parse_mode="html")
            else:
                # Envia a mensagem formatada, caso tenha links
                await client.send_message(entity, formatted_message, parse_mode="html")
            
            print(f"Mensagem enviada para {destino} com sucesso!")  # Debug: Mensagem enviada
            await asyncio.sleep(5)  # Delay de 5 segundos
        except Exception as e:
            print(f"Erro ao enviar para {destino}: {e}")  # Mostra erros

def main():
    print('Monitoramento Iniciado...')
    client = TelegramClient(sessao, api_id, api_hash)
    
    @client.on(events.NewMessage(chats=[1002437160561]))
    async def handler(event):
        await enviar_mensagem(client, event)  # Passando o client como argumento
    
    client.start()
    client.run_until_disconnected()

main()


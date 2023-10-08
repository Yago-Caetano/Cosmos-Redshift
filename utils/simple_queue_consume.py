import pika

# Conexão com o servidor RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Nome da fila que você deseja consumir
queue_name = '4971bc52-d144-4411-b89d-d02f02d81c0c'

# Declaração da fila (caso ainda não exista)
channel.queue_declare(queue=queue_name)

# Função de callback que será chamada quando uma mensagem for recebida
def callback(ch, method, properties, body):
    print(f"Recebido: {body}")

    with open('queue_out.txt', 'w') as arquivo:
        # Escreva conteúdo no arquivo
        arquivo.write(body.decode('utf-8'))


# Configura a função de callback para consumir mensagens da fila
channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

print(f"Esperando por mensagens. Para sair, pressione Ctrl+C")

# Começa a consumir mensagens indefinidamente
channel.start_consuming()
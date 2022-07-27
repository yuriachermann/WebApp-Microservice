import json

import pika

from main import Tool, db

params = pika.URLParameters('amqps://pmziknme:f3cWxF4lPVoxG6UBBbEPHlySIXvZWMGN@cow.rmq2.cloudamqp.com/pmziknme')

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='microservice')


def callback(ch, method, properties, body):
    print('Received in microservice')
    data = json.loads(body)
    print(data)
    print(properties.content_type)
    print(method)

    if properties.content_type == 'tool_created':
        print('Tool Created')
        tool = Tool(id=data['id'], title=data['title'], tool_num=data['tool_num'], raw_image=data['image'])
        db.session.add(tool)
        db.session.commit()

    elif properties.content_type == 'tool_updated':
        print('Tool Updated')
        tool = Tool.query.get(data['id'])
        tool.title = data['title']
        tool.tool_num = data['tool_num']
        tool.raw_image = data['image']
        db.session.commit()

    elif properties.content_type == 'tool_deleted':
        print('Tool Deleted')
        tool = Tool.query.get(data)
        db.session.delete(tool)
        db.session.commit()


channel.basic_consume(queue='microservice', on_message_callback=callback, auto_ack=True)

print('Started Consuming')

channel.start_consuming()

channel.close()

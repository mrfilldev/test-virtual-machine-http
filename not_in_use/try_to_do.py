import json
from types import SimpleNamespace
import re

string = b'{"CarWashId":"2","BoxNumber":"3","Id":"8a0672687d0646ae866885521025375f","ContractId":"individual","Sum":3500.0,"Status":"OrderCreated","DateCreate":"2023-02-22T12:41:03.026Z","SumCompleted":3500.0,"SumPaidStationCompleted":3416.42,"Services":[{"Id":"6","Description":"\xd0\x9a\xd0\xbe\xd0\xbc\xd0\xbf\xd0\xbb\xd0\xb5\xd0\xba\xd1\x81 ALL IN","Cost":3500.0}]}'
string2 = b'{"id":"295852f47c6440d0ac5461045bb9b47f","status":"UserCanceled"}'


def to_camel_case(request):
    # print('request.data: ', type(request.data), request.data)
    # data = json.loads(request.data.decode('utf-8'))  # bytes object -> dict
    data = json.loads(request.decode('utf-8'))  # bytes object -> dict
    print('data: ', type(data), data, '\n')
    #data = str(data)
    print('data: ', type(data), data, '\n')
    print('Magic?')
    #data = re.sub(r'_(\w)', lambda x: x.group(1).title(), data)
    data = {k.title(): v for k, v in data.items()}

    print('data: ', type(data), data, '\n')
    # data = eval(data)
    print('data: ', type(data), data, '\n')
    data = json.dumps(data, default=lambda x: x.__dict__)
    print('data: ', type(data), data, '\n')
    data = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
    print('data: ', type(data), data, '\n')
    return data


order = to_camel_case(string2)
print(
    type(order),
    order,

)
print(order.Status)

"""import json

import boto3
import os

order = {
    "CarWashId": "term_76",
    "BoxNumber": "1",
    "Id": "aca65d7573c24e9abf1bfb23e48fdf3d",
    "ContractId": "Corporation",
    "Sum": 600.0,
    "Status": "OrderCreated",
    "DateCreate": "2023-02-09T17:20:17.95Z",
    "SumCompleted": 600.0,
    "SumPaidStationCompleted": 540.0,
    "Services": [
        {
            "Id": "287",
            "Description": "____",
            "Cost": 600.0
        }
    ]
}
order = json.dumps(order, default=lambda x: x.__dict__)


def main():
    # Create client
    client = boto3.client(
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
        service_name='sqs',
        endpoint_url='https://message-queue.api.cloud.yandex.net',
        region_name='ru-central1'
    )

    # Create queue and get its url
    queue_url = client.create_queue(QueueName='mq_example_boto3').get('QueueUrl')
    print('Created queue url is "{}"'.format(queue_url))

    # Send message to queue
    print(client.send_message(
        QueueUrl=queue_url,
        MessageBody=order
    ))

    print('Successfully sent test message to queue')

    # Receive sent message
    messages = client.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=10,
        VisibilityTimeout=60,
        WaitTimeSeconds=20
    ).get('Messages')
    for msg in messages:
        print('Received message: "{}"'.format(msg.get('Body')))

    # Delete processed messages
    for msg in messages:
        client.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=msg.get('ReceiptHandle')
        )
        print('Successfully deleted message by receipt handle "{}"'.format(msg.get('ReceiptHandle')))

    # Delete queue
    client.delete_queue(QueueUrl=queue_url)
    print('Successfully deleted queue')


if __name__ == '__main__':
    main()
"""

urls = ['/FUZZ']

async def app(scope, receive, send):
    body = await read_body(receive)
    print(f"data: {body.decode('utf-8')}")
    
    assert scope['type'] == 'http'
    await send({
        'type': 'http.response.start',
        'status': 200 if scope['path'] in urls else 404,
        'headers': [
            [b'content-type', b'text/plain'],
        ],
    })
    await send({
        'type': 'http.response.body',
        'body': b'Hello, world!',
    })
    


async def read_body(receive):
    body = b''
    more_body = True

    while more_body:
        message = await receive()
        body += message.get('body', b'')
        more_body = message.get('more_body', False)

    return body
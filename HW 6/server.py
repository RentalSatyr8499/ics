# This creates a very basic uvicorn server that will respond with a 200(OK) to
# a small set of URLs, and 404 (not found) to anything else.  It is modified
# from the example code from https://www.uvicorn.org/.
#
# Run as:
# uvicorn server:app --reload --port 5000

# The URLs to respond with a 200 to
urls = [ '/employers', '/.gitignore', '/~admin', '/alerts.html' ]


async def app(scope, receive, send):
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

    print(f"HTTP method: {scope['method']}")
    print(f"headers: {scope['headers']}")
    body = await read_body(receive)
    print(f"data: {body}")


async def read_body(receive):
    """
    Read and return the entire body from an incoming ASGI message.
    """
    body = b''
    more_body = True

    while more_body:
        message = await receive()
        body += message.get('body', b'')
        more_body = message.get('more_body', False)

    return body

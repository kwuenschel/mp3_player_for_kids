import mp3
import uasyncio as asyncio
import ure


def parse_url(url):
    #PARSE THE URL AND RETURN THE PATH AND GET PARAMETERS
    parameters = {}
    path = ure.search("(.*?)(\?|$)", url)
    while True:
        vars = ure.search("(([a-z0-9]+)=([a-z0-9.]*))&?", url)
        if vars:
            parameters[vars.group(2)] = vars.group(3)
            url = url.replace(vars.group(0), '')
        else:
            break

    return path.group(1), parameters


def handle_request(reader, writer):
    request = yield from reader.read()
    method, url, *_ = request.decode('utf-8').split(' ')

    path, parameters = parse_url(url)
    if path.startswith("/folder"):
        folder = parameters.get("folder", 1)
        mp3.play_folder(int(folder))
    elif path.startswith("/play"):
        track = parameters.get("track", 1)
        mp3.play_track(int(track))
    elif path.startswith("/next"):
        mp3.next()
    elif path.startswith("/prev"):
        mp3.previous()
    elif path.startswith("/resume"):
        mp3.resume()
    elif path.startswith("/pause"):
        mp3.pause()

    yield from writer.awrite(
        'HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n'
    )
    with open('index.html') as f:
        for line in f:
            yield from writer.awrite(line)

    yield from writer.aclose()


def create_server():
    loop = asyncio.get_event_loop()
    loop.call_soon(
        asyncio.start_server(
            handle_request,
            '0.0.0.0',
            80,
            backlog=100,
        )
    )

import micropython
import mp3
import readerplayer
import uasyncio as asyncio
import webplayer


def main():
    mp3.set_volume(15)
    loop = asyncio.get_event_loop()
    webplayer.create_server()

    reader_player = readerplayer.ReaderPlayer()
    loop.create_task(reader_player.run())
    loop.run_forever()


if __name__ == '__main__':
    micropython.kbd_intr(-1)
    main()

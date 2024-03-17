#!/usr/bin/env python3
import asyncio
import shlex

clients = {}

async def chat(reader, writer):
    me = "{}:{}".format(*writer.get_extra_info('peername'))
    print(me)
    clients[me] = asyncio.Queue()
    send = asyncio.create_task(reader.readline())
    receive = asyncio.create_task(clients[me].get())
    while not reader.at_eof():
        tasks = [send, receive]
        done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
        for task in done:
            if task is send:
                input_line = task.result().decode().strip()
                args = shlex.split(input_line)
                match args:
                    case ['who']:
                        pass
                    case ['cows']:
                        pass
                    case ['login', name]:
                        pass
                    case ['say', name, text]:
                        pass
                    case ['yield', text]:
                        pass
                    case ['quit']:
                        pass
                    case _:
                        writer.write('Invalid command!\n'.encode())
                        await writer.drain()
                send = asyncio.create_task(reader.readline())
            elif task is receive:
                receive = asyncio.create_task(clients[me].get())
                writer.write(f"{task.result()}\n".encode())
                await writer.drain()
    send.cancel()
    receive.cancel()
    print(me, "DONE")
    del clients[me]
    writer.close()
    await writer.wait_closed()

async def main():
    server = await asyncio.start_server(chat, '0.0.0.0', 1337)
    async with server:
        await server.serve_forever()

asyncio.run(main())

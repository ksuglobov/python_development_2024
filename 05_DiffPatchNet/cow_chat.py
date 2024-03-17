#!/usr/bin/env python3
import asyncio
import shlex
import cowsay

clients = {}

async def process_login(me, name):
    if me is None:
        if name not in cowsay.list_cows():
            return False, 'The name should be a cow\'s name!'
        if name in clients:
            return False, 'This name is already taken!'
        clients[name] = asyncio.Queue()
        return True, 'Successfully logged in!'
    return False, f'You are already logged in under the name {me}!'

async def chat(reader, writer):
    peername = '{}:{}'.format(*writer.get_extra_info('peername'))
    print(f'{peername} has joined the server')
    me = None

    send = asyncio.create_task(reader.readline())
    receive = None

    while not reader.at_eof():
        tasks = [send, receive] if receive else [send]
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
                        login_status, response = await process_login(me, name)
                        if login_status:
                            me = name
                            receive = asyncio.create_task(clients[me].get())
                            print(f'{peername} has logged in as {me}')
                        writer.write(f'{response}\n'.encode())
                        await writer.drain()
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
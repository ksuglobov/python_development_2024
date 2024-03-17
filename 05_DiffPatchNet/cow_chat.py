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

async def process_say(me, name, text):
    if me is None:
        return False, 'You need to log in to send a message!'
    if name not in clients:
        return False, f'There is no user with {name} username!'

    message_text = cowsay.cowsay(text, cow=me)
    await clients[name].put(f'\n[{me}]:\n{message_text}')
    return True, ''

async def process_yield(me, text):
    if me is None:
        return False, 'You need to log in to send a message!'

    for name in clients:
        if name != me:
            message_text = cowsay.cowsay(text, cow=me)
            await clients[name].put(f'\n[{me}] [to all]:\n{message_text}')
    return True, ''

async def chat(reader, writer):
    peername = '{}:{}'.format(*writer.get_extra_info('peername'))
    print(f'{peername} has joined the server')
    me = None

    writer.write(f'>>> '.encode())
    await writer.drain()
    send = asyncio.create_task(reader.readline())
    receive = None

    quit_flag = False
    while not reader.at_eof() and not quit_flag:
        tasks = [send, receive] if receive is not None else [send]
        done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
        for task in done:
            if task is send:
                send = asyncio.create_task(reader.readline())
                input_line = task.result().decode().strip()
                args = shlex.split(input_line)
                match args:
                    case ['who']:
                        if clients:
                            writer.write(f'Logged users:\n'.encode())
                            for i, client in enumerate(clients):
                                if me is not None and client == me:
                                    writer.write(f'{i + 1}*. {client} (you)\n'.encode())
                                else:
                                    writer.write(f'{i + 1}. {client}\n'.encode())
                        else:
                            writer.write(f'There are no logged users yet.\n'.encode())
                        await writer.drain()
                    case ['cows']:
                        available_names = set(cowsay.list_cows()) - set(clients)
                        if available_names:
                            writer.write(f'Available usernames:\n'.encode())
                            for i, name in enumerate(available_names):
                                writer.write(f'{i + 1}. {name}\n'.encode())
                        else:
                            writer.write(f'There are no available usernames!\n'.encode())
                        await writer.drain()
                    case ['login', name]:
                        login_status, response = await process_login(me, name)
                        if login_status:
                            me = name
                            receive = asyncio.create_task(clients[me].get())
                            print(f'{peername} has logged in as {me}')
                        writer.write(f'{response}\n'.encode())
                        await writer.drain()
                    case ['say', name, text]:
                        say_status, response = await process_say(me, name, text)
                        if not say_status:
                            writer.write(f'{response}\n'.encode())
                            await writer.drain()
                    case ['yield', text]:
                        yield_status, response = await process_yield(me, text)
                        if not yield_status:
                            writer.write(f'{response}\n'.encode())
                            await writer.drain()
                    case ['quit']:
                        writer.write('Quitting...\n'.encode())
                        await writer.drain()
                        quit_flag = True
                        break
                    case []:
                        pass
                    case _:
                        writer.write('Invalid command!\n'.encode())
                        await writer.drain()

                prompt = '>>> ' if me is None else f'[{me}] >>> '
                writer.write(prompt.encode())
                await writer.drain()
            elif task is receive:
                receive = asyncio.create_task(clients[me].get())
                writer.write(f'{task.result()}\n'.encode())
                await writer.drain()

    send.cancel()
    if receive is not None:
        receive.cancel()
    if me is not None:
        del clients[me]
    writer.write('You have been disconnected from the server. Good bye!\n'.encode())
    await writer.drain()
    writer.close()
    await writer.wait_closed()
    print(f'{peername} has left the server')

async def main():
    server = await asyncio.start_server(chat, '0.0.0.0', 1337)
    async with server:
        await server.serve_forever()

asyncio.run(main())

from pyrogram import Client, filters
from time import sleep
from random import choice

app = Client("my_account")
with app:
    for i in range(51):
        app.send_message('me', 'Замерить состояние', schedule_date=1635928200 + i * 60 * 15)

users = {}

class User():
    def __init__(self, name, id):
        self.id = id
        self.name = name
        self.last_messages = []


@app.on_message(filters.text & filters.me & filters.command("p", prefixes="/"))
def echo(client, message):
    text = message.text.split("/p")[1]
    for i in range(1, len(text)+1):
        if i != len(text): new_text = text[:i] + '|'
        else: new_text = text
        if i == 1 or text[i-2] != " ": sleep(0.2)
        else: sleep(0.7)
        message.edit_text(new_text)

@app.on_message(filters.text & filters.me & filters.command("r", prefixes="/"))
def random_emote(client, message):
    emjs = [chr(c) for c in range(0x1f300, 0x1f53e)] + [chr(c) for c in range(0x1f573, 0x1f57b)] + \
                            [chr(c) for c in range(0x1f595, 0x1f597)] + [chr(c) for c in range(0x1f5fa, 0x1f650)] + \
                            [chr(c) for c in range(0x1f680, 0x1f6c6)] + [chr(c) for c in range(0x1f6f3, 0x1f6fb)] + \
                            [chr(c) for c in range(0x1f7e0, 0x1f7eb)] + [chr(c) for c in range(0x1f90d, 0x1f946)] + \
                            [chr(c) for c in range(0x1f947, 0x1f972)] + [chr(c) for c in range(0x1f973, 0x1f976)] + \
                            [chr(c) for c in range(0x1f97a, 0x1f9a3)] + [chr(c) for c in range(0x1f9a5, 0x1f9ab)] + \
                            [chr(c) for c in range(0x1f9ae, 0x1f9cb)] + [chr(c) for c in range(0x1f9cd, 0x1fa00)] + \
                            [chr(0x1f6f0)] + [chr(0x26F8)] + [chr(0x1f590)]
    random_emjs = [choice(emjs) for i in range(50)]
    for i in range(7, len(random_emjs)+1):
        sleep(0.078)
        message.edit_text('...............' + chr(0x2B07) + '...............' + '\n' + (''.join(random_emjs[i-7:i])) + '\n' + '...................................')
    sleep(2.9)
    message.edit_text(random_emjs[-4])

    #for i in range(20):
        #sleep(0.1)
        #random_emj = choice(emjs)
        #message.edit_text(random_emj + random_emj)
    #message.edit_text(chr(0x2764) + chr(0x2764))
    #message.edit_text(chr(0x1F60D) + chr(0x1F60D))

@app.on_message(filters.private)
def message_saver(client, message):
    global users
    if message.from_user['id'] not in users:
        user = User(message.from_user['first_name'], message.from_user['id'])
        user.last_messages = list(map(lambda x: x.text if x.from_user['id'] == message.from_user['id'] else None, app.iter_history(message.from_user['id'], limit=20)))
        user.last_messages = list(reversed(list(filter(lambda a: a != None, user.last_messages))[:5]))
        if user.id != 998559096:
            users[user.id] = user
    else:
        users[message.from_user['id']].last_messages.append(message.text)
        users[message.from_user['id']].last_messages = users[message.from_user['id']].last_messages[1:]

@app.on_deleted_messages()
def deleted(client, messages):
    global users
    for user in users.values():
        last_msg = list(map(lambda x: x.text if x.from_user['id'] == user.id else None, app.iter_history(user.id, limit=20)))
        last_msg = list(reversed(list(filter(lambda a: a != None, last_msg))[:5]))
        if user.last_messages != last_msg:
            app.send_message('me', user.name + ' удалил сообщение! 😱 \n "' + ''.join(list(set(user.last_messages) - set(last_msg))) + '"')
            user.last_messages = last_msg

app.run()


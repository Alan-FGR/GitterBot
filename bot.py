

#CONFS
room_name = 'nem0/LumixEngine'
# room_name = 'gitterHQ/sandbox'
# room_name = 'AtomicGameEngine/AtomicGameEngine'


from gitterpy.client import GitterClient
from asteval.asteval import Interpreter
from json import loads

aeval = Interpreter()
gitter = GitterClient(open("token.txt").readline())
users = [x.rstrip() for x in open("users.txt").readlines()]
aeval("users = "+str(users))
last_message = ":trollface:"

# TESTING
# def say2(msg):
#     print(str(msg))
# while True:
#     message = {'text':input("> "),'fromUser':{"username":"Alan-FRG"}}
#     try:
#         text = message['text']
#         if "$LAST" in text:
#             text = text.replace("$LAT", "'"+last_message+"'")
#         last_message = text
#         user = message['fromUser']['username']
#         command = text.split(' ')[0]
#         if command == 'eval':
#             args = ' '.join(text.split(' ')[1:])
#             eval_result = aeval(args)
#             if eval_result is not None:
#                 say2(eval_result)
#     except:
#         pass

def say(msg):
    gitter.messages.send(room_name, str(msg))

gitter.rooms.join(room_name)

print('initting stream')
stream = gitter.stream.chat_messages(room_name)

print('starting streaming')
say("I'm starting. How to use me: simply type `eval python_code`. $LAST is the last message")

for bytes in stream.iter_lines():
    if bytes:
        try:
            message = loads(str(bytes, 'utf-8'))
            #------------
            text = message['text']
            if "$LAST" in text:
                text = text.replace("$LAST", "'" + last_message + "'")
            last_message = text
            user = message['fromUser']['username']
            command = text.split(' ')[0]
            if command == 'eval':
                args = ' '.join(text.split(' ')[1:])
                eval_result = aeval(args)
                if eval_result is not None:
                    say(eval_result)
            # ------------
        except Exception as e:
            print(str(e))

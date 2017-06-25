from state import State
from nn_model_fast import NN
from rule_simulator2 import RuleSimulator, initializer2
import tensorflow as tf
from tensorflow.contrib import rnn
import numpy as np
from w2v_fast import DataPrepare
import argparse
import fileinput
import json
from flask import Flask, request
import requests
import speech_recognition
import os
import subprocess as sp, os, traceback
FFMPEG_PATH = os.environ['FFMPEG_PATH'] if 'FFMPEG_PATH' in os.environ else '/usr/bin/ffmpeg'
app = Flask(__name__)
print("hi")
w_in = open('../All/w_in','w')
w_s = open('../All/w_s','w')
w_i = open('../All/w_i','w')
w_sa = open('../All/w_sa','w')
w_r = open('../All/w_r','w')
url_USDX = "https://scontent-tpe1-1.xx.fbcdn.net/v/t1.0-9/19145807_1907936742751378_1454936767914684007_n.jpg?oh=d7d3ebcb730800ba9e4fcc9f42afd3ca&oe=59CCD0C6"
url_query = "https://scontent-tpe1-1.xx.fbcdn.net/v/t1.0-9/19366143_1907936702751382_3493929736078059228_n.jpg?oh=1be5ac02feae79b3e453197ab79df44f&oe=59DC2075"
url_get_exchange_rate = "https://scontent-tpe1-1.xx.fbcdn.net/v/t1.0-9/19145722_1907936682751384_5945446393590147224_n.jpg?oh=17ad4dc21286f76864c8360c88f1958d&oe=599E3F16"
url_exchange = "https://scontent-tpe1-1.xx.fbcdn.net/v/t1.0-9/19146295_1907945296083856_6384446911611080282_n.jpg?oh=881e3600d4797620068749a27614ea18&oe=59EA101B"

def run_an_episode():
     
    print ("New episode, user goal:")
    user.goal.dump()
    print('_ _ _ _ _ _ _ _ _ _ _ _')
    
    #nl_input = initializer(user.goal)
    example_input = initializer2(user.goal)
    #print("Here are the example input, TA can random choose one or type your own(do not just type the number of sentence):")
    i = 1
    for a in example_input:
        print(str(i)+". "+a)
        i += 1
    #nl_input = input("TA types: ")
    #turn_by_turn(currturn,nl_input,'user')
    # while (not over):

        #system side
        # slot,intent = nlu.predict(nl_input,system)
        # system.update(slot,intent,nl_input)
        
        # frame_output, sys_nl = system.reply()
        """server send msg"""


        # print("system: "+sys_nl)
        # print(frame_output)
        # a = str(frame_output['system_action'][0])
        # a += "("
        # if frame_output['system_action'][0] == "response" or frame_output['system_action'][0] == "confirm_answer":
        #   for i in frame_output['slot'].keys():
        #       a += str(i)
        #       a += ', '
        # elif frame_output['system_action'][0] == 'request':
        #   for i in frame_output['slot']:
        #       a += str(i)
        #       a += ', '

        # a += ")"

        # turn_by_turn(currturn+1,a,'system')
        # currturn += 2
        # if currturn>= maxturn :
        #   print("[DM] maxturn reached")
        #   break
        # reward -= 2
        #user side
        #nl_input = user.next(frame_output)
        # example_next = user.next(frame_output)
        # print("Here are some example response for User according to agent response, TA can type your own(if there's only Thanks, please type Thanks):")
        # a = 1
        # for i in example_next:
        #   print(str(a)+". "+i)
        #nl_input = input("TA types: ")
        """get user input"""
        
    # if user.success:
    #   print("Successful")
    #   reward += 2*maxturn
    # else:
    #   print("Failing")
    #   reward -= maxturn
    return 
count = 1.
succ = 0.
config = tf.ConfigProto()
#config.gpu_options.allow_growth = True
config.gpu_options.per_process_gpu_memory_fraction = 0.2
sess = tf.Session(config=config)
nlu = NN(sess)
nlu.loadmodel()
# system = State()
# user = RuleSimulator()
# run_an_episode()
nl_input = None
#ACCESS_TOKEN = "EAAQ9hKlpknABAA1O4FXYNqvJZBn12rDxwg9bh6UVvs8toXhDXotdPQyifMYyrelQ8gCzZAoy7539sd6p1hUooXArZBy5yA2YyYrCAGo6mEOGQVwLks3TUP9d9yVF1CRc46vWpEthGsRlivREtbAH1ZA7SaZANjxNmcDzFvETzAAZDZD"
ACCESS_TOKEN = "EAAQ9hKlpknABAMVFHFIZBuYQJ5hYTeebE6GJbNpbEYCAQpCnden37ZA59leRS1KFgJGDfMUId9qiGUNT871ZB2mdtkIZAO3xZAZCtZB7Ny4OT4jpRgBztlo6vWFmkJW3wNSVBPD4Ugx1DTrX0winZCoDUkvKjeJuDQqwldTuS9rL5wZDZD"
#ACCESS_TOKEN = "EAAI05VJniQMBAAWVinJb2gmRFTmHfv3R0au2ZCWogjUIYh6pfpnhQh8hMKdUPKTBXJ6lNVJco32Pn4Nr0SgfZB3oC8HUMetcYvjboTgj4XNZAklUCJJk5qYqBJQchUVqviWLiPF7ArThG3ZBqgY6ngd8BuU69dQzXbJKQlo73n7DHsrHtZCp5"
VERIFY_TOKEN = "hi"
quick = None
audio_num = 0
BING_KEY = '92ab7fb7ee3b4d338ccc0712f4353c63'
alluser_state = dict()
def transcribe(audio_url):
    raw_audio = convert(audio_url)
    
    return raw_audio
def convert(file_path):
    try:
        #command = [
        #    FFMPEG_PATH, '-i', file_path, '-y', '-loglevel', '16','-threads', '8',  '-c:v', 'mp4' , '-f', 'wav' , '-'
        #]
        global audio_num
        audio_path = str(str("./audio/audio")+str(audio_num)+str(".wav"))
        command = [
            FFMPEG_PATH, '-i', file_path, '-ar', '16000', audio_path
        ]
        audio_num += 1
        print(command)
        # Get raw audio from stdout of ffmpeg shell command
        pipe = sp.Popen(command, stdout=sp.PIPE, bufsize=10**8)
        raw_audio = pipe.stdout.read()
        return audio_path
        
    except Exception as e:
        #print Exception
        print(e)
        traceback.print_exc()
def messaging_events(payload):
    
    data = payload
    
    messaging_events = data["entry"][0]["messaging"]
    
    for event in messaging_events:
        sender_id = event["sender"]["id"]

        # Not a message
        if "message" not in event:
            yield sender_id, None

        if "message" in event and "text" in event["message"] and "quick_reply" not in event["message"]:
            data = event["message"]["text"]
            yield sender_id, {'type':'text', 'data': data, 'message_id': event['message']['mid']}

        elif "attachments" in event["message"]:
            if "audio" == event['message']['attachments'][0]["type"]:
                audio_url = event['message']['attachments'][0]['payload']['url']
                yield sender_id, {'type':'audio','data': audio_url, 'message_id': event['message']['mid']}           
            else:
                yield sender_id, {'type':'text','data':"I don't understand this", 'message_id': event['message']['mid']}
        
        elif "quick_reply" in event["message"]:
            data = event["message"]["quick_reply"]["payload"]
            yield sender_id, {'type':'quick_reply','data': data, 'message_id': event['message']['mid']}
        
        else:
            yield sender_id, {'type':'text','data':"I don't understand this", 'message_id': event['message']['mid']}

def reply(user_id, msg):
    data = {
        "recipient": {"id": user_id},
        "message": {"text": msg}
    }
    print(user_id)
    print(msg)
    resp = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + ACCESS_TOKEN, json=data)
    #print(resp.content)

def reply_image2(user_id, url):
    data = {
        "recipient": {"id": user_id},
        "message":{
            "attachment":{
                "type":"image",
                "payload":{
                    "url":url
                }
            }
        }
    }
    print("hello")
    resp = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + ACCESS_TOKEN, json=data)
def reply_image(user_id, msg, url):
    ratio = "square"
    if url == url_exchange:
        ratio = "horizontal"
    data = {
        "recipient":{
            "id":user_id
          },
          "message":{
            "attachment":{
              "type":"template",
              "payload":{
                "template_type":"generic",
                "image_aspect_ratio":ratio,
                "elements":[
                   {
                    "title":msg,
                    "image_url":url,
                  }
                ]
              }
            }
          }    
    }
    resp = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + ACCESS_TOKEN, json=data)
def reply_help(user_id, msg):
    data = {
      "recipient":{
        "id":user_id
      },
      "message":{
        "text":msg,
        "quick_replies":[
          {
            "content_type":"text",
            "title":"stock",
            "payload":"query"
          },
          {
            "content_type":"text",
            "title":"global currency",
            "payload":"exchange"
          },
          {
            "content_type":"text",
            "title":"local bank currecy",
            "payload":"get_exchange_rate"
          },
          {
            "content_type":"text",
            "title":"USDX value",
            "payload":"USDX"
          }
        ]
      }    
    }
    resp = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + ACCESS_TOKEN, json=data)
def reply_quick(user_id, msg, option1, option2):
    data = {
      "recipient":{
        "id":user_id
      },
      "message":{
        "text":msg,
        "quick_replies":[
          {
            "content_type":"text",
            "title":option1,
            "payload":option1
          },
          {
            "content_type":"text",
            "title":option2,
            "payload":option2
          }
        ]
      }    
    }
    resp = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + ACCESS_TOKEN, json=data)
@app.route('/', methods=['GET'])
def handle_verification():
    print("Handling Verification.")
    return request.args['hub.challenge']

temp_message_id = ""
@app.route('/', methods=['POST'])
def handle_incoming_messages():
    #data = request.json
    #sender = data['entry'][0]['messaging'][0]['sender']['id']
    #message = ""
    #message = data['entry'][0]['messaging'][0]['message']['text']
    #nl_input = data['entry'][0]['messaging'][0]['message']['text']
    global nl_input
    payload = request.json
    webhook_type = get_type_from_payload(payload)
    if webhook_type == 'message':
        for sender, message in messaging_events(payload):
            if not message:
                return "ok"
            global temp_message_id 
            mid = message['message_id']
            if mid == temp_message_id:
                return 'ok'
            temp_message_id = mid
            if message['type'] == 'text':
                nl_input = message['data']
            elif message['type'] == 'audio':
                audio_url = message['data']
                r = speech_recognition.Recognizer()
                path = transcribe(audio_url)
                with speech_recognition.AudioFile(path) as source:
                    audio = r.record(source)
                #r.recognize_google(audio,language='')
                try:
                    #nl_input = STT.transcribe(audio_url)
                    nl_input = r.recognize_bing(audio, key = BING_KEY)
                    if nl_input == "" or nl_input == None:
                        return
                    # if 'DISPLAY_STT_RESULT' in os.environ and os.environ['DISPLAY_STT_RESULT'] != 0:
                    print(nl_input)
                except Exception as e:
                    message_ = "Sorry I can't process that now :("
                    print(e)
                nl_input = nl_input
            # global system
            # global user
            elif message['type'] == 'quick_reply':
                nl_input = message['data']
                if nl_input == "query":
                    msg = "get stock information with date and stock name(company name)"
                    reply_image(sender, msg, url_query)
                    return "ok"
                elif nl_input == "exchange":
                    msg = "the exchange rate between two countries using currency code"
                    reply_image(sender, msg, url_exchange)
                    return "ok"
                elif nl_input == "get_exchange_rate":
                    msg = "the exchange rate of other country to NTD in Bank of Taiwan for sell and buy also with account or cash"
                    reply_image(sender, msg, url_get_exchange_rate)
                    return "ok"
                elif nl_input == "USDX":
                    msg = "the value of USDX in a period of time(start data and end date)"
                    reply_image(sender, msg, url_USDX)
                    return "ok"
                elif nl_input == "buy":
                    s = [['B-action', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
                    i = [['get_exchange_rate'], [1]]
                    user_state = alluser_state[sender]
                    user_state.update(s,i,nl_input,w_in)
                    frame_output, sys_nl, quick = user_state.reply(w_s,w_i,w_sa)
                    message_ = sys_nl
                    alluser_state[sender] = user_state
                    if quick == "quick_action":
                        reply_quick(sender, message_, "buy", "sell")
                    elif quick == "quick_types":
                        reply_quick(sender, message_, "account", "cash")
                    else:
                        reply(sender, message_)
                    return "ok"
                elif nl_input == "sell":
                    s = [['B-action', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
                    i = [['get_exchange_rate'], [1]]
                    user_state = alluser_state[sender]
                    user_state.update(s,i,nl_input,w_in)
                    frame_output, sys_nl, quick = user_state.reply(w_s,w_i,w_sa)
                    message_ = sys_nl
                    alluser_state[sender] = user_state
                    if quick == "quick_action":
                        reply_quick(sender, message_, "buy", "sell")
                    elif quick == "quick_types":
                        reply_quick(sender, message_, "account", "cash")
                    else:
                        reply(sender, message_)
                    return "ok"
                elif nl_input == "account":
                    s = [['B-types', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
                    i = [['get_exchange_rate'], [1]]
                    user_state = alluser_state[sender]
                    user_state.update(s,i,nl_input,w_in)
                    frame_output, sys_nl, quick = user_state.reply(w_s,w_i,w_sa)
                    message_ = sys_nl
                    alluser_state[sender] = user_state
                    if quick == "quick_action":
                        reply_quick(sender, message_, "buy", "sell")
                    elif quick == "quick_types":
                        reply_quick(sender, message_, "account", "cash")
                    else:
                        reply(sender, message_)
                    return "ok"
                elif nl_input == "cash":
                    s = [['B-types', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
                    i = [['get_exchange_rate'], [1]]
                    user_state = alluser_state[sender]
                    user_state.update(s,i,nl_input,w_in)
                    frame_output, sys_nl, quick = user_state.reply(w_s,w_i,w_sa)
                    message_ = sys_nl
                    alluser_state[sender] = user_state
                    if quick == "quick_action":
                        reply_quick(sender, message_, "buy", "sell")
                    elif quick == "quick_types":
                        reply_quick(sender, message_, "account", "cash")
                    else:
                        reply(sender, message_)
                    return "ok"
                print(str("quick reply: ")+str(nl_input))
            if sender not in alluser_state or nl_input in ['hi', 'hello']:
                user_state = State()
                alluser_state[sender] = user_state
                message_ = "hi, this is Finbot.\nI can only understand English.\nI have the ability to do speech recognition by useing messneger's record function\nIf you find me dead just type: 'thanks' and then I will restart!\nI provide some fuctions below:\n1.stock: stock information with date\n2. exchange rates between countries\n3.USDX: USDX in an interval\n4. the exchange rate in the bank from taiwan to other countries. Enter 'help' if you have problems."
            elif nl_input.lower() in ['Thanks','thanks','thanks.', 'Thanks.']:#user.episode_over==True or nl_input in ['Thanks','thanks','thanks.', 'Thanks.']:
                message_ = 'Thanks.'
                if sender in alluser_state:
                    alluser_state[sender] = State()
            elif nl_input.lower() in ['help', 'Help', 'help.', 'Help.']:
                msg = "please choose the following four options to get the example dialogue"
                reply_help(sender, msg)
                if sender in alluser_state:                
                    alluser_state[sender] = State()
                return "ok"
            elif nl_input in ['test']:
                reply_quick(sender, "account", "cash")
                return "ok"
            else:
                if sender in alluser_state:
                    user_state = alluser_state[sender]
                else:
                    user_state = State()
                    alluser_state[sender] = user_state
                nl_input = " " + nl_input + " "
                d = dict()
                country = [[' new taiwan dollars ',' new taiwan dollar ', ' taiwan ',' ntd '],[' us dollars ', ' us dollar ',' united states ',' american dollars ', ' american dollar '," america " ," u.s.a ", ' usa ',' u.s. ',' u.s ',' us '],
                [' japan yen ',' japanese ',' japan ', 'yen '],[' rmb ', ' china '],[' eu '],[' france ']]
                currency = [' TWD ', ' USD ', ' JPY ', ' CNY ', ' EUR ', ' FRF ']
                for i in range(len(country)):
                    for j in range(len(country[i])):
                        tmp = nl_input.lower()
                        if country[i][j] in tmp:
                            index = tmp.find(country[i][j])
                            nl_input = nl_input[:index] + currency[i] + nl_input[index+len(country[i][j]):]
                slot,intent = nlu.predict(nl_input,user_state)
                user_state.update(slot,intent,nl_input,w_in)
                global quick
                frame_output, sys_nl, quick = user_state.reply(w_s,w_i,w_sa)
                message_ = sys_nl
                alluser_state[sender] = user_state
            global quick
            if quick == "quick_action":
                reply_quick(sender, message_, "buy", "sell")
            elif quick == "quick_types":
                reply_quick(sender, message_, "account", "cash")
            else:
                reply(sender, message_)
    return "ok"




def turn_by_turn(currturn,turn,who):
    print("[DM] turn{0} {1}:".format(currturn,who),turn)

def get_type_from_payload(payload):
    data = payload
    if "postback" in data["entry"][0]["messaging"][0]:
        return "postback"

    elif "message" in data["entry"][0]["messaging"][0]:
        return "message"

if __name__ == '__main__':
    #fb messenger
    app.run(debug=False)



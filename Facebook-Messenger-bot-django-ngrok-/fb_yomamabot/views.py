from django.shortcuts import render
import json, requests, random, re
from pprint import pprint
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http.response import HttpResponse

ACCESS_TOKEN = 'EAARJC5uL8NcBANT0lZA05bZCKDU9lmykWunqVnEztkty3DTQ8unfAaGLKZAOyNpHSUN74g61qODX3JUja8lxO0sgylfQXe5FFnMWzsu5IVFZAp5BUWaWowyhiCA1CzUoUX2uX2FjFdUZAd5QcWAAxcsVZAXqsZBVrZB4uVteucoGZAC7SV8xQnuWKMdQ2Ygyf7usZD'  # paste your token here
VERYFY_TOKEN = '01760755706'   # paste your token here



jokes = { 'pujateasi': ["""oh..puja! ha bolsila age""",
                """koro moja koro""",
           """ to amar jonnno time hobe nah?"""],
'kicukhaiso': ["""nahh..tumi?""",
                """ektu por khabo..""",
        """ ajke agei kheye felsi. tumi?"""],
'amikhaiso': ["""ki die khaila babu""",
                """amader ajke chicken hoise""",
                """ good."""],
'amiektuagekhaisi': ["""ki die khaila babu""",
               """amader ajke chicken hoise""",
               """ good."""],
'khainaiekhno': ["""khaba nah naki?""",
                        """thikbhabe khaite hobe""",
                        """ kheye feilo. sick korba"""],
'kikoro':  ["""kichu nah""",
             """ekta kaje asi..pore call dibo""",
             """ eito suye asi"""],
'ohkikoro?': ["""temon kichu nah""",
            """ekta kaje asi..pore call dibo"""],
'tobolo': ["""aj amar monta temon ekta valo nah """,
            """tumi to dhakar baire nah?""",
            """ki ar bolbo, kichu valo lagche nah"""],
'hmmdhakarbairedesherbaritepujahooche': ["""aj amar monta temon ekta valo nah """,
                                                """koro moja koro cousinder sathe. lol""",
                                                """miss u baby ❤️"""],
'missyoutooiloveyou': ["""tumi ki call diba?""",
                             """i love you too""",
                             """tai?"""],
'hmm': ["""i love you too"""
        """Sona ❤️"""],
'love' : ["""যতো ভালবাসা পেয়েছি,
তোমার কাছ থেকে।দুষ্টু এই মন চায়,
আরো বেশি পেতে।কি জানি,
তোমার মধ্যে কি আছে।কেনো যে এ মন চায়,
তোমাকে আরো বেশি করে কাছে পেতে॥""",
             """Hariye jate issa kore onnek dure
             Jekhane royese tumer valobashar shukhar nir""",
             """ami kolponar sagore vese jabo
             jabo tumer ridoy soikot a 
             tume dhora dibe nah """],
'tarporoachi' : ["""ta thaktei hobe""",
                   """পুরো পৃথিবীকে ব্রেকআপ দিবো।
                   শুধু একবার বল,
                   You wont leave"""],
'iwont' : ["""ta thaktei hobe""",
            """You cant leave""",
            """tai?"""],
'Socutebebe' : ["""Thank u babe""",
              """পুরো পৃথিবীকে ব্রেকআপ দিবো।
                but not you"""],
'valoasoajke' : ["""aj amar monta temon ekta valo nah """,
            """good. you?"""],
'kemonaso?' : ["""aj amar monta temon ekta valo nah """,
            """good. you?"""],
'good' :  ["""ami kolponar sagore vese jabo 
jabo tumer ridoy soikot a 
tume dhora dibe nah """,
            """জীবন এক বিরক্তিকর অধ্যায়।
            তবুও পরবর্তী পরিচ্ছেদে
            তুমি আছ ভেবে পাতা উল্টাই।"""],
'goodnight': ["""ghumau. good night""",
                """ghumaba? ok bye""",
                """ bye bye ❤️"""]

          }



def post_facebook_message(fbid, recevied_message):
    # Remove all punctuations, lower case the text and split it based on space
    tokens = re.sub(r"[^a-zA-Z0-9\s]", ' ', recevied_message).lower().split()
    joke_text = ''
    for token in tokens:
        if token in jokes:
            joke_text = random.choice(jokes[token])
            break
    if not joke_text:
        joke_text = "Anik ki koro! miss u baby"


    user_details_url = "https://graph.facebook.com/v2.6/%s" % fbid
    user_details_params = {'fields': 'first_name,last_name,profile_pic', 'access_token': ACCESS_TOKEN}
    user_details = requests.get(user_details_url, user_details_params).json()
    joke_text = joke_text

    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=EAARJC5uL8NcBANT0lZA05bZCKDU9lmykWunqVnEztkty3DTQ8unfAaGLKZAOyNpHSUN74g61qODX3JUja8lxO0sgylfQXe5FFnMWzsu5IVFZAp5BUWaWowyhiCA1CzUoUX2uX2FjFdUZAd5QcWAAxcsVZAXqsZBVrZB4uVteucoGZAC7SV8xQnuWKMdQ2Ygyf7usZD'
    response_msg = json.dumps({"recipient": {"id": fbid}, "message": {"text": joke_text}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=response_msg)
    pprint(status.json())


class YoMamaBotView(generic.View):
    def get(self, request, *args, **kwargs):
        if self.request.GET['hub.verify_token'] == VERYFY_TOKEN:
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Error, invalid token')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    # Post function to handle Facebook messages
    def post(self, request, *args, **kwargs):
        # Converts the text payload into a python dictionary
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        # Facebook recommends going through every entry since they might send
        # multiple messages in a single call during high load
        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                # Check to make sure the received call is a message call
                # This might be delivery, optin, postback for other events
                if 'message' in message:
                    # Print the message to the terminal
                    pprint(message)
                    # Assuming the sender only sends text. Non-text messages like stickers, audio, pictures
                    # are sent as attachments and must be handled accordingly.
                    post_facebook_message(message['sender']['id'], message['message']['text'])
        return HttpResponse()



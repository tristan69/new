#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from snipsTools import SnipsConfigParser
from hermes_python.hermes import Hermes
from hermes_python.ontology import *
import io
import random
# import requests
# import HTMLParser

CONFIG_INI = "config.ini"

# If this skill is supposed to run on the satellite,
# please get this mqtt connection info from <config.ini>
# Hint: MQTT server is always running on the master device
MQTT_IP_ADDR = "localhost"
MQTT_PORT = 1883
MQTT_ADDR = "{}:{}".format(MQTT_IP_ADDR, str(MQTT_PORT))

class Polite(object):
    """Class used to wrap action code with mqtt connection

        Please change the name refering to your application
    """

    def __init__(self):
        # get the configuration if needed
        try:
            self.config = SnipsConfigParser.read_configuration_file(CONFIG_INI)
        except :
            self.config = None

        # start listening to MQTT
        self.start_blocking()

    # --> Sub callback function, one per intent

    def Apres_midi_callback(self, hermes, intent_message):
        # terminate the session first if not continue
        hermes.publish_end_session(intent_message.session_id, "")

        # action code goes here...
        print '[Received] intent: {}'.format(intent_message.intent.intent_name)
        say = ["bon après midi", "bonne sieste", "bonne digestion", "bon après midi très cher"]
        result_sentence = random.choice(say)
        # if need to speak the execution result by tts
        hermes.publish_start_session_notification(intent_message.site_id, result_sentence, "Apres_midi")

    def Appetit_callback(self, hermes, intent_message):
        # terminate the session first if not continue
        hermes.publish_end_session(intent_message.session_id, "")

        # action code goes here...
        print '[Received] intent: {}'.format(intent_message.intent.intent_name)
        say = ["bon appétit", "ne mangez pas trop", "attention aux calories", "il faut macher lentement", "Merci ! Bon appetit !"]
        result_sentence = random.choice(say)
        # if need to speak the execution result by tts
        hermes.publish_start_session_notification(intent_message.site_id, result_sentence, "Appetit")

    def Bonsoir_callback(self, hermes, intent_message):
        # terminate the session first if not continue
        hermes.publish_end_session(intent_message.session_id, "")

        # action code goes here...
        print '[Received] intent: {}'.format(intent_message.intent.intent_name)
        say = ["bonsoir, cordialement", "bonsoir", "heu bonsoir", "bien le bonsoir", "oh bonsoir", "bonsoir très cher", "A vous aussi ! Je vous souhaite une bonne soiree."]
        result_sentence = random.choice(say)
        # if need to speak the execution result by tts
        hermes.publish_start_session_notification(intent_message.site_id, result_sentence, "Bonsoir")

    def Bonjour_callback(self, hermes, intent_message):
        # terminate the session first if not continue
        hermes.publish_end_session(intent_message.session_id, "")

        # action code goes here...
        print '[Received] intent: {}'.format(intent_message.intent.intent_name)
        say = ["Bonjour", "Salut", "Bonjour. sa fait longtemps.", "Yo. J'espaire que tu vas bien", "Bonjour. Prait pour une super journer?", "Salut. Je suis pas d'humeur aujourd'hui", "Je suis de très bonne humeur aujourd'hui", "Hello", "Bonjour ! J'espere que vous allez bien aujourd'hui !"]
        result_sentence = random.choice(say)
        # if need to speak the execution result by tts
        hermes.publish_start_session_notification(intent_message.site_id, result_sentence, "Bonjour")

    def Bonne_nuit_callback(self, hermes, intent_message):
        # terminate the session first if not continue
        hermes.publish_end_session(intent_message.session_id, "")

        # action code goes here...
        print '[Received] intent: {}'.format(intent_message.intent.intent_name)
		# Entrez des phrases dans le tableau ci-dessous, une phrase sera choisie aléatoirement
        say = ["A demain, faites de beaux raives", "Moi aussi je suis fatigue ! Passez une bonne nuit !", "Moi aussi je vais dormir, je suis crever", "Bonne nuit !", "Dormez bien, a demain ", "Baille baille ", "OK. Moi je vais regarder un bon film à la ter ler", "Dors bien et à demain pour une autre super journer"]
        #choix aléatoire d'une phrase
        result_sentence = random.choice(say)
        # if need to speak the execution result by tts
        hermes.publish_start_session_notification(intent_message.site_id, result_sentence, "Bonne_nuit")
    # More callback function goes here...

    # --> Master callback function, triggered everytime an intent is recognized
    def master_intent_callback(self,hermes, intent_message):
        coming_intent = intent_message.intent.intent_name
        if coming_intent == 'Darghorn:Apres_midi':
            self.Apres_midi_callback(hermes, intent_message)
        if coming_intent == 'Darghorn:Appetit':
            self.Appetit_callback(hermes, intent_message)
        if coming_intent == 'Darghorn:Bonsoir':
            self.Bonsoir_callback(hermes, intent_message)
        if coming_intent == 'Darghorn:Bonjour':
            self.Bonjour_callback(hermes, intent_message)
        if coming_intent == 'Darghorn:Bonne_nuit':
            self.Bonne_nuit_callback(hermes, intent_message)
        # more callback and if condition goes here...

    # --> Register callback function and start MQTT
    def start_blocking(self):
        with Hermes(MQTT_ADDR) as h:
            h.subscribe_intents(self.master_intent_callback).start()

if __name__ == "__main__":
    Polite()

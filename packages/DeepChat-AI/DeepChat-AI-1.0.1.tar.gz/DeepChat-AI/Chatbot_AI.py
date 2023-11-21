import nltk
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import pickle
import numpy as np
import pyttsx3
from keras.models import load_model
import os
import json
import random

class ChatBot:
    def __init__(self):
        # Load model and data files
        self.model = self.load_model()
        self.intents = self.load_intents()
        self.words, self.classes = self.load_words_classes()

    def load_model(self):
        current_dir = os.path.dirname(__file__)
        model_path = os.path.join(current_dir, 'model', 'chatbot_model2.h5')
        return load_model(model_path)

    def load_intents(self):
        current_dir = os.path.dirname(__file__)
        intents_path = os.path.join(current_dir, 'data', 'intents.json')
        with open(intents_path) as file:
            return json.load(file)

    def load_words_classes(self):
        current_dir = os.path.dirname(__file__)
        words_path = os.path.join(current_dir, 'model', 'words.pkl')
        classes_path = os.path.join(current_dir, 'model', 'classes.pkl')
        with open(words_path, 'rb') as words_file:
            words = pickle.load(words_file)
        with open(classes_path, 'rb') as classes_file:
            classes = pickle.load(classes_file)
        return words, classes

    def clean_up_sentence(self, sentence):
        sentence_words = nltk.word_tokenize(sentence)
        sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
        #print("Cleaned up sentence:", sentence_words)
        return sentence_words


    def bow(self, sentence, show_details=True):
        sentence_words = self.clean_up_sentence(sentence)
        bag = [0] * len(self.words)
        for s in sentence_words:
            for i, w in enumerate(self.words):
                if w == s:
                    bag[i] = 1
                    if show_details:
                        print("Found in bag: %s" % w)
        #print("Bag of words:", bag)
        return np.array(bag)

    def predict_class(self, sentence):
        p = self.bow(sentence, show_details=False)
        res = self.model.predict(np.array([p]))[0]
        ERROR_THRESHOLD = 0.25
        results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
        results.sort(key=lambda x: x[1], reverse=True)
        return_list = []
        for r in results:
            return_list.append({"intent": self.classes[r[0]], "probability": str(r[1])})
        return return_list

    def get_response(self, sentence):
        ints = self.predict_class(sentence)
        tag = ints[0]['intent']
        list_of_intents = self.intents['intents']
        for i in list_of_intents:
            if i['tag'] == tag:
                return random.choice(i['responses'])
        return "Sorry, I don't understand that."

    def take_command(self):
        return input("Enter your sentence: ")

    def speak(self, response):
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[0].id)
        engine.say(response)
        engine.runAndWait()

#if __name__ == "__main__":
#    bot = ChatBot()
#    while True:
#        user_input = bot.take_command()
#        if user_input.lower() == 'quit':
#            break
#        try:
#            response = bot.get_response(user_input)
#        except Exception as e:
#            print(e)
#            pass
#        print(response)
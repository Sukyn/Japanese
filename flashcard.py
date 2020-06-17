"""FLASHCARD PROGRAM"""
import json
import os
from random import randint

MAX_LEVEL = 10 #This means that a new card has 10x more chances to be picked up than a mastered card

class Card:
    """represents a card"""
    def __init__(self, **kwargs):
        #Finding the identificator
        self.identificator = kwargs.pop('identificator', -1)
        #Finding informations
        for key, value in kwargs.items():
            setattr(self, key, value)


class Flashcard():
    """represents a flashcard"""
    #CARDS is used at initialization to collect data from json
    CARDS = []

    def __init__(self, activation=True, progress=0, **kwargs):
        #If not activated it shouldn't be pickable
        self._activated = activation
        #The higher skill you have, the lower chance of picking this card you get
        self._skill = progress
        # --- #
        self.card = Card(**kwargs)
        # --- #

        Flashcard.CARDS.append(self)

    def correct(self):
        """called when someone gives a right answer"""
        if self._skill < MAX_LEVEL-1:
            self._skill += 1
            print_card()

    def wrong(self):
        """called when someone gives a wront answer"""
        self._skill = 0
        print_card()

    def change_activation(self):
        """called when someone want to activate/deactivate a card"""
        if self.activated:
            self._activated = False
        else:
            self._activated = True

    def send_random_information(self):
        """sends a random information about a card"""
        str(self)
        datas = []
        for key, value in self.card.items():
            temp = [key,value]
            datas.append(temp)
        amount_of_data = len(datas)
        while True:
            selected_data = randint(0, amount_of_data-1)
            if datas[selected_data][0] != "identificator":
                break
        return datas[selected_data]

    def send_random_half_information(self):
        """sends a random information about a card buy without the answer"""
        data = self.send_random_information()
        return data[0]

    def validate_answer(self, question, answer):
        """Tells if an asnwer is the good one"""
        str(self)
        if self.card[question] == answer:
            self.correct()
            return True
        else:
            self.wrong()
            return False



    @classmethod
    def initialize(cls):
        """Initializes datas"""
        #We read all datas...
        filesize = os.path.getsize("data/flashcard.json")

        if filesize == 0:
            print("The file is empty, initialization aborted")
        else:
            with open("data/flashcard.json", "r", encoding='utf-8') as read_file:
                every = json.load(read_file)
            cls.CARDS = []
            #... and then we transform it into Flashcards
            for cardv in every:
                Flashcard(activation=cardv["_activated"], progress=cardv["_skill"], **cardv["card"])


    @classmethod
    def random_card(cls):
        """Chose a random existing card"""
        if not cls.CARDS:
            cls.initialize()
        # --- The lower skill you have on a card, the more it will be chosen --- #
        cards = []
        for card in cls.CARDS:
            for i in range(MAX_LEVEL-card.skill):
                cards.append(card)
        # ---------------------------------------------------------------------- #
        number_of_cards = len(cards)
        random_card = randint(0, number_of_cards-1)
        return cards[random_card]

    @classmethod
    def last_identificator(cls):
        """shows last registered identificator"""
        maximum = 0
        for card in cls.CARDS:
            str(card)
            if card.card["identificator"] > maximum:
                maximum = card.card["identificator"]
        return maximum

    # --- ENCAPSULATION ---
    @property
    def skill(self):
        """shows skill"""
        return self._skill

    @property
    def activated(self):
        """shows activation"""
        return self._activated
    # ---               ---

    #Representing in an easier way to convert into json
    def __str__(self):
        if not isinstance(self.card, dict):
            self.card = self.card.__dict__
        json_str = json.dumps(self.__dict__)
        return json_str

def print_card():
    """Saves a card into our json document"""
    # --- START OF THE JSON-FRIENDLY WRITING ---
    desc = "["
    first = True
    for card in Flashcard.CARDS:
        #'first' removes the first comma
        if first:
            first = False
        else:
            desc += ", "
        desc += str(card)
    desc += "]"
    # -------------------------------------------
    with open("data/flashcard.json", "w", encoding='utf-8') as writing_file:
        json.dump(json.loads(desc), writing_file)

def add_card(**kwargs):
    """adds a card and save it"""
    identificator = Flashcard.last_identificator() + 1
    Flashcard(identificator=identificator, **kwargs)
    print_card()
    print("Card successfully added with identificator : {}".format(identificator))

def delete_card(identificator):
    """deletes a card by its identificator"""
    for cardv in Flashcard.CARDS:
        if cardv.card["identificator"] == identificator:
            Flashcard.CARDS.remove(cardv)
            print_card()
            print("Card with identificator {} was successfully deleted".format(identificator))
            return
    print("There was an error during suppression" \
          "of card with identificator : {}".format(identificator))

if __name__ == '__main__':
    Flashcard.initialize()
    selected_card = Flashcard.random_card()
    given_information = selected_card.send_random_information() #User needs to know a part of a card to guess the other one
    print("Given information : ", given_information)
    while True:
        question = selected_card.send_random_half_information()
        if question != given_information[0]:
            break
    print(question, " ?")
    answer = input()
    if selected_card.validate_answer(question, answer):
        print("GG boy")
    else:
        print(":/")

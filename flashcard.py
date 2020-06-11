"""FLASHCARD PROGRAM"""
import json
#import random

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
        self._skill += 1

    def wrong(self):
        """called when someone gives a wront answer"""
        self._skill = 0

    def change_activation(self):
        """called when someone want to activate/deactivate a card"""
        if self.activated:
            self._activated = False
        else:
            self._activated = True

    @classmethod
    def initialize(cls):
        """Initializes datas"""
        #We read all datas...
        with open("data/flashcard.json", "r", encoding='utf-8') as read_file:
            every = json.load(read_file)
        cls.CARDS = []
        #... and then we transform it into Flashcards
        for cardv in every:
            Flashcard(activation=cardv["_activated"], progress=cardv["_skill"], **cardv["card"])


    @classmethod
    def last_identificator(cls):
        """shows last registered identificator"""
        maximum = 0
        for card in cls.CARDS:
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
    #Flashcard.initialize()
    add_card(nom="DENIS", prenom="Martin")
    add_card(profession="pingu")
    delete_card(1)

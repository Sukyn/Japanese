#KATAKANIZATION PROGRAM
import json

class Katakana:
    KATAKANA = []
    """Represents a Katakana"""
    def __init__(self, roumaji, katakana, type):
        self.roumaji = roumaji
        self.katakana = katakana
        self.type = type

    @classmethod
    def initialize(cls):
        """Initializes datas"""
        with open("data/katakana.json", "r", encoding='utf-8') as read_file:
            every = json.load(read_file)
        cls.KATAKANA = []
        for ktk in every:
            katakana = Katakana(ktk["roumaji"], ktk["kana"], ktk["type"])
            cls.KATAKANA.append(katakana)

    # --- ENCAPSULATION --- #
    def toRoumaji(self):
        return self.roumaji

    def toKatakana(self):
        return self.katakana
    # ---              --- #

def showAlphabet():
    if not Katakana.KATAKANA:
        Katakana.initialize()
    for ktk in Katakana.KATAKANA:
        print("Romaji :", ktk.roumaji, "\n",
              "Katakana :", ktk.katakana, "\n",
              "Type :", ktk.type, "\n\n")

def convertSyllabus(sqc):
    """Converts from roumaji to katakana, and reprocity"""
    if len(sqc) > 3:
        return "Syllabe invalide : {}".format(sqc)
    for ktk in Katakana.KATAKANA:
        if ktk.roumaji == sqc:
            return ktk.katakana
        if ktk.katakana == sqc:
            return ktk.roumaji


def convertWord(word):
    pass

if __name__ == '__main__':
    showAlphabet()

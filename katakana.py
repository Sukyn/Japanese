"""KATAKANIZATION PROGRAM"""
import json

class Katakana:
    """Represents a Katakana"""
    KATAKANA = []
    def __init__(self, roumaji, katakana, category):
        self.roumaji = roumaji
        self.katakana = katakana
        self.category = category

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
    def to_roumaji(self):
        """Converts a katakana into a roumaji"""
        return self.roumaji

    def to_katakana(self):
        """Converts a roumaji into a katakana"""
        return self.katakana
    # ---              --- #

def show_alphabet():
    """Shows all the katakana alphabet"""
    if not Katakana.KATAKANA:
        Katakana.initialize()
    for ktk in Katakana.KATAKANA:
        print("Romaji :", ktk.roumaji, "\n",
              "Katakana :", ktk.katakana, "\n",
              "category :", ktk.category, "\n\n")

def convert_syllabus(sqc):
    """Converts from roumaji to katakana, and reprocity"""
    if len(sqc) > 3:
        return "Syllabe invalide : {}".format(sqc)
    for ktk in Katakana.KATAKANA:
        if ktk.roumaji == sqc:
            return ktk.katakana
        if ktk.katakana == sqc:
            return ktk.roumaji
    return -1

#WITHOUT ARTIFICIAL INTELLIGENCE WAY
def rewrite(word):
    """Rewrites a word into roumaji"""
    word = word.lower()
    if not Katakana.KATAKANA:
        Katakana.initialize()
    #vowel = ["a", "e", "i", "u", "o"]
    vowel_extended = {"é":"e", "è":"e", "ê":"e", "à":"a", "â":"a", "ô":"o", "î":"i"}
    consonant = ["k", "g", "b", "m", "n", "h", "p", "f", "r",
                 "w", "y", "t", "d", "s", "z", "j", "v", "d"]
    consonant_extended = {"c":"k", "l":"r", "q":"k", "x":"kusu"}
    # -- REPLACING SEMI SYLLABUS BY THEIR PHONETIC NEIGHBOUR --
    for value in enumerate(word):
        if value in vowel_extended:
            word = word.replace(value, vowel_extended[value])
        if value in consonant_extended:
            word = word.replace(value, consonant_extended[value])
    # ---- #
    decalage = 1
    for i in range(len(word)-1):
        true_i = i+decalage
        if (word[true_i-1] in consonant and
                word[true_i] in consonant): #We insert an 'u' if there are two consonants followed
            word = word[:true_i] + 'u' + word[true_i:]
            decalage += 1
        if word[true_i-1] in consonant and (word[true_i] == " " or
                                            word[true_i] == "," or
                                            word[true_i] == "." or
                                            word[true_i] == "'"):
                                            #We insert an 'u' if it is at the end of a word
            word = word[:true_i] + 'u' + word[true_i:]
            decalage += 1
    if word[-1] in consonant:
        word = word + "u"
    return word

def transform_to_katakana(string_to_convert):
    """Transforms a sentence into katakana"""
    roumaji = rewrite(string_to_convert)
    desc = ""
    vowel = ["a", "e", "i", "u", "o"]
    decalage = 0
    for i in range(len(roumaji)-1):
        true_i = i+decalage
        temp = " "

        if true_i >= (len(roumaji) - 1):
            break
        if roumaji[true_i] in vowel:
            temp = convert_syllabus(roumaji[true_i])
        elif (roumaji[true_i] == " " or
              roumaji[true_i] == "," or
              roumaji[true_i] == "." or
              roumaji[true_i] == "'"):
            pass
        else: #If not a vowel nor a space, it means that it is a two char syllabus
            temp = convert_syllabus(roumaji[true_i] + roumaji[true_i+1])
            decalage += 1
        desc += temp

    return desc

if __name__ == '__main__':
    sentence = input()
    print(transform_to_katakana(sentence))

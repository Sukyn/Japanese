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
    def _initialize(cls):
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
        Katakana._initialize()
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

#WITHOUT ARTIFICIAL INTELLIGENCE WAY
def rewrite(word):
    """Rewrites a word into roumaji"""
    word = word.lower()
    if not Katakana.KATAKANA:
        Katakana._initialize()
    vowel = ["a", "e", "i", "u", "o"]
    vowel_extended = {"é":"e", "è":"e", "ê":"e", "à":"a", "â":"a", "ô":"o", "î":"i" }
    consonant = ["k", "g", "b", "m", "n", "h", "p", "f", "r", "w", "y", "t", "d", "s", "z", "j", "v", "d"]
    consonant_extended = {"c":"k", "l":"r", "q":"k", "x":"kusu"}
    # -- REPLACING SEMI SYLLABUS BY THEIR PHONETIC NEIGHBOUR --
    for i in range(len(word)):
        if word[i] in vowel_extended:
            word = word.replace(word[i], vowel_extended[word[i]])
        if word[i] in consonant_extended:
            word = word.replace(word[i], consonant_extended[word[i]])
    # ---- #
    decalage = 1
    for i in range(len(word)-1):
        print(i,word[i+decalage-1], decalage, word, len(word))
        if word[i+decalage-1] in consonant and word[i+decalage] in consonant:
            word = word[:i+decalage] + 'u' + word[i+decalage:]
            decalage += 1
        if word[i+decalage-1] in consonant and word[i+decalage] == " ":
            word = word[:i+decalage] + 'u' + word[i+decalage:]
            decalage += 1
    if word[-1] in consonant:
        word = word + "u"
    return word

def transformToKatakana(sentence):
    """Transforms a sentence into katakana"""
    roumaji = rewrite(sentence)
    desc = ""
    decalage = 2
    vowel = ["a", "e", "i", "u", "o"]
    for i in range (0, len(roumaji)-1, decalage):
        decalage = 2
        temp = " "
        if roumaji[i] in vowel:
            print(roumaji[i], roumaji)
            temp = convertSyllabus(roumaji[i])
            decalage = 1
        elif roumaji[i] == " ":
            decalage = 1
        else:
            print(roumaji[i], roumaji)
            temp = convertSyllabus(roumaji[i] + roumaji[i+1])
        desc += temp
        print(desc)
    return desc

if __name__ == '__main__':
    sentence = input()
    print(transformToKatakana(sentence))

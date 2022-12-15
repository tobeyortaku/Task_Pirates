from flask import Flask, request, jsonify
from googletrans import Translator
from math import sqrt
import spacy
from langdetect import detect


class Pirates:
    def __init__(self, sentence, magic_number):
        self.sentence = sentence
        self.magic_number = magic_number

    def error_checker(self):
        if type(self.sentence) != str:
            return "Sentence has to be str type or can not be null."
        elif detect(self.sentence) != 'en':
            return "Please use proper english sentence"
        elif self.get_subject() == None:
            return "Where am I?"
        elif type(self.magic_number) != int:
            return "Where is magic?"
        else:
            pass

    def get_subject(self):
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(self.sentence)

        for token in doc:
            if ("subj" in token.dep_):
                subtree = list(token.subtree)
                start = subtree[0].i
                end = subtree[-1].i + 1
                return str(doc[start:end])

    def tobe_changer(self):
        sentence = self.sentence
        tobes = ['am', 'are', 'is']
        tobe_matches = [tobe for tobe in tobes if tobe in sentence]
        if tobe_matches == None:
            for match in tobe_matches:
                changed_sentence = sentence.replace(match, '<to/be>')
            return changed_sentence
        else:
            return sentence

    def sentence_editor(self):
        subject = self.get_subject()
        tobe_changed_sentence = self.tobe_changer()
        match subject:
            case 'I':
                subject_tobe_changed_sentence = tobe_changed_sentence.replace(
                    subject, 'Pirate king')
                new_sentence = subject_tobe_changed_sentence.replace(
                    '<to/be>', 'is')

            case _:
                subject_tobe_changed_sentence = str(self.count_divisor()) + \
                    tobe_changed_sentence.replace(subject, ' Pirates')
                new_sentence = subject_tobe_changed_sentence.replace(
                    '<to/be>', 'are')

        return new_sentence

    def count_divisor(self):
        number = self.magic_number
        divisor_count = 0
        for i in range(1, int(sqrt(number)) + 1):
            if (number % i == 0):
                divisor_count = divisor_count + 2
        if sqrt(number).is_integer():
            divisor_count = divisor_count - 1
        return divisor_count

    def translation_json(self):
        translator = Translator()
        translation_en = self.sentence_editor()
        translation_jp = translator.translate(translation_en, dest="ja").text
        translation_mn = translator.translate(translation_en, dest="mn").text

        return jsonify(english_sentences=translation_en, mongolian_sentence=translation_mn, japanese_sentence=translation_jp)


app = Flask(__name__)


@app.route('/', methods=['POST'])
def handle_json():
    data = request.get_json(force=True)

    try:
        pirate = Pirates(data['sentence'], data['magic_number'])
    except:
        return jsonify(error="Invalid json request")

    if pirate.error_checker():
        return jsonify(error=pirate.error_checker())
    else:
        return pirate.translation_json()


if __name__ == '__main__':
    app.run(debug=True, port=5000)

from flask import Flask, request, jsonify
from googletrans import Translator
from math import sqrt


class Pirates:
    def __init__(self, sentence, magic_number):
        self.sentence = sentence
        self.magic_number = magic_number

    def error_checker(self):
        words = self.sentence.split()

        if words[0] in ['am', 'is', 'are', 'Am', 'Is', 'Are']:
            return "Where am I?"
        elif type(self.magic_number) != int:
            return "Where is magic?"
        else:
            pass

    def sentence_editor(self):
        words = self.sentence.split()
        match words[0]:
            case 'I':
                new_sentence = "Pirate King is " + ' '.join(words[2:])
            case _:
                new_sentence = str(self.count_divisor()) + \
                    " Pirates are " + ' '.join(words[2:])
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
    pirate = Pirates(data['sentence'], data['magic_number'])

    if pirate.error_checker():
        return jsonify(error=pirate.error_checker())
    else:
        return pirate.translation_json()


if __name__ == '__main__':
    app.run(debug=True, port=5000)

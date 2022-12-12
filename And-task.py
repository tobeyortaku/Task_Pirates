from flask import Flask, request, jsonify
from googletrans import Translator


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
                new_sentence = "Pirates are " + ' '.join(words[2:])
        return new_sentence

    def magic_number(self):
        pirates_count = self.magic_number/3
        return pirates_count

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
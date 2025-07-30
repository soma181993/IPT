from flask import Flask, request, jsonify
import gtts
import os
from googletrans import Translator
from datetime import datetime
from langdetect import detect

app = Flask(__name__)

@app.route('/translate', methods=['POST'])
def translate_text():
    try:
        data = request.get_json()
        text = data.get('text', '')
        lang = data.get('lang', 'en')
        language = detect(text)  # Default to English if lang is not provided
        print(language)
        # Translate the input text to English
        translator = Translator()
        translated_to_english = translator.translate(text, src=language, dest=lang).text

        # Translate the English text to the specified destination language
        dest_lang = data.get('dest_lang', 'en')  # Default to English if dest_lang is not provided
        translated_text = translator.translate(translated_to_english, src='en', dest=dest_lang).text

        # Create and save the translated audio with the current date
        save_directory = "E:\\IPT\\audio"
        current_date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        audio_file_name = f"audio_{current_date}.mp3"
        file_path = os.path.join(save_directory, audio_file_name)

        # Generate the speech from the translated text in the destination language
        tts = gtts.gTTS(translated_text, lang=dest_lang, slow=False)
        tts.save(file_path)

        # Play the translated audio
        os.system(f'start {file_path}')

        return jsonify({"translated_text": translated_text, "audio_file_name": file_path})

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Return a 500 Internal Server Error for any exception

if __name__ == '__main__':
    app.run(debug=True)

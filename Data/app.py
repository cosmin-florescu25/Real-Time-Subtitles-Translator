from flask import Flask, jsonify, request
from flask_cors import CORS
from do_photo import take_screenshot
from analyze_image import analyze_image_and_translate
import os
from dictionary_utils import get_example_sentence
from db_utils import log_word, initialize_db, get_logged_words
from dictionary_utils import clean_text

initialize_db()

app = Flask(__name__)
CORS(app)

server_enabled = True

@app.post("/status_update")
def status_update():
    global server_enabled
    data = request.get_json()
    status = data.get("status", "OFF")
    server_enabled = (status == "ON")
    print(f"Server state updated: {server_enabled}")
    return jsonify({"new_status": server_enabled})


@app.get("/ocr")
def ocr():
    if not server_enabled:
        return jsonify({
            "text": "",
            "original_lines_data": [],
            "border_box": [],
            "screenshot_left": 0,
            "screenshot_top": 0,
        }), 403

    s_info = take_screenshot()
    image_path = os.path.join("images", "documentation_image.png")
    result = analyze_image_and_translate(image_path)

    return jsonify({
        "text": result['translated_text'],
        "original_lines_data": result['processed_lines_data'],
        "border_box": result.get('border_box', []),
        "screenshot_left": s_info['left'],
        "screenshot_top": s_info['top'],
    })



@app.get("/definition")
def definition():
    if not server_enabled:
        return jsonify({"definition": None}), 403

    word = request.args.get('word')
    if not word:
        return jsonify({"definition": None}), 400

    definition_text = get_example_sentence(word)

    if definition_text:
        log_word(word, definition_text)

    definition_text = clean_text(word) + ": " + definition_text
    
    return jsonify({"definition": definition_text})

@app.get("/export_words")
def export_words():
    words_list = get_logged_words() 
    return jsonify({"words": words_list})


if __name__ == "__main__":
    app.run(debug=True, threaded=True, port = 5002)
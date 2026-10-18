from PIL import Image, ImageOps, ImageFilter
import numpy as np
import pytesseract
from translate_text import translate_text
from hitbox_line import get_words
from polish_text import post_process_with_tool


def get_tesseract_boxes(img_np):
    data = pytesseract.image_to_data(img_np, output_type=pytesseract.Output.DICT)

    words = data["text"]
    n = len(words)

    boxes = []
    for i in range(n):
        if not words[i].strip():
            continue

        x = data["left"][i]
        y = data["top"][i]
        w = data["width"][i]
        h = data["height"][i]

        conf_value = data["conf"][i]
        try:
            conf = float(conf_value)
        except:
            conf = 0


        boxes.append({
            "word": words[i],
            "conf": conf,
            "x": x,
            "y": y,
            "w": w,
            "h": h
        })

    return boxes

def group_into_lines(boxes, tolerance=20):
    lines = []

    for box in boxes:
        inserted = False
        for line in lines:
            if abs(line["y"] - box["y"]) <= tolerance:
                line["words"].append(box)
                line["y"] = (line["y"] + box["y"]) / 2
                inserted = True
                break

        if not inserted:
            lines.append({"y": box["y"], "words": [box]})

    lines.sort(key=lambda l: l["y"])

    return lines


def analyze_image_and_translate(image_path):
    image = Image.open(image_path)

    gray_image = ImageOps.grayscale(image)

    # it affects the linebox if we resize it
    # scale_factor = 2
    # resized_image = gray_image.resize(
    #     (gray_image.width * scale_factor, gray_image.height * scale_factor),
    #     resample=Image.LANCZOS
    # )

    thresholded_image = gray_image.filter(ImageFilter.FIND_EDGES)

    img_np = np.array(thresholded_image.convert('RGB'))

    word_boxes = get_tesseract_boxes(img_np)

    filtered_boxes = [b for b in word_boxes if b["conf"] > 45]

    lines = group_into_lines(filtered_boxes)

    extracted_lines = []
    border_box = []

    for line in lines:
        # sort words by X position
        line["words"].sort(key=lambda w: w["x"])

        text_line = " ".join([w["word"] for w in line["words"]])
        extracted_lines.append(text_line)

        # line bounding box
        x_min = min(w["x"] for w in line["words"])
        y_min = min(w["y"] for w in line["words"])
        x_max = max(w["x"] + w["w"] for w in line["words"])
        y_max = max(w["y"] + w["h"] for w in line["words"])

        width = x_max - x_min
        height = y_max - y_min

        border_box.append(((x_min, y_min), (x_max, y_max), width, height))

    extracted_text = " ".join(extracted_lines).strip()

    original_clean_text = post_process_with_tool(extracted_text)

    translated_text = translate_text(original_clean_text)

    processed_lines_data = []
    for raw_line in extracted_lines:
        clean_line = post_process_with_tool(raw_line)
        word_intervals = get_words(clean_line)
        processed_lines_data.append({
            'text': clean_line,
            'word_intervals': word_intervals
        })

    return {
        'original_text': original_clean_text,
        'translated_text': translated_text,
        'processed_lines_data': processed_lines_data,
        'border_box': border_box
    }


if __name__ == "__main__":
    res = analyze_image_and_translate('images/documentation_image.png')
    print(res)

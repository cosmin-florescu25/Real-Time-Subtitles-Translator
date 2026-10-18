from PIL import Image
import numpy as np
from translate_text import translate_text
import easyocr
from hitbox_line import get_words
from polish_text import post_process_with_tool

try:
    reader = easyocr.Reader(['en'])
except Exception as e:
    reader = None

def analyze_image_and_translate(image_path):
        
    image = Image.open(image_path)
    img_np = np.array(image.convert('RGB')) 
    
    raw_results = reader.readtext(img_np, detail=1)
    
    # getting the coordonates of the lines
    border_box = []
    for box, text, conf in raw_results:
        x_coords = [int(point[0]) for point in box]
        y_coords = [int(point[1]) for point in box]
        x_min, x_max = min(x_coords), max(x_coords)
        y_min, y_max = min(y_coords), max(y_coords)
        width = x_max - x_min
        height = y_max - y_min
        border_box.append(((x_min, y_min), (x_max, y_max), width, height))

    # keep the words with confidence > 0.45
    filtered_and_sorted = sorted(
        [item for item in raw_results if item[2] > 0.45], 
        key=lambda item: item[0][0][1] 
    )

    extracted_lines = [item[1] for item in filtered_and_sorted]    

    extracted_text = " ".join(extracted_lines).strip()

    original_clean_text = extracted_text
    
    original_clean_text = post_process_with_tool(original_clean_text)
    
    translated_text = translate_text(original_clean_text)

    processed_lines_data = []

    for raw_line_text in extracted_lines:

        clean_line_text = post_process_with_tool(raw_line_text)

        word_intervals = get_words(clean_line_text)
        
        processed_lines_data.append({
            'text': clean_line_text,
            'word_intervals': word_intervals
        })

    return {
        'original_text': original_clean_text,
        'translated_text': translated_text,
        'processed_lines_data': processed_lines_data,
        'border_box': border_box,
    }

if __name__ == "__main__":
    analyze_image_and_translate('images/documentation_image.png')
    print(analyze_image_and_translate('images/documentation_image.png'))

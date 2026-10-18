#!/bin/bash


if [ -d "Data/TranslateVenv" ]; then
    rm -rf Data/TranslateVenv
fi

if [ -d "Data/__pycache__" ]; then
    rm -rf Data/__pycache__
fi

echo "The following questions can determine which variant of image analyze the program will use."
echo "If all requirments are met, the translated subtitles will be more accurate, but the setup will take longer and require more resources.(easyOCR)"
echo "If not, a lighter variant will be used. (pytesseract)"

echo "Do you have at least 8GB of free storage? (Y/n)"
read ram

echo "Do you have a dedicated GPU? (Y/n)"
read gpu

echo "Can you wait approximately 1 minute and a half for the process? (Y/n)"
read time

python3 -m venv Data/TranslateVenv
if [[ "$ram" =~ ^([Yy]|[Yy][Ee][Ss])$ ]] && [[ "$gpu" =~ ^([Yy]|[Yy][Ee][Ss])$ ]] && [[ "$time" =~ ^([Yy]|[Yy][Ee][Ss])$ ]]; then
    echo "Using the EasyOCR variant (more accurate)..."
    cp Data/Options/easy_ocr_variant.py Data/analyze_image.py
    source Data/TranslateVenv/bin/activate
    pip install -r Data/requirements_heavy.txt
    echo ""
    echo "More accurate variant setup complete."
else
    echo "Using the PyTesseract variant (light)..."
    cp Data/Options/pytesseract_variant.py Data/analyze_image.py
    source Data/TranslateVenv/bin/activate
    pip install -r Data/requirements_light.txt
    echo ""
    echo "Light variant setup complete."
fi
echo "Succesful setup! Please read the README for steps regarding the instalation of the extension."
echo "Now you can run 'run.sh! Don't forget to activate the extension. It takes a few second for the server to start."

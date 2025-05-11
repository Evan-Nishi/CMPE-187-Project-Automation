# CMPE-187 Autoamtion Scripts

This is the test automation scripts for group #6.  This project automates querying, evaluating, and comparing the performance of ChatGPT vs Deepseek in high school level algebra.

## Setup
Install dependencies: `pip install sympy flask openai pillow easyocr sentence-transformers`

Add input folder to [./static]().  
We split the inputs into two to make it easier to run multiple instances simultaenously.
[./static/in1-3]() contains chapters 1 and 3
[./static/in2-4]() contains chapters 2 and 4

Create a .env with the following variables:
```
OPENAI_API_KEY="your openai api key"
DEEPSEEK_API_KEY="your deepseek api key"
```

Run `augment.py` on your selected folder to creat test case augmentations: 
For example `python augment.py ./static/in1-3`

If you wish to run the ui run in a seperate terminal: `python app.py` and navigate to [http://127.0.0.1:5000]()

Change the `base_im_path` variable on line 39 in [main.py]() to the input directory.

Then run `python main.py`
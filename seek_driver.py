from openai import OpenAI
from processutils import get_text
from sympy import Eq

def prompt_image_seek(client, is_student, img_path, reader):
    work = get_text(reader, img_path)
    if is_student:
        prompt = "I am going to give you an ocr reading of a screenshot of a math problem that you must solve.  Please put each step on a separate line.  No explanations or any other text are to be displayed.  Please don't format using latex or markdown, just simple notation in a single paragraph.  If the question doesn't have enough information to be solved the answer is \"Not enough information\".  Don't use percentages, use decimal instead.  Fractions are ok when appropriate.  The last line of the output must be formatted like so:`Answer:<answer>` with no other text or units. Just the numerical answer if a number, or the answer text if not.  If there are multiple answers, seperate them with AND like so:`Answer:<answer_1> AND <answer_2> AND <answer_n>`."
    else:
        prompt = "I am going to give you an ocr reading of a problem that is already solved.  Simply state if it is \"Incorrect\" if it is solved wrong, \"Correct\" if it solved correctly, or \"Not enough information\" if there is not enough information provided to determine.  No other explanations or any other text is to be displayed."
    
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "user", "content": prompt},
            {"role": "user", "content": work},
        ],
        stream=False
    )

    return response
'''
import os
from dotenv import load_dotenv
import easyocr
load_dotenv()
chatgpt_api_key = os.getenv("OPENAI_API_KEY")
deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")
reader = easyocr.Reader(['en'])
seek_client = OpenAI(api_key=deepseek_api_key, base_url="https://api.deepseek.com")
print(prompt_image_seek(seek_client, True, './in/1-1-1.png', reader))
'''
from openai import OpenAI
import mimetypes
from fileutils import encode_image
from sympy import Eq

def prompt_image_gpt(client, is_student, image_path):
    if is_student:
        prompt = "I am going to give you a screenshot of a math problem that you must solve.  Please put each step on a separate line.  No explanations or any other text are to be displayed.  Please don't format using latex or markdown, just simple notation in a single paragraph.  If the question doesn't have enough information to be solved the answer is \"Not enough information\".  Don't use percentages, use decimal instead.  Fractions are ok when appropriate.  The last line of the output must be formatted like so:`Answer:<answer>` with no other text or units.  Just the numerical answer if a number, or the answer text if not.  If there are multiple answers, seperate them with AND like so:`Answer:<answer_1> AND <answer_2> AND <answer_n>`."
    else:
        prompt = "I am going to give you a problem that is already solved.  Simply state if it is \"Incorrect\" if it is solved wrong, \"Correct\" if it solved correctly, or \"Not enough information\" if there is not enough information provided to determine.  No other explanations or any other text is to be displayed."
    
    img_str = encode_image(image_path=image_path)
    response = client.responses.create(
        model="gpt-4.1",
        input=[
            {
                "role": "user",
                "content": [
                    { "type": "input_text", "text": prompt },
                    {
                        "type": "input_image",
                        "image_url": f"data:image/jpeg;base64,{img_str}",
                    },
                ],
            }
        ],
    )

    return response
from openai import OpenAI
import easyocr

import mimetypes
from dotenv import load_dotenv
import os
import json

import requests

from chat_driver import prompt_image_gpt
from seek_driver import prompt_image_seek

from fileutils import get_image_paths, get_json_dict, Logger
from processutils import cos_similarity, check_math_eq

from sympy import sympify, Eq

import warnings
warnings.filterwarnings("ignore")
#venv\Scripts\activate


WORK_THRESHOLD = 0.50

#just a graphic
def print_loading_bar(completed, total, length=40):
    if total == 0:
        percent = 0
    else:
        percent = completed / total

    filled = int(length * percent)
    bar = '=' * filled + '-' * (length - filled)
    print(f'[{bar}] {int(percent * 100)}% ({completed}/{total})')


def main():
    base_im_path = "./static/in1-3"

    reader = easyocr.Reader(['en'])
    target_paths = get_image_paths(base_im_path)


    total_cases = len(target_paths)

    cases_done = 0

    test_logger = Logger()

    ans_keys = get_json_dict(base_im_path)
    
    load_dotenv()
    chatgpt_api_key = os.getenv("OPENAI_API_KEY")
    deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")

    gpt_client = OpenAI(api_key=chatgpt_api_key)
    seek_client = OpenAI(api_key=deepseek_api_key, base_url="https://api.deepseek.com")
    
    for p in target_paths:
        #if on unix like systems change this!
        try:
            full_fname = p.split('\\')[-1]
            case_fname = full_fname.split('.')[0]

            aug_tokens = case_fname.split('-AUG-')
            if len(aug_tokens) != 1:
                case_fname = aug_tokens[0]
                aug_code = aug_tokens[1]
            else:
                aug_code = "Normal"

            if case_fname not in ans_keys:
                print(f"case {case_fname} doesn't have an answer key!")
            else:
                try:
                    with open(ans_keys[case_fname], 'r') as f:
                        testcase_data = json.load(f)
                except:
                    print(case_fname, " answer key failed to load")

                is_student = testcase_data['actor'] == 'student'

                gpt_res = prompt_image_gpt(client=gpt_client, is_student=is_student, image_path=p)
                gpt_lines = gpt_res.output_text.split('\n')
                gpt_ans_line = gpt_lines[-1].removeprefix("Answer:").strip().lower()
                gpt_lines = "".join(gpt_lines[0:-1]) + gpt_ans_line

                seek_res = prompt_image_seek(client=seek_client, is_student=is_student, img_path=p, reader=reader)
                seek_lines = seek_res.choices[0].message.content.split('\n')
                
                seek_ans_line = seek_lines[-1].removeprefix("Answer:").strip().lower()
                seek_lines = "".join(seek_lines[0:-1]) + seek_ans_line
                
                if is_student:
                    if 'work' in testcase_data and len(testcase_data['work']) > 1:
                        gpt_work_sim = cos_similarity(testcase_data['work'], gpt_lines)
                        seek_work_sim = cos_similarity(testcase_data['work'], seek_lines)
                    else:
                        gpt_work_sim = 1
                        seek_work_sim = 1
 
                    gpt_correct = (gpt_work_sim >= WORK_THRESHOLD and check_math_eq(testcase_data['answer'], gpt_ans_line))
                    seek_correct = (seek_work_sim >= WORK_THRESHOLD and check_math_eq(testcase_data['answer'], seek_ans_line))

                    #I should have passed in the whole object
                    test_logger.log_gpt(full_fname, gpt_correct, aug_code, testcase_data['actor'], testcase_data['problem_type'])
                    test_logger.log_seek(full_fname, seek_correct, aug_code, testcase_data['actor'], testcase_data['problem_type'])
                else:
                    if gpt_ans_line.lower().strip() == testcase_data['answer'].lower().strip():
                        test_logger.log_gpt(full_fname, True, aug_code, testcase_data['actor'], testcase_data['problem_type'])
                        gpt_correct = True
                    else:
                        test_logger.log_gpt(full_fname, False, aug_code, testcase_data['actor'], testcase_data['problem_type'])
                        gpt_correct = False
                    
                    if seek_ans_line.lower().strip() == testcase_data['answer'].lower().strip():
                        test_logger.log_seek(full_fname, True, aug_code, testcase_data['actor'], testcase_data['problem_type'])
                        seek_correct = True
                    else:
                        test_logger.log_seek(full_fname, False, aug_code, testcase_data['actor'], testcase_data['problem_type'])
                        seek_correct = False
            cases_done += 1
            print_loading_bar(cases_done, total_cases)
            requests.post("http://localhost:5000/set_image", data={
                "path": f'./in1-3/{full_fname}',
                "gpt": gpt_res.output_text.strip(),
                "seek": seek_res.choices[0].message.content.strip(),
                "gpt_correct": gpt_correct,
                "seek_correct": seek_correct,
                "fname": full_fname
            })

        except TypeError:
            print("tescase type failed")
            

if __name__ == "__main__":
    main()
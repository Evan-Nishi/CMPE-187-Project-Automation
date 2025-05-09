from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

current_case = {'filename': None, 'gpt_res' : None, 'seek_res': None, 'gpt_correct': None, 'seek_correct': None, 'fname': None}

@app.route('/')
def index():
    return render_template('index.html',
                           image_file=current_case['filename'],
                           current_case=current_case)

@app.route('/set_image', methods=['POST'])
def set_image():
    data = request.form
    path = data.get('path')
    gpt_res = data.get('gpt')
    seek_res = data.get('seek')
    gpt_correct = data.get('gpt_correct')
    seek_correct = data.get('seek_correct')
    fname = data.get('fname')

    if path:
        current_case['filename'] = path
        current_case['gpt_res'] = gpt_res
        current_case['seek_res'] = seek_res
        current_case['gpt_correct'] = gpt_correct
        current_case['seek_correct'] = seek_correct
        current_case['fname'] = fname
    return '', 204  # No content


if __name__ == '__main__':
    app.run(debug=True)

from collections import defaultdict

from PIL import Image

from easyocr import Reader
from sentence_transformers import SentenceTransformer, util
from sympy import sympify, Eq, simplify, SympifyError


def get_text(reader : Reader, image):
    result = reader.readtext(image, detail = 0,contrast_ths=0.3, adjust_contrast=0.7)
    query = ""

    for i in result:
        query += i + "\n"
    return query

def check_math_eq(key, ans):
    #not enough info 
    stripped_a = "".join(ans.split()).lower()
    if stripped_a == 'notenoughinformation':
        return stripped_a == "".join(key.split()).lower()
    
    #direct check math equiv if possible
    try:
        ans_expr = sympify(ans)
        key_expr = sympify(key)
        if type(Eq(ans_expr, key_expr)) == bool:
            return Eq(ans_expr, key_expr)
    except SympifyError:
        #wasn't able to parse as math equiv
        pass

    #last resort to semantic similairity with high threshold
    return cos_similarity(key, ans) > 0.70


similarity_model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
def cos_similarity(ans, res):
    ans_emb = similarity_model.encode(ans, convert_to_tensor=True)
    res_emb = similarity_model.encode(res, convert_to_tensor=True)

    return util.pytorch_cos_sim(ans_emb, res_emb).item()


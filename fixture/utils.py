import string
import random

def genearte_random_string(N=5):
    try:
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=N))
    except: # python 2
        return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(N))
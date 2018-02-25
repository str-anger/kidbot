import os

Context = None

def __init__():
    global Context
    Context = Context or {'keys': {}, 'states': {}, 'data-folder': './users'}
    if not os.path.exists(Context['data-folder']):
        os.mkdir(Context['data-folder'])
from typing import Union
from stockfish import Stockfish

import fastapi
import uvicorn
import json

import sys
import os
from dotenv import load_dotenv

load_dotenv()
app = fastapi.FastAPI()

entrypoint = os.getenv('ENTRYPOINT')
if entrypoint == None:
    entrypoint = ''
else:
    if entrypoint[-1] == '/':
        entrypoint = entrypoint[:-1]

port = os.getenv('PORT')
if port == None:
    port = 30000
else:
    try:
        port = int(port)
    except:
        print('Invalid port')
        sys.exit()

"""
* x-FEN
  x-config = {}
  x-depth  = 15

return evaluation point white side
"""
@app.get(f'{entrypoint}/eval')
async def eval(x_FEN: Union[str, None] = fastapi.Header(default=None), x_config: Union[str, None] = fastapi.Header(default=None), x_depth: Union[str, None] = fastapi.Header(default=None)):
    if x_depth == None:
        x_depth = 15
    if x_config == None:
        x_config = '{}'

    try:
        x_config = json.loads(x_config)
    except:
        return { "error": 'Invalid config' }
    try:
        x_depth = int(x_depth)
    except:
        return { "error": 'Invalid depth' }

    littlefish = Stockfish(depth=x_depth, parameters=x_config)

    if x_FEN == None:
        return { "error": 'Any FEN found' }
    if not littlefish.is_fen_valid(x_FEN):
        return { "error": 'Invalid FEN'}

    littlefish.set_fen_position(x_FEN)
    return { "response": littlefish.get_evaluation() }

"""
* x-FEN
  x-config = {}
  x-depth  = 15

return best move
"""
@app.get(f'{entrypoint}/best')
async def best(x_FEN: Union[str, None] = fastapi.Header(default=None), x_config: Union[str, None] = fastapi.Header(default=None), x_depth: Union[str, None] = fastapi.Header(default=None)):
    if x_depth == None:
        x_depth = 15
    if x_config == None:
        x_config = '{}'

    try:
        x_config = json.loads(x_config)
    except:
        return { "error": 'Invalid config' }
    try:
        x_depth = int(x_depth)
    except:
        return { "error": 'Invalid depth' }

    littlefish = Stockfish(depth=x_depth, parameters=x_config)

    if x_FEN == None:
        return { "error": 'Any FEN found' }
    if not littlefish.is_fen_valid(x_FEN):
        return { "error": 'Invalid FEN'}

    littlefish.set_fen_position(x_FEN)
    return { "response": littlefish.get_best_move() }

"""
* x-FEN
  x-config = {}
  x-depth  = 15
  x-count  = 3

return top moves
"""
@app.get(f'{entrypoint}/top')
async def top(x_FEN: Union[str, None] = fastapi.Header(default=None), x_config: Union[str, None] = fastapi.Header(default=None), x_depth: Union[str, None] = fastapi.Header(default=None), x_count: Union[str, None] = fastapi.Header(default=None)):
    if x_depth == None:
        x_depth = 15
    if x_config == None:
        x_config = '{}'
    if x_count == None:
        x_count = 3

    try:
        x_config = json.loads(x_config)
    except:
        return { "error": 'Invalid config' }
    try:
        x_depth = int(x_depth)
    except:
        return { "error": 'Invalid depth' }
    try:
        x_count = int(x_count)
    except:
        return { "error": 'Invalid count' }

    littlefish = Stockfish(depth=x_depth, parameters=x_config)

    if x_FEN == None:
        return { "error": 'Any FEN found' }
    if not littlefish.is_fen_valid(x_FEN):
        return { "error": 'Invalid FEN'}

    littlefish.set_fen_position(x_FEN)
    return { "response": littlefish.get_top_moves(x_count) }

"""
* x-FEN
* x-ELO | x-LVL
* x-depth  = 15
  x-config = {}

return AI play
"""
@app.get(f'{entrypoint}/play')
async def play(x_FEN: Union[str, None] = fastapi.Header(default=None), x_ELO: Union[str, None] = fastapi.Header(default=None), x_LVL: Union[str, None] = fastapi.Header(default=None), x_config: Union[str, None] = fastapi.Header(default=None), x_depth: Union[str, None] = fastapi.Header(default=None)):
    if x_depth == None:
        return { "error": 'Invalid depth' }
    if x_config == None:
        x_config = '{}'

    try:
        x_config = json.loads(x_config)
    except:
        return { "error": 'Invalid config' }
    try:
        x_depth = int(x_depth)
    except:
        return { "error": 'Invalid depth' }

    littlefish = Stockfish(depth=x_depth, parameters=x_config)

    if x_ELO == None and x_LVL == None:
        return { "error": 'Invalid ELO and level' }
    elif x_ELO != None:
        try:
            x_ELO = int(x_ELO)
            littlefish.set_elo_rating(x_ELO)
        except:
            return { "error": 'Invalid ELO' }
    else:
        try:
            x_LVL = int(x_LVL)
            littlefish.set_skill_level(x_LVL)
        except:
            return { "error": 'Invalid level' }

    if x_FEN == None:
        return { "error": 'Any FEN found' }
    if not littlefish.is_fen_valid(x_FEN):
        return { "error": 'Invalid FEN'}

    littlefish.set_fen_position(x_FEN)
    return { "response": littlefish.get_best_move() }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=port)

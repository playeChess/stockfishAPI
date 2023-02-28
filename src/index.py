from typing import Union
from stockfish import Stockfish

import fastapi
import uvicorn
import json

app = fastapi.FastAPI()

"""
* x-FEN
  x-config = {}
  x-depth  = 15

return evaluation point white side
"""
@app.get('/eval')
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
@app.get('/best')
async def best(x_FEN: Union[str, None] = fastapi.Header(default=None), x_config: Union[str, None] = fastapi.Header(default=None), x_depth: Union[str, None] = fastapi.Header(default=None)):
    return {}

"""
* x-FEN
  x-config = {}
  x-depth  = 15
  x-count  = 3

return top moves
"""
@app.get('/top')
async def top(x_FEN: Union[str, None] = fastapi.Header(default=None), x_config: Union[str, None] = fastapi.Header(default=None), x_depth: Union[str, None] = fastapi.Header(default=None), x_count: Union[str, None] = fastapi.Header(default=None)):
    return {}

"""
* x-FEN
* x-ELO | x-LVL
  x-config = {}
  x-depth  = 15
  x-count  = 3
"""
@app.get('/play')
async def play(x_FEN: Union[str, None] = fastapi.Header(default=None), x_ELO: Union[str, None] = fastapi.Header(default=None), x_LVL: Union[str, None] = fastapi.Header(default=None), x_config: Union[str, None] = fastapi.Header(default=None), x_depth: Union[str, None] = fastapi.Header(default=None), x_count: Union[str, None] = fastapi.Header(default=None)):
    return {}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=30000)

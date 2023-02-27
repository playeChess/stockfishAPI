require('dotenv').config();

const app = require('express')();
const { exec } = require('child_process');
const { stderr } = require('process');

/*
/eval       :
return eval (fen) as points

/best_move  :
return best move

*/

let entrypoint = process.env.ENTRYPOINT;
if (entrypoint.endsWith('/')) 
    entrypoint = entrypoint.slice(0, -1);

app.get(`${entrypoint}/eval`, async (req, res) => {
    //const FEN = JSON.parse(req.headers['x-FEN']);

    var datas = '';

    var append = (c) => {
        datas += c
    }

    let child = exec('stockfish');
    let cmds = ['position fen 4k2r/6r1/8/8/8/8/3R4/R3K3 w Qk - 0 1', 'd'];
    child.stdout.on('data', function (stdout) {
        //console.log(stdout);
        append(stdout)
    })
    child.stdin.write(cmds.join('\n'));
    child.stdin.end();

    child.on('exit', function () {
        res.send(datas)
    });
})

app.listen(process.env.PORT, () => {
    console.log(`🐟 Stockfish API listening on :${process.env.PORT}/${entrypoint}`)
});
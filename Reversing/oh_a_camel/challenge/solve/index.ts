const sleep = (delay: number) => new Promise(_ => setTimeout(_, delay));

const solveMaze = (maze: Array<Array<number>>, result: Array<string>, current: [number, number], visited: Set<string>): boolean => {
    const [x, y] = current;

    if(x === 64 && y === 64) {
        return true;
    }

    if(visited.has(`${x},${y}`)) {
        return false;
    }

    visited.add(`${x},${y}`);

    let deltas: Array<[string, number, number]> = [['L', -1, 0], ['R', 1, 0], ['U', 0, -1], ['D', 0, 1]];
    for(let [dir, dx, dy] of deltas) {
        let nx = x + dx;
        let ny = y + dy;

        if(nx < 0 || ny < 0 || nx >= 65 || ny >= 65 || maze[ny][nx] === 0) {
            continue;
        }

        if(solveMaze(maze, result, [nx, ny], visited)) {
            result.push(dir);
            return true;
        }
    }

    return false;
};

const main = async () => {
    console.log('entry');
    await sleep(1000);
    console.log('slept');
    const isPositionLegalAddress = DebugSymbol.fromName('camlDune__exe__Main__is_position_legal_84').address;
    console.log(`Original function at: ${isPositionLegalAddress}`);
    const isPositionLegal_wrapper = Memory.alloc(Process.pageSize);
    Memory.protect(isPositionLegal_wrapper, Process.pageSize, 'rwx');
    console.log(`Wrapper at: ${isPositionLegal_wrapper}`);
    Memory.patchCode(isPositionLegal_wrapper, 64, code => {
        const cw = new X86Writer(code, { pc: isPositionLegal_wrapper });

        cw.putMovRegReg('rax', 'rdi');
        cw.putShlRegU8('rax', 1);
        cw.putAddRegImm('rax', 1);
        cw.putMovRegReg('rbx', 'rsi');
        cw.putShlRegU8('rbx', 1);
        cw.putAddRegImm('rbx', 1);
        cw.putCallAddress(isPositionLegalAddress);
        cw.putShrRegU8('rax', 1);
        cw.putRet();
        cw.flush();
    });

    const isPositionLegal = new NativeFunction(isPositionLegal_wrapper, 'bool', ['uint64', 'uint64']);
    const maze = new Array(65);

    for(let y = 0; y < 65; y++) {
        maze[y] = new Array(65);
        for(let x = 0; x < 65; x++) {
            maze[y][x] = isPositionLegal(x, y);
        }
    }

    const result = new Array();
    solveMaze(maze, result, [0, 0], new Set());
    const path = result.reverse().join('');
    console.log(`The path is: ${path}`);
};

main();
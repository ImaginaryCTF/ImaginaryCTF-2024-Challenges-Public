const { chromium } = require('playwright-chromium');
const fs = require('fs');
const net = require('net');

const FLAG = fs.readFileSync('flag.txt', 'utf8').replace(/\s/g, '');

(async function () {
  const browser = await chromium.launch({
    chromiumSandbox: true,
    logger: {
      isEnabled: () => true,
      log: (name, severity, message, _args) => console.log(`chrome log: [${name}/${severity}] ${message}`)
    }
  });

  function ask_for_url(socket) {
    socket.state = 'URL';
    socket.write('Please send me a URL to open: ');
  }

  async function load_url(socket, data) {
    let url = data.toString().trim();
    console.log(`checking url: ${url}`);
    if (!url.startsWith('http://') && !url.startsWith('https://')) {
      socket.state = 'ERROR';
      socket.write('Invalid scheme (http/https only).\n');
      socket.destroy();
      return;
    }
    socket.state = 'LOADED';

    const context = await browser.newContext();
    const page = await context.newPage();
    socket.write(`Loading page ${url}.\n`);

    await page.goto('https://heapnotes.chal.imaginaryctf.org/login');

    await page.getByLabel('username').fill(FLAG);
    await page.getByLabel('password').fill(FLAG);
    await page.getByRole('button').dispatchEvent('click');

    await page.waitForNavigation();

    await page.goto(url);

    setTimeout(() => {
      try {
        page.close();
        socket.write('timeout\n');
        socket.destroy();
      } catch (err) {
        console.log(`err: ${err}`);
      }
    }, 10000);
  }

  var server = net.createServer();
  server.listen(1338)
  console.log('listening on port 1338');

  server.on('connection', socket => {
    socket.on('data', data => {
      try {
        if (socket.state == 'URL') {
          load_url(socket, data);
        }
      } catch (err) {
        console.log(`err: ${err}`);
      }
    });

    try {
      ask_for_url(socket);
    } catch (err) {
      console.log(`err: ${err}`);
    }
  });
})();

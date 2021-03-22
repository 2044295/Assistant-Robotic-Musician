const { app, BrowserWindow, ipcMain } = require('electron')
const PythonShell = require('python-shell').PythonShell;

function createWindow () {
  const win = new BrowserWindow({
    width: 1440,
    height: 900,
    webPreferences: {
      nodeIntegration: true
    }
  })

  win.loadFile('assets/html/0landingpage.html');
  ipcMain.on('asynchronous-message', (event, arg) => {                          // https://www.electronjs.org/docs/api/ipc-main
    if (arg == "home") { win.loadFile('assets/html/0landingpage.html'); }
    if (arg == "newfile") { win.loadFile('assets/html/1editpage.html'); }
    if (arg == "playpage") { win.loadFile('assets/html/2playpage.html'); }
    if (arg == "loadfile") {
      let options = {args: ['samples/sampleSimple.smml'], mode: 'json'}         // will need to be customizable later
      let pyshell = new PythonShell('./assets/scripts/file_track.py', options);
      pyshell.on('message', (message) => {
        win.webContents.send('new_node', message);                              // broken somehow -- https://www.electronjs.org/docs/api/web-contents#contentssendchannel-args
      });
    }
    event.returnValue = 1;
  })
}

// This function (trackFile) fully works -- it's up to Saketh to implement -- I'm realizing we'll need error handling
// What I'm thinking is that you start by just displaying four measures on every
// page -- that way you can consistently calculate when to turn the page
function trackSMML(filename) {
  let options = {args: [filename], mode: 'json'}
  let pyshell = new PythonShell('./assets/scripts/file_track.py', options);
  pyshell.on('message', (message) => {
    win.webContents.send('new_node', message);
  });
}

app.whenReady().then(createWindow)
app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit()
  }
})
app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow()
  }
})

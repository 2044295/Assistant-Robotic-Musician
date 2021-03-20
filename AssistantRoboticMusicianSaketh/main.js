const { app, BrowserWindow } = require('electron')
const PythonShell = require('python-shell').PythonShell;

function createWindow () {
  const win = new BrowserWindow({
    width: 1440,
    height: 900,
    webPreferences: {
      nodeIntegration: true
    }
  })

  win.loadFile('0landingpage.html')
}

function loadFile(filename) {
  let options = {args: [filename], mode: 'json'}
  let pyshell = new PythonShell('scripts/file_load.py', options);
  pyshell.on('message', (message) => {
    console.log(message);
  });
}

function trackFile(filename) {
  let options = {args: [filename], mode: 'json'}
  let pyshell = new PythonShell('scripts/file_track.py', options);
  pyshell.on('message', (message) => {
    console.log(message);
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

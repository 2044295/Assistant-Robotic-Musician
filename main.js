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

  win.loadFile('assets/html/0landingpage.html');
  loadSMML('samples/sampleBach.html'); // replace with communication with play page
  trackSMML('samples/sampleSimple.html'); // replace with communication with play page
  console.log('Testing asynchronous functionality - it works');
}

// This function fully works
function loadSMML(filename) {
  let options = {args: [filename], mode: 'json'}
  let pyshell = new PythonShell('./assets/scripts/file_load.py', options);
  pyshell.on('message', (message) => {
    console.log(message); // replace with communication with play page
  });
}

// This function (trackFile) fully works -- it's up to Saketh to implement -- I'm realizing we'll need error handling
// What I'm thinking is that you start by just displaying four measures on every
// page -- that way you can consistently calculate when to turn the page
function trackSMML(filename) {
  let options = {args: [filename], mode: 'json'}
  let pyshell = new PythonShell('./assets/scripts/file_track.py', options);
  pyshell.on('message', (message) => {
    console.log(message); // replace with communication with play page
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

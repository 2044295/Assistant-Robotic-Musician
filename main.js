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
  // Set Up Cross-Communication https://www.electronjs.org/docs/api/ipc-main
  ipcMain.on('load-page', (event, arg) => {
    if (arg == "home") { win.loadFile('assets/html/0landingpage.html'); }
    if (arg == "newFile") { win.loadFile('assets/html/1editpage.html'); }
    if (arg == "playPage") { win.loadFile('assets/html/2playpage.html'); }
    event.returnValue = 1;
  });
  ipcMain.on('loadFile', (event, filename) => {
    let options = {args: [filename], mode: 'json'}
    let pyshell = new PythonShell('./assets/scripts/file_load.py', options);
    pyshell.on('message', (message) => {
      console.log(message);
      win.webContents.send('data', message);
    });
  });
  ipcMain.on('trackFile', (event, filename) => {                                // lacks any error handling
    let options = {args: [filename], mode: 'json'}
    let pyshell = new PythonShell('./assets/scripts/file_track.py', options);
    pyshell.on('message', (message) => {
      win.webContents.send('new_node', message);
    });
  });
  ipcMain.on('testFile', (event, filename) => {                                 // lacks any error handling
    let options = {args: [filename], mode: 'json'}
    let pyshell = new PythonShell('./assets/scripts/file_test.py', options);
    pyshell.on('message', (message) => {
      win.webContents.send('new_node', message);
    });
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

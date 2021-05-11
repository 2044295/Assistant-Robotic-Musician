const { ipcRenderer } = require('electron');
function goHome() { ipcRenderer.send('load-page', 'home'); }
function newFile() { ipcRenderer.send('load-page', 'newFile'); }
function playPage() { ipcRenderer.send('load-page', 'playPage'); }
function loadFile(filename) { ipcRenderer.send('loadFile', filename); }
function trackFile(filename) { ipcRenderer.send('trackFile', filename); }
function testFile(filename) { ipcRenderer.send('testFile', filename); }

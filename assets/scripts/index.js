const { ipcRenderer } = require('electron');
function gohome() { ipcRenderer.send('asynchronous-message', 'home'); }
function newfile() { ipcRenderer.send('asynchronous-message', 'newfile'); }
function playpage() { ipcRenderer.send('asynchronous-message', 'playpage'); }
function loadfile() { ipcRenderer.send('asynchronous-message', 'loadfile'); }

/* eslint-disable space-before-function-paren */
/* global XMLHttpRequest */

function GET(url) {
  var xmlHttp = new XMLHttpRequest();

  console.log(`Making GET request to ${url}`);
  xmlHttp.open('GET', url, false); // false for synchronous
  xmlHttp.send(null);

  return xmlHttp.responseText;
}

function ls(lsdir) {
  console.log(`ls request for ${lsdir}`);

  if (lsdir[0] === '/') lsdir = lsdir.slice(1, lsdir.length);
  var url = new URL(lsdir, window.location.origin + '/ls/');

  console.log(`determined ls url: ${url}`);
  return GET(url);
}

function setProperties(lsRes, title, url, dirs, files) {
  title.innerText = 'File Explorer: ' + lsRes.url;

  var URLlink = document.createElement('a');
  URLlink.href = new URL(lsRes.url, window.location.origin);
  URLlink.innerText = lsRes.url;
  url.appendChild(URLlink);

  lsRes.directories.forEach(dir => {
    var dirLink = document.createElement('a');
    dirLink.href = new URL(lsRes.url + dir, window.location.origin);
    dirLink.innerText = dir + '/';
    dirs.appendChild(dirLink);
    dirs.appendChild(document.createElement('br'));
  });

  lsRes.files.forEach(file => {
    var fileLink = document.createElement('a');
    fileLink.href = new URL(lsRes.url + file, window.location.origin);
    fileLink.innerText = file;
    files.appendChild(fileLink);
    files.appendChild(document.createElement('br'));
  });
}

var lsRes = JSON.parse(ls(window.location.pathname));

console.log(lsRes);

setProperties(
  lsRes,
  document.getElementById('title'),
  document.getElementById('URL'),
  document.getElementById('dirs'),
  document.getElementById('files')
);

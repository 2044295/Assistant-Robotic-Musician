/* eslint-disable space-before-function-paren */

/**
 *
 * Makes a GET request to the specified URL and returns the result
 *
 * @param {str} url The URL to which the GET request is made
 * @return {str} Returns the response text of the GET request
 *
 */
function get(url) {
  let xmlHttp = new XMLHttpRequest();

  console.log(`Making GET request to ${url}`);
  xmlHttp.open('GET', url, false); // false for synchronous
  xmlHttp.send(null);

  return xmlHttp.responseText;
}

/**
 *
 * Makes a GET request of the /ls/ subdirectory for a specific path
 *
 * @see {get}
 * @param {str} lsdir The path to the directory for which the ls request is made
 * @return {str} Returns the response text of the get request
 */
function ls(lsdir) {
  console.log(`ls request for ${lsdir}`);

  if (lsdir[0] === '/') lsdir = lsdir.slice(1, lsdir.length);
  let url = new URL(lsdir, window.location.origin + '/ls/');

  console.log(`determined ls url: ${url}`);
  return get(url);
}

/**
 *
 * Edits the page HTML to display a "file explorer page", using "ls" results
 *
 * @see {ls}
 * @param {JSON} lsRes The JSON returned by "ls", should be parsed
 * @param {Element} title The "title" element to be written to
 * @param {Element} url The "url" div to be written to
 * @param {Element} dirs The "dirs" div to be written to
 * @param {Element} files The "files" div to be written to
 */
function setProperties(lsRes, title, url, dirs, files) {
  title.innerText = 'File Explorer: ' + lsRes.url;

  let URLlink = document.createElement('a');
  URLlink.href = new URL(lsRes.url, window.location.origin);
  URLlink.innerText = lsRes.url;
  url.appendChild(URLlink);

  lsRes.directories.forEach((dir) => {
    let dirname = dir + '/';
    let dirLink = document.createElement('a');
    dirLink.href = new URL(lsRes.url + dirname, window.location.origin);
    dirLink.innerText = dirname;
    dirs.appendChild(dirLink);
    dirs.appendChild(document.createElement('br'));
  });

  lsRes.files.forEach((file) => {
    let fileLink = document.createElement('a');
    fileLink.href = new URL(lsRes.url + file, window.location.origin);
    fileLink.innerText = file;
    files.appendChild(fileLink);
    files.appendChild(document.createElement('br'));
  });
}

let lsRes = JSON.parse(ls(window.location.pathname));

console.log(lsRes);

setProperties(
    lsRes,
    document.getElementById('title'),
    document.getElementById('URL'),
    document.getElementById('dirs'),
    document.getElementById('files')
);

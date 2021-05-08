function staffchange() {
  var r = document.querySelector(':root');
  var rs = getComputedStyle(r);
  var foo = rs.getPropertyValue('--staffwidth');
  if (foo == '0%') {
    r.style.setProperty('--staffwidth', '31%');
    let divvl = document.createElement('div');
    divvl.className = 'vl';
    document.body.appendChild(divvl);
    let divvlm1 = document.createElement('div');
    divvlm1.className = 'vlm1';
    document.body.appendChild(divvlm1);
  }
  else if (foo == '31%') {
    r.style.setProperty('--staffwidth', '54%');
    let divvlm2 = document.createElement('div');
    divvlm2.className = 'vlm2';
    document.body.appendChild(divvlm2);
  }
  else if (foo == '54%') {
    r.style.setProperty('--staffwidth', '77%');
    let divvlm3 = document.createElement('div');
    divvlm3.className = 'vlm3';
    document.body.appendChild(divvlm3);
  }
  else if (foo == '77%') {
    r.style.setProperty('--staffwidth', '100%');
    let divvlmend1 = document.createElement('div');
    divvlmend1.className = 'vlmend1';
    document.body.appendChild(divvlmend1);
    let divvlmend2 = document.createElement('div');
    divvlmend2.className = 'vlmend2';
    document.body.appendChild(divvlmend2);
  }
  else {
    console.log([foo]);
  }
}

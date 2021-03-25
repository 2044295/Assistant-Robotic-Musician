function noteAdd() {
  var notelength = window.prompt("Length");
  var notepitch = window.prompt("Pitch");
  if (notelength == "4") {
    var whole = document.createElement("img");
    whole.src = "./Notes/semibreve.png";
    whole.style.maxWidth = "1%";
    whole.style.position = "relative";
    document.getElementById("notes").appendChild(whole);
    if (notepitch == "D4") {
      whole.style.marginTop = "205px";
    }
    else if (notepitch == "E4") {
      whole.style.marginTop = "200px";
    }
    else if (notepitch == "F4") {
      whole.style.marginTop = "195px";
    }
    else if (notepitch == "G4") {
      whole.style.marginTop = "190px";
    }
    else if (notepitch == "A4") {
      whole.style.marginTop = "185px";
    }
    else if (notepitch == "B4") {
      whole.style.marginTop = "180px";
    }
    else if (notepitch == "C5") {
      whole.style.marginTop = "175px";
    }
    else if (notepitch == "D5") {
      whole.style.marginTop = "170px";
    }
    else if (notepitch == "E5") {
      whole.style.marginTop = "165px";
    }
    else if (notepitch == "F5") {
      whole.style.marginTop = "160px";
    }
    else if (notepitch == "G5") {
      whole.style.marginTop = "155px";
    }
  }

  else if (notelength == "2") {
    var half = document.createElement("img");
    half.src = "./Notes/minim.png";
    half.style.maxWidth = "2.5%";
    half.style.marginTop = "10%";
    half.style.position = "relative";
    document.getElementById("notes").appendChild(half);
    if (notepitch == "D4") {
      half.style.marginTop = "175px";
    }
    else if (notepitch == "E4") {
      half.style.marginTop = "170px";
    }
    else if (notepitch == "F4") {
      half.style.marginTop = "165px";
    }
    else if (notepitch == "G4") {
      half.style.marginTop = "160px";
    }
    else if (notepitch == "A4") {
      half.style.marginTop = "155px";
    }
    else if (notepitch == "B4") {
      half.style.marginTop = "150px";
    }
    else if (notepitch == "C5") {
      half.style.marginTop = "145px";
    }
    else if (notepitch == "D5") {
      half.style.marginTop = "140px";
    }
    else if (notepitch == "E5") {
      half.style.marginTop = "135px";
    }
    else if (notepitch == "F5") {
      half.style.marginTop = "130px";
    }
    else if (notepitch == "G5") {
      half.style.marginTop = "125px";
    }
  }
  else if (notelength == "1") {
    var quarter = document.createElement("img");
    quarter.src = "./Notes/crotchet.png";
    quarter.style.maxWidth = "2.5%";
    quarter.style.marginTop = "20%";
    quarter.style.position = "relative";
    document.getElementById("notes").appendChild(quarter);
    if (notepitch == "D4") {
      quarter.style.marginTop = "175px";
    }
    else if (notepitch == "E4") {
      quarter.style.marginTop = "170px";
    }
    else if (notepitch == "F4") {
      quarter.style.marginTop = "165px";
    }
    else if (notepitch == "G4") {
      quarter.style.marginTop = "160px";
    }
    else if (notepitch == "A4") {
      quarter.style.marginTop = "155px";
    }
    else if (notepitch == "B4") {
      quarter.style.marginTop = "150px";
    }
    else if (notepitch == "C5") {
      quarter.style.marginTop = "145px";
    }
    else if (notepitch == "D5") {
      quarter.style.marginTop = "140px";
    }
    else if (notepitch == "E5") {
      quarter.style.marginTop = "135px";
    }
    else if (notepitch == "F5") {
      quarter.style.marginTop = "130px";
    }
    else if (notepitch == "G5") {
      quarter.style.marginTop = "125px";
    }
  }
  else if (notelength == "1/2") {
    var eighth = document.createElement("img");
    eighth.src = "./Notes/quaver.png";
    eighth.style.maxWidth = "2.5%";
    eighth.style.marginTop = "20%";
    eighth.style.position = "relative";
    document.getElementById("notes").appendChild(eighth);
    if (notepitch == "D4") {
      eighth.style.marginTop = "174px";
    }
    else if (notepitch == "E4") {
      eighth.style.marginTop = "169px";
    }
    else if (notepitch == "F4") {
      eighth.style.marginTop = "164px";
    }
    else if (notepitch == "G4") {
      eighth.style.marginTop = "159px";
    }
    else if (notepitch == "A4") {
      eighth.style.marginTop = "154px";
    }
    else if (notepitch == "B4") {
      eighth.style.marginTop = "149px";
    }
    else if (notepitch == "C5") {
      eighth.style.marginTop = "144px";
    }
    else if (notepitch == "D5") {
      eighth.style.marginTop = "139px";
    }
    else if (notepitch == "E5") {
      eighth.style.marginTop = "134px";
    }
    else if (notepitch == "F5") {
      eighth.style.marginTop = "129px";
    }
    else if (notepitch == "G5") {
      eighth.style.marginTop = "124px";
    }
  }
  else if (notelength == "1/4") {
    var sixteenth = document.createElement("img");
    sixteenth.src = "./Notes/semiquaver.png";
    sixteenth.style.maxWidth = "1.5%";
    sixteenth.style.marginTop = "20%";
    sixteenth.style.position = "relative";
    document.getElementById("notes").appendChild(sixteenth);
    if (notepitch == "D4") {
      sixteenth.style.marginTop = "173px";
    }
    else if (notepitch == "E4") {
      sixteenth.style.marginTop = "168px";
    }
    else if (notepitch == "F4") {
      sixteenth.style.marginTop = "163px";
    }
    else if (notepitch == "G4") {
      sixteenth.style.marginTop = "158px";
    }
    else if (notepitch == "A4") {
      sixteenth.style.marginTop = "153px";
    }
    else if (notepitch == "B4") {
      sixteenth.style.marginTop = "148px";
    }
    else if (notepitch == "C5") {
      sixteenth.style.marginTop = "143px";
    }
    else if (notepitch == "D5") {
      sixteenth.style.marginTop = "138px";
    }
    else if (notepitch == "E5") {
      sixteenth.style.marginTop = "133px";
    }
    else if (notepitch == "F5") {
      sixteenth.style.marginTop = "128px";
    }
    else if (notepitch == "G5") {
      sixteenth.style.marginTop = "123px";
    }
  }
  else if (notelength == "1/8") {
    var thirtysecond = document.createElement("img");
    thirtysecond.src = "./Notes/demisemiquaver.png";
    thirtysecond.style.maxWidth = "1.25%";
    thirtysecond.style.marginTop = "20%";
    thirtysecond.style.position = "relative";
    document.getElementById("notes").appendChild(thirtysecond);
    if (notepitch == "D4") {
      thirtysecond.style.marginTop = "170px";
    }
    else if (notepitch == "E4") {
      thirtysecond.style.marginTop = "165px";
    }
    else if (notepitch == "F4") {
      thirtysecond.style.marginTop = "160px";
    }
    else if (notepitch == "G4") {
      thirtysecond.style.marginTop = "155px";
    }
    else if (notepitch == "A4") {
      thirtysecond.style.marginTop = "150px";
    }
    else if (notepitch == "B4") {
      thirtysecond.style.marginTop = "145px";
    }
    else if (notepitch == "C5") {
      thirtysecond.style.marginTop = "140px";
    }
    else if (notepitch == "D5") {
      thirtysecond.style.marginTop = "135px";
    }
    else if (notepitch == "E5") {
      thirtysecond.style.marginTop = "130px";
    }
    else if (notepitch == "F5") {
      thirtysecond.style.marginTop = "125px";
    }
    else if (notepitch == "G5") {
      thirtysecond.style.marginTop = "120px";
    }
  }
}

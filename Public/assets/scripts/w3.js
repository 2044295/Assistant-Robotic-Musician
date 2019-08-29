// Script to open and close sidebar
function SidebarToggle() {
  mySidebar = document.getElementById("mySidebar")
  myOverlay = document.getElementById("myOverlay")
  if ((mySidebar.style.display === "block") || (myOverlay.style.display = "block")) {
    mySidebar.style.display = "none";
    myOverlay.style.display = "none";
  } else {
    mySidebar.style.display = "block";
    myOverlay.style.display = "block";
  }
}

function Stem2Toggle() {
  let dropdown = document.getElementById("stem-2-dropdown")
  if (dropdown.style.display === "block") {
    dropdown.style.display = "none"
  } else {
    dropdown.style.display = "block"
  }
}

// Modal Image Gallery
function onClick(element) {
  document.getElementById("img01").src = element.src;
  document.getElementById("modal01").style.display = "block";
  var captionText = document.getElementById("caption");
  captionText.innerHTML = element.alt;
}

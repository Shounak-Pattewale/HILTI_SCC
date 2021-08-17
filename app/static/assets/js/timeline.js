
var downArrow = document.getElementById("btn1");
var upArrow = document.getElementById("btn2");

downArrow.onclick = function () {
    'use strict';
    document.getElementById("first-list").style = "top:-620px";
    document.getElementById("second-list").style = "top:-620px";
    downArrow.style = "display:none";
    upArrow.style = "display:block";
};

upArrow.onclick = function () {
    'use strict';
    document.getElementById("first-list").style = "top:0";
    document.getElementById("second-list").style = "top:80px";
    upArrow.style = "display:none";
    downArrow.style = "display:block";
};

photo.onmouseover = function() {
  this.style.transform = "scale(1.1,1.1)";
  this.style.boxShadow = "5px 5px 15px #000";
};

photo.onmouseout = function() {
  this.style.transform = "scale(1,1)";
  this.style.boxShadow = "none";
};
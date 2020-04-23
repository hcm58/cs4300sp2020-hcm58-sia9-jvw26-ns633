
function show() {
  var document = "app/templates/search.html"
  var x = document.getElementById("results");
  if (x.style.display === "none") {
    x.style.display = "block";
  } else {
    x.style.display = "none";
  }
}

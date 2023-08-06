let ColorField = (function(window) {
  let colorFieldArr = [];

  function init() {
    colorFieldArr = document.querySelectorAll(".morris-hexcolor");

    for (var i = 0, len = colorFieldArr.length; i < len; i++) {
      const field = colorFieldArr[i];
      updateColor(field);
      field.addEventListener("input", updateColor);
    }
  }

  const hexRegex = /^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$/
  function isValidHexColor(text) {
    return !!hexRegex.exec(text);
  }

  function makeBgImage(color) {
    return "linear-gradient(to left, " + color + " 5ch, white 5ch)";
  }

  function updateColor(field) {
    field = field.target || field;
    const color = field.value;
    let bgImage = null;
    if (isValidHexColor(color)) {
      bgImage = makeBgImage(color);
    }
    field.style["background-image"] = bgImage;
  }

  return {
    init,
  }
}(window));

window.addEventListener("load", function (ev) {
  if (typeof django !== "undefined") {
    (function() {
        ColorField.init();
    })();
  }
});

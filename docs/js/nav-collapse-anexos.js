(function () {
  function collapseAnexos() {
    var links = document.querySelectorAll("label.md-nav__link");
    links.forEach(function (label) {
      if (label.textContent.trim() !== "Anexos") {
        return;
      }

      var toggleId = label.getAttribute("for");
      if (!toggleId) {
        return;
      }

      var toggle = document.getElementById(toggleId);
      if (toggle && toggle.type === "checkbox") {
        toggle.checked = false;
      }
    });
  }

  if (window.document$ && typeof window.document$.subscribe === "function") {
    window.document$.subscribe(collapseAnexos);
  } else {
    document.addEventListener("DOMContentLoaded", collapseAnexos);
  }
})();

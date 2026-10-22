(function () {
  var root = document.documentElement;
  try {
    var q = new URLSearchParams(location.search);
    if (q.get("theme")) root.setAttribute("data-theme", q.get("theme"));
    if (q.get("view") === "dev") document.body.classList.add("dev");
  } catch (e) {}
  var toggle = document.getElementById("view-toggle");
  if (toggle) toggle.addEventListener("click", function () {
    var on = document.body.classList.toggle("dev");
    toggle.setAttribute("aria-pressed", on ? "true" : "false");
  });
  document.querySelectorAll("[data-filter]").forEach(function (b) {
    b.addEventListener("click", function () {
      var s = b.getAttribute("data-filter");
      document.querySelectorAll("[data-filter]").forEach(function (x) { x.classList.toggle("on", x === b); });
      document.querySelectorAll("tr[data-status]").forEach(function (r) {
        r.hidden = s !== "all" && r.getAttribute("data-status") !== s;
      });
    });
  });
  function done(b) { b.textContent = b.getAttribute("data-done"); }
  document.querySelectorAll("button.copy").forEach(function (b) {
    b.addEventListener("click", function () {
      var text = b.getAttribute("data-text");
      var fallback = function () {
        var a = document.createElement("textarea");
        a.value = text; document.body.appendChild(a); a.select();
        try { document.execCommand("copy"); done(b); } catch (e) {}
        a.remove();
      };
      if (navigator.clipboard) navigator.clipboard.writeText(text).then(function () { done(b); }, fallback);
      else fallback();
    });
  });
})();

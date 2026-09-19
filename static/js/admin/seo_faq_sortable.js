// Drag-and-drop ordering for FAQs on the SEO Page admin form.
// Dragging sets each FAQ's hidden "rank" field to its position in the list.
document.addEventListener("DOMContentLoaded", function () {
  var group = document.getElementById("faqs-group");
  if (!group || typeof Sortable === "undefined") return; // fall back to the visible rank field

  var list = group.querySelector("fieldset.module");
  group.classList.add("faq-sortable");

  function isBlank(form) {
    var question = form.querySelector('textarea[name$="-question"]');
    var answer = form.querySelector('textarea[name$="-answer"]');
    return (!question || !question.value.trim()) && (!answer || !answer.value.trim());
  }

  // Header labels (#1, #2, ...) follow list order. Rank is written only for
  // filled-in forms, so blank extra forms stay unused in Django's eyes.
  function renumber() {
    var position = 1;
    var rankPosition = 1;
    list.querySelectorAll(".inline-related:not(.empty-form)").forEach(function (form) {
      var label = form.querySelector(".inline_label");
      if (label) label.textContent = "#" + position++;

      var rank = form.querySelector('input[name$="-rank"]');
      if (!rank || isBlank(form)) return;
      rank.value = rankPosition++;
    });
  }

  Sortable.create(list, {
    draggable: ".inline-related:not(.empty-form)",
    handle: "h3",
    animation: 150,
    ghostClass: "faq-sortable-ghost",
    onEnd: renumber,
  });

  renumber();

  // Django relabels rows by form index after add/remove; restore list order afterwards.
  ["formset:added", "formset:removed"].forEach(function (eventName) {
    document.addEventListener(eventName, function () {
      setTimeout(renumber, 0);
    });
  });

  var form = group.closest("form");
  if (form) form.addEventListener("submit", renumber);
});

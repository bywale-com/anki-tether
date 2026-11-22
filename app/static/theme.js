(() => {
  const key = "anki-tether-theme";
  const root = document.documentElement;
  const apply = (choice) => {
    if (choice === "light" || choice === "dark") {
      root.dataset.theme = choice;
      return choice;
    }
    delete root.dataset.theme;
    return "system";
  };

  try {
    apply(localStorage.getItem(key));
  } catch {
    // The system theme still works when browser storage is unavailable.
  }

  window.addEventListener("DOMContentLoaded", () => {
    const picker = document.getElementById("theme");
    picker.value = root.dataset.theme || "system";
    picker.hidden = false;

    picker.addEventListener("change", () => {
      const theme = apply(picker.value);
      try {
        localStorage.setItem(key, theme);
      } catch {
        // Keep the selected theme for this page.
      }
    });

    window.addEventListener("storage", (event) => {
      if (event.key === key || event.key === null) {
        picker.value = apply(event.newValue);
      }
    });
  });
})();

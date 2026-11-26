const clock = document.querySelector(".timed-clock");
if (clock && clock.dataset.clock !== "fixed") {
  const started = performance.now();
  const initial = Number(clock.dataset.ms);
  const down = clock.dataset.clock === "down";
  const update = () => {
    const ms = Math.max(0, initial + (down ? -1 : 1) * (performance.now() - started));
    const seconds = down ? Math.ceil(ms / 1000) : Math.floor(ms / 1000);
    const pad = (n) => String(n).padStart(2, "0");
    const hours = Math.floor(seconds / 3600);
    clock.value = (hours ? pad(hours) + ":" : "") + pad(Math.floor(seconds / 60) % 60) + ":" + pad(seconds % 60);
    if (down && ms === 0) {
      window.clearInterval(interval);
      // Ask the server to finalize expiry and render the result.
      window.location.reload();
    }
  };
  const interval = window.setInterval(update, 250);
  update();
}
for (const date of document.querySelectorAll("time[datetime]")) {
  const timestamp = new Date(date.dateTime);
  if (!Number.isNaN(timestamp.getTime())) date.textContent = timestamp.toLocaleDateString();
}

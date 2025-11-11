import { loadTanks, initTankEvents, initAddForm, initEditForm  } from "./tank.js";
import { initTabs } from "./tabs.js";
import { initRegulationTab } from "./regulations.js";
import { initCargoTab } from "./cargo.js";
import { initCertificateTab } from "./certificate.js"; 

window.addEventListener("DOMContentLoaded", async () => {
  await loadTanks();
  initTankEvents();
  initAddForm();
  initEditForm();
  initTabs();
  initRegulationTab();
  initCargoTab();
  initCertificateTab();
});
(async function init() {
  await loadTanks();
  initTankEvents();
})();

import { createApp } from "vue";
import App from "./App.vue";
import StudentPortal from "./StudentPortal.vue";
import "./styles.css";

createApp(window.location.pathname.endsWith("student-portal") ? StudentPortal : App).mount("#app");

if ("serviceWorker" in navigator) {
  window.addEventListener("load", () => {
    navigator.serviceWorker.register("/assets/university_erp/frontend/service-worker.js");
  });
}

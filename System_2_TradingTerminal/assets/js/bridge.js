// ==============================================================
// 📄 FILE: assets/js/bridge.js
// ==============================================================
// PURPOSE:
//   1️⃣ Listen to drag/resize messages from React bundle
//   2️⃣ Forward them to Streamlit via the component iframe bridge
//   3️⃣ Receive layout updates back and refresh positions
// ==============================================================

// --- Listen to messages from React app ---
window.addEventListener("message", (event) => {
  if (!event?.data || !event.data.type) return;

  const msg = event.data;
  const channel = window.parent || window.top;

  switch (msg.type) {
    // ---- DRAG EVENTS ----
    case "start_drag":
      Streamlit.setComponentValue({ action: "start_drag", panel: msg.panel });
      break;
    case "update_drag":
      Streamlit.setComponentValue({
        action: "update_drag",
        panel: msg.panel,
        dx: msg.dx,
        dy: msg.dy,
      });
      break;
    case "end_drag":
      Streamlit.setComponentValue({
        action: "end_drag",
        panel: msg.panel,
        w: msg.w,
        h: msg.h,
      });
      break;

    // ---- RESIZE EVENTS ----
    case "start_resize":
      Streamlit.setComponentValue({ action: "start_resize", panel: msg.panel });
      break;
    case "update_resize":
      Streamlit.setComponentValue({
        action: "update_resize",
        panel: msg.panel,
        dw: msg.dw,
        dh: msg.dh,
      });
      break;
    case "end_resize":
      Streamlit.setComponentValue({ action: "end_resize", panel: msg.panel });
      break;

    default:
      console.log("Bridge: unknown message", msg);
  }
});

// --- Optional visual feedback ---
console.log("%c Streamlit ↔ React Bridge Active ", "color:#00aaff;font-weight:bold;");

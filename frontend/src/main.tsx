import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";

import "@fontsource-variable/plus-jakarta-sans";
import "@fontsource/noto-sans-sinhala/400.css";
import "@fontsource/noto-sans-sinhala/600.css";

import "./app.css";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
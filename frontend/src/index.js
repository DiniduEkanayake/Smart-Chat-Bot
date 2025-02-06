import React from "react";
import ReactDOM from "react-dom/client";
import Chatbot from "./Chatbot";
import "./App.css";

const App = () => {
  return (
    <div style={{ display: "flex", flexDirection: "column", alignItems: "center", padding: "20px" }}>
      <h1>Chatbot</h1>
      <Chatbot />
    </div>
  );
};

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
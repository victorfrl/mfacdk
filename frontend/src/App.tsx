import React, { useEffect } from "react";
import "./App.css";
import TasksComponent from "./components/TasksComponent";

export default function App() {
  useEffect(() => {
    document.title = "Lista de Tareas";
  }, []);
  return (
    <>
      <div className="App" style={{ padding: "20px" }}>
        <h1>Lista de Tareas</h1>
        <div>
          <TasksComponent />
        </div>
      </div>
    </>
  );
}

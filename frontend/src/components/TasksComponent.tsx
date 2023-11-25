import * as React from "react";
import { useEffect, useState } from "react";
import Box from "@mui/material/Box";
import TextField from "@mui/material/TextField";
import Button from "@mui/material/Button";
import { getTasks, saveTask } from "../tools/api";
import Task from "../interfaces/Task";
import TaskDataGrip from "./TaskDataGrip";

export default function TasksComponent() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");

  const handleSubmit = (event: { preventDefault: () => void }) => {
    event.preventDefault();
    saveTask(name, description).then((newTask) => {
      setTasks([...tasks, newTask]);
    });
    setName("");
    setDescription("");
  };

  useEffect(() => {
    getTasks().then((newTasks) => {
      setTasks(newTasks);
    });
  }, []);
  return (
    <>
      <Box
        component="form"
        sx={{
          "& .MuiTextField-root": { m: 1, width: "25ch" },
        }}
        noValidate
        autoComplete="off"
        onSubmit={handleSubmit}
      >
        <TextField
          required
          id="name"
          label="Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
        <TextField
          required
          id="description"
          label="Description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
        />
        <Button variant="contained" type="submit">
          Add Task
        </Button>
      </Box>
      <>
        <TaskDataGrip tasks={tasks} />
      </>
    </>
  );
}

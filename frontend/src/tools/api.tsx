import Task from "../interfaces/Task";

const API_URL: string = process.env.REACT_APP_BACKEND_ENDPOINT_URL + "/items";

export async function getTasks(): Promise<Task[]> {
  const data = await fetch(API_URL);
  return await data.json();
}

export async function saveTask(
  name: string,
  description: string,
): Promise<Task> {
  const data = await fetch(API_URL, {
    method: "POST",
    body: JSON.stringify({ name, description }),
  });
  return await data.json();
}

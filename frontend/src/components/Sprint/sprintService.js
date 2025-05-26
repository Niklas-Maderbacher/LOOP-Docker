export async function createSprint(sprintData) {
  const token = localStorage.getItem("token");

  const response = await fetch("/api/v1/sprints/create", {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${token}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      name: sprintData.name,
      start_date: sprintData.startDate,
      end_date: sprintData.endDate,
      goal: sprintData.goal,
      project_id: parseInt(sprintData.projectId), // sicherstellen, dass es eine Zahl ist
    }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || "Fehler beim Erstellen des Sprints");
  }

  return await response.json();
}

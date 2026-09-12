const form = document.getElementById("task-form");
const input = document.getElementById("task-input");
const taskList = document.getElementById("task-list");
const errorElement = document.getElementById("error");


async function loadTasks() {
    try {
        const response = await fetch("/api/tasks");

        if (!response.ok) {
            throw new Error("Не удалось загрузить задачи");
        }

        const tasks = await response.json();

        renderTasks(tasks);

    } catch (error) {
        showError(error.message);
    }
}


function renderTasks(tasks) {
    taskList.innerHTML = "";

    tasks.forEach(task => {
        const li = document.createElement("li");

        li.className = "task";

        if (task.completed) {
            li.classList.add("completed");
        }

        li.innerHTML = `
            <input
                type="checkbox"
                ${task.completed ? "checked" : ""}
            >

            <span class="task-title"></span>

            <button class="delete-button">
                Удалить
            </button>
        `;

        const checkbox = li.querySelector("input");
        const title = li.querySelector(".task-title");
        const deleteButton = li.querySelector(".delete-button");

        title.textContent = task.title;

        checkbox.addEventListener("change", () => {
            updateTask(task.id, checkbox.checked);
        });

        deleteButton.addEventListener("click", () => {
            deleteTask(task.id);
        });

        taskList.appendChild(li);
    });
}


async function createTask(title) {
    try {
        const response = await fetch("/api/tasks", {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                title: title
            })
        });

        if (!response.ok) {
            throw new Error("Не удалось создать задачу");
        }

        input.value = "";

        await loadTasks();

    } catch (error) {
        showError(error.message);
    }
}


async function updateTask(id, completed) {
    try {
        const response = await fetch(`/api/tasks/${id}`, {
            method: "PUT",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                completed: completed
            })
        });

        if (!response.ok) {
            throw new Error("Не удалось обновить задачу");
        }

        await loadTasks();

    } catch (error) {
        showError(error.message);
    }
}


async function deleteTask(id) {
    try {
        const response = await fetch(`/api/tasks/${id}`, {
            method: "DELETE"
        });

        if (!response.ok) {
            throw new Error("Не удалось удалить задачу");
        }

        await loadTasks();

    } catch (error) {
        showError(error.message);
    }
}


function showError(message) {
    errorElement.textContent = message;

    setTimeout(() => {
        errorElement.textContent = "";
    }, 3000);
}


form.addEventListener("submit", event => {
    event.preventDefault();

    const title = input.value.trim();

    if (!title) {
        return;
    }

    createTask(title);
});


loadTasks();

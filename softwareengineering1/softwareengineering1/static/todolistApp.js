// todolistApp.js

// Author: Alexander Aldama-Apodaca

// Contains functions for basic functionality of a to-do list

const taskInput = document.getElementById("task");
const taskList = document.getElementById("taskList");

function addTask() {
    const taskText = taskInput.value.trim();
    if (taskText) {
        const li = document.createElement("li");
        li.textContent = taskText;
        taskList.appendChild(li);
        taskInput.value = "";
        li.addEventListener("click", toggleTask);
        addCloseButton(li);
    }
}

function toggleTask(event) {
    event.target.classList.toggle("checked");
}

function addCloseButton(li) {
    const closeButton = document.createElement("span");
    closeButton.className = "close";
    closeButton.textContent = "\u00D7";
    closeButton.addEventListener("click", removeTask);
    li.appendChild(closeButton);
}

function removeTask(event) {
    const li = event.target.parentElement;
    li.remove();
}

document.getElementById("add").addEventListener("click", addTask);

// Initial references
let canvas = document.getElementById("canvas");
let backgroundButton = document.getElementById("color-background");
let colorButton = document.getElementById("color-input");
let clearButton = document.getElementById("button-clear");
let eraseButton = document.getElementById("button-erase");
let penButton = document.getElementById("button-pen");
let penSize = document.getElementById("pen-slider");
let toolType = document.getElementById("tool-type");
// Eraser and drawing flags
let erase_bool = false;
let draw_bool = false;
// Canvas context
let context = canvas.getContext("2d");
// Mouse position initialization
let mouseX = 0;
let mouseY = 0;
// Canvas offset
let rectLeft = canvas.getBoundingClientRect().left;
let rectTop = canvas.getBoundingClientRect().top;

// Initialize canvas with default settings
const init = () => {
    context.strokeStyle = "#000"; // Default drawing color
    context.lineWidth = penSize.value; // Default pen size
    toolType.innerHTML = "Pen"; // Default tool type

    canvas.style.backgroundColor = backgroundButton.value;
    context.fillStyle = backgroundButton.value;
    context.fillRect(0, 0, canvas.width, canvas.height); // Fill canvas background
};

// Detect touch capability
const is_touch_device = () => {
    try {
        document.createEvent("TouchEvent");
        return true;
    } catch (e) {
        return false;
    }
};

// Get accurate x and y position
const getXY = (e) => {
    mouseX = (!is_touch_device() ? e.pageX : e.touches?.[0].pageX) - rectLeft;
    mouseY = (!is_touch_device() ? e.pageY : e.touches?.[0].pageY) - rectTop;
};

// Stop drawing
const stopDrawing = () => {
    context.beginPath();
    draw_bool = false;
};

// Start drawing
const startDrawing = (e) => {
    draw_bool = true;
    getXY(e);
    context.beginPath();
    context.moveTo(mouseX, mouseY);
};

// Draw on canvas
const drawOnCanvas = (e) => {
    if (!is_touch_device()) {
        e.preventDefault();
    }
    getXY(e);
    if (draw_bool) {
        context.lineTo(mouseX, mouseY);
        context.stroke();
        context.globalCompositeOperation = erase_bool ? "destination-out" : "source-over";
    }
};

// Event listeners for drawing
canvas.addEventListener("mousedown", startDrawing);
canvas.addEventListener("touchstart", startDrawing);
canvas.addEventListener("mousemove", drawOnCanvas);
canvas.addEventListener("touchmove", drawOnCanvas);
canvas.addEventListener("mouseup", stopDrawing);
canvas.addEventListener("touchend", stopDrawing);
canvas.addEventListener("mouseleave", stopDrawing);

// Tool change listeners
penButton.addEventListener("click", () => {
    toolType.innerHTML = "Pen";
    erase_bool = false;
});

eraseButton.addEventListener("click", () => {
    toolType.innerHTML = "Eraser";
    erase_bool = true;
});

penSize.addEventListener("input", () => {
    context.lineWidth = penSize.value;
});

colorButton.addEventListener("change", () => {
    context.strokeStyle = colorButton.value;
});

backgroundButton.addEventListener("change", () => {
    canvas.style.backgroundColor = backgroundButton.value;
    // To ensure the background change is applied immediately
    if (!draw_bool) {
        context.fillStyle = backgroundButton.value;
        context.fillRect(0, 0, canvas.width, canvas.height);
    }
});

clearButton.addEventListener("click", () => {
    context.clearRect(0, 0, canvas.width, canvas.height);
    canvas.style.backgroundColor = "#fff"; // Reset to default background color
    backgroundButton.value = "#fff";
});

// Resize canvas to fit available screen space
function resizeCanvas() {
    let optionsHeight = document.querySelector('.options').offsetHeight;
    let availableHeight = window.innerHeight - optionsHeight;
    canvas.width = window.innerWidth;
    canvas.height = availableHeight;
    context.fillStyle = backgroundButton.value;
    context.fillRect(0, 0, canvas.width, canvas.height); // Reapply the background color on resize
}

// AJAX Save Doodle functionality
function saveDoodle() {
    const imageData = canvas.toDataURL('image/png');
    const csrfToken = getCookie('csrftoken'); // Fetch CSRF token from cookies

    fetch('/save_doodle/', { // Make sure this endpoint matches your URL configuration in Django
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify({ image_data: imageData }),
    })
    .then(response => response.json())
    .then(data => {
        alert('Doodle saved successfully!');
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error saving doodle.');
    });
}

// Fetch CSRF token from cookies (Function reused from your setup)
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Initialize and attach event listeners when the document is fully loaded
document.addEventListener('DOMContentLoaded', function() {
    init();
    resizeCanvas();
    document.getElementById('button-save').addEventListener('click', saveDoodle); // Make sure the ID matches your Save button's ID
    window.addEventListener('resize', resizeCanvas);
});

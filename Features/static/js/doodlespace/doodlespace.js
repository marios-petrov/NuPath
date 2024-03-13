// Initial references
let canvas = document.getElementById("canvas");
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

// Initialize canvas with default settings
const init = () => {
    context.strokeStyle = "#000"; // Default drawing color
    context.lineWidth = penSize.value; // Default pen size
    toolType.innerHTML = "Pen"; // Default tool type

    // Set canvas background to white
    canvas.style.backgroundColor = "#ffffff";
    context.fillStyle = "#ffffff";
    context.fillRect(0, 0, canvas.width, canvas.height); // Fill canvas background with white
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

// Get accurate x and y position relative to the canvas
const getXY = (e) => {
    const rect = canvas.getBoundingClientRect();
    mouseX = (!is_touch_device() ? e.clientX : e.touches[0].clientX) - rect.left;
    mouseY = (!is_touch_device() ? e.clientY : e.touches[0].clientY) - rect.top;
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
    if (e.cancelable) {
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
    context.globalCompositeOperation = "source-over";
});

eraseButton.addEventListener("click", () => {
    toolType.innerHTML = "Eraser";
    erase_bool = true;
    context.globalCompositeOperation = "destination-out";
});

penSize.addEventListener("input", () => {
    context.lineWidth = penSize.value;
});

colorButton.addEventListener("change", () => {
    context.strokeStyle = colorButton.value;
});

clearButton.addEventListener("click", () => {
    context.clearRect(0, 0, canvas.width, canvas.height);
    // Reset to default white background after clearing
    context.fillStyle = "#ffffff";
    context.fillRect(0, 0, canvas.width, canvas.height);
});

// Resize canvas to fit available screen space
// Resize canvas to fit available screen space
function resizeCanvas() {
    // Use window's innerWidth and innerHeight as a starting point
    let newWidth = window.innerWidth;
    let newHeight = window.innerHeight;

    // Account for the size of the navbar and options if they are present
    const navbar = document.querySelector('nav');
    const options = document.querySelector('.options');
    if (navbar) {
        newHeight -= navbar.offsetHeight;
    }
    if (options) {
        newHeight -= options.offsetHeight;
    }

    // Now set the canvas width and height to the new calculated values
    canvas.width = newWidth;
    canvas.height = newHeight;

    // Reapply the white background to the entire canvas
    context.fillStyle = "#ffffff";
    context.fillRect(0, 0, canvas.width, canvas.height);
}


// Fetch CSRF token from cookies
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

// AJAX Save Doodle functionality
function saveDoodle() {
    const imageData = canvas.toDataURL('image/png');
    const csrfToken = getCookie('csrftoken');

    fetch('/save_doodle/', {
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

// Initialize and attach event listeners when the document is fully loaded
document.addEventListener('DOMContentLoaded', function() {
    init();
    resizeCanvas();
    document.getElementById('button-save').addEventListener('click', saveDoodle);
    window.addEventListener('resize', resizeCanvas);
});

const canvas = document.getElementById('paintCanvas');
const ctx = canvas.getContext('2d');
const colorPicker = document.getElementById('colorPicker');
const clearBtn = document.getElementById('clearBtn');
const saveBtn = document.getElementById('saveBtn');

canvas.width = window.innerWidth;
canvas.height = window.innerHeight - 60;

let drawing = false;
let currentLine = [];
let allLines = []; 

ctx.lineWidth = 3;
ctx.lineCap = 'round';
ctx.lineJoin = 'round';

function getCoordinates(e) {
    const rect = canvas.getBoundingClientRect();
    const clientX = e.touches ? e.touches[0].clientX : e.clientX;
    const clientY = e.touches ? e.touches[0].clientY : e.clientY;
    return {
        x: Math.round(clientX - rect.left),
        y: Math.round(clientY - rect.top)
    };
}

function startDrawing(e) {
    drawing = true;
    const coords = getCoordinates(e);
    
    ctx.beginPath();
    ctx.moveTo(coords.x, coords.y);
    ctx.strokeStyle = colorPicker.value;
    
    currentLine = [{ x: coords.x, y: coords.y }];
}

function draw(e) {
    if (!drawing) return;
    e.preventDefault(); 
    
    const coords = getCoordinates(e);
    ctx.lineTo(coords.x, coords.y);
    ctx.stroke();
    
    currentLine.push({ x: coords.x, y: coords.y });
}

function stopDrawing() {
    if (!drawing) return;
    drawing = false;
    

    if (currentLine.length > 0) {
        allLines.push({
            color: colorPicker.value,
            points: currentLine
        });
    }
}

clearBtn.addEventListener('click', () => {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    allLines = [];
});

saveBtn.addEventListener('click', async () => {
    if (allLines.length === 0) {
        alert("Canvas is empty!");
        return;
    }

    const payload = {
        width: canvas.width,
        height: canvas.height,
        lines: allLines
    };

    console.log("Sending payload:", payload);

    try {
        const response = await fetch('/save', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        
        if (response.ok) {
            alert("Saved successfully!");
        } else {
            alert("Failed to save.");
        }
    } catch (err) {
        console.error("Error connecting to server:", err);
    }
});

// Event Listeners for both PC and Tablet compatibility
canvas.addEventListener('mousedown', startDrawing);
canvas.addEventListener('mousemove', draw);
window.addEventListener('mouseup', stopDrawing);

canvas.addEventListener('touchstart', startDrawing, { passive: false });
canvas.addEventListener('touchmove', draw, { passive: false });
window.addEventListener('touchend', stopDrawing);
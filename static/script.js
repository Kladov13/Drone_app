// Функции для взаимодействия с API
function getStatus() {
    fetch('/status')
        .then(response => response.json())
        .then(data => {
            document.getElementById('status-info').innerText =
                `Height: ${data.height} meters, Velocity: ${data.velocity} m/s, ` +
                `Coordinates: ${data.coordinates}, Battery: ${data.battery}%`;
        });
}

function updatePosition() {
    const coords = document.getElementById('coordinates').value.split(',').map(Number);
    fetch('/position', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ coordinates: coords })
    }).then(getStatus);
}

function updateHeight() {
    const height = Number(document.getElementById('height').value);
    fetch('/height', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ height: height })
    }).then(getStatus);
}

function updateVelocity() {
    const velocity = Number(document.getElementById('velocity').value);
    fetch('/velocity', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ velocity: velocity })
    }).then(getStatus);
}

function checkBattery() {
    fetch('/battery')
        .then(response => response.json())
        .then(data => alert(`Battery level: ${data.battery_level || data.warning}`));
}

function returnToBase() {
    fetch('/return_to_base', {
        method: 'POST'
    }).then(response => response.json())
      .then(data => alert(data.warning || 'Drone has returned to base.'));
}

// Получение статуса при загрузке страницы
window.onload = getStatus;

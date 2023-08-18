document.addEventListener("DOMContentLoaded", function() {
    const registrationForm = document.getElementById("registration-form");
    const sendLocationButton = document.getElementById("send-location-button");

    registrationForm.addEventListener("submit", function(event) {
        event.preventDefault();
        const name = document.getElementById("name").value;
        const number = document.getElementById("number").value;
        registerUser(name, number);
    });

    sendLocationButton.addEventListener("click", function() {
        sendLocation();
    });

    function registerUser(name, number) {
        fetch('/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                name: name,
                number: number
            })
        })
        .then(response => response.json())
        .then(data => {
            const messageElement = document.getElementById("registration-message");
            messageElement.textContent = data.message;
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }

    function sendLocation() {
        const name = document.getElementById("name").value;
        fetch('/send_location', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                name: name
            })
        })
        .then(response => response.json())
        .then(data => {
            const messageElement = document.getElementById("location-message");
            messageElement.textContent = data.message;
        })
        .catch(error => {
            console.error('Error:', error);
            console.error('Error:', error);
        });
    }
});


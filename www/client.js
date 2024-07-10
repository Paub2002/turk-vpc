document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('move').addEventListener('click', function() {
        sendGetRequest('/move');
    });

    document.getElementById('hint').addEventListener('click', function() {
        sendGetRequest('/hint');
    });

    document.getElementById('undo').addEventListener('click', function() {
        sendGetRequest('/undo');
    });
});

function sendGetRequest(action) {
    const serverAddress = document.getElementById('serverAddress').value;

    // ip format
    const regex = /^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}$/;
    if (!regex.test(serverAddress)) {
        alert('The format of the text should be ip:port');
        return
    }
    const url = `http://${serverAddress}${action}`;
    
    fetch(url, {
        method: 'GET'
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}
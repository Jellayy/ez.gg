document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('exitButton').addEventListener('click', function() {
        eventSource.close();
        fetch('/exit', { method: 'POST' })
            .then(() => console.log('Exit request sent'))
            .catch(error => console.error('Error:', error));
    });
    document.getElementById('minimizeButton').addEventListener('click', function() {
        fetch('/minimize', { method: 'POST' })
            .then(() => console.log('Minimize request sent'))
            .catch(error => console.error('Error:', error));
    });
})
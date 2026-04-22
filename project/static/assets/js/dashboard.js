function updateDateTime() {
    const now = new Date();
    const options = {
        weekday: 'short',
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    };
    const dtString = now.toLocaleDateString('en-US', options);
    const dtElement = document.getElementById('datetime-display');
    if (dtElement) {
        dtElement.textContent = dtString;
    }
}

// Update the time every second
setInterval(updateDateTime, 1000);

// Call initially to populate the display immediately
updateDateTime();

document.addEventListener('DOMContentLoaded', function() {

    function checkLCUStatus() {
        fetch('/lcu_detect')
            .then(response => response.json())
            .then(data => {
                if (data === true) {
                    console.log("LCU detected!");
                    getProfile()
                    getParty()
                } else {
                    console.log("LCU not detected.");
                    // Add your code here for when LCU is not detected
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
    }
    

    // Run LCU polling every 30 seconds
    function startPeriodicCheck() {
        checkLCUStatus();
        setInterval(checkLCUStatus, 30000);
    }
    startPeriodicCheck();


    function getProfile() {
        fetch('/lcu/profile')
            .then(response => response.text())
            .then(html => {
                document.getElementById('profile').innerHTML = html;
            })
            .catch(error => {
                console.error('Error fetching profile HTML:', error);
            });
    }


    function getParty() {
        fetch('/lcu/party')
            .then(response => response.text())
            .then(html => {
                document.getElementById('party-members').innerHTML = html;
            })
            .catch(error => {
                console.error('Error fetching party HTML:', error);
            });
    }
    document.getElementById('refresh-party-btn').onclick = getParty;

})
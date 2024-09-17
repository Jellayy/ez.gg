document.getElementById('reSearchLCUButton').addEventListener('click', function() {
    loader = document.getElementById('reSearchLoader');
    this.classList.add('hidden');
    loader.classList.remove('hidden');
    fetch('/re_search_lcu', { 
        method: 'POST',
        redirect: 'follow' // This tells fetch to follow redirects
    })
    .then(response => {
        if (response.redirected) {
            // If the response was redirected, navigate to the new URL
            window.location.href = response.url;
        } else {
            console.log('re_search_lcu request sent, but no redirect received');
        }
    })
    .catch(error => console.error('Error:', error));
});
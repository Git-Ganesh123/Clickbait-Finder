document.addEventListener('DOMContentLoaded', function() {
    const urlParams = new URLSearchParams(window.location.search);
    const videoUrl = urlParams.get('url');
    if (videoUrl) {
        fetch(`http://localhost:5000/get_percentage?url=${encodeURIComponent(videoUrl)}`)
            .then(response => response.json())
            .then(data => {
                if (data.percentage) {
                    document.getElementById('percentage').innerText = `Clickbait Percentage: ${data.percentage}%`;
                } else {
                    document.getElementById('percentage').innerText = `Error: ${data.error}`;
                }
            })
            .catch(error => {
                document.getElementById('percentage').innerText = `Error: ${error.message}`;
            });
    } else {
        document.getElementById('percentage').innerText = 'No video URL provided.';
    }
});

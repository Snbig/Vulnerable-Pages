const hardcodedUrl = 'https://vulnerable-pages.onrender.com/accounts/victim_123'; // Replace with your desired URL

async function fetchResource() {
    const contentBox = document.getElementById('content');
    
    contentBox.innerHTML = '<p>Loading...</p>';
    
    try {
        const response = await fetch(hardcodedUrl);
        if (!response.ok) throw new Error('Network response was not ok');
        const text = await response.text();
        contentBox.innerHTML = `<pre>${text}</pre>`;
    } catch (error) {
        contentBox.innerHTML = `<p style="color: red;">Failed to fetch resource: ${error.message}</p>`;
    }
}

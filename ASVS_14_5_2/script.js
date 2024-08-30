document.getElementById('fetchButton').addEventListener('click', async function() {
    // Hardcoded URL
    const hardcodedUrl = 'https://vulnerable-pages.onrender.com/protected';

    const resultContainer = document.getElementById('resultContainer');

    fetch(hardcodedUrl)
    .then(response => response.text())
    .then(data => {
        resultContainer.innerHTML = data;
    });});

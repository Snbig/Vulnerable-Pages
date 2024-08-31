document.getElementById('fetchButton').addEventListener('click', async function() {

    const hardcodedUrl = 'https://vulnerable-pages.onrender.com/protected';

    var xhttp = new XMLHttpRequest();
    xhttp.open("GET", hardcodedUrl, false);
    xhttp.send();
    if (xhttp.status == 403) {
        document.getElementById("resultContainer").innerHTML = "As you can see, the resource cannot be downloaded due to the use of the Origin header for authentication or access control. However, you can easily bypass this restriction by modifying the Origin header outside of the browser.";
        };

});

function clean() {
    document.getElementById("response").style.backgroundColor = "";
    document.getElementById("response").style.color = "";
    document.getElementById("response").innerHTML ="";
}

function set_payload(url ,payload){
    clean()
    let input = document.getElementById('inputField');
    input.value = payload
    document.getElementById('url').value = url
    input.addEventListener("keypress", function(event) {
        if (event.key === "Enter") {
            document.getElementById("submit").click();
        }
    });
}

function send_payload(){

var payload = document.getElementById('inputField').value
var url = document.getElementById('url').value;
document.getElementById('response').innerHTML = ` <svg class="ip" viewBox="0 0 256 128" width="256px" height="128px" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <linearGradient id="grad1" x1="0" y1="0" x2="1" y2="0">
            <stop offset="0%" stop-color="#5ebd3e" />
            <stop offset="33%" stop-color="#ffb900" />
            <stop offset="67%" stop-color="#f78200" />
            <stop offset="100%" stop-color="#e23838" />
        </linearGradient>
        <linearGradient id="grad2" x1="1" y1="0" x2="0" y2="0">
            <stop offset="0%" stop-color="#e23838" />
            <stop offset="33%" stop-color="#973999" />
            <stop offset="67%" stop-color="#009cdf" />
            <stop offset="100%" stop-color="#5ebd3e" />
        </linearGradient>
    </defs>
    <g fill="none" stroke-linecap="round" stroke-width="16">
        <g class="ip__track" stroke="#ddd">
            <path d="M8,64s0-56,60-56,60,112,120,112,60-56,60-56"/>
            <path d="M248,64s0-56-60-56-60,112-120,112S8,64,8,64"/>
        </g>
        <g stroke-dasharray="180 656">
            <path class="ip__worm1" stroke="url(#grad1)" stroke-dashoffset="0" d="M8,64s0-56,60-56,60,112,120,112,60-56,60-56"/>
            <path class="ip__worm2" stroke="url(#grad2)" stroke-dashoffset="358" d="M248,64s0-56-60-56-60,112-120,112S8,64,8,64"/>
        </g>
    </g>
</svg>`

let xhr = new XMLHttpRequest();
xhr.onreadystatechange = function() {
try{
    if (xhr.readyState === XMLHttpRequest.DONE) {
        if (xhr.status === 200) {
            setTimeout(() => {
                    document.getElementById("response").innerHTML = this.responseText;
                    document.getElementById("response").style.color = "#000000";
                }, 1000);
            }
            
        else {
                setTimeout(() => {
                document.getElementById("response").innerHTML = xhr.responseText;
                document.getElementById("response").style.color = "#ff0000";
            }, 1000);
            }}}
catch(err){
            document.getElementById("response").innerHTML = err;
        }
        

        }
xhr.open("POST", url, true);
xhr.setRequestHeader("Content-Type", "application/json");
xhr.send(JSON.stringify({url :payload}));

};
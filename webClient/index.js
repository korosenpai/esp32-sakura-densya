var textArea = document.getElementById("msg")
let button = document.getElementById("btn")
let timeoutButton = 5000 // 5s

let ip = document.getElementById("ip")

function sendData() {
    if (!textArea.value) return
    
    button.disabled = true
    setTimeout(() => button.disabled = false, timeoutButton)
    

    const xhr = new XMLHttpRequest();
    xhr.open('POST', 'http://192.168.4.1');
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onreadystatechange = function() {
    if (xhr.readyState === 4 && xhr.status === 200) {
        console.log(xhr.responseText);
        // Do something with the response data
        ip.innerText = JSON.parse(xhr.responseText).ip
        
    }
    };
    const data = { "msg": textArea.value };
    xhr.send(JSON.stringify(data));

    textArea.value = ""

}


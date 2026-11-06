
var c = document.getElementById('nav_bar');
var b1 = document.getElementById('button1');
var b2 = document.getElementById('button2');
function nav_bar(click) {
    if (click == "open") {
        c.style.display = "inline-block";
        b1.style.display = "none";
        b2.style.display = "inline-block";
    }
    else {
        c.style.display = "none";
        b1.style.display = "inline-block";
        b2.style.display = "none";
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const container = document.getElementById('popup-container');
    const messagesScript = document.getElementById('messages-json');
    if (!messagesScript) return;

    const djangoMessages = JSON.parse(messagesScript.textContent);

    djangoMessages.forEach(msg => {
        const msgDiv = document.createElement('div');
        msgDiv.classList.add('popup-message');

        if (msg.tags) {
            msgDiv.classList.add('popup-' + msg.tags);
        }

        msgDiv.innerText = msg.message;
        container.appendChild(msgDiv);

        setTimeout(() => { msgDiv.remove(); }, 3000);
    });
});




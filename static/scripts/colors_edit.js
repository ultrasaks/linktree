
document.querySelector(".ava-circle").setAttribute('style', `width:calc(${document.querySelector(".ava-circle").clientHeight}px - 4rem);height:calc(${document.querySelector(".ava-circle").clientHeight}px - 4rem)`)
const HEADERS = {"Content-Type": "application/json",'X-CSRFToken': document.getElementsByName('csrfmiddlewaretoken')[0].value}

const username = document.getElementById('username')
const description = document.getElementById('about')

const outlinedSelector = document.querySelector(".outlined-selector");

function changeColor(elemId, value) {
    console.log(elemId, `${elemId}-text`);
    document.querySelector(`#${elemId}-text`).innerHTML = value;
    fetch("/profile/design/change/color/", {
        method: "POST",
        body: JSON.stringify({
            color_id: elemId,
            color_hash: value
        }),
        headers: HEADERS,
    });
}

function changeName() {
    document.querySelector('avaname').innerHTML = username.value[0].toUpperCase()
    fetch("/profile/change/", {
        method: "POST",
        body: JSON.stringify({
            name: username.value,
            about: description.value
        }),
        headers: HEADERS,
    });
}

function changeButton(element, send) {
    outlinedSelector.style.top = element.offsetTop - 7 + "px";
    outlinedSelector.style.left = element.offsetLeft - 7 + "px";
    outlinedSelector.style.width = element.clientWidth + 10 + "px";
    outlinedSelector.style.height = element.clientHeight + 10 + "px";
    if (!send) { return }
    fetch("/profile/design/change/button/", {
        method: "POST",
        body: JSON.stringify({
            button_id: element.id,
        }),
        headers: HEADERS,
    });
}

document.querySelectorAll('.color-description').forEach(inputElement => {
    inputElement.setAttribute('style', `width:${inputElement.clientHeight}px`)
})
colors = document.querySelectorAll('input[type=color]')
colors.forEach(inputElement => {
    inputElement.addEventListener('blur', () => {
        changeColor(inputElement.id, inputElement.value)
    });
});

username.addEventListener('blur', () => { changeName() })
description.addEventListener('blur', () => { changeName() })

document.querySelectorAll('.s').forEach(inputElement => {
    inputElement.addEventListener('click', () => { changeButton(inputElement, true) })
})


const HEADERS = { "Content-Type": "application/json", 'X-CSRFToken': document.getElementsByName('csrfmiddlewaretoken')[0].value }

const username = document.getElementById('username');
const description = document.getElementById('about');
const avaname = document.querySelector('avaname');
const avapic = document.getElementById('profile-image');

const outlinedSelector_button = document.getElementById('selector_1');
const outlinedSelector_shape = document.getElementById('selector_2');



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
    }).then(response => {update_frame()});
}

function changeName() {
    avaname.innerHTML = username.value[0].toUpperCase()
    fetch("/profile/change/", {
        method: "POST",
        body: JSON.stringify({
            name: username.value,
            about: description.value
        }),
        headers: HEADERS,
    }).then(response => {update_frame()});
}

function changeShape(element, send) {
    outlinedSelector_shape.style.top = element.offsetTop - 7 + "px";
    outlinedSelector_shape.style.left = element.offsetLeft - 7 + "px";
    outlinedSelector_shape.style.width = element.clientWidth + 10 + "px";
    outlinedSelector_shape.style.height = element.clientHeight + 10 + "px";
    if (!send) { return }
    fetch("/profile/design/change/shape/", {
        method: "POST",
        body: JSON.stringify({
            shape: element.id.slice(-1),
        }),
        headers: HEADERS,
    }).then(response => {update_frame()});
}


function changeButton(element, send) {
    outlinedSelector_button.style.top = element.offsetTop - 7 + "px";
    outlinedSelector_button.style.left = element.offsetLeft - 7 + "px";
    outlinedSelector_button.style.width = element.clientWidth + 10 + "px";
    outlinedSelector_button.style.height = element.clientHeight + 10 + "px";
    if (!send) { return }
    fetch("/profile/design/change/button/", {
        method: "POST",
        body: JSON.stringify({
            button_id: element.id,
        }),
        headers: HEADERS,
    }).then(response => {update_frame()});
}

function changeAvatar() {
    files = avatarInput.files
    var formdata = new FormData(document.getElementById('ava-form'))

    fetch("/profile/image/", {
        method: "POST",
        body: formdata,
        headers: { 'X-CSRFToken': document.getElementsByName('csrfmiddlewaretoken')[0].value }
    }).then(response => { if (response.ok) { return response.json() } throw new Error(''); })
        .then(data => {
            avapic.setAttribute('src', data['url'])
            avaname.classList.add('hid')
            avapic.classList.remove('hid')
            update_frame();
        }).catch((error) => {
            alert('Плохая у тебя картинка');
        });
    

}

document.querySelector(".ava-circle").setAttribute('style', `width:calc(${document.querySelector(".ava-circle").clientHeight}px - 4rem);height:calc(${document.querySelector(".ava-circle").clientHeight}px - 4rem)`)

document.querySelectorAll('.color-description').forEach(inputElement => {
    inputElement.setAttribute('style', `width:${inputElement.clientHeight}px`)
})
document.querySelector(".font-text").setAttribute('style', `width: calc(${document.querySelector('.color-description').clientWidth}px - 1rem) `)
avapic.setAttribute('style', `width:${document.querySelector(".ava-circle").clientHeight}px`)

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

document.querySelectorAll('.d').forEach(inputElement => {
    inputElement.addEventListener('click', () => { changeShape(inputElement, true) })
})

const avatarInput = document.getElementById('avatar')
avatarInput.addEventListener('change', () => {
    changeAvatar();

})

const fontPopup = document.querySelector('.showable');

function toggleFontPopup(update){
    fontPopup.classList.toggle('hid');
    if (update) {
        fetch("/profile/new/font", {
            method: "GET"
        }).then(response => { if (response.ok) { return response.json() } throw new Error(''); })
        .then(data => {update_font(data)});

    }
}

function update_font(response) {
    document.querySelector('#font-input-text').innerHTML = response[1]
    document.querySelector('#font-input-square').setAttribute('src', `/media/fonts/${response[2]}.webp`)
    update_frame()
}

document.querySelector('#color-wrapper').addEventListener('click', () => { toggleFontPopup(false) });
document.querySelector('#new_font').addEventListener('click', () => { toggleFontPopup(true) });

document.getElementById('avatar-delete').addEventListener('click', () => {
    avaname.classList.remove('hid');
    avapic.classList.add('hid');
    fetch("/profile/image/delete/", { method: "GET" }).then(response => {update_frame()});
    
})

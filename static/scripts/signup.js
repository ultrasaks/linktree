const namebutton = document.getElementById('name-button');
const wholebutton = document.getElementById('whole-button');
const password_pattern = /^((?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{6,})$/

namebutton.addEventListener('click', () => { checkName() });
document.getElementById('id_username').addEventListener('click', () => { rem_error('id_username') });
document.getElementById('id_email').addEventListener('click', () => { rem_error('id_email') });


const pass1 = document.getElementById('id_password')
const pass2 = document.getElementById('id_password2')

const help1 = document.getElementById('password_help1')
const help2 = document.getElementById('password_help2')


pass1.addEventListener('change', () => { checkPassword() });
pass2.addEventListener('change', () => { checkPassword() });

function rem_error(elem_id) {
    document.getElementById(elem_id).classList.remove('edit-error')
}
function add_error(elem_id) {
    document.getElementById(elem_id).classList.add('edit-error')
}


function checkPassword() {
    if (pass1.value == pass2.value && (password_pattern.test(pass1.value)) && document.getElementById('id_email').value != pass1.value) {
        wholebutton.removeAttribute('disabled');
        help1.classList.remove('errtext');
        help2.classList.remove('errtext');
        help1.classList.add('oktext');
        help2.classList.add('oktext');
    } else {
        if (pass1.value != pass2.value) { help2.classList.add('errtext'); help2.classList.remove('oktext'); } else { help2.classList.remove('errtext'); help2.classList.add('oktext'); }
        if (!password_pattern.test(pass1.value)) { help1.classList.add('errtext'); help1.classList.remove('oktext'); } else { help1.classList.remove('errtext'); help1.classList.add('oktext'); }
        wholebutton.setAttribute('disabled', '');
    }
}

function checkName() {
    var formdata = new FormData(document.getElementById('regform'))

    rem_error('id_email')
    rem_error('id_username')
    fetch("/signup/first/", {
        method: "POST",
        body: formdata,
        headers: { 'X-CSRFToken': document.getElementsByName('csrfmiddlewaretoken')[0].value }
    }).then(response => response.json().then(data => ({ status: data.status }))

        .then(data => {
            switch (data.status) {
                case 0:
                    console.log('email');
                    add_error('id_email')
                    break;
                case 1:
                    console.log('username');
                    add_error('id_username')
                    break;
                case 2:
                    console.log('wrong');
                    add_error('id_email')
                    add_error('id_username')
                    break;
                default:
                    document.getElementById('password-container').classList.remove('hid')
                    document.getElementById('name-container').classList.add('hid')
                    namebutton.classList.add('hid')
                    wholebutton.classList.remove('hid')
                    document.getElementById('card-title').innerHTML = 'Придумайте пароль'
            }

        }))
}
const popup = document.querySelector('#popup');
const popupButton = document.querySelector('#btn_add');
const popupOverlay = document.querySelector('.popup-overlay');
const popupError = document.querySelector(".popup-error");
const urlInput = document.querySelector("#new_site_url");


const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value

var url = ""
var they = document.querySelectorAll('.card-edit')

const regex = /^([a-z]+:\/\/)?([a-z0-9-]+\.)?[a-z0-9-]+\.[a-z]+(\/.*)?$/i;

they.forEach(inputElement => {
  inputElement.addEventListener('blur', () => {
    change_name(inputElement.id);
  });
});


function change_name(id){
    id = id.split('_')[0]

    var name = make_safe(document.getElementById(`${id}_name_inp`).value);
    var url = make_safe(document.getElementById(`${id}_url_inp`).value);

    url_elem = document.getElementById(`${id}_url`);
    name_elem = document.getElementById(`${id}_name`);

    url_elem.classList.remove('hid');
    name_elem.classList.remove('hid');

    url_elem.innerHTML = url + document.getElementById(`${id}_url_btn`).outerHTML;
    name_elem.innerHTML = name + document.getElementById(`${id}_name_btn`).outerHTML;

    document.querySelectorAll('.card-edit').forEach(element => {
        element.classList.add('hid');
    });
    request_name_change(id, name, url)
}


function request_name_change(id, name, url) {
  fetch("/profile/links/edit/", {
      method: "POST",
      body: JSON.stringify({
        id:id,
        title:make_safe(name),
        url:make_safe(url)
      }),
      headers: {
        "Content-Type": "application/json",
        'X-CSRFToken': csrf
      },
    })
}


function del_link(id) {
  fetch("/profile/links/delete/", {
      method: "POST",
      body: JSON.stringify({
        id:id
      }),
      headers: {
        "Content-Type": "application/json",
        'X-CSRFToken': csrf
      },
    })
    document.getElementById(`${id}c`).remove()
}


function sh_name(id){
  var inp = document.getElementById(`${id}_name_inp`);
  inp.classList.remove('hid');
  inp.focus();
  document.getElementById(`${id}_name`).classList.add('hid')
}

function sh_url(id){
  var inp = document.getElementById(`${id}_url_inp`);
  inp.classList.remove('hid');
  inp.focus();
  document.getElementById(`${id}_url`).classList.add('hid')
}


popupButton.addEventListener('click', () => {
    popup.classList.add('visible');
    popupOverlay.classList.add('visible');
    urlInput.focus();
});

function close_popup(){
  popup.classList.remove('visible');
  popupOverlay.classList.remove('visible');
  urlInput.value = '';
  popupError.innerHTML = '';
  document.querySelector('#popup_add').classList.remove('button-disabled');
}

function create_url() {
  url = urlInput.value.trim();

  if (url !== "") {
    if (regex.test(url)){
    document.querySelector('#popup_add').classList.add('button-disabled');
    fetch("/profile/links/new/", {
      method: "POST",
      body: JSON.stringify({
        url:make_safe(url),
        csrfmiddlewaretoken:csrf
      }),
      headers: {
        "Content-Type": "application/json",
        'X-CSRFToken': csrf
      },
    })
    .then(response => response.json())
    .then(data => {
      add_card(data)
      close_popup();
  });}else{
    popupError.innerHTML = 'Неправильный формат ссылки'
  }
  }
}

const cardContainer = document.querySelector('.card-list');


function switch_cards(id, where) {
  var cards = cardContainer.querySelectorAll('.card');
  need_card_pos = document.getElementById(`${id}_pos`);
  pos = parseInt(need_card_pos.value)
  if ((pos == 0 && where == 0) || (pos + 1 == cards.length && where == 1)){}
  else{
    const card1 = cards[pos];
    if (where == 0){
      var card2 = cards[pos - 1]
      cardContainer.removeChild(card1);
      cardContainer.insertBefore(card1, card2);
    }else{
      var card2 = cards[pos + 1]
      console.log(cards, id, need_card_pos)
      cardContainer.removeChild(card2);
      cardContainer.insertBefore(card2, card1);
    }
    second_pos = card2.querySelector('.pos')
    need_card_pos.value = second_pos.value;
    second_pos.value = pos;
    send_pos_change(id, where);
  }
  
}

function send_pos_change(id, where) {
  fetch("/profile/links/edit/pos/", {
      method: "POST",
      body: JSON.stringify({
        id:id,
        where:where
      }),
      headers: {
        "Content-Type": "application/json",
        'X-CSRFToken': csrf
      },
    })
}

function add_card(data) {
  console.log(data);
  link_id = data[0];link_url = data[1];link_title = data[2];link_position = data[3];
  to_add = document.createElement("div");
  to_add.classList.add('card')
  to_add.id = `${link_id}c`
  to_add.innerHTML = `
      <input type="hidden" class="pos" id="${link_id}_pos" value="${link_position}">
        <input id="${link_id}_name_inp" class="card-edit hid" value="${link_title}">
        <b id="${link_id}_name">${link_title} <i class="ti ti-pencil card-icon intext" id="${link_id}_name_btn" onclick="javascript: sh_name('${link_id}')"></i></b>
        <div>
            <input id="${link_id}_url_inp" class="card-edit hid" value="${link_url}">
            <div class="card-link" id="${link_id}_url">${link_url} <i class="ti ti-pencil card-icon intext" id="${link_id}_url_btn" onclick="javascript: sh_url('${link_id}')"></i></div></div>
        <div class="card-icons">
            <span>
                <i class="ti ti-arrow-big-up card-icon" onclick="javascript: switch_cards('${link_id}', 0)"></i>
                <i class="ti ti-arrow-big-down card-icon" onclick="javascript: switch_cards('${link_id}', 1)"></i>
            </span>
            <i class="ti ti-trash card-icon" onclick="javascript: del_link('${link_id}')"></i>
        </div>`;
    cardContainer.appendChild(to_add);
    
    they = document.querySelectorAll('.card-edit')
    they.forEach(inputElement => {
        inputElement.addEventListener('blur', () => {
          change_name(inputElement.id);
      });
    });
}
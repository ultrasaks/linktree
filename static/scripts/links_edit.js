
$(document).on('submit', '#popup-form', function (e) {
    e.preventDefault();
    url = $('#form_url').val()
    title = $('#form_title').val()
    icon = $('#form_icon').val()
    edit_id = $('#edit_id').val()
    $.ajax({
        type: 'POST',
        url: '/profile/links/new/',
        data: {
            url: url,
            title: title,
            icon: icon,
            edit_id: edit_id,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
        },
        success: function (data) {
            hide_popup();
            if (edit_id == "") {
                add_link(data.id, url, title, icon);
            } else {
                edit_link(edit_id, url, title, icon)
            }
        },
        error: function (data) {
            alert('Unknown error');
            console.log(data);
        }
    });
});

function set_class(icon) {
    $("#icon_preview")[0].classList = ['ti ti-' + icon]
}

$("#form_icon").change(function () {
    set_class($("#form_icon").val())
});

function make_empty_popup() {
    $("#form_url").val("");
    $("#form_title").val("");
    $("#edit_id").val("");
    $("#form_icon").val("link");
    set_class('link');
    $("#submit-button")[0].innerText = "Создать"
}

function link_to_popup(id) {
    name = $(`#${id}_title`).val()
    icon = $(`#${id}_icon`).val()
    url = $(`#${id}_url`).val()

    $("#form_url").val(url);
    $("#form_title").val(name);
    $("#edit_id").val(id);
    $("#form_icon").val(icon);
    set_class(icon);
    $("#submit-button")[0].innerText = "Сохранить"

    toggle_popup()
}

function get_link_element(id, link, name, icon) {
    return `
            <span>
                <i class="ti ti-${icon}"></i>
                ${name} (<a class="white-link" href="${link}">${link}</a>)
            </span>
            <input type="hidden" id="${id}_url" value="${url}">
            <input type="hidden" id="${id}_title" value="${name}">
            <input type="hidden" id="${id}_icon" value="${icon}">
            <span class="link-buttons">
                <i class="ti ti-pencil cross cross-red edit-icon" onclick="link_to_popup('${id}')"></i>
                <i class="ti ti-x cross cross-red" onclick="delete_link('${id}')"></i>
            </span>
        `
}

function add_link(id, link, name, icon) {
    name = make_safe(name)
    link = make_safe(link)

    var inside_link = get_link_element(id, link, name, icon);
    $('#links').append(`
            <p id="link_${id}" class="link-mobile">
                ${inside_link}
            </p>
        `)
}
function edit_link(id, link, name, icon) {
    name = make_safe(name)
    link = make_safe(link)

    $("#link_" + id)[0].innerHTML = get_link_element(id, link, name, icon)
}

function delete_link(id) {
    $.ajax({
        type: 'POST',
        url: '/profile/links/delete/',
        data: {
            id: id,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
        },
        success: function (data) {
            $("#link_" + id).remove()
        }
    });
}

function toggle_popup() {
    $('#modal')[0].classList.toggle('show');
    $('#popup')[0].classList.toggle('show2');
    $('#central')[0].classList.toggle('show-central');
}
function hide_popup() {
    toggle_popup();
    make_empty_popup();
}

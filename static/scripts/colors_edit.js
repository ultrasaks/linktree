var color_object = $('#color_obj');
var color = $('#color_pick');
function send_change() {
    $.ajax({
        type: 'POST',
        url: '/profile/design/change/',
        data: {
            to_change: color_object.val(),
            color: color.val(),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
        },
        error: function (data) {
        },
        success: function (data) {
            $("#" + color_object.val() + "_preview")[0].style.backgroundColor = color.val()
            $("#" + color_object.val() + "_hash")[0].value = color.val()
        }

    });
}

function change_color(color_id) {
    $("form")[0].classList = []

    color_object[0].value = color_id;
    color[0].value = $("#" + color_id + "_hash")[0].value
}

const color_objects = ["background", "font", "card", "button", "button_hover", "button_click", "button_font"]
for (color_obj in color_objects) {
    color_name = color_objects[color_obj]
    $("#" + color_name).click(function () { change_color(this.id) }); // костыль мечты
}

$("#change").click(send_change)
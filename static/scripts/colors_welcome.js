function create_empty() {
    $.ajax({
        type: 'GET',
        url: '/profile/colors/create/',
    });
}

$("#emp").click(function () {
    create_empty();
    window.open('/profile/links', '_self');
})
$("#own").click(function () {
    create_empty();
    window.open('/profile/colors/edit', '_self');
})
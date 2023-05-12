function create_empty() {
    fetch('/profile/colors/create/', {
        method: 'GET'
    });
}

document.getElementById('emp').addEventListener('click', function () {
    create_empty();
    window.open('/profile/links', '_self');
});

document.getElementById('own').addEventListener('click', function () {
    create_empty();
    window.open('/profile/colors/edit', '_self');
});
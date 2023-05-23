function create_empty() {
    fetch('/profile/design/create/', {
        method: 'GET'
    });
}

document.getElementById('emp').addEventListener('click', function () {
    create_empty();
    window.open('/profile/links', '_self');
});

document.getElementById('own').addEventListener('click', function () {
    create_empty();
    window.open('/profile/design/edit', '_self');
});
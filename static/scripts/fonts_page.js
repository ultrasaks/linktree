const HEADERS = { "Content-Type": "application/json", 'X-CSRFToken': document.getElementsByName('csrfmiddlewaretoken')[0].value }

const outlinedSelector = document.getElementById('selector_font');
function set_selector(element, send) {
    outlinedSelector.style.top = element.offsetTop - 7 + "px";
    outlinedSelector.style.left = element.offsetLeft - 7 + "px";
    outlinedSelector.style.width = element.clientWidth + 10 + "px";
    outlinedSelector.style.height = element.clientHeight + 10 + "px";
    if (!send) { return }
    fetch("/profile/design/change/font_type/", {
        method: "POST",
        body: JSON.stringify({
            font_name: element.id,
        }),
        headers: HEADERS,
    })
}
document.querySelectorAll('.font').forEach(inputElement => {
    inputElement.addEventListener('click', () => { set_selector(inputElement, true) })
})
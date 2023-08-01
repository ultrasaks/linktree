const screen_width = window.screen.width;
const widget = document.createElement('iframe');
widget.src = "/profile/design/test";
widget.id = 'pagePreview'
if (screen_width < 1400) {
    // mobile
}else{
    // pc
    widget.classList.add('widget-pc')
    document.getElementsByTagName('header')[0].appendChild(widget)
}
const iframe = document.getElementById('pagePreview');

function update_frame() {
    iframe.contentWindow.location.reload();
}
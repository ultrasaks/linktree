const htmlEntities = { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&apos;" };
function make_safe(str) {
    return str.replace(/([&<>\"'])/g, match => htmlEntities[match]);
}
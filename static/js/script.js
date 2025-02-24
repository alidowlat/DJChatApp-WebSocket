document.getElementById("room-name-input").addEventListener("input", function () {
    this.value = this.value.toUpperCase().replace(/\s+/g, "_")
});

function validateSearch() {
    let input = document.getElementById("chat-message-input").value.trim();
    return !(input === "" || input === " ");
}
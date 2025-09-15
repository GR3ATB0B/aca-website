document.addEventListener("DOMContentLoaded", function() {
    const wickyImg = document.getElementById("wicky-img");
    if (wickyImg) {
        wickyImg.addEventListener("click", function() {
            alert("Wicky says: you are gay for clicking!");
        });
    }
});
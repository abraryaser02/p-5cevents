document.addEventListener("DOMContentLoaded", function() {
    // Get the button and the dropdown content
    var dropbtn = document.querySelector(".dropbtn");
    var dropdownContent = document.querySelector(".dropdown-content");

    // Toggle the display of the dropdown content on click
    dropbtn.onclick = function() {
        dropdownContent.style.display = dropdownContent.style.display === "block" ? "none" : "block";
    };

    // Close the dropdown if the user clicks outside of it
    window.onclick = function(event) {
        if (!event.target.matches('.dropbtn')) {
            if (dropdownContent.style.display === "block") {
                dropdownContent.style.display = "none";
            }
        }
    };
});
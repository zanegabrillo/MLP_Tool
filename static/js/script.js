// JavaScript function for validating grams input
function validateForm() {
    var grams = document.getElementById("grams").value;
    var modal = document.getElementById("myModal");
    var modalMessage = document.getElementById("modalMessage");
    
    // Check if grams is a valid number and greater than 0
    if (isNaN(grams) || grams <= 0) {
        modalMessage.innerText = "Please enter a valid number for grams (positive number).";
        modal.style.display = "block"; // Show modal
        return false;  // Prevent form submission
    }
    return true;  // Allow form submission
}

// When the user clicks on <span> (x), close the modal
function closeModal() {
    var modal = document.getElementById("myModal");
    modal.style.display = "none";
}
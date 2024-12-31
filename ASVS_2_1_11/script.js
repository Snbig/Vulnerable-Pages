document.addEventListener('DOMContentLoaded', function() {
    const passwordField = document.getElementById('password');

    // Attempt to disable autofill
    passwordField.setAttribute('autocomplete', 'off'); 
    passwordField.setAttribute('readonly', 'readonly'); // Temporarily make it readonly

    // Remove readonly on focus to allow input
    passwordField.addEventListener('focus', function() {
        passwordField.removeAttribute('readonly');
    });
});
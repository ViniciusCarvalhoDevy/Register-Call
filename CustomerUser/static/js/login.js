var passwordField = document.getElementById('id_password');
var passwordViewCheckbox = document.getElementById('passwordview');
passwordViewCheckbox.addEventListener('click', function() { 
    if (passwordViewCheckbox.checked) {
        passwordField.type = 'text';
    } else {
        passwordField.type = 'password';
    }
});
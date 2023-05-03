let checkConfirmPassword = function() {
    let password = document.getElementById('password');
    let confirm_password = document.getElementById('confirm_password');
    let submit = document.getElementById('submit');

    if (password.value !== confirm_password.value) {
        submit.disabled = true;
        confirm_password.setCustomValidity('Passwords do not match');
        confirm_password.reportValidity();
    } else {
        confirm_password.setCustomValidity('');
        confirm_password.reportValidity();
        submit.disabled = false;
    }
}
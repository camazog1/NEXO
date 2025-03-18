const userTypeField = document.getElementById('user_type');
const adminPasswordField = document.getElementById('admin-password-field');

userTypeField.addEventListener('change', function () {
    if (this.value === 'admin') {
        adminPasswordField.style.display = 'block'; // Show the field
    } else {
        adminPasswordField.style.display = 'none'; // Hide the field
    }
});
// Reveals password fields for user registration and login forms.
// Adapted from guide at: https://gomakethings.com/creating-a-toggle-password-plugin-with-vanilla-javascript/


// Listen for click events
document.addEventListener('click', function (event) {

  // If the clicked element isn't our show password checkbox, return
  if (!event.target.hasAttribute('data-show-password')) return;

  // Get the password field
  var password = document.querySelectorAll(event.target.getAttribute('data-show-password'));
  if (password.length < 1) return;

  // Loop through each field
  for (var i = 0; i < password.length; i++) {

    // Check if the password should be shown or hidden
    if (event.target.checked) {
      // Show the password
      password[i].type = 'text';
    } else {
      // Hide the password
      password[i].type = 'password';
    }

  }

}, false);

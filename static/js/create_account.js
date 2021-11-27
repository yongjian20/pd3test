function isNumber(evt) {
    evt = (evt) ? evt : window.event;
    var charCode = (evt.which) ? evt.which : evt.keyCode;
    if (charCode > 31 && (charCode < 48 || charCode > 57)) {
        return false;
    }
    return true;
}

function isLetters(event) {
    var key = event.keyCode;
    return ((key >= 65 && key <= 90) || key > 96 && key < 123 || key == 32 || key == 8);
}

function checkDOB(event) {
    var message = document.getElementById('message');
    var dateString = document.getElementById('dob').value;
    var inputDate = new Date(dateString);
    var today = new Date();
    var age = over21(inputDate);

    if ( inputDate > today ) {
        message.style.color = 'red';
        message.innerHTML = 'You cannot enter future date.'
        return false;
    }

    else if ( age < 21 ) {
        message.style.color = 'red';
        message.innerHTML = 'You must be 21 and above to register.'
        return false;
    }

    else {
        message.style.display = "none";
    }

    return true;
}

function over21(inputDate) {
    var dateString = document.getElementById('dob').value;
    var inputDate = new Date(dateString);
    var today = new Date();
    var age = today.getFullYear() - inputDate.getFullYear();
    var m = today.getMonth() - inputDate.getMonth();

    if (m < 0 || (m === 0 && today.getDate() < inputDate.getDate())) {
            age--;
    }
    return age;
}

var checkPassword = function() {
    var password = document.getElementById('password');
    var confirmPassword = document.getElementById('confirmPassword');

    var userInputP = password.value;
    var userInputCP = confirmPassword.value;

    if (userInputP.length >= 8) {
        document.getElementById('message').style.color = 'green';
        document.getElementById('message').innerHTML = 'Password requirements satisfied.';

        if (userInputP.length ==
            userInputCP.length) {
                document.getElementById('message').style.display = 'block';
                document.getElementById('message').style.color = 'green';
                document.getElementById('message').innerHTML = 'Password match.';
        }

        else {
            document.getElementById('message').style.display = 'block';
            document.getElementById('message').style.color = 'red';
            document.getElementById('message').innerHTML = 'Password does not match.';
        }
    }

    else {
        document.getElementById('message').style.display = 'block';
        document.getElementById('message').style.color = 'red';
        document.getElementById('message').innerHTML = 'Minimum password requirements: 8 characters.';
    }
}

var checkEmail = function() {
  if (document.getElementById('email').value ==
    document.getElementById('confirmEmail').value) {
    document.getElementById('message').style.color = 'green';
    document.getElementById('message').innerHTML = 'Email match.';
  } else {
    document.getElementById('message').style.color = 'red';
    document.getElementById('message').innerHTML = 'Email does not match.';
  }
}

const togglePassword = document.querySelector('#togglePassword');
const togglePassword1 = document.querySelector('#togglePassword1');
const password = document.querySelector('#password');
const cPassword = document.querySelector('#confirmPassword');

togglePassword.addEventListener('click', function (e) {
    // toggle the type attribute
    const type = password.getAttribute('type') === 'password' ? 'text' : 'password';
    password.setAttribute('type', type);

    // toggle the eye / eye slash icon
    this.classList.toggle('bi-eye');
});

togglePassword1.addEventListener('click', function (e) {
    // toggle the type attribute
    const type = cPassword.getAttribute('type') === 'password' ? 'text' : 'password';
    cPassword.setAttribute('type', type);

    // toggle the eye / eye slash icon
    this.classList.toggle('bi-eye');
});

jQuery(document).ready(function () {
    "use strict";
    var options = {};
    options.ui = {
    bootstrap4: true,
    container: "#pwd-container",
    viewports: {
        progress: ".pwstrength_viewport_progress"
    },
    showVerdictsInsideProgressBar: true
    };
    $('#password').pwstrength(options);
});
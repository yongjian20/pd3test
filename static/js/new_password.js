var checkPassword = function() {
    var password = document.getElementById('newPassword');
    var confirmPassword = document.getElementById('confirmNewPassword');

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
    $('#newPassword').pwstrength(options);
});
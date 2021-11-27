var editBtn;
var saveBtn;
var cancelBtn;

$('#editBtn').click(function () {
    $(this).hide();
    $('#saveBtn, #cancelBtn').show();
});

$('#saveBtn').click(function () {
    $(this).hide();
    $('#cancelBtn').hide();
    $('#editBtn').show();
});

function enableEdits() {
    // Retrieve elements to be editable from input fields
    var firstName = document.getElementById("firstName");
    var lastName = document.getElementById("lastName");
    var mailingAddress = document.getElementById("mailingAddress");
    var deliveryAddress = document.getElementById("deliveryAddress");
    var image_file = document.getElementById("image_file");
    var oldPassword = document.getElementById("oldPassword")
    var password = document.getElementById("password");
    var confirmPassword = document.getElementById("confirmPassword");
    // Enable these input fields to be editable
    firstName.disabled = false;
    lastName.disabled = false;
    mailingAddress.disabled = false;
    deliveryAddress.disabled = false;
    image_file.disabled = false;
    oldPassword.disabled = false;
    password.disabled = false;
    confirmPassword.disabled = false;
    // When cancelBtn is clicked, it will disable the input fields
    $('#cancelBtn').click(function () {
        $('#editBtn').show();
        $('#saveBtn, #cancelBtn').hide();

        firstName.disabled = true;
        lastName.disabled = true;
        mailingAddress.disabled = true;
        deliveryAddress.disabled = true;
        image_file.disabled = true;
        oldPassword.disabled = true;
        password.disabled = true;
        confirmPassword.disabled = true;
    });
}
var checkPassword = function() {
    if (document.getElementById('password').value > 8) {
        document.getElementById('message').style.color = 'green';
        document.getElementById('message').innerHTML = 'Password requirements satisfied.';

        if (document.getElementById('password').value ==
            document.getElementById('confirmPassword').value) {
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
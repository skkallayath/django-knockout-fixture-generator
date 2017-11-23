$("#signup_form").validate({
    rules: {
        username: {
            required: true,
            minlength: 2,
            alphanumeric: true
        },
        password: {
            required: true,
            minlength: 5
        },
        password_confirm: {
            required: true,
            minlength: 5,
            equalTo: "#password"
        }
    },
    messages: {
        username: {
            required: "Please enter a username",
            minlength: "Your username must consist of at least 2 characters",
            alphanumeric: "Special characters are not allowed"
        },
        password: {
            required: "Please provide a password",
            minlength: "Your password must be at least 5 characters long"
        },
        password_confirm: {
            required: "Please provide a password",
            minlength: "Your password must be at least 5 characters long",
            equalTo: "Please enter the same password as above"
        }
    },
    submitHandler: function (form) {
        form.submit();
    }
});
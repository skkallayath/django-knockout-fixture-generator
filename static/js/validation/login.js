$("#login-form").validate({
    rules: {
        username: {
            required: true
        },
        password: {
            required: true,
        }
    },
    messages: {
        username: {
            required: "Please enter username.",
        },
        password: {
            required: "Please enter password.",
        }
    }
});
function registration(event) {
    event.preventDefault();
    const email = $('#email').val();
    const pwd_1 = $('#pwd').val();
    const pwd_2 = $('#confirm-pwd').val();

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
        alert('Invalid email format');
        return;
    }
    if (pwd_1 !== pwd_2) {
        alert('Passwords do not match');
        return;
    }
    const userCredentials = {'email': email, 'password': pwd_1};
    $.post('/users', userCredentials, (response) => {
        alert(response.message);
    }).fail((whr, status, error) => {
        alert(status);
    });
}

function connect(event) {
    event.preventDefault();
    const email = $('#email').val();
    const pwd = $('#pwd').val();

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
        alert('Invalid email format');
        return;
    }

    const userCredentials = {'email': email, 'password': pwd};
    $.post('/sessions', userCredentials, (response) => {
        alert(response.message);
        window.location.href = '/';
    }).fail((whr, status, error) => {
        alert(error);
    });
}

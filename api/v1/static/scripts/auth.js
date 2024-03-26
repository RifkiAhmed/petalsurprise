function register(event) {
  event.preventDefault();
  const email = $('#email').val();
  const pwd_1 = $('#pwd').val();
  const pwd_2 = $('#confirm-pwd').val();

  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(email)) {
    $('.alert_message').text('Invalid email format');
    $('.alert-danger').css('display', 'block');
    setTimeout(() => $('.alert-danger').css('display', 'none'), 3000);
    return;
  }
  if (pwd_1 !== pwd_2 || pwd_1 === '') {
    $('.alert_message').text('Passwords do not match');
    if (pwd_1 === '') { $('.alert_message').text('Password should not be empty'); };
    $('.alert-danger').css('display', 'block');
    setTimeout(() => $('.alert-danger').css('display', 'none'), 3000);
    return;
  }
  $.ajax({
    method: 'POST',
    url: '/users',
    data: {'email': email, 'password': pwd_1},
    success: () => {
      connect(event);
    },
    error: (error) => {
      $('.alert_message').text(error.responseJSON.message);
      $('.alert-danger').css('display', 'block');
      setTimeout(() => $('.alert-danger').css('display', 'none'), 3000);
      console.log("Error:", error.responseJSON.message);
    }
  });
}

function connect(event) {
  event.preventDefault();
  const email = $('#email').val();
  const pwd = $('#pwd').val();
  $.ajax({
    method: 'POST',
    url: '/sessions',
    data: {'email': email, 'password': pwd},
    success: () => {
      window.location.href = '/';
    },
    error: () => {
      $('.alert_message').text('Invalid email, username, or password');
      $('.alert-danger').css('display', 'block');
      setTimeout(() => $('.alert-danger').css('display', 'none'), 3000);
      console.log("Error:", 'Incorrect email or password');
    }
  });
}

function disconnect(event) {
  event.preventDefault();
  $.ajax({
    method: 'DELETE',
    url: '/sessions',
    success: () => {
      setTimeout(() => window.location.href = '/', 100)
    },
    error: () => {
      console.log("Error:", 'Unauthorized!');
    }
  });
}

function dropDownMenu() {
  $('.menu-dropdown').css('display', 'block');
}

function signUp() {
  $('.btn-connect').css('display', 'none');
  $('.btn-sign-up').css('display', 'none');
  const link = $('.sign-up');
  if (link.text() === 'Sign In') {
    link.text('Sign Up');
    $('#username-label').text('Email or username:')
    $('#email').attr('placeholder', 'Email or username');
    $('.confirm-pwd').css('display', 'none');
    $('.user-account').text('Sign up for an account');
    $('.login-header').text('Sign In');
    $('.btn-connect').css('display', 'block');
  } else {
    link.text('Sign In');
    $('#username-label').text('Email:')
    $('#email').attr('placeholder', 'Email');
    $('.confirm-pwd').css('display', 'block');
    $('.user-account').text('Sign in to an existing account');
    $('.login-header').text('Sign Up');
    $('.btn-sign-up').css('display', 'block');
  }
};

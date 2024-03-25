function send(event, user) {
  event.preventDefault();
  removeWarning();
  const email = $('#email').val();
  const subject = $('#subject').val();
  const message = $('#message').val();
  if (user === 'False' && email === '') {
    $('#email').css('border', '2px solid red');
    $('#email').focus();
    return;
  } else if (subject === '') {
    $('#subject').css('border', '2px solid red');
    $('#subject').focus();
    return;
  } else if (message === '') {
    $('#message').css('border', '2px solid red');
    $('#message').focus();
    return;
  }
  $.ajax({
    type: "POST",
    url: "/contact",
    data: { email, subject, message },
    success: (response) => {
      clearText();
      $('.alert-info').css('display', 'block');
      $('.alert_message').text(`${response.message}, Thank you!`);
      
      
    },
    error: (error) => {
        console.log(`Error: ${error}`)
    }
  });
}

function removeWarning() {
  $('#email').css('border', '0px');
  $('#subject').css('border', '0px');
  $('#message').css('border', '0px');
}

function clearText() {
  $('#email').val('');
  $('#subject').val('');
  $('#message').val('');
}
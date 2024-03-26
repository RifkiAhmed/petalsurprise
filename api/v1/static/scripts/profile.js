function showUserNameInput() {
  $('#username-link').css('display', 'none');
  $('#username').css('display', 'inline-block');
  $('#save-username').css('display', 'inline-block');
}

function updateProfile(prop) {
  removeAlert();

  let data = {};

  if (prop === 'username') {
    const username = $('#username').val();
    if (username === '') {
      $('#username').css('border', '2px solid red');
      return;
    }
    data = { username };
  } else if (prop === 'email') {
    const newEmail = $('#email').val();
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(newEmail) || newEmail === '') {
      $('#email').css('border', '2px solid red');
      return;
    }
    data['email'] = newEmail;
  } else {
    const currentPassword = $('#pwd-0').val();
    const newPassword = $('#pwd-1').val();

    if (currentPassword === '') {
      $('#pwd-0').css('border', '2px solid red');
      return;
    }
    if (newPassword === '') {
      $('#pwd-1').css('border', '2px solid red');
      return;
    }
    if ($('#pwd-2').val() === '') {
      $('#pwd-2').css('border', '2px solid red');
      return;
    }
    if (newPassword !== $('#pwd-2').val()) {
      $('.alert-danger').css('display', 'block');
      $('.alert_message').html('<strong> Passwords do not match </strong>');
      setInterval(() =>  $('.alert-danger').css('display', 'none'), 3000);
      return;
    }
    data['currentPassword'] = currentPassword;
    data['password'] = newPassword;
  }

  $.ajax({
    url: '/profile',
    method: 'PUT',
    data,
    success: (response) => {
      window.location.href = '/profile';
      $('.alert-info').css('display', 'block');
      $('.alert-info').html(`<strong> ${response.message} successfully </strong>`);
      setInterval(() =>  $('.alert-info').css('display', 'none'), 3000);
    },
    error: (error) => {
      $('.alert-danger').css('display', 'block');
      if (prop === 'username') {
        $('.alert_message').html('<strong> Username already registred </strong>');
      } else if (prop === 'email') {
        $('.alert_message').html('<strong> Email already registred </strong>');
      } else $('.alert_message').html('<strong> Invalid password </strong>');
      setInterval(() =>  $('.alert-danger').css('display', 'none'), 3000);
    }
  });
}

function userOrders() {
  hideContainers();
  $('.li-orders').css('color', 'white');
  const $container = $('.list-orders');
  $container.css('display', 'block');
  $container.empty();
  const $table = $('<table class="table scroll" style="color: white;"></table>');
  $table.append(`<thead>
    <tr>
      <th></th>
      <th>Created at</th>
      <th>Recipient name</th>
      <th>Status</th>
      <th>Action</th>
    </tr>
  </thead>`);
  $.ajax({
    url: '/user_orders',
    method: 'GET',
    success: (response) => {
      let $ordersContent = response.map((order, i) => {
        let products = order.products.map((product, i) => `
        <tr>
          <td>N°${i + 1}</td>
          <td><img src="../static/flowers/${product.image}" height="40px"></td>
          <td>${product.name}</td>
        </tr>`).join('');
        return `
          <tr>
            <td><h6>N°${i + 1}</h6></td>
            <td><h6>${order.created_at}</h6></td>
            <td><h6>${order.recipient_name}</h6></td>     
            <td><h6>${order.status}</h6></td>
            <td><a class='link_${order.id}' href='#' onclick='showDetails(${order.id})'>details</a></td>      
          </tr>
          <tr class='${order.id}' style="display: none; color: black;">
            <td colspan='5' style='background-color: #6d597a'>
            <div style="width: 100%;">
              <h6>Message: ${order.message}</h6>
              <h6>Recipient address: ${order.recipient_address}</h6>
              <h6>Payment method type: ${order.payment_method_type}</h6>
              <h6>Total amount: $${order.amount}</h6>
              <br>
              <h6>Liste of orders:</h6>
              <table class='table'>
                <tr>
                  <th></th>
                  <th>Flower</th>
                  <th>Name</th>
                </tr>
                ${products}
              </table>
            </div>
            </td>
          </tr>`;
      }).join('');
    
      $table.append($ordersContent);
      $container.append($table);
    },
    error: () => {
      
    }
  })
}

function showDetails(order_id) {
  const $detailsRow = $(`.${order_id}`);
  if ($detailsRow.css('display') === 'none') {
    $detailsRow.css('display', 'table-row');
    $(`.link_${order_id}`).text('hide');
  } else {
    $detailsRow.css('display', 'none');
    $(`.link_${order_id}`).text('details');
  }
}

function userProfile() {
  hideContainers();
  $('.li-profile').css('color', 'white');
  $('.updateEmailForm').css('display', 'block');
}

function userWishes() {
  hideContainers();
  $('.li-wishes').css('color', 'white');
}

function showChangePassword() {
  hideContainers();
  $('.li-profile').css('color', 'white');
  $('.changePasswordForm').css('display', 'block');
}

function hideContainers() {
  $('li').css('color', 'grey');
  $('.updateEmailForm').css('display', 'none');
  $('.changePasswordForm').css('display', 'none');
  $('#email').css('border', '0px');
  $('#username').css('border', '0px');
  $('#pwd-0').css('border', '0px');
  $('#pwd-1').css('border', '0px');
  $('#pwd-2').css('border', '0px');
  $('.list-orders').css('display', 'none');
  $('.list-wishes').css('display', 'none');
  $('.alert-info').css('display', 'none');
  $('.alert-danger').css('display', 'none');
}

function removeAlert() {
  $('#username').css('border', '0px');
  $('#pwd-0').css('border', '0px');
  $('#pwd-1').css('border', '0px');
  $('#pwd-2').css('border', '0px');
}

function dropDownMenu() {
  $('.menu-dropdown').css('display', 'block');
}

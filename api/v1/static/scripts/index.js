const stripe = Stripe('pk_test_51OsCjcRoWq4O3O1iVOgvSSwgvhUGeMjnlC1FttsEeCbpptE1dUoGORd1D35ciVEQPaQbljUA9nZXhQMpf6favtky00IRNCXihG');
let cart = [];
let products = [];

$(document).ready(function() {
  const $badge = $('#badge');
  $badge.html(cart.length);
});

function checkoutRemoveBorders() {
  $('#sender-email').css('border', '0px');
  $('#recipient-name').css('border', '0px');
  $('#recipient-address').css('border', '0px');
}

function addToCart(product) {
  $('.list-items').eq(0).css('visibility', 'hidden');
  $('.add-new-item').eq(0).css('visibility', 'hidden');
  try {
    const $badge = $('#badge');
    const $count = parseInt($badge.html()) || 0;
    if (cart.some(item => item.id === product.id)) {
      cart = cart.filter(item => item.id !== product.id);
      $badge.html($count - 1);
      $(`#${product.id}`).css('color', '#ffffff');
    } else {
      cart.push(product);
      $badge.html($count + 1);
      $(`#${product.id}`).css('color', '#ffd60a');
    }
    localStorage.setItem('cart', JSON.stringify(cart));
  } catch (err) {
    console.error(err.message);
  }
}

async function showCartItems(product) {
  const $listOfItems = $('#list-items');
  const $table = $('<table class="table" style="background-color: rgba(0, 0, 0, 0.3); color: #ffffff"></table>');
  $table.append('<thead><tr><th></th><th>Flower</th><th>Price</th></tr></thead>');

  $listOfItems.empty();
  products = product ? [product] : cart;

  let $itemsContent = products.length > 0
    ? products.map((item, i) => `
    <tr>
    <td><h6 style="padding: 8px 0px">N°${i + 1}</h6></td>
    <td>
      <img src="../static/flowers/${item.img_path}" height="40px">
      <h6 style="display: inline-block">${item.name} #${item.id}</h6>
    </td>
    <td><h6 style="padding: 8px 0px">$${item.price}</h6></td>      
    </tr>`).join('')
    : 'Empty';
  
  const totalPrice = await products.reduce((total, item) => total + parseInt(item.price), 0);
  $itemsContent += `<tr><td colspan="2"><h5>Total :</h5></td><td><h5>$${totalPrice}</h5></td></tr>`
  $itemsContent = `<tbody>${$itemsContent}</tbody>`

  $table.append($itemsContent);
  $listOfItems.append($table);
  checkoutRemoveBorders();
  $('#sender-email').val('');
  $('#recipient-name').val('');
  $('#recipient-address').val('');
  $('#sender-message').val('');
  $('.list-items').eq(0).css('visibility', 'visible');
}

function showAddItemsModal(className) {
  $(`.${className}`).eq(0).css('visibility', 'visible');
}

function checkout(id) {
  checkoutRemoveBorders();
  const sender_email = $('#sender-email').val();
  const recipient_name = $('#recipient-name').val();
  const recipient_address = $('#recipient-address').val();
  const message = $('#sender-message').val();

  if (products.length === 0) return;
  if (sender_email === '' && id == null) {
    $('#sender-email').css('border', '2px solid red');
    $('#sender-email').focus();
    return;
  }

  if (sender_email === '' && id == null) {
    $('#sender-email').css('border', '2px solid red');
    $('#sender-email').focus();
    return;
  }
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(sender_email)) {
    $('#sender-email').css('border', '2px solid red');
    $('#sender-email').focus();
    return;
  }
  if (recipient_name === '') {
    $('#recipient-name').css('border', '2px solid red');
    $('#recipient-name').focus();
    return;
  }
  if (recipient_address === '') {
    $('#recipient-address').css('border', '2px solid red');
    $('#recipient-address').focus();
    return;
  }
  fetch('/create-checkout-session', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ cart: products, sender_email, recipient_name, recipient_address, message })
  })
  .then(function(response) {
    return response.json();
  })
  .then(function(session) {
    return stripe.redirectToCheckout({ sessionId: session.sessionId });
  })
  .then(function(result) {
    if (result.error) {
      console.error(result.error.message);
    }
  })
  .catch(function(error) {
    console.error('Error:', error);
  });
};

function showFilters() {
  $('.filters').toggle();
}

function searchWithName(event) {
  event.preventDefault();
  $('#search').css('border', '0px');
  let searchString = $('#search').val();

  if (searchString === '') {
    $('#search').css('border', '2px solid red');
    return;
  };
  $.ajax({
    method: 'POST',
    url: '/search',
    data: { 'search-string': searchString },
    success: (response) => { 
      displayProducts(response.products, response.user);
    },
    error: (error) => { console.log(`Error: ${error}`); }
  });
}


function productsWithinRange(event) {
  event.preventDefault();
  $('#min-price').css('border', '0px');
  $('#max_price').css('border', '0px');
  let min_price = $('#min-price').val();
  let max_price = $('#max-price').val();

  if (min_price === '' && max_price === '') {
    return;
  };
  $.ajax({
    method: 'POST',
    url: '/range',
    data: { min_price, max_price },
    success: (response) => { 
      displayProducts(response.products, response.user);
    },
    error: (error) => { console.log(`Error: ${error}`); }
  });
}

function sortProducts(element) {
  const selectedIndex = $(element).find('option:selected').index();
  const values = { 0: 'recent_listing', 1: 'low_to_hight', 2: 'high_to_low' };
  $.ajax({
    method: 'GET',
    url: `/index/products/${values[selectedIndex]}`,
    success: (response) => { 
      displayProducts(response.products, response.user);
    },
    error: (error) => { console.log(`Error: ${error}`); }
  });
}

function displayProducts(products, user) {
  $('.products').empty();
  const productsItems = products.map(product => {
    let btn_admin = '';
    if (user.is_admin) {
    btn_admin =
      `
      <div class="admin_buttons row">
      <div class="update_item col-sm-3" onclick='fillUpdateProductModal(${ product })'>
        <i class="fa fa-sync fa-2x"></i>
      </div>
      <div class="remove_item col-sm-3" onclick="deleteProduct(${ product.id })">
        <i class="fa fa-times fa-2x"></i>
      </div>
      </div>
      `;
    };
    return `
    <div class="item">
    <div>
      <div class="item_img">
        <div class="image-placeholder">
          <img id src="../static/flowers/${ product.img_path }" width="100%"/>
        </div>
        <div class="user_buttons row">
          <div class="add_to_cart col-sm-3" onclick='addToCart(${ product })'>
            <i id="${product.id}" class="fa fa-shopping-cart fa-2x"></i>
          </div>
          <div class="buy_item col-sm-8" onclick='showCartItems(${ product })'>
            Buy
          </div>
        </div>
        ${btn_admin}
      </div>
      <!-- flower name -->
      <div>
        <br>
        <span><h5>${ product.name }</h5></span>
        <!-- flower description -->
        <div>
          <h6>9 flowers</h6>
        </div>
      </div>
      <!-- flower price -->
      <div>
        <div class="item_price">
          <h5>Price</h5>
          <h5>${ product.price }</h5>
        </div>
      </div>
    </div>
    </div>
    `
  });
  $('.products').append(productsItems);
}

const stripe = Stripe('pk_test_51OsCjcRoWq4O3O1iVOgvSSwgvhUGeMjnlC1FttsEeCbpptE1dUoGORd1D35ciVEQPaQbljUA9nZXhQMpf6favtky00IRNCXihG');
let cart = [];

$(document).ready(function() {
  const $badge = $('#badge');
  $badge.html(cart.length);
});

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
  console.log('Updated cart:', cart);
}

async function showCartItems(product) {
  const $listOfItems = $('#list-items');
  const $table = $('<table class="table" style="background-color: #272640; color: #ffffff"></table>');
  $table.append('<thead><tr><th></th><th>Flower</th><th>Price</th></tr></thead>');

  $listOfItems.empty();
  const products = product ? [product] : cart;

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
  $itemsContent += `<tr><td colspan="2"><h4>Total :</h4></td><td><h4>$${totalPrice}</h4></td></tr>`
  $itemsContent = `<tbody>${$itemsContent}</tbody>`

  $table.append($itemsContent);
  $listOfItems.append($table);
  $('.list-items').eq(0).css('visibility', 'visible');
}

function showAddItemsModal(className) {
  $(`.${className}`).eq(0).css('visibility', 'visible');
}

function checkout() {
  const recipient_name = $('#recipient-name').val();
  const recipient_address = $('#recipient-address').val();
  const message = $('#sender-message').val();

  if (cart.length === 0) return;
  if (recipient_name === '') {
    $('#name').css('border', '2px solid red');
    $('#address').css('border', '0px');
    return;
  }
  if (recipient_address === '') {
    $('#name').css('border', '0px');
    $('#address').css('border', '2px solid red');
    return;
  }
  fetch('/create-checkout-session', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ cart, recipient_name, recipient_address, message })
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

function buy(id) {
  fetch('/create-checkout-session', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ cart: [{id: id, name: "Buy 1", price: 10000}] })
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


function sortProducts(element) {
  const selectedIndex = $(element).find('option:selected').index();
  const values = { 0: 'recent_listing', 1: 'low_to_hight', 2: 'high_to_low' };
  $.ajax({
    method: 'GET',
    url: `/index/products/${values[selectedIndex]}`,
    success: (response) => { 
      displayProducts(response.products, response.page, response.user);
    },
    error: (error) => { console.log(`Error: ${error}`); }
  });
}


function displayProducts(products, page, user) {
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
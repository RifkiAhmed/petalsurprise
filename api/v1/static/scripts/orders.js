document.addEventListener('DOMContentLoaded', function() {
  orderStatus(undefined, 'Load');
});

function orderStatus(event, arg) {
  if (event) {
    event.preventDefault();
  }
  const status = $('#status').val();
  data = { status };
  if (arg !== 'Load') {
    const from = $('#from').val();
    const to = $('#to').val();
    if (from) {
      data = { ...data, from};
    }
    if (to) {
      data = { ...data, to};
    }
  }

  $.ajax({
    type: "GET",
    url: "/orders",
    data,
    success: (response) => {
      updateTable(response);
    },
    error: (error) => {
      console.log(error.message);
    }
  });
}

function updateStatus(orderId, status) {
  $.ajax({
    type: "PUT",
    url: "/orders",
    data: { id: orderId, status },
    success: (response) => {
      orderStatus();
    },
    error: (error) => {
      console.log(error.message);
    }
  });
}

function refundCustomer(chargeId, orderId) {
  $.ajax({
    type: "PUT",
    url: "/refund",
    data: { chargeId, orderId },
    success: (response) => {
      orderStatus();
    },
    error: (error) => {
      console.log(error.message);
    }
  });
}

function updateTable(data) {
  const tbody = $('#orders-table-tbody');
  tbody.empty();
  const rows = data.map(order => {
    let actions;
    let products = order.products.map((product, i) => `
    <tr>
      <th style='border: none'>N°${i + 1}</th>
      <th style='border: none'><img src="../static/flowers/${product.image}" height="40px"></th>
      <th style='border: none'>${product.name}</th>
      <th style='border: none'>$ ${product.price}</th>
    </tr>`).join('');
    switch (order.status) {
    case 'Pending':
      actions = `
      <th style="color: #4cc9f0;">
        <i class="fas fa-truck" onclick="updateStatus(${order.id}, 'Delivering')"
           data-toggle="tooltip" data-placement="left" title="Deliver"></i>
      </th>
      <th style="color: #dc3545;">
        <i class="fas fa-times" onclick="updateStatus(${order.id}, 'Cancelled')"
           data-toggle="tooltip" data-placement="left" title="Cancel"></i>
      </th>
      `;
      break;
    case 'Cancelled':
      actions = `
      <th colspan="2" style="text-align: center; color: #6c757d;">
        <i class="fas fa-money-check-alt" onclick="refundCustomer('${order.charge_id}', ${order.id})"
           data-toggle="tooltip" data-placement="left" title="Refund"></i>
      </th> 
      `;
      break;
    case 'Delivering':
      actions = `
      <th style="color: #28a745;">
        <i class="fas fa-check" onclick="updateStatus(${order.id}, 'Delivered')"
           data-toggle="tooltip" data-placement="left" title="Delivered"></i>
      </th>
      <th style="color: #dc3545;">
        <i class="fas fa-times" onclick="updateStatus(${order.id}, 'Cancelled')"
           data-toggle="tooltip" data-placement="left" title="Cancel"></i>
      </th>
      `;
      break;
    case 'Delivered':
      actions = `
      <th colspan="2" style="text-align: center; color: #28a745;"><i class="fas fa-check"
          data-toggle="tooltip" data-placement="left" title="Delivered"></i></th>
      `
      break;
    case 'Refunded':
      actions = `
      <th colspan="2" style="text-align: center; color: #6c757d;"><i class="fas fa-check"
          data-toggle="tooltip" data-placement="left" title="Refunded"></i></th>
      `
      break;
    }
    return `
    <tr class='main_${order.id}'>
    <th><i class="fas fa-eye show-details_${order.id}"  onclick="showDetails(${order.id})"
        data-toggle="tooltip" data-placement="left" title="Plus"></i></th>         
    <th>${order.created_at}</th>
    <th>${order.recipient_name}</th>
    <th>${order.recipient_address}</th>
    <th>${order.message}</th>
    <th>${order.number_of_products}</th>
    <th>$ ${order.amount}</th>
    <th>${order.status}</th>
    ${actions}
    </tr>
    <tr class='details_${order.id}' style="display: none; color: black;">
    <th colspan='11' style='background-color: #6d597a; border: none'>
      <div style="width: 100%;">
        <h6 style="border-top: 2px solid grey; padding-top: 15px">
           <u><b>Charge ID:</b></u> <br>${order.charge_id}
        </h6>
        <h6><u><b>Payment Method Type:</b></u> <br>${order.payment_method_type}</h6>
	<h6><u><b>Sender:</b></u> <br>${order.user_email}</h6>
        <h6><u><b>List Items:</b></u></h6>
        <table class='table'>
          <tr>
            <th style='border: none'></th>
            <th style='border: none'>Flower</th>
            <th style='border: none'>Name</th>
            <th style='border: none'>Price</th>
          </tr>
          ${products}
        </table>
      </div>
    </th>
    </tr>`
  });
  tbody.append(rows);
}

let show_details_id;
function showDetails(order_id) {
  const $mainRow = $(`.main_${order_id}`);
  const $detailsRow = $(`.details_${order_id}`);
  
  $("[class^='main_']").css('background-color', '#272640');
  $("[class^='main_']").css('color', '#ffffff');
  $(`.show-details_${show_details_id}`).removeClass('fa-eye-slash');
  $(`.show-details_${show_details_id}`).addClass('fa-eye');
  $detailsRow.find('th').css('border', 'none');

  if ($detailsRow.css('display') === 'none') {
    $("[class^='details_']").css('display', 'none');
    $mainRow.css('color', '#000000');
    $mainRow.css('background-color', '#6d597a');
    $detailsRow.css('display', 'table-row');
    $(`.show-details_${order_id}`).addClass('fa-eye-slash');
    $(`.show-details_${order_id}`).removeClass('fa-eye');
  } else {
    $detailsRow.css('display', 'none');
    $(`.show-details_${order_id}`).removeClass('fa-eye-slash');
    $(`.show-details_${order_id}`).addClass('fa-eye');
  }
  show_details_id = order_id;
}

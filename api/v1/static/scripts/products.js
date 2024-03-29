// Remove borders style of the inputs fields
function removeBorders() {
  $("#flower-name").css('border', '0px');
  $("#flower-price").css('border', '0px');
  $(".custom-file").css('outline', '0px');
  $("#product-new-name").css('border', '0px');
  $("#product-new-price").css('border', '0px');
}

// Add new product to the database
function addProducts(event) {
  event.preventDefault();
  removeBorders();
  const name = $("#flower-name").val();
  const price = $("#flower-price").val();
  const description = $("#flower-description").val();
  const path = $("#customFile")[0].files[0];

  if (name === '') {
    $("#flower-name").css('border', '2px solid red');
    return;
  }
  if (price === '') {
    $("#flower-price").css('border', '2px solid red');
    return;
  }

  if (path === undefined) {
    $(".custom-file").css('outline', '2px solid red');
    return;
  }

  const formData = new FormData();
  formData.append("name", name);
  formData.append("price", price);
  formData.append("description", description);
  formData.append("image", path);

  $.ajax({
    method: 'POST',
    url: "/products",
    data: formData,
    processData: false,
    contentType: false,
    success: () => {
      window.location.href = '/';
    },
    error: (error) => {
      $('.alert_message').text(error.responseJSON.error);
      $('.alert-danger').css('display', 'block');
      setTimeout(() => $('.alert-danger').css('display', 'none'), 3000);
      console.log("Error:", error.responseJSON.error);
    },
  });
}

// Delete product with the id passed as agument from the database
function deleteProduct(id) {
  $.ajax({
    type: "DELETE",
    url: "/products",
    data: { id: id },
    success: () => {
      window.location.href = "/";
    },
    error: (error) => {
      console.log(error.message);
    }
  });
}

// Fill inputs fields of the update product modal with the data of the product passed as argument
function fillUpdateProductModal(product) {
  $('#product-name-id').text(`${product.name} #${product.id}`);
  $('#product-new-name').val(product.name);
  $('#product-new-price').val(product.price);
  $('#product-new-description').val(product.description);
  $('#product-image').attr('src', `../static/flowers/${product.img_path}`).css({
    'width': '305px',
    'height': '305px',
    'border-radius': '8px'
  });
  $('#submit-update-product').attr('onclick', `submitUpdateProduct(event, ${product.id})`)
  $('#updateProduct').modal('show');
}

// Submit the changes for the product with the id passed as argument
function submitUpdateProduct(event, id) {
  event.preventDefault();
  removeBorders();
  const name = $("#product-new-name").val();
  const price = $("#product-new-price").val();
  const description = $("#product-new-description").val();
  const path = $("#newCustomFile")[0].files[0];

  if (name === '') {
    $("#product-new-name").css('border', '2px solid red');
    return;
  }
  if (price === '') {
    $("#product-new-price").css('border', '2px solid red');
    return;
  }

  const formData = new FormData();
  formData.append("id", id);
  formData.append("name", name);
  formData.append("price", price);
  formData.append("description", description);
  formData.append("image", path);

  $.ajax({
    method: "PUT",
    url: "/products",
    data: formData,
    processData: false,
    contentType: false,
    success: () => {
      window.location.href = '/';
    },
    error: (error) => {
      $('.update_alert_message').text(JSON.parse(error.responseText).error);
      $('.update-alert-danger').css('display', 'block');
      setTimeout(() => $('.update-alert-danger').css('display', 'none'), 3000);
      console.log("Error:", JSON.parse(error.responseText).error);
    },
  });
}

function removeWarning() {
  $("#flower-name").css('border', '0px');
  $("#flower-price").css('border', '0px');
  $(".custom-file").css('outline', '0px');
}

function addProducts(event) {
  event.preventDefault();
  removeWarning();
  const name = $("#flower-name").val();
  const price = $("#flower-price").val();
  const path = $("#customFile")[0].files[0];
  const formData = new FormData();
  formData.append("name", name);
  formData.append("price", price);
  formData.append("image", path);

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
      console.log(error.message);
    },
  });
}

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

function fillUpdateProductModal(product) {
  $('#product-name-id').text(`${product.name} #${product.id}`);
  $('#product-new-name').val(product.name).prop('disabled', true);
  $('#product-new-price').val(product.price).prop('disabled', true);
  $('#product-image').attr('src', `../static/flowers/${product.img_path}`).css({
    'width': '305px',
    'height': '305px',
    'border-radius': '8px'
  });
  $('#submit-update-product').attr('onclick', `submitUpdateProduct(event, ${product.id})`)
  $('#updateProduct').modal('show');
}

function submitUpdateProduct(event, id) {
  event.preventDefault();
  const name = $("#product-new-name").val();
  const price = $("#product-new-price").val();
  const path = $("#newCustomFile")[0].files[0];
  const formData = new FormData();
  formData.append("id", id);
  formData.append("name", name);
  formData.append("price", price);
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
      console.log(error.message);
    },
  });
}


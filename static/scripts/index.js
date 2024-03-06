let carts = [];

function addToCart(id) {
    try {
        const badge = document.getElementById('badge');
        const count = badge.innerHTML;
        if (carts.includes(id)) {
            const parsedCount = parseInt(count) || 0;
            badge.innerHTML = parsedCount - 1;
            carts = carts.filter(item => item !== id);
        } else {
            carts.push(id);
            badge.innerHTML = parseInt(count) + 1;
        }
        toggleCartColor(id);
    }
    catch (err) {
        console.error(err.message);
    }
}

function toggleCartColor(id) {
    var cartIcon = document.getElementById(id);
    if (cartIcon.classList.contains('green')) {
      cartIcon.classList.remove('green');
      cartIcon.classList.add('Sky-Blue');
    } else {
      cartIcon.classList.remove('Sky-Blue');
      cartIcon.classList.add('green');
    }
}

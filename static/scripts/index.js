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

function showCartItems() {
    const listOfItems = document.getElementById('list-items');
    const unorderedList = document.createElement('ul');
    while (listOfItems.firstChild) {
        listOfItems.removeChild(listOfItems.firstChild);
    }
    const itemsContent = carts.length > 0
        ? carts.map(item => `<li>${item}</li>`).join('')
        : 'Empty';

    unorderedList.innerHTML = itemsContent;
    listOfItems.appendChild(unorderedList);
    document.getElementsByClassName('list-items')[0].style.visibility = 'visible';
}


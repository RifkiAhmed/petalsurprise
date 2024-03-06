let carts = [];

function addToCart(id) {
    $('.list-items').eq(0).css('visibility', 'hidden');
    $('.add-new-item').eq(0).css('visibility', 'hidden');
    try {
        const $badge = $('#badge');
        const $count = parseInt($badge.html()) || 0;
        if (carts.includes(id)) {
            $badge.html($count - 1);
            carts = carts.filter(item => item !== id);
        } else {
            carts.push(id);
            $badge.html($count + 1);
        }
        toggleCartColor(id);
    } catch (err) {
        console.error(err.message);
    }
}

function toggleCartColor(id) {
    if ($(`#${id}`).hasClass('green')) {
        $(`#${id}`).removeClass('green');
        $(`#${id}`).addClass('Sky-Blue');
    } else {
        $(`#${id}`).removeClass('Sky-Blue');
        $(`#${id}`).addClass('green');
    }
}

function showCartItems() {
    const $listOfItems = $('#list-items');
    const $unorderedList = $('<ul></ul>');
    $listOfItems.empty();

    const $itemsContent = carts.length > 0
        ? carts.map(item => `<li>${item}</li>`).join('')
        : 'Empty';

    $unorderedList.html($itemsContent);
    $listOfItems.append($unorderedList);
    $('.list-items').eq(0).css('visibility', 'visible');
}

function showAddItemsModal(className) {
    $(`.${className}`).eq(0).css('visibility', 'visible');
}

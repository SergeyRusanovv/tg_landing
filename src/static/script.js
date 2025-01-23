// Используется в онлайн магазине

const products = [
    { id: 1, name: 'Cheeseburger', price: 5.99 },
    { id: 2, name: 'Double Cheeseburger', price: 7.99 },
    { id: 3, name: 'Veggie Burger', price: 4.99 },
];

let cart = [];

function displayProducts() {
    const productList = document.getElementById('product-list');
    products.forEach(product => {
        const productDiv = document.createElement('div');
        productDiv.classList.add('product');
        productDiv.innerHTML = `
            <h3>${product.name}</h3>
            <p>Price: $${product.price.toFixed(2)}</p>
            <button onclick="addToCart(${product.id})">Add to Cart</button>
        `;
        productList.appendChild(productDiv);
    });
}

function addToCart(productId) {
    const product = products.find(p => p.id === productId);
    cart.push(product);
    updateCart();
}

function updateCart() {
    const cartItems = document.getElementById('cart-items');
    cartItems.innerHTML = '';
    let total = 0;

    cart.forEach(item => {
        const li = document.createElement('li');
        li.textContent = `${item.name} - $${item.price.toFixed(2)}`;
        cartItems.appendChild(li);
        total += item.price;
    });

    document.getElementById('total-price').textContent = total.toFixed(2);
}

document.getElementById('checkout-button').addEventListener('click', () => {
    alert('Proceeding to checkout!');
});

displayProducts();

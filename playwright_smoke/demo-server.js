const express = require('express');
const path = require('path');
const app = express();
const PORT = 3000;

// Middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// In-memory storage
let products = [
    { id: 1, name: 'Laptop', price: 999, stock: 10 },
    { id: 2, name: 'Phone', price: 599, stock: 5 },
    { id: 3, name: 'Tablet', price: 399, stock: 8 }
];

let users = [];
let orders = [];
let cart = [];

// HTML template function
function htmlTemplate(title, body) {
    return `
<!DOCTYPE html>
<html>
<head>
    <title>${title}</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .nav { background: #333; padding: 10px; margin-bottom: 20px; }
        .nav a { color: white; text-decoration: none; margin-right: 20px; }
        .product { border: 1px solid #ddd; padding: 10px; margin: 10px 0; }
        .btn { background: #007bff; color: white; padding: 8px 16px; border: none; cursor: pointer; }
        .btn:hover { background: #0056b3; }
        .error { color: red; }
        .success { color: green; }
        .cart-item { background: #f8f9fa; padding: 10px; margin: 5px 0; }
    </style>
</head>
<body>
    <div class="nav">
        <a href="/">Home</a>
        <a href="/products">Products</a>
        <a href="/cart">Cart (${cart.length})</a>
        <a href="/login">Login</a>
        <a href="/register">Register</a>
    </div>
    ${body}
</body>
</html>`;
}

// Routes
app.get('/', (req, res) => {
    const body = `
    <h1>Welcome to Demo E-Commerce</h1>
    <p>This is a demo e-commerce site for smoke testing.</p>
    <p><a href="/products" class="btn">Browse Products</a></p>
    <p><a href="/cart" class="btn">View Cart (${cart.length} items)</a></p>
  `;
    res.send(htmlTemplate('Home - Demo Shop', body));
});

app.get('/products', (req, res) => {
    const productList = products.map(p => `
    <div class="product">
      <h3>${p.name}</h3>
      <p>Price: $${p.price}</p>
      <p>Stock: ${p.stock}</p>
      <form method="post" action="/cart/add" style="display: inline;">
        <input type="hidden" name="productId" value="${p.id}">
        <button type="submit" class="btn">Add to Cart</button>
      </form>
    </div>
  `).join('');

    const body = `
    <h1>Products</h1>
    ${productList}
  `;
    res.send(htmlTemplate('Products - Demo Shop', body));
});

app.get('/cart', (req, res) => {
    const cartItems = cart.map(item => {
        const product = products.find(p => p.id === item.productId);
        return `
      <div class="cart-item">
        <h4>${product.name}</h4>
        <p>Price: $${product.price}</p>
        <p>Quantity: ${item.quantity}</p>
        <form method="post" action="/cart/remove" style="display: inline;">
          <input type="hidden" name="productId" value="${item.productId}">
          <button type="submit" class="btn">Remove</button>
        </form>
      </div>
    `;
    }).join('');

    const total = cart.reduce((sum, item) => {
        const product = products.find(p => p.id === item.productId);
        return sum + (product.price * item.quantity);
    }, 0);

    const body = `
    <h1>Shopping Cart</h1>
    ${cartItems || '<p>Your cart is empty</p>'}
    <h3>Total: $${total}</h3>
    ${cart.length > 0 ? '<a href="/checkout" class="btn">Checkout</a>' : ''}
  `;
    res.send(htmlTemplate('Cart - Demo Shop', body));
});

app.post('/cart/add', (req, res) => {
    const productId = parseInt(req.body.productId);
    const existingItem = cart.find(item => item.productId === productId);

    if (existingItem) {
        existingItem.quantity += 1;
    } else {
        cart.push({ productId, quantity: 1 });
    }

    res.redirect('/cart');
});

app.post('/cart/remove', (req, res) => {
    const productId = parseInt(req.body.productId);
    cart = cart.filter(item => item.productId !== productId);
    res.redirect('/cart');
});

app.get('/login', (req, res) => {
    const body = `
    <h1>Login</h1>
    <form method="post" action="/login">
      <p>
        <label>Username:</label><br>
        <input type="text" name="username" required>
      </p>
      <p>
        <label>Password:</label><br>
        <input type="password" name="password" required>
      </p>
      <p>
        <button type="submit" class="btn">Login</button>
      </p>
    </form>
    <p><a href="/register">Don't have an account? Register here</a></p>
  `;
    res.send(htmlTemplate('Login - Demo Shop', body));
});

app.post('/login', (req, res) => {
    const { username, password } = req.body;
    const user = users.find(u => u.username === username && u.password === password);

    if (user) {
        res.redirect('/');
    } else {
        const body = `
      <h1>Login</h1>
      <p class="error">Invalid username or password</p>
      <form method="post" action="/login">
        <p>
          <label>Username:</label><br>
          <input type="text" name="username" required>
        </p>
        <p>
          <label>Password:</label><br>
          <input type="password" name="password" required>
        </p>
        <p>
          <button type="submit" class="btn">Login</button>
        </p>
      </form>
    `;
        res.send(htmlTemplate('Login - Demo Shop', body));
    }
});

app.get('/register', (req, res) => {
    const body = `
    <h1>Register</h1>
    <form method="post" action="/register">
      <p>
        <label>Username:</label><br>
        <input type="text" name="username" required>
      </p>
      <p>
        <label>Email:</label><br>
        <input type="email" name="email" required>
      </p>
      <p>
        <label>Password:</label><br>
        <input type="password" name="password" required>
      </p>
      <p>
        <button type="submit" class="btn">Register</button>
      </p>
    </form>
    <p><a href="/login">Already have an account? Login here</a></p>
  `;
    res.send(htmlTemplate('Register - Demo Shop', body));
});

app.post('/register', (req, res) => {
    const { username, email, password } = req.body;

    if (users.find(u => u.username === username)) {
        const body = `
      <h1>Register</h1>
      <p class="error">Username already exists</p>
      <form method="post" action="/register">
        <p>
          <label>Username:</label><br>
          <input type="text" name="username" required>
        </p>
        <p>
          <label>Email:</label><br>
          <input type="email" name="email" required>
        </p>
        <p>
          <label>Password:</label><br>
          <input type="password" name="password" required>
        </p>
        <p>
          <button type="submit" class="btn">Register</button>
        </p>
      </form>
    `;
        res.send(htmlTemplate('Register - Demo Shop', body));
    } else {
        users.push({ username, email, password });
        res.redirect('/login');
    }
});

app.get('/checkout', (req, res) => {
    const total = cart.reduce((sum, item) => {
        const product = products.find(p => p.id === item.productId);
        return sum + (product.price * item.quantity);
    }, 0);

    const body = `
    <h1>Checkout</h1>
    <h3>Order Total: $${total}</h3>
    <form method="post" action="/checkout">
      <p>
        <label>Card Number:</label><br>
        <input type="text" name="cardNumber" placeholder="1234 5678 9012 3456" required>
      </p>
      <p>
        <label>Expiry Date:</label><br>
        <input type="text" name="expiry" placeholder="MM/YY" required>
      </p>
      <p>
        <label>CVV:</label><br>
        <input type="text" name="cvv" placeholder="123" required>
      </p>
      <p>
        <button type="submit" class="btn">Place Order</button>
        <a href="/cart" class="btn" style="background: #6c757d;">Back to Cart</a>
      </p>
    </form>
  `;
    res.send(htmlTemplate('Checkout - Demo Shop', body));
});

app.post('/checkout', (req, res) => {
    const orderId = orders.length + 1;
    orders.push({
        id: orderId,
        items: [...cart],
        timestamp: new Date()
    });
    cart = []; // Clear cart

    const body = `
    <h1>Order Confirmation</h1>
    <p class="success">Thank you! Your order #${orderId} has been placed successfully.</p>
    <p><a href="/" class="btn">Continue Shopping</a></p>
  `;
    res.send(htmlTemplate('Order Confirmation - Demo Shop', body));
});

// API Routes
app.get('/api/products', (req, res) => {
    res.json(products);
});

app.get('/api/health', (req, res) => {
    res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

// 404 handler
app.use((req, res) => {
    res.status(404).send(htmlTemplate('Page Not Found', '<h1>404 - Page Not Found</h1>'));
});

app.listen(PORT, () => {
    console.log(`🚀 Demo E-Commerce Server running at http://localhost:${PORT}`);
    console.log(`📝 Demo data initialized with ${products.length} products`);
    console.log(`🛑 Press Ctrl+C to stop the server`);
});
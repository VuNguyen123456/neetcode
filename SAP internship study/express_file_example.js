// server.js
const express = require('express');
const app = express();

app.use(express.json());          // parse JSON bodies
app.use(express.urlencoded({ extended: true })); // parse form data

// --- Routes ---

// GET — read data
app.get('/accounts', async (req, res) => {
  try {
    const accounts = await db.query('SELECT * FROM accounts');
    res.json(accounts);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Failed to fetch accounts' });
  }
});

// GET with a URL parameter
app.get('/accounts/:id', async (req, res) => {
  try {
    const account = await db.query('SELECT * FROM accounts WHERE id = ?', [req.params.id]);
    if (!account) {
      return res.status(404).json({ error: 'Account not found' });
    }
    res.json(account);
  } catch (err) {
    res.status(500).json({ error: 'Failed to fetch account' });
  }
});

// POST — create something new
app.post('/accounts', async (req, res) => {
  try {
    const { name, balance } = req.body;   // destructuring the request body
    const newAccount = await db.query(
      'INSERT INTO accounts (name, balance) VALUES (?, ?)',
      [name, balance]
    );
    res.status(201).json(newAccount);
  } catch (err) {
    res.status(500).json({ error: 'Failed to create account' });
  }
});

// --- Middleware (runs before your routes) ---
app.use((req, res, next) => {
  console.log(`${req.method} ${req.url}`);
  next();  // pass control to the next thing in line
});

// --- Start the server ---
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));


// To run stuff along each other (at tge sane tune)
const [profile, orders] = await Promise.all([
    getProfile(id),
    getOrders(id),
]);
// Insteaad of this

const profile = getProfile(id);
const orders = getOrders(id);

// req object in Express
app.get('/accounts/:id', (req, res) => {
  console.log(req.params);
  res.json({ message: `You asked for account ${req.params.id}` });
});

// example URL is: GET /accounts/42
// req.params        // { id: "42" }
// req.params.id     // "42"   (note: it's a string, even though it looks like a number)

app.get('/accounts/:accountId/transactions/:transactionId', (req, res) => {
  req.params.accountId;      // e.g. "42"
  req.params.transactionId;  // e.g. "17"
});

// the :id is a place holder so req.params able to get you the actual value you got from that place holder

// req.params is directly from URL path
// req.body is the JSON (form data) sent in the request body 
// Request: POST /accounts  body: { "name": "Acme", "balance": 5000 }
app.post('/accounts', (req, res) => {
  req.body.name;     // "Acme"
  req.body.balance;  // 5000
});

//req.query => everything after the ? in the URL => Optional stuff like filter, sorting,...
// URL: /accounts?sort=name&limit=10
app.get('/accounts', (req, res) => {
  req.query.sort;   // "name"
  req.query.limit;  // "10"  (note: always a string, even if it looks like a number)
});

// Quiz
app.get('/users/:userId/posts/:postId', (req, res) => {
  
});
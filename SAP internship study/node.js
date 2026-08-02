// JS

let count = 5;
const name = "vu";

//Function

function add(a, b) {
    return a + b;
}

const add = function(a, b) {return a + b;};
const add = (a,b) => a + b; // Arrow function

const account = { id: 1, name: "Acme Corp", balance: 5000 }; 
// Accessing
account.balance;
account["balance"];

const accounts = [account1, account2, account3];
accounts.map(a => a.name) // new array of just names
accounts.filter(a => a.balance > 1000) // New array with only matching a with balance > 1000
accounts.find(a => a.id === 1);         // first match, or undefined

// const id = account.id;
// const name = account.name;

const { id, name } = account;        // instead of account.id, account.name
const [first, second] = accounts;    // same idea for arrays

const accounts = ["Acme Corp", "Beta Inc", "Gamma LLC"];
const [first, second] = accounts;
// first = "Acme Corp", second = "Beta Inc"

const msg = 'Acc ${id} has balance ${balance}';

const updated = { ...account, balance : 6000}; // Copy the whole account but overwrite the balance
const combined = [...arr1, ...arr2]; // Common from Reat too (will revisit later)

// Node can read files, talk to db, hanndle web page
// Basically JS unleashed from the browser

// Async by default:
// "I'll go ask the database for this data, but I'm not going to sit and wait. I'll go do other work, and you tell me when the answer's ready."

// Promise: "I don't have your value yet, but I will."
// 3 States:
// pending (still waiting)
// fulfilled (got the value)
// rejected (something went wrong)

// async/await
// 1. If a function does anything async (db call) => it's async
// 2. Inside an async function, when you call something that return a promise you need o put await infront of it so it doesn't move to the next line until it's actually done

async function getAccount(id) {
    const result = await db.query('SELECT * FROM accounts WHERE id = ?', [id]);
    return result;
}

// Node.js pattern

// math.js
function add(a, b) { return a + b; }
module.exports = { add };

// app.js
const { add } = require('./math');

async function getAccount(id) {
    try{
        const result = await db.query('SELECT * FROM accounts WHERE id = ?', [id]);
        return result;
    } catch (err) {
        console.error('Query failed:', err);
        throw err;  // re-throw so whoever called this knows it failed        
    }
}

// 3. Express route: handling a web request 
// EXPRESSSSSSSSSSSSSSS - routing and shit here
const express = require('express');
const app = express();
app.use(express.json());

app.get('/accounts/:id', async (req, res) => {
    try{
        const account = await getAccount(req.params.id);
        res.json(account);
    } catch (err) {
        res.status(500).json({ error: 'Something went wrong' });
    }
});

app.listen(3000);

// 4. Running multiple async things at once
const [account, transactions] = await Promise.all([
    getAccount(id),
    getTransactions(id),
]);




// async/await patterns you'll see constantly
async function processOrder(orderId) {
    const order = await getOrder(orderId);
    const customer = await getCustomer(order.customerId); // needs order first
    return { order, customer };
}

// Running multiple async things at once => Promise.all
async function getDashboard(userId) {
  const [account, transactions, notifications] = await Promise.all([
    getAccount(userId),
    getTransactions(userId),
    getNotifications(userId),
  ]);
  return { account, transactions, notifications };
}
// GET     /accounts        → get all accounts
// GET     /accounts/5      → get one specific account
// POST    /accounts        → create a new account
// PUT     /accounts/5      → replace account 5 entirely
// PATCH   /accounts/5      → update part of account 5
// DELETE  /accounts/5      → delete account 5

const { request } = require("node:http")

app.get('/accounts/:id', ...)     // READ one
app.post('/accounts', ...)        // CREATE
app.put('/accounts/:id', ...)     // REPLACE
app.patch('/accounts/:id', ...)   // UPDATE part
app.delete('/accounts/:id', ...)  // DELETE

// calling someone else REST API:
// in JS
const res = await fetch('https://api.example.com/accounts/5');
const data = await res.json()

// in python:
const res = await fetch('https://api.example.com/accounts/5');
data = res.json()
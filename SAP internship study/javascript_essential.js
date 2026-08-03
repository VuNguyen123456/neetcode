const balances = [500, 1200, 300];
// Arrow function
const total = balances.reduce((sum, current) => sum + current, 0);
// (sum, current) => sum + current — the function that runs once per item
// sum — the "running total" so far (called the accumulator)
// current — the item currently being looked at
// 0 — the starting value for sum, before any items are processed

const accounts = [
  { name: "Acme", balance: 5000 },
  { name: "Beta", balance: 3000 },
  { name: "Gamma", balance: 1200 },
];

// const totalBalance = accounts.balance.reduce((sum, current) => sum + current, 0) => DOESN"T WORK
const totalBalance = accounts.reduce((sum, current) => sum + current.balance, 0)

// SORT: ordering an array
const numbers = [5, 1, 8, 3];
numbers.sort((a, b) => a - b) // ascending: [1, 3, 5, 8]
numbers.sort((a, b) => b - a) // descending: [8, 5, 3, 1]

// return negative → a comes first
// return positive → b comes first
// return 0 → leave their order as-is

//Sorting object by field
const accounts = [
  { name: "Beta", balance: 3000 },
  { name: "Acme", balance: 5000 },
  { name: "Gamma", balance: 1200 },
];
accounts.sort((a, b) => a.balance - b.balance); // ascending: [1, 3, 5, 8] due to it being negative
// if you want to make a copy instead of mutate
const sarr2 = [...accounts].sort((a, b) => a.balance - b.balance);

// Chaining together!!
const total = accounts
  .filter(acc => acc.balance > 0)           // only positive balances
  .sort((a, b) => b.balance - a.balance)    // highest first
  .reduce((sum, acc) => sum + acc.balance, 0); // sum them up
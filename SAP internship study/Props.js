// Parent component that passes props to child components
function AccountList(){
    const accounts = [
        { id: 1, name: "Acme Corp", balance: 5000 },
        { id: 2, name: "Beta Inc", balance: 3000 },
    ];

    // The <AccountCard /> is the inner child here!!!
    return (
        <div>
        {accounts.map(acc => (
            <AccountCard key={acc.id} name={acc.name} balance={acc.balance} />
        ))}
        </div>
    );
}

// Child component
function AccountCard({ name, balance }) {
  return (
    <div className="card">
      <h3>{name}</h3>
      <p>Balance: ${balance}</p>
    </div>
  );
}

// AccountList is called "parent" here only because it's the one that renders AccountCard

// This is not inheritance; it's just passing data down from parent to child components via props.
// "Parent/child" in React just describes which component renders which — it's a tree of function calls, not a class hierarchy.

function outer() {
  return inner("some value"); // outer calls inner, passes it an argument
}

function inner(value) {
  return value.toUpperCase();
}
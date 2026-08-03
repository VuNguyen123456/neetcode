// Optional chaining => ?.

const account = { name: "Acme Corp" };
account.address.city; // CRASHES: "Cannot read properties of undefined"

account.address?.city;  //  undefined — no crash

// => ?. means "if the thing on the left is null or undefined, 
// stop right here and just return undefined instead of throwing.
// " If account.address did exist, it works exactly like a normal ..

// Work in a lot of case in JS 
<h1>{account?.name}</h1>

// Function call
onDelete?.();  // only calls onDelete if it exists, otherwise does nothing

user?.profile?.address?.city  // safe even if user, profile, or address is missing

// Nullish coalescing — ??
// providing a fallback value, but only when something is actually null/undefined 
// not for other "falsy" values like 0 or "".
const balance = account.balance ?? 0;
// If account.balance is null or undefined, use 0 instead. If it's any other value — including 0 itself — keep it as-is.

// Putting together:
function AccountCard({ account }) {
  return (
    <div>
      <h3>{account?.name ?? "Unnamed account"}</h3>
      <p>Balance: ${account?.balance ?? 0}</p>
    </div>
  );
}

// <h3>{account?.name ?? "Unnamed account"}</h3> => So write the name if it exist if not right Unamed acc?


// 1. Imports
import { useState, useEffect } from 'react';

// 2. Component definition (function, capitalized name)
function AccountList() {

  // 3. State — all your useState calls, usually grouped at the top
  const [accounts, setAccounts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  // accounts is the current value. setAccounts is the only correct way to change it — you never do accounts = newValue directly, because React wouldn't know that happened.
  // calling the setter function (setAccounts(...))


  // 4. Effects — side effects like fetching data, subscriptions
  // Run after every render, or only when certain values change (dependency array)
  useEffect(() => {
    async function fetchAccounts() {
      try {
        const res = await fetch('/api/accounts');
        setAccounts(await res.json());
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }
    fetchAccounts();
  }, []); // the dependency array is empty, so this effect runs only once, after the first render
  // if the dependency array had values, it would run after the first render and whenever those values changed

  // 5. Event handlers — functions triggered by user actions
  function handleDelete(id) {
    setAccounts(accounts.filter(a => a.id !== id));
    fetch(`/api/accounts/${id}`, { method: 'DELETE' });
  }

  // 6. Early returns for loading/error states
  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error: {error}</p>;

  // 7. The actual JSX being rendered
  return (
    <ul>
      {accounts.map(a => (
        <li key={a.id}>
          {a.name}
          <button onClick={() => handleDelete(a.id)}>Delete</button>
        </li>
      ))}
    </ul>
  );
}

// 8. Export
export default AccountList;

// Concretely, step by step:

// 1. You call setAccounts(newData)
// 2. React schedules a re-render of that component
// 3. React re-runs the entire component function top to bottom — yes, the whole thing, including your JSX at the bottom
// 3. This time, when the code hits useState([]), React quietly hands back newData instead of [] — that's the "remembering across renders" part
// 4. Since accounts is now newData, your JSX (accounts.map(...)) renders differently — new list on screen
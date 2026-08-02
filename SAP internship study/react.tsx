// useState handles the "store it" part, 
// useEffect handles the "when it loads" part.

// useState - holding a value that can change
const [accounts, setAccounts] = useState([]);

function useState(arg0: never[]): [any, any] {
    throw new Error("Function not implemented.");
}

// useEffect: running code in response to something
useEffect(() => {
  // code here runs after the component renders
}, [dependencyArray]);

// Together
function AccountList() {
    // useState - holding a value that can change
    const [accounts, setAccounts] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        async function fetchAccounts() {
            try {
                const res = await fetch('/api/accounts');
                const data = await res.json();
                setAccounts(data);
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        fetchAccounts();
        }, []); // empty array = run once when this component loads
    }

    if (loading) return <p>Loading...</p>;
    if (error) return <p>Error: {error}</p>;
    
    return (
        <ul>
        {accounts.map(a => <li key={a.id}>{a.name}</li>)}
        </ul>
    );
}

1. Component renders the first time → accounts is [], loading is true → shows "Loading..."
2. useEffect fires after that first render, kicks off the fetch
3. Data comes back → setAccounts(data) and setLoading(false) are called
4. Those set calls trigger a re-render → now loading is false, accounts has real data → the list actually shows

function AccountDetail({ accountId }) {
  const [account, setAccount] = useState(null);

  useEffect(() => {
    async function fetchAccount() {
      const res = await fetch(`/api/accounts/${accountId}`);
      setAccount(await res.json());
    }
    fetchAccount();
  }, [accountId]); // re-runs whenever accountId changes

  if (!account) return <p>Loading...</p>;
  return <h1>{account.name}</h1>;
}
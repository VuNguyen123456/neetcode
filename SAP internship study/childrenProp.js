function Card({ children }) {
  return <div className="card">{children}</div>;
}

function App() {
  return (
    <Card>
      <h3>Acme Corp</h3>
      <p>Balance: $5000</p>
    </Card>
  );
}

//children is a special, automatic prop — whatever JSX you put between a 
// component's opening and closing tags gets passed in as children, 
// without you naming it explicitly like other props.

<Card>
  <h3>Acme Corp</h3>
</Card>

// is basically the same as writing:
Card({ children: <h3>Acme Corp</h3> })


// Let you build one reusable wrapper (styling, layout, behavior) that works with any content inside
function Card({ children }) {
  return <div className="card">{children}</div>;
}

// same Card, totally different content each time
<Card><h3>Acme Corp</h3><p>$5000</p></Card>
<Card><img src="chart.png" /></Card>
<Card><button>Click me</button></Card>

// Everything between <Card> and </Card> — that's <h3>Acme Corp</h3><p>$5000</p> — becomes children


//
function Modal({ title, children, onClose }) {
  return (
    <div className="modal">
      <div className="modal-header">
        <h2>{title}</h2>
        <button onClick={onClose}>×</button>
      </div>
      <div className="modal-body">{children}</div>
    </div>
  );
}

<Modal title="Confirm Delete" onClose={() => setShowModal(false)}>
  <p>Are you sure you want to delete this account?</p>
</Modal>


//

function Card({ children }) {
  return <div className="card">{children}</div>;
}

function AccountPage() {
  return <Card><h3>Acme Corp</h3></Card>;
}

function ProductPage() {
  return <Card><h3>Some Product</h3></Card>;   // reused elsewhere too
}

// same idea as calling a regular function twice with different arguments.
function double(x) {
  return x * 2;
}

double(5);   // x = 5 this time
double(10);  // x = 10 this time, totally separate call

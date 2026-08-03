// useContext — sharing state without passing props through every level

// Without context — painful
function App() {
  const user = { name: "Vu" };
  return <Layout user={user} />;
}
function Layout({ user }) {
  return <Sidebar user={user} />; // Layout doesn't need user, just passing it through
}
function Sidebar({ user }) {
  return <UserBadge user={user} />; // same here
}
function UserBadge({ user }) {
  return <p>{user.name}</p>; // finally actually used
}

// 
import { createContext, useContext, useState } from 'react';

// 1. Create the context (usually in its own file)
const UserContext = createContext(null);

// 2. Wrap your app in a Provider, give it a value
function App() {
  const [user, setUser] = useState({ name: "Vu" });
  return (
    <UserContext.Provider value={user}>
      <Layout />
    </UserContext.Provider>
  );
}

// 3. Middle components don't mention user at all anymore
function Layout() {
  return <Sidebar />;
}
function Sidebar() {
  return <UserBadge />;
}

// 4. Whoever actually needs it just grabs it directly
function UserBadge() {
  const user = useContext(UserContext);
  return <p>{user.name}</p>;
}

// ANOTHER Example of context:
// Wuthout context, you have to pass the theme through every level of the tree
function App() {
  const user = { name: "Vu" };
  return <Layout user={user} />;          // App must pass it
}

function Layout({ user }) {
  return <Sidebar user={user} />;         // Layout doesn't use it, just relays
}

function Sidebar({ user }) {
  return <UserBadge user={user} />;       // Sidebar doesn't use it, just relays
}

function UserBadge({ user }) {
  return <p>{user.name}</p>;              // finally actually used
}

// Every single component between App and UserBadge has to accept user as a prop and manually pass it along, even though Layout and Sidebar never touch it.

// With Context (App → Layout → Sidebar → UserBadge) nesting itself never goes away, with or without context:
const UserContext = createContext(null);

function App() {
  const user = { name: "Vu" };
  return (
    <UserContext.Provider value={user}>
      <Layout />                          {/* no user prop needed */}
    </UserContext.Provider>
  );
}

function Layout() {
  return <Sidebar />;                     // no user prop needed
}

function Sidebar() {
  return <UserBadge />;                   // no user prop needed
}

function UserBadge() {
  const user = useContext(UserContext);   // pulls it directly
  return <p>{user.name}</p>;
}


// What context removes is only the data traveling alongside that nesting — not the nesting itself. Without context:
<Layout user={user} />       // structure AND data both passed
<Layout />                   // just structure, no data riding along
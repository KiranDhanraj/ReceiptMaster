import { BrowserRouter, Routes, Route, Navigate, Link, useNavigate } from "react-router-dom";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import Upload from "./pages/Upload";
import Help from "./pages/Help";
import About from "./pages/About";
import { clearTokens, getUsername, hasAccessToken } from "./services/api";

type ProtectedRouteProps = {
  children: JSX.Element;
};

function ProtectedRoute({ children }: ProtectedRouteProps) {
  if (!hasAccessToken()) {
    return <Navigate to="/login" replace />;
  }
  return children;
}

function Navigation() {
  const navigate = useNavigate();
  const handleLogout = () => {
    clearTokens();
    navigate("/login");
  };
  const isAuthenticated = hasAccessToken();
  const username = getUsername();

  return (
    <nav>
      {isAuthenticated && username ? (
        <span>{username} is logged in</span>
      ) : null}
      {isAuthenticated && username ? " | " : null}
      {!isAuthenticated ? (
        <>
          <Link to="/login">Login</Link> | <Link to="/register">Register</Link> |{" "}
        </>
      ) : null}
      <Link to="/dashboard">Dashboard</Link> | <Link to="/upload">Upload</Link> |{" "}
      <Link to="/help">Help</Link> | <Link to="/about">About</Link>
      {isAuthenticated ? (
        <>
          {" "}|{" "}
          <button type="button" onClick={handleLogout}>
            Logout
          </button>
        </>
      ) : null}
    </nav>
  );
}

function App() {
  return (
    <BrowserRouter>
      <Navigation />
      <Routes>
        <Route path="/" element={<Navigate to="/login" replace />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <Dashboard />
            </ProtectedRoute>
          }
        />
        <Route
          path="/upload"
          element={
            <ProtectedRoute>
              <Upload />
            </ProtectedRoute>
          }
        />
        <Route path="/help" element={<Help />} />
        <Route path="/about" element={<About />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
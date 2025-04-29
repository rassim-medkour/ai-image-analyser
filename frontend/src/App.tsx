import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './store/auth/AuthContext';
import ProtectedRoute from './components/common/ProtectedRoute';
import Register from './pages/auth/Register';
import Login from './pages/auth/Login';
import Layout from './components/layout/Layout';
import UploadImage from './pages/images/UploadImage';
import ImagesPage from './pages/images/ImagesPage';
import './App.css';

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          {/* Public routes */}
          <Route element={<Layout />}>
            <Route path="/" element={<Navigate to="/images" replace />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />

            {/* Protected routes */}
            <Route element={<ProtectedRoute />}>
              <Route path="/images" element={<ImagesPage />} />
              <Route path="/images/upload" element={<UploadImage />} />
              <Route path="/profile" element={<div>Profile Page (to be implemented)</div>} />
            </Route>

            {/* Catch all route */}
            <Route path="*" element={<div>404 - Not Found</div>} />
          </Route>
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;

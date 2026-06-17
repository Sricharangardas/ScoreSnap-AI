import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Navbar from './components/Navbar';
import DynamicIsland from './components/DynamicIsland';
import Dashboard from './pages/Dashboard';
import Matches from './pages/Matches';
import Standings from './pages/Standings';
import Insights from './pages/Insights';
import SettingsPage from './pages/Settings';
import Login from './pages/Login';
import Register from './pages/Register';
import MatchSummaryModal from './components/MatchSummaryModal';
import { authAPI } from './services/api';
import { RefreshCw } from 'lucide-react';

export default function App() {
  const [darkMode, setDarkMode] = useState(true); // Default to gorgeous dark mode
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [selectedMatchId, setSelectedMatchId] = useState(null);

  // Sync dark mode HTML classes
  useEffect(() => {
    if (darkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [darkMode]);

  // Fetch logged-in user profile if token is present
  useEffect(() => {
    const checkAuth = async () => {
      const token = localStorage.getItem('token');
      if (token) {
        try {
          const res = await authAPI.me();
          setUser(res.data);
        } catch (err) {
          console.error("Token verification failed:", err);
          localStorage.removeItem('token');
          setUser(null);
        }
      }
      setLoading(false);
    };
    checkAuth();
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('token');
    setUser(null);
  };

  const handlePreferencesUpdated = (updatedUser) => {
    setUser(updatedUser);
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-[#000000] text-white flex flex-col items-center justify-center gap-3">
        <RefreshCw className="animate-spin text-apple-blue-dark" size={32} />
        <span className="text-xs font-bold tracking-widest uppercase text-apple-text-subDark">
          Initializing ScoreSnap AI...
        </span>
      </div>
    );
  }

  return (
    <Router>
      <div className={`min-h-screen transition-colors duration-300 ${
        darkMode ? 'bg-apple-bg-dark text-white' : 'bg-apple-bg-light text-slate-900'
      }`}>
        
        {/* Dynamic Island Notification Overlay */}
        <DynamicIsland onOpenMatchSummary={(id) => setSelectedMatchId(id)} />

        {/* Floating Glass Navigation */}
        <Navbar 
          darkMode={darkMode} 
          setDarkMode={setDarkMode} 
          user={user} 
          onLogout={handleLogout} 
        />

        {/* Global Page Wrapper */}
        <main className="max-w-7xl mx-auto pt-24 pb-12 px-4 sm:px-6 lg:px-8">
          <Routes>
            <Route 
              path="/" 
              element={<Dashboard darkMode={darkMode} user={user} onOpenMatchSummary={(id) => setSelectedMatchId(id)} />} 
            />
            <Route 
              path="/matches" 
              element={<Matches darkMode={darkMode} user={user} onOpenMatchSummary={(id) => setSelectedMatchId(id)} />} 
            />
            <Route 
              path="/standings" 
              element={<Standings darkMode={darkMode} user={user} />} 
            />
            <Route 
              path="/insights" 
              element={<Insights darkMode={darkMode} user={user} />} 
            />
            <Route 
              path="/settings" 
              element={
                user ? (
                  <SettingsPage 
                    darkMode={darkMode} 
                    user={user} 
                    onPreferencesUpdated={handlePreferencesUpdated} 
                  />
                ) : (
                  <Navigate to="/login" replace />
                )
              } 
            />
            <Route 
              path="/login" 
              element={<Login darkMode={darkMode} onLoginSuccess={(u) => setUser(u)} />} 
            />
            <Route 
              path="/register" 
              element={<Register darkMode={darkMode} />} 
            />
            {/* Fallback to Dashboard */}
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </main>

        {/* Global AI Summary Modal Overlay */}
        {selectedMatchId && (
          <MatchSummaryModal 
            matchId={selectedMatchId} 
            onClose={() => setSelectedMatchId(null)} 
            darkMode={darkMode} 
          />
        )}
      </div>
    </Router>
  );
}

import React from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { Sun, Moon, LogOut, ShieldAlert, Award, Calendar, BarChart2, Info, Settings, LayoutDashboard } from 'lucide-react';

export default function Navbar({ darkMode, setDarkMode, user, onLogout }) {
  const location = useLocation();
  const navigate = useNavigate();

  const navItems = [
    { name: 'Dashboard', path: '/', icon: LayoutDashboard },
    { name: 'Matches', path: '/matches', icon: Calendar },
    { name: 'Standings', path: '/standings', icon: BarChart2 },
    { name: 'Insights', path: '/insights', icon: Award },
    { name: 'Settings', path: '/settings', icon: Settings },
  ];

  return (
    <nav className={`fixed top-4 left-1/2 -translate-x-1/2 w-[92%] max-w-7xl z-50 rounded-full transition-all duration-300 ${
      darkMode ? 'glass-nav-dark shadow-appleDark' : 'glass-nav-light shadow-appleLight'
    } px-6 py-3 flex items-center justify-between`}>
      {/* Logo */}
      <Link to="/" className="flex items-center gap-2">
        <span className="text-xl font-bold tracking-tight bg-gradient-to-r from-apple-blue-light to-blue-500 bg-clip-text text-transparent dark:from-apple-blue-dark dark:to-cyan-400">
          ScoreSnap AI
        </span>
        <div className="bg-apple-blue-light/10 text-apple-blue-light dark:bg-apple-blue-dark/15 dark:text-apple-blue-dark px-2 py-0.5 rounded-full text-[10px] font-semibold">
          WC 2026
        </div>
      </Link>

      {/* Nav Tabs */}
      <div className="hidden md:flex items-center gap-1 bg-black/5 dark:bg-white/5 p-1 rounded-full">
        {navItems.map((item) => {
          const isActive = location.pathname === item.path;
          const Icon = item.icon;
          return (
            <Link
              key={item.path}
              to={item.path}
              className={`flex items-center gap-2 px-4 py-1.5 rounded-full text-xs font-medium transition-all duration-300 ${
                isActive
                  ? (darkMode ? 'bg-white text-black shadow-md scale-105' : 'bg-black text-white shadow-md scale-105')
                  : (darkMode ? 'text-apple-text-subDark hover:text-white' : 'text-apple-text-subLight hover:text-black')
              }`}
            >
              <Icon size={14} />
              {item.name}
            </Link>
          );
        })}
      </div>

      {/* Right Controls */}
      <div className="flex items-center gap-3">
        {/* Dark Mode Toggle */}
        <button
          onClick={() => setDarkMode(!darkMode)}
          className={`p-2 rounded-full transition-colors ${
            darkMode ? 'hover:bg-white/10 text-yellow-400' : 'hover:bg-black/5 text-slate-700'
          }`}
          aria-label="Toggle Theme"
        >
          {darkMode ? <Sun size={18} /> : <Moon size={18} />}
        </button>

        {/* User Info / Auth Buttons */}
        {user ? (
          <div className="flex items-center gap-3">
            <span className="hidden sm:inline text-xs font-semibold px-3 py-1 rounded-full border border-black/10 dark:border-white/10 max-w-[120px] truncate">
              ⚽ {user.name}
            </span>
            <button
              onClick={onLogout}
              className={`p-2 rounded-full transition-colors ${
                darkMode ? 'hover:bg-red-500/20 text-apple-red-dark' : 'hover:bg-red-500/10 text-apple-red-light'
              }`}
              title="Logout"
            >
              <LogOut size={18} />
            </button>
          </div>
        ) : (
          <Link
            to="/login"
            className="text-xs font-semibold px-4 py-2 rounded-full bg-apple-blue-light hover:bg-blue-600 text-white shadow-appleBlue transition-all duration-200"
          >
            Log In
          </Link>
        )}
      </div>
    </nav>
  );
}

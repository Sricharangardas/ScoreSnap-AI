import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { authAPI } from '../services/api';
import { Mail, Lock, ShieldAlert, Check } from 'lucide-react';

export default function Login({ onLoginSuccess, darkMode }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await authAPI.login(email, password);
      localStorage.setItem('token', response.data.access_token);
      
      // Fetch user profile info
      const userProfile = await authAPI.me();
      onLoginSuccess(userProfile.data);
      navigate('/');
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.detail || 'Invalid email or password. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-[85vh] flex items-center justify-center px-4">
      <div className={`w-full max-w-md p-8 rounded-[30px] border transition-all duration-300 ${
        darkMode ? 'glass-card-dark' : 'glass-card-light'
      }`}>
        <div className="text-center mb-8">
          <h2 className="text-2xl font-bold tracking-tight mb-2 text-slate-900 dark:text-white">
            Welcome Back
          </h2>
          <p className="text-xs text-apple-text-subLight dark:text-apple-text-subDark">
            Enter your credentials to access your World Cup dashboard
          </p>
        </div>

        {error && (
          <div className="mb-6 p-4 rounded-2xl bg-red-500/10 border border-red-500/20 text-apple-red-light dark:text-apple-red-dark text-xs flex items-center gap-2">
            <ShieldAlert size={16} />
            <span>{error}</span>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-5">
          <div>
            <label className="block text-xs font-semibold mb-2 text-slate-700 dark:text-slate-300">
              Email Address
            </label>
            <div className="relative">
              <span className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400">
                <Mail size={16} />
              </span>
              <input
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="alex@apple.com"
                className="w-full pl-11 pr-4 py-3 rounded-2xl border border-black/10 dark:border-white/10 bg-transparent text-sm focus:outline-none focus:ring-2 focus:ring-apple-blue-light dark:focus:ring-apple-blue-dark transition-all"
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold mb-2 text-slate-700 dark:text-slate-300">
              Password
            </label>
            <div className="relative">
              <span className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400">
                <Lock size={16} />
              </span>
              <input
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                className="w-full pl-11 pr-4 py-3 rounded-2xl border border-black/10 dark:border-white/10 bg-transparent text-sm focus:outline-none focus:ring-2 focus:ring-apple-blue-light dark:focus:ring-apple-blue-dark transition-all"
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-apple-blue-light hover:bg-blue-600 dark:bg-apple-blue-dark dark:hover:bg-blue-700 text-white font-semibold py-3 rounded-2xl text-sm transition-all shadow-appleBlue hover:scale-[1.01] active:scale-[0.99] disabled:opacity-50"
          >
            {loading ? 'Signing In...' : 'Sign In'}
          </button>
        </form>

        <div className="mt-8 text-center text-xs text-apple-text-subLight dark:text-apple-text-subDark">
          Don't have an account?{' '}
          <Link to="/register" className="text-apple-blue-light dark:text-apple-blue-dark font-semibold hover:underline">
            Register for Free
          </Link>
        </div>
      </div>
    </div>
  );
}

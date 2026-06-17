import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { authAPI } from '../services/api';
import { User, Mail, Lock, ShieldAlert, CheckCircle2 } from 'lucide-react';

export default function Register({ darkMode }) {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      await authAPI.register(name, email, password);
      setSuccess(true);
      setTimeout(() => {
        navigate('/login');
      }, 2000);
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.detail || 'Registration failed. Email might already be registered.');
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
            Create Account
          </h2>
          <p className="text-xs text-apple-text-subLight dark:text-apple-text-subDark">
            Register to monitor matches, receive digests, and configure alerts
          </p>
        </div>

        {error && (
          <div className="mb-6 p-4 rounded-2xl bg-red-500/10 border border-red-500/20 text-apple-red-light dark:text-apple-red-dark text-xs flex items-center gap-2">
            <ShieldAlert size={16} />
            <span>{error}</span>
          </div>
        )}

        {success && (
          <div className="mb-6 p-4 rounded-2xl bg-emerald-500/10 border border-emerald-500/20 text-emerald-600 dark:text-emerald-400 text-xs flex items-center gap-2">
            <CheckCircle2 size={16} className="animate-bounce" />
            <span>Account created successfully! Redirecting to login...</span>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-5">
          <div>
            <label className="block text-xs font-semibold mb-2 text-slate-700 dark:text-slate-300">
              Full Name
            </label>
            <div className="relative">
              <span className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400">
                <User size={16} />
              </span>
              <input
                type="text"
                required
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="Alex Smith"
                className="w-full pl-11 pr-4 py-3 rounded-2xl border border-black/10 dark:border-white/10 bg-transparent text-sm focus:outline-none focus:ring-2 focus:ring-apple-blue-light dark:focus:ring-apple-blue-dark transition-all"
              />
            </div>
          </div>

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
                placeholder="Min. 8 characters"
                minLength={8}
                className="w-full pl-11 pr-4 py-3 rounded-2xl border border-black/10 dark:border-white/10 bg-transparent text-sm focus:outline-none focus:ring-2 focus:ring-apple-blue-light dark:focus:ring-apple-blue-dark transition-all"
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={loading || success}
            className="w-full bg-apple-blue-light hover:bg-blue-600 dark:bg-apple-blue-dark dark:hover:bg-blue-700 text-white font-semibold py-3 rounded-2xl text-sm transition-all shadow-appleBlue hover:scale-[1.01] active:scale-[0.99] disabled:opacity-50"
          >
            {loading ? 'Creating Account...' : 'Register'}
          </button>
        </form>

        <div className="mt-8 text-center text-xs text-apple-text-subLight dark:text-apple-text-subDark">
          Already have an account?{' '}
          <Link to="/login" className="text-apple-blue-light dark:text-apple-blue-dark font-semibold hover:underline">
            Log In
          </Link>
        </div>
      </div>
    </div>
  );
}

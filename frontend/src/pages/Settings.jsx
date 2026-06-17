import React, { useState } from 'react';
import { usersAPI } from '../services/api';
import { Settings, Save, ShieldCheck, Mail, MessageSquare, Info, Star } from 'lucide-react';

export default function SettingsPage({ darkMode, user, onPreferencesUpdated }) {
  const [favoriteTeam, setFavoriteTeam] = useState(user?.favorite_team || 'None');
  const [notificationsEnabled, setNotificationsEnabled] = useState(user?.notifications_enabled ?? true);
  const [dailyDigestEnabled, setDailyDigestEnabled] = useState(user?.daily_digest_enabled ?? true);
  const [preferredLanguage, setPreferredLanguage] = useState(user?.preferred_language || 'English');
  
  // WhatsApp settings
  const [whatsappEnabled, setWhatsappEnabled] = useState(user?.whatsapp_enabled ?? false);
  const [whatsappPhone, setWhatsappPhone] = useState(user?.whatsapp_phone || '');
  const [whatsappApikey, setWhatsappApikey] = useState(user?.whatsapp_apikey || '');

  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setSuccess(false);

    try {
      const response = await usersAPI.updatePreferences({
        favorite_team: favoriteTeam,
        notifications_enabled: notificationsEnabled,
        daily_digest_enabled: dailyDigestEnabled,
        preferred_language: preferredLanguage,
        whatsapp_enabled: whatsappEnabled,
        whatsapp_phone: whatsappPhone || null,
        whatsapp_apikey: whatsappApikey || null
      });

      onPreferencesUpdated(response.data);
      setSuccess(true);
      setTimeout(() => setSuccess(false), 3000);
    } catch (err) {
      console.error("Failed to update preferences:", err);
      alert("Failed to update settings. Please check your inputs.");
    } finally {
      setLoading(false);
    }
  };

  const teams = [
    'None', 'Algeria', 'Argentina', 'Australia', 'Austria', 'Belgium', 'Bosnia and Herzegovina',
    'Brazil', 'Curaçao', 'Canada', 'Cape Verde', 'Colombia', 'Croatia', 'Czechia', 'DR Congo',
    'Ecuador', 'Egypt', 'England', 'France', 'Germany', 'Ghana', 'Haiti', 'Iran', 'Iraq',
    'Ivory Coast', 'Japan', 'Jordan', 'Mexico', 'Morocco', 'Netherlands', 'New Zealand',
    'Norway', 'Panama', 'Paraguay', 'Portugal', 'Qatar', 'Saudi Arabia', 'Scotland',
    'Senegal', 'South Africa', 'South Korea', 'Spain', 'Sweden', 'Switzerland', 'Tunisia',
    'Türkiye', 'USA', 'Uruguay', 'Uzbekistan'
  ];

  const languages = ['English', 'Hindi', 'Spanish', 'French', 'German'];

  return (
    <div className="space-y-8 py-6 max-w-3xl mx-auto px-4 sm:px-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold tracking-tight text-slate-900 dark:text-white">
          Account Settings & Preferences
        </h1>
        <p className="text-xs text-apple-text-subLight dark:text-apple-text-subDark">
          Configure notifications, choose your favorite team, and customize AI summary languages
        </p>
      </div>

      {success && (
        <div className="p-4 rounded-2xl bg-emerald-500/10 border border-emerald-500/20 text-emerald-600 dark:text-emerald-400 text-xs flex items-center gap-2">
          <ShieldCheck size={16} />
          <span>Settings saved successfully! Your agent will apply these updates.</span>
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-6">
        
        {/* Core Preferences Card */}
        <div className={`p-6 rounded-[24px] border ${
          darkMode ? 'glass-card-dark border-white/5 shadow-appleDark' : 'glass-card-light border-black/5 shadow-appleLight'
        } space-y-6`}>
          <h3 className="text-sm font-bold uppercase tracking-wider text-slate-800 dark:text-slate-200 flex items-center gap-1.5 border-b border-black/5 dark:border-white/5 pb-3">
            <Star size={16} className="text-amber-500" /> Football Intelligence
          </h3>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-xs font-semibold mb-2 text-slate-700 dark:text-slate-300">
                Favorite Team
              </label>
              <select
                value={favoriteTeam}
                onChange={(e) => setFavoriteTeam(e.target.value)}
                className="w-full text-xs p-3 rounded-xl border border-black/10 dark:border-white/10 bg-transparent focus:outline-none focus:ring-1 focus:ring-apple-blue-light"
              >
                {teams.map(t => (
                  <option key={t} value={t} className="text-black">{t}</option>
                ))}
              </select>
              <span className="text-[10px] text-apple-text-subLight dark:text-apple-text-subDark mt-1.5 block">
                Highlights your team on standings and flags relevant fixtures.
              </span>
            </div>

            <div>
              <label className="block text-xs font-semibold mb-2 text-slate-700 dark:text-slate-300">
                AI Summary Language
              </label>
              <select
                value={preferredLanguage}
                onChange={(e) => setPreferredLanguage(e.target.value)}
                className="w-full text-xs p-3 rounded-xl border border-black/10 dark:border-white/10 bg-transparent focus:outline-none focus:ring-1 focus:ring-apple-blue-light"
              >
                {languages.map(l => (
                  <option key={l} value={l} className="text-black">{l}</option>
                ))}
              </select>
              <span className="text-[10px] text-apple-text-subLight dark:text-apple-text-subDark mt-1.5 block">
                Gemini translates tactical analyses and headlines to this language.
              </span>
            </div>
          </div>
        </div>

        {/* Notifications Channels Card */}
        <div className={`p-6 rounded-[24px] border ${
          darkMode ? 'glass-card-dark border-white/5 shadow-appleDark' : 'glass-card-light border-black/5 shadow-appleLight'
        } space-y-6`}>
          <h3 className="text-sm font-bold uppercase tracking-wider text-slate-800 dark:text-slate-200 flex items-center gap-1.5 border-b border-black/5 dark:border-white/5 pb-3">
            <Mail size={16} className="text-apple-blue-light" /> Email Notifications
          </h3>

          <div className="space-y-4">
            <label className="flex items-center gap-3 cursor-pointer">
              <input
                type="checkbox"
                checked={notificationsEnabled}
                onChange={(e) => setNotificationsEnabled(e.target.checked)}
                className="w-4 h-4 rounded text-apple-blue-light border-black/10 dark:border-white/10 focus:ring-apple-blue-light"
              />
              <div>
                <span className="text-xs font-bold text-slate-800 dark:text-slate-200">Enable Match Completed Emails</span>
                <p className="text-[10px] text-apple-text-subLight dark:text-apple-text-subDark">Receive one summary email immediately after any match finishes.</p>
              </div>
            </label>

            <label className="flex items-center gap-3 cursor-pointer">
              <input
                type="checkbox"
                checked={dailyDigestEnabled}
                onChange={(e) => setDailyDigestEnabled(e.target.checked)}
                className="w-4 h-4 rounded text-apple-blue-light border-black/10 dark:border-white/10 focus:ring-apple-blue-light"
              />
              <div>
                <span className="text-xs font-bold text-slate-800 dark:text-slate-200">Enable Daily Morning Digest</span>
                <p className="text-[10px] text-apple-text-subLight dark:text-apple-text-subDark">Receive a morning brief summarizing all matches played overnight.</p>
              </div>
            </label>
          </div>
        </div>

        {/* WhatsApp Notification Card */}
        <div className={`p-6 rounded-[24px] border ${
          darkMode ? 'glass-card-dark border-white/5 shadow-appleDark' : 'glass-card-light border-black/5 shadow-appleLight'
        } space-y-6`}>
          <h3 className="text-sm font-bold uppercase tracking-wider text-slate-800 dark:text-slate-200 flex items-center gap-1.5 border-b border-black/5 dark:border-white/5 pb-3">
            <MessageSquare size={16} className="text-emerald-500" /> WhatsApp bot Alerts (CallMeBot)
          </h3>

          <label className="flex items-center gap-3 cursor-pointer mb-4">
            <input
              type="checkbox"
              checked={whatsappEnabled}
              onChange={(e) => setWhatsappEnabled(e.target.checked)}
              className="w-4 h-4 rounded text-emerald-500 border-black/10 dark:border-white/10 focus:ring-emerald-500"
            />
            <div>
              <span className="text-xs font-bold text-slate-800 dark:text-slate-200">Enable WhatsApp Alerts</span>
              <p className="text-[10px] text-apple-text-subLight dark:text-apple-text-subDark">Send match briefings and daily digests directly to WhatsApp.</p>
            </div>
          </label>

          {whatsappEnabled && (
            <div className="space-y-4 pt-2 border-t border-black/5 dark:border-white/5">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-semibold mb-2 text-slate-700 dark:text-slate-300">
                    Phone Number (With Country Code)
                  </label>
                  <input
                    type="text"
                    required={whatsappEnabled}
                    value={whatsappPhone}
                    onChange={(e) => setWhatsappPhone(e.target.value)}
                    placeholder="+919876543210"
                    className="w-full text-xs p-3 rounded-xl border border-black/10 dark:border-white/10 bg-transparent focus:outline-none focus:ring-1 focus:ring-apple-blue-light"
                  />
                </div>

                <div>
                  <label className="block text-xs font-semibold mb-2 text-slate-700 dark:text-slate-300">
                    CallMeBot WhatsApp API Key
                  </label>
                  <input
                    type="password"
                    required={whatsappEnabled}
                    value={whatsappApikey}
                    onChange={(e) => setWhatsappApikey(e.target.value)}
                    placeholder="e.g. 123456"
                    className="w-full text-xs p-3 rounded-xl border border-black/10 dark:border-white/10 bg-transparent focus:outline-none focus:ring-1 focus:ring-apple-blue-light font-mono"
                  />
                </div>
              </div>

              {/* CallMeBot Guide Box */}
              <div className="p-4 rounded-xl bg-emerald-500/5 border border-emerald-500/15 text-[11px] text-slate-700 dark:text-slate-300 space-y-2">
                <div className="font-bold flex items-center gap-1 text-emerald-600 dark:text-emerald-400">
                  <Info size={12} /> How to get a free CallMeBot WhatsApp API Key:
                </div>
                <ol className="list-decimal list-inside space-y-1">
                  <li>Add <b>+34 644 97 53 14</b> to your phone contacts (CallMeBot Bot).</li>
                  <li>Send a WhatsApp message: <code>I allow callmebot to send me messages</code></li>
                  <li>The bot will reply immediately with your free API Key (a 6-digit number).</li>
                  <li>Paste the key and your phone number above and click Save!</li>
                </ol>
              </div>
            </div>
          )}
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full bg-apple-blue-light hover:bg-blue-600 dark:bg-apple-blue-dark dark:hover:bg-blue-700 text-white font-semibold py-3.5 rounded-[18px] text-sm transition-all shadow-appleBlue hover:scale-[1.01] flex items-center justify-center gap-1.5 disabled:opacity-50"
        >
          <Save size={16} />
          {loading ? 'Saving Preferences...' : 'Save Settings'}
        </button>

      </form>
    </div>
  );
}

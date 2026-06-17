import React, { useState, useEffect } from 'react';
import { standingsAPI } from '../services/api';
import { Trophy, RefreshCw, CheckCircle2 } from 'lucide-react';

export default function Standings({ darkMode, user }) {
  const [groupedStandings, setGroupedStandings] = useState({});
  const [loading, setLoading] = useState(true);
  const [updating, setUpdating] = useState(false);
  const [alertMsg, setAlertMsg] = useState('');

  const fetchStandings = async () => {
    setLoading(true);
    try {
      const response = await standingsAPI.getStandings();
      setGroupedStandings(response.data);
    } catch (err) {
      console.error("Error loading standings:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchStandings();
  }, []);

  const handleRecalculate = async () => {
    setUpdating(true);
    setAlertMsg('');
    try {
      await standingsAPI.recalculateStandings();
      const response = await standingsAPI.getStandings();
      setGroupedStandings(response.data);
      setAlertMsg('Standings recalculated successfully!');
      setTimeout(() => setAlertMsg(''), 3000);
    } catch (err) {
      console.error("Failed to recalculate standings:", err);
      alert("Recalculation failed.");
    } finally {
      setUpdating(false);
    }
  };

  const groupKeys = Object.keys(groupedStandings).sort();

  return (
    <div className="space-y-8 py-6 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      {/* Header */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-slate-900 dark:text-white">
            Tournament Standings
          </h1>
          <p className="text-xs text-apple-text-subLight dark:text-apple-text-subDark">
            Live group tables, points tracker, and qualification states
          </p>
        </div>

        {user && (
          <button
            disabled={updating}
            onClick={handleRecalculate}
            className="text-xs font-semibold bg-apple-blue-light hover:bg-blue-600 disabled:opacity-50 text-white px-4 py-2 rounded-xl flex items-center gap-1.5 transition-all shadow-md active:scale-95"
          >
            <RefreshCw size={12} className={updating ? 'animate-spin' : ''} />
            Recalculate Standings
          </button>
        )}
      </div>

      {alertMsg && (
        <div className="p-4 rounded-xl bg-emerald-500/10 border border-emerald-500/20 text-emerald-600 dark:text-emerald-400 text-xs flex items-center gap-2">
          <CheckCircle2 size={16} />
          <span>{alertMsg}</span>
        </div>
      )}

      {loading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div className="h-44 rounded-2xl animate-shimmer" />
          <div className="h-44 rounded-2xl animate-shimmer" />
          <div className="h-44 rounded-2xl animate-shimmer" />
          <div className="h-44 rounded-2xl animate-shimmer" />
        </div>
      ) : groupKeys.length === 0 ? (
        <div className="text-center py-10 bg-white/20 dark:bg-white/5 rounded-3xl border border-black/5 dark:border-white/5">
          <p className="text-sm text-apple-text-subLight dark:text-apple-text-subDark">No standings data available. Seed matches to calculate.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {groupKeys.map((groupName) => (
            <div
              key={groupName}
              className={`p-6 rounded-[24px] border ${
                darkMode ? 'glass-card-dark border-white/5 shadow-appleDark' : 'glass-card-light border-black/5 shadow-appleLight'
              }`}
            >
              <h3 className="text-sm font-bold uppercase tracking-wider mb-4 flex items-center gap-2 text-slate-800 dark:text-slate-200">
                <Trophy size={14} className="text-yellow-500" /> {groupName}
              </h3>

              <div className="overflow-x-auto">
                <table className="w-full text-xs">
                  <thead>
                    <tr className="text-apple-text-subLight dark:text-apple-text-subDark border-b border-black/5 dark:border-white/5 pb-2">
                      <th align="left" className="pb-2 w-5">Pos</th>
                      <th align="left" className="pb-2">Team</th>
                      <th align="center" className="pb-2 w-8">P</th>
                      <th align="center" className="pb-2 w-8">W</th>
                      <th align="center" className="pb-2 w-8">D</th>
                      <th align="center" className="pb-2 w-8">L</th>
                      <th align="center" className="pb-2 w-12">GF:GA</th>
                      <th align="center" className="pb-2 w-8">GD</th>
                      <th align="center" className="pb-2 w-8">PTS</th>
                    </tr>
                  </thead>
                  <tbody>
                    {groupedStandings[groupName].map((team, idx) => {
                      const gd = team.goals_for - team.goals_against;
                      const isFavorite = user && team.team_name === user.favorite_team;
                      const gdFormatted = gd > 0 ? `+${gd}` : gd;
                      
                      return (
                        <tr
                          key={team.team_name}
                          className={`border-b border-black/5 dark:border-white/5 last:border-0 hover:bg-black/5 dark:hover:bg-white/5 transition-colors ${
                            isFavorite ? 'bg-apple-blue-light/10 font-bold text-apple-blue-light' : ''
                          }`}
                        >
                          <td className="py-3 font-mono font-bold text-apple-text-subLight dark:text-apple-text-subDark">
                            {idx + 1}
                          </td>
                          <td className="py-3 font-semibold text-slate-800 dark:text-slate-200">
                            {team.team_name} {isFavorite && '⭐'}
                          </td>
                          <td align="center">{team.played}</td>
                          <td align="center">{team.won}</td>
                          <td align="center">{team.drawn}</td>
                          <td align="center">{team.lost}</td>
                          <td align="center" className="font-mono text-[11px] text-apple-text-subLight dark:text-apple-text-subDark">
                            {team.goals_for}:{team.goals_against}
                          </td>
                          <td align="center" className={`font-mono font-semibold ${gd > 0 ? 'text-emerald-500' : gd < 0 ? 'text-red-500' : ''}`}>
                            {gdFormatted}
                          </td>
                          <td align="center" className="font-bold text-slate-900 dark:text-white">
                            {team.points}
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

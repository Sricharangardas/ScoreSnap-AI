import React, { useState, useEffect } from 'react';
import { matchesAPI } from '../services/api';
import { Calendar, Filter, Sparkles, AlertCircle, Play, CheckCircle } from 'lucide-react';

export default function Matches({ darkMode, user, onOpenMatchSummary }) {
  const [matches, setMatches] = useState([]);
  const [loading, setLoading] = useState(true);
  const [statusFilter, setStatusFilter] = useState('all');
  const [groupFilter, setGroupFilter] = useState('all');
  const [simulatingId, setSimulatingId] = useState(null);

  const fetchMatches = async () => {
    setLoading(true);
    try {
      const response = await matchesAPI.getMatches();
      setMatches(response.data);
    } catch (err) {
      console.error("Error loading matches:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchMatches();
  }, []);

  const handleStartMatch = async (matchId) => {
    setSimulatingId(matchId);
    try {
      await matchesAPI.simulateKickoff(matchId);
      await fetchMatches();
    } catch (err) {
      console.error("Failed to start match:", err);
      alert("Failed to start match.");
    } finally {
      setSimulatingId(null);
    }
  };

  const handleCompleteMatch = async (matchId) => {
    setSimulatingId(matchId);
    // Standard random goals
    const g1 = Math.floor(Math.random() * 4);
    const g2 = Math.floor(Math.random() * 3);
    
    try {
      const matchToEnd = matches.find(m => m.match_id === matchId);
      await matchesAPI.simulateFullTime(matchId, g1, g2);

      // Trigger custom notification event
      const event = new CustomEvent('match-completed', {
        detail: {
          match: {
            match_id: matchId,
            team_1: matchToEnd.team_1,
            team_2: matchToEnd.team_2,
            score_1: g1,
            score_2: g2,
          }
        }
      });
      window.dispatchEvent(event);
      await fetchMatches();
    } catch (err) {
      console.error("Failed to complete match:", err);
      alert("Failed to complete match.");
    } finally {
      setSimulatingId(null);
    }
  };

  // Group options in select
  const groups = ['all', 'Group A', 'Group B', 'Group D', 'Group E', 'Group H', 'Group J'];

  // Apply filters in memory
  const filteredMatches = matches.filter(match => {
    const matchesStatus = statusFilter === 'all' || match.status === statusFilter;
    const matchesGroup = groupFilter === 'all' || match.group_name === groupFilter;
    return matchesStatus && matchesGroup;
  });

  return (
    <div className="space-y-8 py-6 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold tracking-tight text-slate-900 dark:text-white">
          World Cup 2026 Fixtures
        </h1>
        <p className="text-xs text-apple-text-subLight dark:text-apple-text-subDark">
          Explore complete schedules, live scores, and AI match analytics
        </p>
      </div>

      {/* Filter bar */}
      <div className={`p-4 rounded-2xl border flex flex-col sm:flex-row gap-4 items-center justify-between transition-all ${
        darkMode ? 'glass-card-dark border-white/5' : 'glass-card-light border-black/5'
      }`}>
        {/* Status Tabs */}
        <div className="flex gap-1 bg-black/5 dark:bg-white/5 p-1 rounded-xl w-full sm:w-auto overflow-x-auto">
          {['all', 'completed', 'live', 'scheduled'].map((tab) => (
            <button
              key={tab}
              onClick={() => setStatusFilter(tab)}
              className={`px-4 py-1.5 rounded-lg text-xs font-semibold uppercase tracking-wider transition-all ${
                statusFilter === tab
                  ? (darkMode ? 'bg-white text-black shadow-sm' : 'bg-black text-white shadow-sm')
                  : (darkMode ? 'text-apple-text-subDark hover:text-white' : 'text-apple-text-subLight hover:text-black')
              }`}
            >
              {tab}
            </button>
          ))}
        </div>

        {/* Group Select */}
        <div className="flex items-center gap-2 w-full sm:w-auto">
          <Filter size={14} className="text-apple-text-subLight dark:text-apple-text-subDark" />
          <select
            value={groupFilter}
            onChange={(e) => setGroupFilter(e.target.value)}
            className="text-xs p-2 rounded-xl border border-black/10 dark:border-white/10 bg-transparent focus:outline-none focus:ring-1 focus:ring-apple-blue-light w-full sm:w-40"
          >
            {groups.map(g => (
              <option key={g} value={g} className="text-black">
                {g === 'all' ? 'All Groups' : g}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Matches Grid */}
      {loading ? (
        <div className="space-y-4">
          <div className="h-20 rounded-2xl animate-shimmer" />
          <div className="h-20 rounded-2xl animate-shimmer" />
          <div className="h-20 rounded-2xl animate-shimmer" />
        </div>
      ) : filteredMatches.length === 0 ? (
        <div className="text-center py-16 bg-white/20 dark:bg-white/5 rounded-[30px] border border-black/5 dark:border-white/5">
          <AlertCircle size={28} className="mx-auto text-apple-text-subLight dark:text-apple-text-subDark mb-3" />
          <p className="text-sm font-semibold text-slate-800 dark:text-slate-200">No matching fixtures found</p>
          <p className="text-xs text-apple-text-subLight dark:text-apple-text-subDark">Adjust your filter options and try again</p>
        </div>
      ) : (
        <div className="space-y-4">
          {filteredMatches.map((match) => {
            const mDate = new Date(match.match_date);
            const formattedDate = mDate.toLocaleDateString(undefined, { weekday: 'short', day: 'numeric', month: 'short', year: 'numeric' });
            const formattedTime = mDate.toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit', hour12: true }) + ' IST';
            
            return (
              <div
                key={match.match_id}
                className={`p-5 rounded-[22px] border flex flex-col sm:flex-row items-center justify-between gap-4 transition-all duration-200 ${
                  match.status === 'live'
                    ? (darkMode ? 'bg-red-500/10 border-red-500/35 shadow-sm' : 'bg-red-500/5 border-red-500/20 shadow-sm')
                    : (darkMode ? 'glass-card-dark border-white/5 hover:bg-white/10' : 'glass-card-light border-black/5 hover:bg-black/5')
                }`}
              >
                {/* Team / Score Area */}
                <div className="flex items-center gap-4 flex-1 justify-center sm:justify-start">
                  <div className="text-center sm:text-left min-w-[100px]">
                    <span className={`text-sm font-bold ${match.team_1 === user?.favorite_team ? 'text-apple-blue-light dark:text-apple-blue-dark' : ''}`}>
                      {match.team_1}
                    </span>
                  </div>

                  <div className="flex items-center gap-2 bg-black/5 dark:bg-white/5 px-4 py-1.5 rounded-2xl">
                    <span className="font-mono font-black text-sm w-4 text-center">
                      {match.status === 'scheduled' ? '-' : match.score_1}
                    </span>
                    <span className="text-[10px] text-apple-text-subLight dark:text-apple-text-subDark font-semibold">VS</span>
                    <span className="font-mono font-black text-sm w-4 text-center">
                      {match.status === 'scheduled' ? '-' : match.score_2}
                    </span>
                  </div>

                  <div className="text-center sm:text-right min-w-[100px]">
                    <span className={`text-sm font-bold ${match.team_2 === user?.favorite_team ? 'text-apple-blue-light dark:text-apple-blue-dark' : ''}`}>
                      {match.team_2}
                    </span>
                  </div>
                </div>

                {/* Match Metadata */}
                <div className="flex flex-col items-center sm:items-end text-center sm:text-right gap-1 min-w-[150px]">
                  <span className="text-[10px] text-apple-text-subLight dark:text-apple-text-subDark">
                    {formattedDate} • {formattedTime}
                  </span>
                  <span className="text-[9px] font-bold uppercase tracking-wider text-apple-blue-light dark:text-apple-blue-dark">
                    {match.group_name} • {match.stadium.split(',')[0]}
                  </span>
                </div>

                {/* Action Controls / Status badges */}
                <div className="flex items-center gap-3">
                  {match.status === 'completed' && (
                    <button
                      onClick={() => onOpenMatchSummary(match.match_id)}
                      className="text-xs font-semibold bg-apple-blue-light hover:bg-blue-600 dark:bg-apple-blue-dark dark:hover:bg-blue-700 text-white px-4 py-2 rounded-xl transition-all shadow-sm flex items-center gap-1"
                    >
                      <Sparkles size={12} /> AI Summary
                    </button>
                  )}

                  {match.status === 'live' && (
                    <div className="flex items-center gap-2">
                      <span className="text-[10px] text-red-500 font-bold uppercase tracking-wider flex items-center gap-1 bg-red-500/10 px-2.5 py-1 rounded-full">
                        <span className="w-1.5 h-1.5 rounded-full bg-red-500 animate-ping" /> Live
                      </span>
                      {user && (
                        <button
                          disabled={simulatingId === match.match_id}
                          onClick={() => handleCompleteMatch(match.match_id)}
                          className="text-xs font-semibold bg-emerald-500 hover:bg-emerald-600 disabled:opacity-50 text-white px-3 py-1.5 rounded-xl transition-colors shadow-sm"
                        >
                          End
                        </button>
                      )}
                    </div>
                  )}

                  {match.status === 'scheduled' && (
                    <>
                      <span className="text-[10px] text-apple-text-subLight dark:text-apple-text-subDark uppercase tracking-wider font-semibold bg-black/5 dark:bg-white/10 px-3 py-1 rounded-full">
                        Upcoming
                      </span>
                      {user && (
                        <button
                          disabled={simulatingId === match.match_id}
                          onClick={() => handleStartMatch(match.match_id)}
                          className="text-xs font-semibold bg-apple-blue-light hover:bg-blue-600 disabled:opacity-50 text-white px-3 py-1.5 rounded-xl transition-colors shadow-sm flex items-center gap-0.5"
                        >
                          <Play size={10} /> Start
                        </button>
                      )}
                    </>
                  )}
                </div>

              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}

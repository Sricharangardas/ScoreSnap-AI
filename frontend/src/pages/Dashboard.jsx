import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { matchesAPI, standingsAPI, cronAPI } from '../services/api';
import { Sparkles, Calendar, TrendingUp, Trophy, ArrowRight, Play, CheckCircle2, ChevronRight, Activity } from 'lucide-react';

export default function Dashboard({ darkMode, user, onOpenMatchSummary }) {
  const [matches, setMatches] = useState([]);
  const [standings, setStandings] = useState({});
  const [loading, setLoading] = useState(true);
  const [simulating, setSimulating] = useState(false);
  
  // Simulation Form States
  const [selectedMatchId, setSelectedMatchId] = useState('');
  const [score1, setScore1] = useState(2);
  const [score2, setScore2] = useState(1);

  const fetchData = async () => {
    setLoading(true);
    try {
      const matchRes = await matchesAPI.getMatches();
      setMatches(matchRes.data);
      
      const standingsRes = await standingsAPI.getStandings();
      setStandings(standingsRes.data);
      
      // Auto-select first scheduled match for simulation input
      const upcoming = matchRes.data.filter(m => m.status === 'scheduled');
      if (upcoming.length > 0 && !selectedMatchId) {
        setSelectedMatchId(upcoming[0].match_id);
      }
    } catch (err) {
      console.error("Error fetching dashboard data:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleSimulateFullTime = async (e) => {
    e.preventDefault();
    if (!selectedMatchId) return;
    setSimulating(true);

    try {
      // Find the match details before ending it
      const matchToEnd = matches.find(m => m.match_id === selectedMatchId);
      
      const res = await matchesAPI.simulateFullTime(selectedMatchId, score1, score2);
      
      // Dispatch custom event to activate Dynamic Island
      const event = new CustomEvent('match-completed', {
        detail: {
          match: {
            match_id: selectedMatchId,
            team_1: matchToEnd.team_1,
            team_2: matchToEnd.team_2,
            score_1: score1,
            score_2: score2,
          }
        }
      });
      window.dispatchEvent(event);
      
      // Refresh data
      await fetchData();
    } catch (err) {
      console.error("Simulation failed:", err);
      alert("Simulation failed. Make sure the backend server is running.");
    } finally {
      setSimulating(false);
    }
  };

  const liveMatches = matches.filter(m => m.status === 'live');
  const recentMatches = matches.filter(m => m.status === 'completed').slice(0, 3);
  const upcomingMatches = matches.filter(m => m.status === 'scheduled').slice(0, 3);

  // Get favorite team match spotlight if user has a favorite team
  const favoriteTeamMatch = user && user.favorite_team !== 'None' 
    ? matches.find(m => (m.team_1 === user.favorite_team || m.team_2 === user.favorite_team) && m.status === 'completed')
    : null;

  // Get favorite team group or fallback to first available group
  const favTeamGroup = user && user.favorite_team && user.favorite_team !== 'None'
    ? Object.keys(standings).find(group => standings[group].some(t => t.team_name === user.favorite_team))
    : null;
  const displayGroup = favTeamGroup || Object.keys(standings).sort()[0] || 'Group A';

  return (
    <div className="space-y-10 py-6 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      {/* Hero Welcome banner */}
      <div className={`p-8 rounded-[30px] border relative overflow-hidden transition-all ${
        darkMode ? 'glass-card-dark border-white/5' : 'glass-card-light border-black/5'
      }`}>
        <div className="absolute top-0 right-0 w-80 h-80 bg-apple-blue-light/10 dark:bg-apple-blue-dark/15 rounded-full blur-3xl -z-10" />
        
        <div className="max-w-2xl space-y-3">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-apple-blue-light/10 text-apple-blue-light dark:bg-apple-blue-dark/15 dark:text-apple-blue-dark text-xs font-semibold">
            <Sparkles size={12} /> Sleep Through The Match, Wake Up Informed
          </div>
          <h1 className="text-3xl sm:text-4xl font-extrabold tracking-tight text-slate-900 dark:text-white leading-tight">
            Hi, {user ? user.name : 'Football Fan'}! Your World Cup Agent is Active.
          </h1>
          <p className="text-sm text-apple-text-subLight dark:text-apple-text-subDark max-w-lg leading-relaxed">
            ScoreSnap AI automatically monitors FIFA World Cup 2026 fixtures. When a match ends, our Agent collects statistics, generates Gemini AI breakdowns, and pushes updates straight to you.
          </p>
        </div>
      </div>

      {/* Main Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        {/* Left 2 Columns */}
        <div className="lg:col-span-2 space-y-8">
          
          {/* Live Match Alert (glowing card) */}
          {liveMatches.length > 0 && (
            <div className="space-y-4">
              <h2 className="text-xs font-bold uppercase tracking-wider text-apple-text-subLight dark:text-apple-text-subDark flex items-center gap-1.5">
                <span className="w-2 h-2 rounded-full bg-red-500 animate-ping" /> Live Fixtures
              </h2>
              {liveMatches.map(match => (
                <div 
                  key={match.match_id}
                  className={`p-6 rounded-[24px] border relative overflow-hidden transition-all card-glow-blue ${
                    darkMode ? 'bg-gradient-to-r from-red-500/10 via-black/40 to-black/70 border-red-500/20' : 'bg-gradient-to-r from-red-500/5 via-white/50 to-white border-red-500/15'
                  }`}
                >
                  <div className="flex justify-between items-center text-xs mb-4">
                    <span className="font-semibold text-red-500 flex items-center gap-1">
                      <Activity size={12} className="animate-spin" /> LIVE • 68'
                    </span>
                    <span className="text-apple-text-subLight dark:text-apple-text-subDark">{match.stadium}</span>
                  </div>

                  <div className="flex items-center justify-between px-6">
                    <div className="text-center w-24">
                      <div className="text-lg font-bold">{match.team_1}</div>
                    </div>
                    <div className="text-3xl font-extrabold font-mono bg-black/5 dark:bg-white/10 px-4 py-2 rounded-2xl">
                      {match.score_1} - {match.score_2}
                    </div>
                    <div className="text-center w-24">
                      <div className="text-lg font-bold">{match.team_2}</div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}

          {/* Recent Completed Results */}
          <div className="space-y-4">
            <div className="flex justify-between items-center">
              <h2 className="text-xs font-bold uppercase tracking-wider text-apple-text-subLight dark:text-apple-text-subDark">
                Recent Results
              </h2>
              <Link to="/matches" className="text-xs font-bold text-apple-blue-light dark:text-apple-blue-dark flex items-center gap-0.5 hover:underline">
                All Matches <ChevronRight size={14} />
              </Link>
            </div>

            {loading ? (
              <div className="h-44 rounded-3xl animate-shimmer" />
            ) : recentMatches.length === 0 ? (
              <div className="text-center py-10 bg-white/20 dark:bg-white/5 rounded-3xl border border-black/5 dark:border-white/5">
                <p className="text-sm text-apple-text-subLight dark:text-apple-text-subDark">No completed matches yet. Try simulating one below!</p>
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {recentMatches.map(match => {
                  const winner = match.score_1 > match.score_2 ? match.team_1 : (match.score_2 > match.score_1 ? match.team_2 : 'Draw');
                  return (
                    <div 
                      key={match.match_id}
                      className={`p-6 rounded-[22px] border flex flex-col justify-between transition-all duration-300 hover:scale-[1.02] ${
                        darkMode ? 'glass-card-dark border-white/5' : 'glass-card-light border-black/5'
                      }`}
                    >
                      <div>
                        <div className="flex justify-between items-center text-[10px] text-apple-text-subLight dark:text-apple-text-subDark mb-3">
                          <span className="font-semibold">{match.group_name}</span>
                          <span>Completed</span>
                        </div>

                        <div className="flex justify-between items-center my-2">
                          <span className="font-semibold text-sm">{match.team_1}</span>
                          <span className="font-mono text-sm font-bold bg-black/5 dark:bg-white/5 px-2 py-0.5 rounded-md">
                            {match.score_1}
                          </span>
                        </div>
                        <div className="flex justify-between items-center my-2">
                          <span className="font-semibold text-sm">{match.team_2}</span>
                          <span className="font-mono text-sm font-bold bg-black/5 dark:bg-white/5 px-2 py-0.5 rounded-md">
                            {match.score_2}
                          </span>
                        </div>
                      </div>

                      <div className="mt-4 pt-3 border-t border-black/5 dark:border-white/5 flex items-center justify-between">
                        <span className="text-[10px] text-emerald-500 font-semibold">
                          Winner: {winner}
                        </span>
                        <button
                          onClick={() => onOpenMatchSummary(match.match_id)}
                          className="text-[10px] font-bold bg-apple-blue-light hover:bg-blue-600 dark:bg-apple-blue-dark dark:hover:bg-blue-700 text-white px-3 py-1 rounded-full transition-colors"
                        >
                          AI Summary
                        </button>
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
          </div>

          {/* Simulation sandbox panel */}
          <div className={`p-6 rounded-[24px] border ${
            darkMode ? 'glass-card-dark border-white/5' : 'glass-card-light border-black/5'
          }`}>
            <h3 className="text-sm font-bold tracking-tight mb-2 text-slate-900 dark:text-white flex items-center gap-1.5">
              ⚽ Match Simulation Sandbox (Free Testing Center)
            </h3>
            <p className="text-xs text-apple-text-subLight dark:text-apple-text-subDark mb-4">
              Instantly simulate a completed match to execute our 5 agents in series. You will see scores update, Gemini generate stats/narratives, and Resend/CallMeBot dispatch alerts immediately!
            </p>

            {upcomingMatches.length === 0 ? (
              <p className="text-xs text-apple-text-subLight dark:text-apple-text-subDark italic">All preloaded matches completed. Reset the DB to test again.</p>
            ) : (
              <form onSubmit={handleSimulateFullTime} className="grid grid-cols-1 md:grid-cols-4 gap-4 items-end">
                <div>
                  <label className="block text-[10px] font-bold uppercase tracking-wider text-apple-text-subLight dark:text-apple-text-subDark mb-1">
                    Fixture
                  </label>
                  <select
                    value={selectedMatchId}
                    onChange={(e) => setSelectedMatchId(e.target.value)}
                    className="w-full text-xs p-2.5 rounded-xl border border-black/10 dark:border-white/10 bg-transparent focus:outline-none focus:ring-1 focus:ring-apple-blue-light"
                  >
                    {matches.filter(m => m.status === 'scheduled').map(m => (
                      <option key={m.match_id} value={m.match_id} className="text-black">
                        {m.team_1} vs {m.team_2}
                      </option>
                    ))}
                  </select>
                </div>

                <div className="grid grid-cols-2 gap-2">
                  <div>
                    <label className="block text-[10px] font-bold uppercase tracking-wider text-apple-text-subLight dark:text-apple-text-subDark mb-1">
                      Goals T1
                    </label>
                    <input
                      type="number"
                      min="0"
                      max="10"
                      value={score1}
                      onChange={(e) => setScore1(parseInt(e.target.value) || 0)}
                      className="w-full text-xs p-2 rounded-xl border border-black/10 dark:border-white/10 bg-transparent text-center focus:outline-none focus:ring-1 focus:ring-apple-blue-light"
                    />
                  </div>
                  <div>
                    <label className="block text-[10px] font-bold uppercase tracking-wider text-apple-text-subLight dark:text-apple-text-subDark mb-1">
                      Goals T2
                    </label>
                    <input
                      type="number"
                      min="0"
                      max="10"
                      value={score2}
                      onChange={(e) => setScore2(parseInt(e.target.value) || 0)}
                      className="w-full text-xs p-2 rounded-xl border border-black/10 dark:border-white/10 bg-transparent text-center focus:outline-none focus:ring-1 focus:ring-apple-blue-light"
                    />
                  </div>
                </div>

                <div className="md:col-span-2">
                  <button
                    type="submit"
                    disabled={simulating}
                    className="w-full bg-emerald-500 hover:bg-emerald-600 disabled:opacity-50 text-white text-xs font-bold py-2.5 rounded-xl flex items-center justify-center gap-1.5 transition-all shadow-md active:scale-95"
                  >
                    {simulating ? (
                      <>
                        <span className="w-3 h-3 border-2 border-white border-t-transparent rounded-full animate-spin" />
                        Running Agents...
                      </>
                    ) : (
                      <>
                        <Play size={12} /> Complete Match (Trigger AI Summary)
                      </>
                    )}
                  </button>
                </div>
              </form>
            )}
          </div>

        </div>

        {/* Right 1 Column */}
        <div className="space-y-8">
          
          {/* Favorite Team Highlight if configured */}
          {favoriteTeamMatch && (
            <div className={`p-6 rounded-[24px] border relative overflow-hidden transition-all ${
              darkMode ? 'bg-gradient-to-br from-apple-blue-dark/15 to-transparent border-apple-blue-dark/30' : 'bg-gradient-to-br from-apple-blue-light/5 to-transparent border-apple-blue-light/25'
            }`}>
              <div className="text-[10px] uppercase font-bold text-apple-blue-light dark:text-apple-blue-dark mb-2 tracking-widest">
                ⭐ Favorite Team Spotlight
              </div>
              <h4 className="text-sm font-bold text-slate-800 dark:text-slate-200">
                {favoriteTeamMatch.team_1} vs {favoriteTeamMatch.team_2}
              </h4>
              <p className="text-2xl font-black font-mono my-2 text-slate-900 dark:text-white">
                {favoriteTeamMatch.score_1} - {favoriteTeamMatch.score_2}
              </p>
              <button
                onClick={() => onOpenMatchSummary(favoriteTeamMatch.match_id)}
                className="mt-2 text-xs font-bold text-apple-blue-light dark:text-apple-blue-dark flex items-center gap-0.5 hover:underline"
              >
                Read AI Recap <ArrowRight size={12} />
              </button>
            </div>
          )}

          {/* Group Standings Summary (Group J or A) */}
          <div className={`p-6 rounded-[24px] border ${
            darkMode ? 'glass-card-dark border-white/5' : 'glass-card-light border-black/5'
          }`}>
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-xs font-bold uppercase tracking-wider text-apple-text-subLight dark:text-apple-text-subDark flex items-center gap-1">
                <Trophy size={14} className="text-yellow-500" /> {displayGroup} Standing
              </h3>
              <Link to="/standings" className="text-[10px] font-bold text-apple-blue-light dark:text-apple-blue-dark hover:underline">
                View All
              </Link>
            </div>

            {loading ? (
              <div className="h-32 rounded-2xl animate-shimmer" />
            ) : !standings[displayGroup] ? (
              <p className="text-xs text-apple-text-subLight dark:text-apple-text-subDark italic text-center py-6">No {displayGroup} standings calculated yet.</p>
            ) : (
              <div className="space-y-2">
                <table className="w-full text-xs">
                  <thead>
                    <tr className="text-apple-text-subLight dark:text-apple-text-subDark border-b border-black/5 dark:border-white/5 pb-2">
                      <th align="left" className="pb-2">Team</th>
                      <th align="center" className="pb-2">P</th>
                      <th align="center" className="pb-2">GD</th>
                      <th align="center" className="pb-2">PTS</th>
                    </tr>
                  </thead>
                  <tbody>
                    {standings[displayGroup].map((team, idx) => (
                      <tr 
                        key={team.team_name}
                        className={`border-b border-black/5 dark:border-white/5 last:border-0 ${
                          team.team_name === (user?.favorite_team) ? 'bg-apple-blue-light/10 font-bold text-apple-blue-light' : ''
                        }`}
                      >
                        <td className="py-2.5 flex items-center gap-1.5">
                          <span className="font-mono text-apple-text-subLight dark:text-apple-text-subDark w-3">
                            {idx + 1}
                          </span>
                          {team.team_name}
                        </td>
                        <td align="center">{team.played}</td>
                        <td align="center">{team.goals_for - team.goals_against}</td>
                        <td align="center" className="font-bold">{team.points}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>

          {/* Upcoming Matches Preview */}
          <div className={`p-6 rounded-[24px] border ${
            darkMode ? 'glass-card-dark border-white/5' : 'glass-card-light border-black/5'
          }`}>
            <h3 className="text-xs font-bold uppercase tracking-wider text-apple-text-subLight dark:text-apple-text-subDark mb-4 flex items-center gap-1">
              <Calendar size={14} className="text-apple-blue-light" /> Upcoming Fixtures
            </h3>

            {loading ? (
              <div className="h-32 rounded-2xl animate-shimmer" />
            ) : upcomingMatches.length === 0 ? (
              <p className="text-xs text-apple-text-subLight dark:text-apple-text-subDark italic text-center py-6">All group stage matches completed!</p>
            ) : (
              <div className="space-y-3">
                {upcomingMatches.map(match => {
                  const mDate = new Date(match.match_date);
                  const formattedTime = mDate.toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit', hour12: true }) + ' IST';
                  return (
                    <div 
                      key={match.match_id}
                      className="flex items-center justify-between p-2 rounded-xl hover:bg-black/5 dark:hover:bg-white/5 transition-colors"
                    >
                      <div className="text-xs font-semibold">
                        {match.team_1} vs {match.team_2}
                        <div className="text-[9px] text-apple-text-subLight dark:text-apple-text-subDark font-normal">
                          {mDate.toLocaleDateString(undefined, {month: 'short', day: 'numeric'})} at {formattedTime}
                        </div>
                      </div>
                      <span className="text-[9px] font-bold uppercase tracking-wider bg-apple-blue-light/10 text-apple-blue-light dark:bg-apple-blue-dark/15 dark:text-apple-blue-dark px-2 py-0.5 rounded-full">
                        {match.group_name}
                      </span>
                    </div>
                  );
                })}
              </div>
            )}
          </div>

        </div>

      </div>
    </div>
  );
}

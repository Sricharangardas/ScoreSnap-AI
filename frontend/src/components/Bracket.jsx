import React, { useState, useEffect } from 'react';
import { matchesAPI } from '../services/api';

export default function Bracket() {
  const [highlightedTeam, setHighlightedTeam] = useState(null);
  const [bracketData, setBracketData] = useState({
    quarterfinals: [],
    semifinals: [],
    final: []
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchBracket = async () => {
      try {
        const response = await matchesAPI.getMatches();
        const allMatches = response.data;

        const getWinner = (m) => {
          if (m.status !== 'completed') return null;
          if (m.score_1 > m.score_2) return m.team_1;
          if (m.score_2 > m.score_1) return m.team_2;
          
          // Draw (penalty shootout) fallback check by checking who advanced in next match
          const nextMatchMap = {
            "WC26-M91": { id: "WC26-M94", pos: "team_1" },
            "WC26-M90": { id: "WC26-M94", pos: "team_2" },
            "WC26-M92": { id: "WC26-M95", pos: "team_1" },
            "WC26-M93": { id: "WC26-M95", pos: "team_2" },
            "WC26-M94": { id: "WC26-M97", pos: "team_1" },
            "WC26-M95": { id: "WC26-M97", pos: "team_2" },
          };
          
          const mapping = nextMatchMap[m.match_id];
          if (mapping) {
            const nextMatch = allMatches.find(x => x.match_id === mapping.id);
            if (nextMatch) {
              const advancedTeam = mapping.pos === "team_1" ? nextMatch.team_1 : nextMatch.team_2;
              if (advancedTeam && advancedTeam !== "TBD") {
                return advancedTeam;
              }
            }
          }
          return null;
        };

        const formatMatch = (m_id, id, from1 = null, from2 = null) => {
          const m = allMatches.find(x => x.match_id === m_id);
          if (!m) {
            return { id, team1: 'TBD', team2: 'TBD', score1: '?', score2: '?', winner: null, from1, from2 };
          }
          return {
            id,
            team1: m.team_1,
            team2: m.team_2,
            score1: m.status === 'completed' ? String(m.score_1) : '?',
            score2: m.status === 'completed' ? String(m.score_2) : '?',
            winner: getWinner(m),
            from1,
            from2
          };
        };

        setBracketData({
          quarterfinals: [
            formatMatch("WC26-M91", "q1"),
            formatMatch("WC26-M90", "q2"),
            formatMatch("WC26-M92", "q3"),
            formatMatch("WC26-M93", "q4")
          ],
          semifinals: [
            formatMatch("WC26-M94", "s1", "q1", "q2"),
            formatMatch("WC26-M95", "s2", "q3", "q4")
          ],
          final: [
            formatMatch("WC26-M97", "f1", "s1", "s2")
          ]
        });
      } catch (err) {
        console.error("Failed to load bracket data:", err);
      } finally {
        setLoading(false);
      }
    };
    fetchBracket();
  }, []);

  const getTeamClass = (teamName, winnerName) => {
    const isWinner = teamName === winnerName;
    const isHighlighted = highlightedTeam && teamName === highlightedTeam;
    
    return `flex items-center justify-between px-3 py-2 text-xs font-semibold rounded-lg transition-all duration-300 ${
      isHighlighted 
        ? 'bg-apple-blue-light/20 text-apple-blue-light dark:bg-apple-blue-dark/25 dark:text-apple-blue-dark scale-[1.02] shadow-sm'
        : 'text-slate-700 dark:text-slate-300'
    } ${isWinner ? 'text-black dark:text-white font-bold' : 'opacity-60'}`;
  };

  if (loading) {
    return (
      <div className="w-full flex items-center justify-center min-h-[400px]">
        <span className="w-8 h-8 border-4 border-apple-blue-light border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  return (
    <div className="w-full overflow-x-auto py-6 flex items-center justify-start md:justify-center min-h-[400px]">
      <div className="flex items-center gap-8 px-4 min-w-[700px]">
        
        {/* Quarterfinals */}
        <div className="flex flex-col gap-6 w-52">
          <div className="text-center text-[10px] font-bold uppercase tracking-wider text-apple-text-subLight dark:text-apple-text-subDark mb-2">
            Quarter-Finals
          </div>
          {bracketData.quarterfinals.map((match) => (
            <div 
              key={match.id}
              className="p-1 rounded-xl bg-white/40 dark:bg-white/5 border border-black/5 dark:border-white/5 shadow-sm transition-all hover:scale-105"
            >
              <div 
                className="flex flex-col gap-0.5"
                onMouseEnter={() => setHighlightedTeam(match.winner)}
                onMouseLeave={() => setHighlightedTeam(null)}
              >
                <div className={getTeamClass(match.team1, match.winner)}>
                  <span>{match.team1}</span>
                  <span className="font-mono">{match.score1}</span>
                </div>
                <div className="h-[1px] bg-black/5 dark:bg-white/5 my-0.5" />
                <div className={getTeamClass(match.team2, match.winner)}>
                  <span>{match.team2}</span>
                  <span className="font-mono">{match.score2}</span>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Connectors 1 */}
        <div className="hidden lg:flex flex-col justify-around h-[340px] w-4 -mx-6 text-slate-300 dark:text-slate-700">
          <div className="h-24 border-r-2 border-y-2 rounded-r-lg border-current"></div>
          <div className="h-24 border-r-2 border-y-2 rounded-r-lg border-current"></div>
        </div>

        {/* Semifinals */}
        <div className="flex flex-col gap-24 w-52 py-8">
          <div className="text-center text-[10px] font-bold uppercase tracking-wider text-apple-text-subLight dark:text-apple-text-subDark mb-2">
            Semi-Finals
          </div>
          {bracketData.semifinals.map((match) => (
            <div 
              key={match.id}
              className="p-1 rounded-xl bg-white/40 dark:bg-white/5 border border-black/5 dark:border-white/5 shadow-sm transition-all hover:scale-105"
            >
              <div 
                className="flex flex-col gap-0.5"
                onMouseEnter={() => setHighlightedTeam(match.winner)}
                onMouseLeave={() => setHighlightedTeam(null)}
              >
                <div className={getTeamClass(match.team1, match.winner)}>
                  <span>{match.team1}</span>
                  <span className="font-mono">{match.score1}</span>
                </div>
                <div className="h-[1px] bg-black/5 dark:bg-white/5 my-0.5" />
                <div className={getTeamClass(match.team2, match.winner)}>
                  <span>{match.team2}</span>
                  <span className="font-mono">{match.score2}</span>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Connectors 2 */}
        <div className="hidden lg:flex flex-col justify-center h-[340px] w-4 -mx-6 text-slate-300 dark:text-slate-700">
          <div className="h-44 border-r-2 border-y-2 rounded-r-lg border-current"></div>
        </div>

        {/* Finals */}
        <div className="flex flex-col gap-6 w-52 justify-center h-[340px]">
          <div className="text-center text-[10px] font-bold uppercase tracking-wider text-apple-text-subLight dark:text-apple-text-subDark mb-2">
            Final
          </div>
          {bracketData.final.map((match) => (
            <div 
              key={match.id}
              className="p-1.5 rounded-2xl bg-gradient-to-br from-apple-blue-light/10 to-transparent dark:from-apple-blue-dark/15 border border-apple-blue-light/35 dark:border-apple-blue-dark/35 shadow-md transition-all hover:scale-105"
            >
              <div 
                className="flex flex-col gap-0.5"
              >
                <div className={getTeamClass(match.team1, match.winner)}>
                  <span>{match.team1}</span>
                  <span className="font-mono text-apple-blue-light dark:text-apple-blue-dark font-bold">{match.score1}</span>
                </div>
                <div className="h-[1px] bg-apple-blue-light/20 my-1" />
                <div className={getTeamClass(match.team2, match.winner)}>
                  <span>{match.team2}</span>
                  <span className="font-mono text-apple-blue-light dark:text-apple-blue-dark font-bold">{match.score2}</span>
                </div>
              </div>
            </div>
          ))}
        </div>

      </div>
    </div>
  );
}

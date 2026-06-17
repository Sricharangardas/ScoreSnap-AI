import React, { useState } from 'react';

export default function Bracket() {
  const [highlightedTeam, setHighlightedTeam] = useState(null);

  const bracketData = {
    quarterfinals: [
      { id: 'q1', team1: 'Argentina', team2: 'Germany', score1: '2', score2: '1', winner: 'Argentina' },
      { id: 'q2', team1: 'Brazil', team2: 'Spain', score1: '3', score2: '2', winner: 'Brazil' },
      { id: 'q3', team1: 'France', team2: 'England', score1: '1', score2: '0', winner: 'France' },
      { id: 'q4', team1: 'Portugal', team2: 'Netherlands', score1: '1(4)', score2: '1(5)', winner: 'Netherlands' },
    ],
    semifinals: [
      { id: 's1', team1: 'Argentina', team2: 'Brazil', score1: '2', score2: '1', winner: 'Argentina', from1: 'q1', from2: 'q2' },
      { id: 's2', team1: 'France', team2: 'Netherlands', score1: '3', score2: '2', winner: 'France', from1: 'q3', from2: 'q4' },
    ],
    final: [
      { id: 'f1', team1: 'Argentina', team2: 'France', score1: '?', score2: '?', winner: null, from1: 's1', from2: 's2' },
    ],
  };

  const getTeamClass = (teamName, winnerName) => {
    const isWinner = teamName === winnerName;
    const isHighlighted = highlightedTeam && teamName === highlightedTeam;
    
    return `flex items-center justify-between px-3 py-2 text-xs font-semibold rounded-lg transition-all duration-300 ${
      isHighlighted 
        ? 'bg-apple-blue-light/20 text-apple-blue-light dark:bg-apple-blue-dark/25 dark:text-apple-blue-dark scale-[1.02] shadow-sm'
        : 'text-slate-700 dark:text-slate-300'
    } ${isWinner ? 'text-black dark:text-white font-bold' : 'opacity-60'}`;
  };

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

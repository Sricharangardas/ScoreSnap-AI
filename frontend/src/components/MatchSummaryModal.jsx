import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { matchesAPI } from '../services/api';
import { X, Sparkles, Award, Compass, RefreshCw, Languages } from 'lucide-react';

export default function MatchSummaryModal({ matchId, onClose, darkMode }) {
  const [match, setMatch] = useState(null);
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);
  const [lang, setLang] = useState('English');
  const [translating, setTranslating] = useState(false);

  const loadData = async (targetLang) => {
    if (targetLang === lang) {
      setLoading(true);
    } else {
      setTranslating(true);
    }
    
    try {
      const matchRes = await matchesAPI.getMatchDetail(matchId);
      setMatch(matchRes.data);
      
      const summaryRes = await matchesAPI.getMatchAnalysis(matchId, targetLang);
      setSummary(summaryRes.data);
      setLang(targetLang);
    } catch (err) {
      console.error("Error loading match summary:", err);
    } finally {
      setLoading(false);
      setTranslating(false);
    }
  };

  useEffect(() => {
    if (matchId) {
      loadData('English');
    }
  }, [matchId]);

  if (!matchId) return null;

  const languages = ['English', 'Hindi', 'Spanish', 'French', 'German'];

  // Helper to render stats bars
  const renderStatBar = (name, val1, val2, suffix = '') => {
    const num1 = parseFloat(val1);
    const num2 = parseFloat(val2);
    const total = num1 + num2 || 1;
    const pct1 = (num1 / total) * 100;
    const pct2 = (num2 / total) * 100;

    return (
      <div className="space-y-1">
        <div className="flex justify-between text-[11px] font-semibold text-slate-700 dark:text-slate-300">
          <span>{val1}{suffix}</span>
          <span className="text-apple-text-subLight dark:text-apple-text-subDark uppercase tracking-wider text-[9px]">{name}</span>
          <span>{val2}{suffix}</span>
        </div>
        <div className="h-1.5 w-full bg-black/5 dark:bg-white/10 rounded-full overflow-hidden flex">
          <div className="bg-apple-blue-light dark:bg-apple-blue-dark h-full rounded-l-full" style={{ width: `${pct1}%` }} />
          <div className="bg-apple-orange-light dark:bg-apple-orange-dark h-full rounded-r-full" style={{ width: `${pct2}%` }} />
        </div>
      </div>
    );
  };

  return (
    <AnimatePresence>
      <div className="fixed inset-0 z-[150] flex items-center justify-center p-4">
        {/* Backdrop */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          onClick={onClose}
          className="fixed inset-0 bg-black/40 backdrop-blur-sm"
        />

        {/* Modal Window */}
        <motion.div
          initial={{ scale: 0.95, y: 30, opacity: 0 }}
          animate={{ scale: 1, y: 0, opacity: 1 }}
          exit={{ scale: 0.95, y: 30, opacity: 0 }}
          className={`relative w-full max-w-2xl max-h-[85vh] overflow-y-auto rounded-[32px] border p-6 md:p-8 ${
            darkMode 
              ? 'glass-card-dark border-white/10 shadow-2xl text-white' 
              : 'glass-card-light border-black/10 shadow-2xl text-slate-900'
          }`}
        >
          {/* Close button */}
          <button
            onClick={onClose}
            className="absolute top-6 right-6 p-2 rounded-full bg-black/5 dark:bg-white/5 hover:bg-black/10 dark:hover:bg-white/10 transition-colors"
          >
            <X size={16} />
          </button>

          {loading ? (
            <div className="py-20 flex flex-col items-center justify-center gap-3">
              <RefreshCw className="animate-spin text-apple-blue-light" size={24} />
              <p className="text-xs text-apple-text-subLight dark:text-apple-text-subDark">Generating AI summaries & statistics...</p>
            </div>
          ) : (
            <div className="space-y-6">
              
              {/* Header Scoreline */}
              <div className="text-center space-y-2 pb-4 border-b border-black/5 dark:border-white/5">
                <span className="text-[10px] font-bold uppercase tracking-widest text-apple-blue-light dark:text-apple-blue-dark">
                  {match.group_name} • {match.stadium}
                </span>
                <div className="flex items-center justify-center gap-6">
                  <span className="text-lg md:text-xl font-bold">{match.team_1}</span>
                  <span className="text-3xl font-extrabold font-mono bg-black/5 dark:bg-white/10 px-4 py-1.5 rounded-2xl">
                    {match.score_1} - {match.score_2}
                  </span>
                  <span className="text-lg md:text-xl font-bold">{match.team_2}</span>
                </div>
              </div>

              {/* Language Selector */}
              <div className="flex items-center justify-between bg-black/5 dark:bg-white/5 p-3 rounded-2xl">
                <span className="text-[10px] font-bold uppercase tracking-wider text-apple-text-subLight dark:text-apple-text-subDark flex items-center gap-1">
                  <Languages size={14} /> Translations
                </span>
                
                {translating ? (
                  <span className="text-[10px] text-apple-blue-light flex items-center gap-1 font-semibold">
                    <RefreshCw size={10} className="animate-spin" /> Translating via Gemini...
                  </span>
                ) : (
                  <div className="flex gap-1.5">
                    {languages.map(l => (
                      <button
                        key={l}
                        onClick={() => loadData(l)}
                        className={`px-2.5 py-1 rounded-lg text-[10px] font-semibold transition-all ${
                          lang === l
                            ? (darkMode ? 'bg-white text-black' : 'bg-black text-white')
                            : (darkMode ? 'hover:bg-white/10 text-apple-text-subDark' : 'hover:bg-black/5 text-apple-text-subLight')
                        }`}
                      >
                        {l}
                      </button>
                    ))}
                  </div>
                )}
              </div>

              {/* AI Headline Storyline */}
              {summary && (
                <div className="space-y-3">
                  <div className="inline-flex items-center gap-1 text-xs font-bold text-apple-blue-light dark:text-apple-blue-dark">
                    <Sparkles size={14} /> Gemini AI Analysis ({lang})
                  </div>
                  <h4 className="text-base font-extrabold leading-tight text-slate-800 dark:text-white">
                    "{summary.storyline}"
                  </h4>
                  <p className="text-xs text-slate-700 dark:text-slate-300 leading-relaxed">
                    {summary.ai_summary}
                  </p>
                </div>
              )}

              {/* Stats Breakdown Bars */}
              {match.stats_json && (
                <div className="space-y-4 pt-4 border-t border-black/5 dark:border-white/5">
                  <h4 className="text-[10px] font-bold uppercase tracking-widest text-apple-text-subLight dark:text-apple-text-subDark">
                    Match Stats Breakdown
                  </h4>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {renderStatBar('Possession', match.stats_json.possession?.team_1 || '50', match.stats_json.possession?.team_2 || '50', '%')}
                    {renderStatBar('Shots', match.stats_json.shots?.team_1 || '0', match.stats_json.shots?.team_2 || '0')}
                    {renderStatBar('Pass Accuracy', match.stats_json.pass_accuracy?.team_1 || '80', match.stats_json.pass_accuracy?.team_2 || '80', '%')}
                    {renderStatBar('Fouls', match.stats_json.fouls?.team_1 || '0', match.stats_json.fouls?.team_2 || '0')}
                  </div>
                </div>
              )}

              {/* Additional AI Sections */}
              {summary && (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6 pt-4 border-t border-black/5 dark:border-white/5">
                  
                  {/* Tactical Insight */}
                  <div className="space-y-2">
                    <h5 className="text-[10px] font-bold uppercase tracking-wider text-apple-text-subLight dark:text-apple-text-subDark flex items-center gap-1">
                      <Compass size={12} className="text-apple-blue-light" /> Tactical Analysis
                    </h5>
                    <p className="text-xs text-apple-text-subLight dark:text-apple-text-subDark leading-relaxed">
                      {summary.tactical_analysis || 'No tactical notes available.'}
                    </p>
                  </div>

                  {/* Best Player and Impact */}
                  <div className="space-y-4">
                    {summary.best_player && (
                      <div className="space-y-1">
                        <h5 className="text-[10px] font-bold uppercase tracking-wider text-apple-text-subLight dark:text-apple-text-subDark flex items-center gap-1">
                          <Award size={12} className="text-yellow-500" /> Player of the Match
                        </h5>
                        <p className="text-xs text-slate-800 dark:text-slate-200 font-bold">
                          🌟 {summary.best_player}
                        </p>
                      </div>
                    )}
                    
                    {summary.tournament_impact && (
                      <div className="space-y-1">
                        <h5 className="text-[10px] font-bold uppercase tracking-wider text-apple-text-subLight dark:text-apple-text-subDark">
                          Group Impact
                        </h5>
                        <p className="text-xs text-apple-text-subLight dark:text-apple-text-subDark leading-relaxed">
                          {summary.tournament_impact}
                        </p>
                      </div>
                    )}
                  </div>

                </div>
              )}

            </div>
          )}
        </motion.div>
      </div>
    </AnimatePresence>
  );
}

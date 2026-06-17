import React, { useState, useEffect } from 'react';
import { matchesAPI, cronAPI } from '../services/api';
import Bracket from '../components/Bracket';
import { Sparkles, HelpCircle, Activity, Award, CheckCircle2, Send } from 'lucide-react';

export default function Insights({ darkMode, user }) {
  const [matches, setMatches] = useState([]);
  const [selectedMatchId, setSelectedMatchId] = useState('');
  const [prediction, setPrediction] = useState(null);
  const [loadingPred, setLoadingPred] = useState(false);
  
  // Daily digest trigger states
  const [triggeringDigest, setTriggeringDigest] = useState(false);
  const [digestSuccessMsg, setDigestSuccessMsg] = useState('');

  useEffect(() => {
    const fetchUpcoming = async () => {
      try {
        const response = await matchesAPI.getMatches('scheduled');
        setMatches(response.data);
        if (response.data.length > 0) {
          setSelectedMatchId(response.data[0].match_id);
        }
      } catch (err) {
        console.error("Error loading upcoming matches:", err);
      }
    };
    fetchUpcoming();
  }, []);

  const handlePredict = async (e) => {
    e.preventDefault();
    if (!selectedMatchId) return;
    setLoadingPred(true);
    setPrediction(null);

    try {
      const response = await matchesAPI.getMatchPrediction(selectedMatchId);
      setPrediction(response.data);
    } catch (err) {
      console.error("Prediction failed:", err);
      alert("Failed to fetch prediction. Ensure your Gemini API Key is configured.");
    } finally {
      setLoadingPred(false);
    }
  };

  const handleTriggerDigest = async () => {
    setTriggeringDigest(true);
    setDigestSuccessMsg('');
    try {
      await cronAPI.triggerDigest();
      setDigestSuccessMsg('Daily Digest generated and emailed/WhatsApped successfully!');
      setTimeout(() => setDigestSuccessMsg(''), 5000);
    } catch (err) {
      console.error("Failed to trigger digest:", err);
      alert("Digest generation failed.");
    } finally {
      setTriggeringDigest(false);
    }
  };

  const selectedMatch = matches.find(m => m.match_id === selectedMatchId);

  return (
    <div className="space-y-10 py-6 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold tracking-tight text-slate-900 dark:text-white">
          ScoreSnap Intelligence & Tournament Insights
        </h1>
        <p className="text-xs text-apple-text-subLight dark:text-apple-text-subDark">
          Explore AI-driven bracket predictions, match forecasts, and trigger daily briefs
        </p>
      </div>

      {/* Grid: Predictor & Digest Trigger */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        {/* Predictor Card (2 columns) */}
        <div className={`lg:col-span-2 p-6 rounded-[24px] border flex flex-col justify-between ${
          darkMode ? 'glass-card-dark border-white/5 shadow-appleDark' : 'glass-card-light border-black/5 shadow-appleLight'
        }`}>
          <div>
            <h3 className="text-sm font-bold uppercase tracking-wider mb-2 flex items-center gap-1.5 text-apple-blue-light dark:text-apple-blue-dark">
              <Sparkles size={16} /> AI Match Outcome Predictor
            </h3>
            <p className="text-xs text-apple-text-subLight dark:text-apple-text-subDark mb-6">
              Select an upcoming match. Google Gemini will analyze historical team rosters, lineups, and tournament context to output a predicted scoreline, tactical battles, and win probabilities.
            </p>

            {matches.length === 0 ? (
              <p className="text-xs text-apple-text-subLight dark:text-apple-text-subDark italic py-4">
                No upcoming matches scheduled. Play some matches in the Matches tab!
              </p>
            ) : (
              <form onSubmit={handlePredict} className="flex flex-col sm:flex-row gap-3 items-end mb-6">
                <div className="flex-1 w-full">
                  <label className="block text-[10px] font-bold uppercase tracking-wider text-apple-text-subLight dark:text-apple-text-subDark mb-1">
                    Select upcoming fixture
                  </label>
                  <select
                    value={selectedMatchId}
                    onChange={(e) => {
                      setSelectedMatchId(e.target.value);
                      setPrediction(null);
                    }}
                    className="w-full text-xs p-3 rounded-xl border border-black/10 dark:border-white/10 bg-transparent focus:outline-none focus:ring-1 focus:ring-apple-blue-light"
                  >
                    {matches.map(m => (
                      <option key={m.match_id} value={m.match_id} className="text-black">
                        {m.team_1} vs {m.team_2}
                      </option>
                    ))}
                  </select>
                </div>
                <button
                  type="submit"
                  disabled={loadingPred}
                  className="bg-apple-blue-light hover:bg-blue-600 dark:bg-apple-blue-dark dark:hover:bg-blue-700 text-white text-xs font-bold py-3 px-6 rounded-xl transition-all shadow-appleBlue active:scale-95 disabled:opacity-50 w-full sm:w-auto"
                >
                  {loadingPred ? 'Analyzing...' : 'Generate Prediction'}
                </button>
              </form>
            )}

            {/* Prediction Output Display */}
            {prediction && (
              <div className="p-5 rounded-2xl bg-black/5 dark:bg-white/5 border border-black/5 dark:border-white/5 space-y-4">
                <div className="flex justify-between items-center">
                  <span className="text-xs font-bold uppercase tracking-wider text-apple-text-subLight dark:text-apple-text-subDark">
                    Predicted Result
                  </span>
                  <span className="bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 text-[10px] font-bold px-2 py-0.5 rounded-full">
                    Confidence: {prediction.confidence}
                  </span>
                </div>

                <div className="text-xl font-black text-slate-800 dark:text-white text-center py-2">
                  🔮 {prediction.predicted_score}
                </div>

                <div>
                  <h4 className="text-[10px] font-bold uppercase tracking-wider text-apple-text-subLight dark:text-apple-text-subDark mb-1">
                    Key Tactical Battle
                  </h4>
                  <p className="text-xs text-slate-800 dark:text-slate-200 font-semibold">
                    {prediction.key_battle}
                  </p>
                </div>

                <div>
                  <h4 className="text-[10px] font-bold uppercase tracking-wider text-apple-text-subLight dark:text-apple-text-subDark mb-1">
                    Detailed AI Analysis
                  </h4>
                  <p className="text-xs text-apple-text-subLight dark:text-apple-text-subDark leading-relaxed italic">
                    "{prediction.analysis}"
                  </p>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Daily Digest Trigger (1 column) */}
        <div className={`p-6 rounded-[24px] border flex flex-col justify-between ${
          darkMode ? 'glass-card-dark border-white/5 shadow-appleDark' : 'glass-card-light border-black/5 shadow-appleLight'
        }`}>
          <div>
            <h3 className="text-sm font-bold uppercase tracking-wider mb-2 flex items-center gap-1.5 text-slate-800 dark:text-slate-200">
              <Send size={15} className="text-apple-blue-light" /> Broadcast Daily Digest
            </h3>
            <p className="text-xs text-apple-text-subLight dark:text-apple-text-subDark mb-6 leading-relaxed">
              Ordinarily, the **Daily Digest Agent** executes automatically at 8:30 AM IST inside the cloud database. Click below to trigger this agent manually to generate a tournament digest of the last 24h results and send alerts immediately to all opted-in users!
            </p>

            <button
              disabled={triggeringDigest}
              onClick={handleTriggerDigest}
              className="w-full bg-apple-blue-light hover:bg-blue-600 dark:bg-apple-blue-dark dark:hover:bg-blue-700 text-white text-xs font-bold py-3 rounded-xl transition-all shadow-appleBlue active:scale-95 disabled:opacity-50 flex items-center justify-center gap-2"
            >
              {triggeringDigest ? (
                <>
                  <span className="w-3.5 h-3.5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                  Generating Digest...
                </>
              ) : (
                <>
                  <Send size={12} /> Dispatch Digest Now
                </>
              )}
            </button>
          </div>

          {digestSuccessMsg && (
            <div className="mt-4 p-4 rounded-xl bg-emerald-500/10 border border-emerald-500/20 text-emerald-600 dark:text-emerald-400 text-xs flex items-center gap-2">
              <CheckCircle2 size={16} />
              <span>{digestSuccessMsg}</span>
            </div>
          )}
        </div>

      </div>

      {/* Bracket Section */}
      <div className={`p-6 rounded-[30px] border ${
        darkMode ? 'glass-card-dark border-white/5 shadow-appleDark' : 'glass-card-light border-black/5 shadow-appleLight'
      }`}>
        <div>
          <h3 className="text-sm font-bold uppercase tracking-wider mb-1 flex items-center gap-2 text-slate-800 dark:text-slate-200">
            <Award size={15} className="text-yellow-500" /> Knockout Bracket Simulation
          </h3>
          <p className="text-xs text-apple-text-subLight dark:text-apple-text-subDark mb-6">
            Hover over any winner in the Quarterfinals/Semifinals to trace their potential path to the FIFA World Cup 2026 title.
          </p>
        </div>

        <Bracket />
      </div>
    </div>
  );
}

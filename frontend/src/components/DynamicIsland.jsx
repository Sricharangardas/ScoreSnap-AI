import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Eye, BellRing, Sparkles } from 'lucide-react';

export default function DynamicIsland({ onOpenMatchSummary }) {
  const [activeNotification, setActiveNotification] = useState(null);
  const [isExpanded, setIsExpanded] = useState(false);

  useEffect(() => {
    const handleMatchCompleted = (event) => {
      const { match } = event.detail;
      setActiveNotification(match);
      setIsExpanded(false);

      // Animation steps matching Apple's Dynamic Island:
      // 1. Show small capsule after a delay
      // 2. Automatically expand it to show scores
      // 3. Keep it expanded for 7 seconds
      // 4. Shrink it back and dismiss
      setTimeout(() => {
        setIsExpanded(true);
      }, 800);

      setTimeout(() => {
        setIsExpanded(false);
        setTimeout(() => {
          setActiveNotification(null);
        }, 300); // Wait for shrink animation before removing
      }, 9500);
    };

    window.addEventListener('match-completed', handleMatchCompleted);
    return () => {
      window.removeEventListener('match-completed', handleMatchCompleted);
    };
  }, []);

  if (!activeNotification) return null;

  return (
    <div className="fixed top-20 left-1/2 -translate-x-1/2 z-[100] pointer-events-none flex flex-col items-center">
      <AnimatePresence>
        <motion.div
          initial={{ width: 140, height: 35, borderRadius: 999, y: -20, opacity: 0 }}
          animate={
            isExpanded
              ? { 
                  width: 380, 
                  height: 140, 
                  borderRadius: 28, 
                  y: 0, 
                  opacity: 1,
                  boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.5)'
                }
              : { 
                  width: 220, 
                  height: 38, 
                  borderRadius: 999, 
                  y: 0, 
                  opacity: 1,
                  boxShadow: '0 4px 12px rgba(0, 0, 0, 0.15)'
                }
          }
          exit={{ width: 140, height: 35, borderRadius: 999, y: -20, opacity: 0 }}
          transition={{ type: 'spring', stiffness: 350, damping: 25 }}
          className="bg-black border border-white/10 text-white pointer-events-auto overflow-hidden flex flex-col justify-center items-center px-4"
        >
          {isExpanded ? (
            /* Expanded Dynamic Island showing full score and CTA */
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              transition={{ delay: 0.1 }}
              className="w-full h-full flex flex-col justify-between py-3 px-2 text-center"
            >
              <div className="flex justify-between items-center text-[10px] uppercase font-bold text-apple-blue-dark tracking-widest px-1">
                <span className="flex items-center gap-1">
                  <BellRing size={10} className="animate-pulse" /> Live Monitor
                </span>
                <span className="flex items-center gap-0.5 text-emerald-400">
                  <Sparkles size={10} /> Completed
                </span>
              </div>

              {/* Match Score Display */}
              <div className="flex items-center justify-around my-1.5">
                <span className="text-sm font-semibold truncate max-w-[100px]">
                  {activeNotification.team_1}
                </span>
                <span className="bg-white/10 text-xs px-2 py-1 rounded-md font-mono font-bold tracking-wider">
                  {activeNotification.score_1} - {activeNotification.score_2}
                </span>
                <span className="text-sm font-semibold truncate max-w-[100px]">
                  {activeNotification.team_2}
                </span>
              </div>

              {/* Call to action */}
              <button
                onClick={() => {
                  onOpenMatchSummary(activeNotification.match_id);
                  setActiveNotification(null);
                }}
                className="w-full bg-apple-blue-dark hover:bg-blue-600 text-white py-1.5 rounded-full text-xs font-semibold flex items-center justify-center gap-1.5 transition-all duration-200"
              >
                <Eye size={12} /> View AI Summary
              </button>
            </motion.div>
          ) : (
            /* Collapsed Pill Island */
            <div className="w-full h-full flex items-center justify-between text-xs px-2 text-apple-text-subDark font-semibold">
              <span className="animate-pulse text-emerald-400 font-bold">⚽</span>
              <span className="text-[10px] text-white">
                {activeNotification.team_1} vs {activeNotification.team_2} completed!
              </span>
              <span className="text-[9px] text-apple-blue-dark font-bold">View</span>
            </div>
          )}
        </motion.div>
      </AnimatePresence>
    </div>
  );
}

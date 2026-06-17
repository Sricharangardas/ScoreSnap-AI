import urllib.parse
import requests
from typing import Dict, Any

class WhatsAppService:
    @staticmethod
    def send_whatsapp(phone: str, apikey: str, text: str) -> bool:
        """
        Sends a WhatsApp message via CallMeBot API.
        Phone format: international without symbols (e.g., '919876543210')
        """
        if not phone or not apikey:
            print("CallMeBot: Phone number or API key is missing. Skipping WhatsApp dispatch.")
            return False

        # Clean phone number (remove +, spaces, hyphens)
        clean_phone = phone.replace("+", "").replace(" ", "").replace("-", "")
        
        # URL encode the message text
        encoded_text = urllib.parse.quote(text)
        url = f"https://api.callmebot.com/whatsapp.php?phone={clean_phone}&text={encoded_text}&apikey={apikey}"
        
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                print(f"WhatsApp notification sent successfully to {clean_phone} via CallMeBot.")
                return True
            else:
                print(f"CallMeBot returned status {response.status_code}: {response.text}")
                return False
        except Exception as e:
            print(f"Exception sending WhatsApp via CallMeBot: {e}")
            return False

    @classmethod
    def send_match_summary(cls, phone: str, apikey: str, match: Dict[str, Any], summary: Dict[str, Any]) -> bool:
        """
        Agent 4 - Formats the match report for WhatsApp using bolding and bullet points.
        """
        stats = match.get("stats_json") or {}
        winner = match['team_1'] if match['score_1'] > match['score_2'] else (match['team_2'] if match['score_2'] > match['score_1'] else "Draw")
        
        # Format scorers
        scorers = []
        for s in stats.get("scorers", []):
            scorers.append(f"• {s['player']} ({s['minute']}') - {s['team']}")
        scorers_str = "\n".join(scorers) if scorers else "• None"

        # Match date
        date_str = match.get("match_date")
        if isinstance(date_str, str):
            date_str = date_str[:10]
        elif hasattr(date_str, "strftime"):
            date_str = date_str.strftime("%d %B %Y")
        else:
            date_str = "15 June 2026"

        message = (
            f"*⚽ ScoreSnap AI | {match['team_1']} {match['score_1']}-{match['score_2']} {match['team_2']}*\n\n"
            f"Good Morning,\n\n"
            f"🏆 *Winner:* {winner}\n"
            f"⚽ *Final Score:* {match['team_1']} {match['score_1']} - {match['score_2']} {match['team_2']}\n"
            f"📅 *Date:* {date_str}\n"
            f"⏰ *Kickoff:* 4:30 AM IST\n"
            f"📍 *Stadium:* {match.get('stadium', 'World Cup Stadium')}\n"
            f"⭐ *Player of the Match:* {stats.get('player_of_the_match', 'N/A')}\n\n"
            f"*⚽ Goal Scorers:*\n{scorers_str}\n\n"
            f"*📊 Match Statistics:*\n"
            f"• Possession: {stats.get('possession_1', 50)}% - {stats.get('possession_2', 50)}%\n"
            f"• Shots: {stats.get('shots_1', 0)} - {stats.get('shots_2', 0)}\n"
            f"• Corners: {stats.get('corners_1', 0)} - {stats.get('corners_2', 0)}\n"
            f"• Cards: {stats.get('yellow_cards_1', 0)}Y/{stats.get('red_cards_1', 0)}R - {stats.get('yellow_cards_2', 0)}Y/{stats.get('red_cards_2', 0)}R\n"
            f"• Expected Goals (xG): {stats.get('expected_goals_1', 0.0)} - {stats.get('expected_goals_2', 0.0)}\n\n"
            f"📈 *Tournament Impact:*\n"
            f"{summary.get('tournament_impact', 'Standings updated.')}\n\n"
            f"📝 *AI Match Analysis:*\n"
            f"_{summary.get('ai_summary', '')}_\n\n"
            f"📅 *Next Match:* {match['team_1']} vs France\n\n"
            f"Thank you for using ScoreSnap AI."
        )
        return cls.send_whatsapp(phone, apikey, message)

    @classmethod
    def send_daily_digest(cls, phone: str, apikey: str, digest: Dict[str, Any], date_str: str) -> bool:
        """
        Agent 6 - Formats the daily digest report for WhatsApp.
        """
        message = (
            f"*⚽ ScoreSnap AI | Daily Digest - {date_str}*\n"
            f"_{digest.get('digest_title', 'ScoreSnap World Cup Morning Digest')}_\n\n"
            f"Good Morning,\n\n"
            f"*Overnight Action Summary:*\n"
            f"{digest.get('overnight_summary', '')}\n\n"
            f"⭐ *Biggest Upset:*\n"
            f"{digest.get('biggest_upset', 'None.')}\n\n"
            f"🔥 *Match of the Day:*\n"
            f"{digest.get('match_of_the_day', 'None.')}\n\n"
            f"⚽ *Highest-Scoring Match:*\n"
            f"{digest.get('highest_scoring_match', 'None.')}\n\n"
            f"👟 *Golden Boot Update:*\n"
            f"{digest.get('top_scorers_digest', 'Updated.')}\n\n"
            f"📊 *Standing Updates:*\n"
            f"{digest.get('standings_insight', '')}\n\n"
            f"Thank you for using ScoreSnap AI."
        )
        return cls.send_whatsapp(phone, apikey, message)

import os
import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Any

RESEND_API_KEY = os.getenv("RESEND_API_KEY")
FROM_EMAIL = os.getenv("FROM_EMAIL", "onboarding@resend.dev")

# SMTP Configuration (Optional Fallback)
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "") # e.g. Gmail App Password

class EmailService:
    @staticmethod
    def send_email(to_email: str, subject: str, html_content: str) -> bool:
        """
        Main sender method. Tries Resend first (if API key available),
        then falls back to SMTP if configured, else prints to stdout for local testing.
        """
        # 1. Try Resend
        if RESEND_API_KEY:
            url = "https://api.resend.com/emails"
            headers = {
                "Authorization": f"Bearer {RESEND_API_KEY}",
                "Content-Type": "application/json"
            }
            # Note: Onboarding email only allows sending to the registered Resend account email.
            payload = {
                "from": f"ScoreSnap AI <{FROM_EMAIL}>",
                "to": [to_email],
                "subject": subject,
                "html": html_content
            }
            try:
                response = requests.post(url, headers=headers, json=payload, timeout=10)
                if response.status_code in [200, 201]:
                    print(f"Email sent successfully to {to_email} via Resend.")
                    return True
                else:
                    print(f"Resend returned error status {response.status_code}: {response.text}")
            except Exception as e:
                print(f"Exception sending email via Resend: {e}")

        # 2. Try SMTP Fallback
        if SMTP_USER and SMTP_PASSWORD:
            try:
                msg = MIMEMultipart("alternative")
                msg["Subject"] = subject
                msg["From"] = f"ScoreSnap AI <{SMTP_USER}>"
                msg["To"] = to_email

                part = MIMEText(html_content, "html")
                msg.attach(part)

                with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                    server.starttls()
                    server.login(SMTP_USER, SMTP_PASSWORD)
                    server.sendmail(SMTP_USER, to_email, msg.as_string())
                print(f"Email sent successfully to {to_email} via SMTP.")
                return True
            except Exception as e:
                print(f"Exception sending email via SMTP: {e}")

        # 3. Development Console Print Fallback
        try:
            print("\n=== [MOCK EMAIL DISPATCH] ===")
            print(f"To: {to_email}")
            print(f"Subject: {subject}")
            print("Body Preview (first 500 chars):")
            print(html_content[:500] + "...")
            print("===============================\n")
        except UnicodeEncodeError:
            # Fallback to ascii representation if console encoding doesn't support emojis
            print("\n=== [MOCK EMAIL DISPATCH (Ascii Safe)] ===")
            print(f"To: {to_email}")
            print(f"Subject: {subject.encode('ascii', 'replace').decode('ascii')}")
            print("Body Preview (first 500 chars):")
            print(html_content[:500].encode('ascii', 'replace').decode('ascii') + "...")
            print("===============================\n")
        return True

    @classmethod
    def send_match_summary(cls, to_email: str, match: Dict[str, Any], summary: Dict[str, Any]) -> bool:
        """
        Agent 4 - Formats the match report using a premium HTML template matching the requested email layout.
        """
        stats = match.get("stats_json") or {}
        
        # Format lists
        scorers_list = ""
        for scorer in stats.get("scorers", []):
            scorers_list += f"<li>{scorer['player']} ({scorer['minute']}') - {scorer['team']}</li>"
        if not scorers_list:
            scorers_list = "<li>None</li>"

        # Format subject
        subject = f"⚽ ScoreSnap AI | {match['team_1']} {match['score_1']}-{match['score_2']} {match['team_2']}"
        
        # Standardize date format
        match_date = match.get("match_date")
        if isinstance(match_date, str):
            # Parse or slice
            date_str = match_date[:10]
        elif hasattr(match_date, "strftime"):
            date_str = match_date.strftime("%d %B %Y")
        else:
            date_str = "15 June 2026"

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{
                    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
                    background-color: #F5F5F7;
                    color: #1D1D1F;
                    margin: 0;
                    padding: 20px;
                }}
                .card {{
                    background: #ffffff;
                    border-radius: 20px;
                    padding: 30px;
                    box-shadow: 0 4px 30px rgba(0, 0, 0, 0.03);
                    border: 1px solid rgba(0, 0, 0, 0.05);
                    max-width: 600px;
                    margin: 0 auto;
                }}
                .header {{
                    text-align: center;
                    border-bottom: 1px solid #E5E5EA;
                    padding-bottom: 20px;
                    margin-bottom: 25px;
                }}
                .logo {{
                    font-weight: 700;
                    font-size: 24px;
                    color: #007AFF;
                    margin: 0;
                }}
                .tagline {{
                    color: #6E6E73;
                    font-size: 14px;
                    margin: 5px 0 0 0;
                }}
                .score-container {{
                    text-align: center;
                    margin: 20px 0;
                }}
                .teams {{
                    font-size: 20px;
                    font-weight: 600;
                }}
                .score {{
                    font-size: 48px;
                    font-weight: 800;
                    color: #1D1D1F;
                    margin: 10px 0;
                }}
                .details-grid {{
                    display: grid;
                    grid-template-columns: 1fr 1fr;
                    gap: 15px;
                    background: #F5F5F7;
                    padding: 15px;
                    border-radius: 12px;
                    margin-bottom: 25px;
                    font-size: 14px;
                }}
                .details-item b {{
                    color: #6E6E73;
                }}
                .section-title {{
                    font-size: 16px;
                    font-weight: 700;
                    color: #1D1D1F;
                    margin-top: 25px;
                    margin-bottom: 10px;
                    border-left: 4px solid #007AFF;
                    padding-left: 10px;
                }}
                .scorers-list {{
                    list-style-type: none;
                    padding-left: 0;
                    font-size: 14px;
                }}
                .scorers-list li {{
                    padding: 5px 0;
                    border-bottom: 1px solid #F5F5F7;
                }}
                .stats-table {{
                    width: 100%;
                    border-collapse: collapse;
                    font-size: 14px;
                    margin-bottom: 20px;
                }}
                .stats-table td {{
                    padding: 8px 10px;
                    border-bottom: 1px solid #F5F5F7;
                }}
                .stats-label {{
                    text-align: center;
                    color: #6E6E73;
                    font-weight: 600;
                }}
                .ai-box {{
                    background: rgba(0, 122, 255, 0.05);
                    border: 1px solid rgba(0, 122, 255, 0.1);
                    border-radius: 12px;
                    padding: 20px;
                    margin-bottom: 25px;
                }}
                .footer {{
                    text-align: center;
                    font-size: 12px;
                    color: #8E8E93;
                    margin-top: 30px;
                }}
            </style>
        </head>
        <body>
            <div class="card">
                <div class="header">
                    <div class="logo">ScoreSnap AI</div>
                    <div class="tagline">Sleep Through The Match, Wake Up Informed.</div>
                </div>
                
                <p>Good Morning,</p>
                
                <div class="score-container">
                    <div class="teams">{match['team_1']} vs {match['team_2']}</div>
                    <div class="score">{match['score_1']} - {match['score_2']}</div>
                    <div style="font-size: 14px; color: #34C759; font-weight: 600;">
                        🏆 Winner: {match['team_1'] if match['score_1'] > match['score_2'] else (match['team_2'] if match['score_2'] > match['score_1'] else "Draw")}
                    </div>
                </div>

                <div class="details-grid">
                    <div class="details-item"><b>📅 Date:</b><br>{date_str}</div>
                    <div class="details-item"><b>⏰ Kickoff:</b><br>4:30 AM IST</div>
                    <div class="details-item"><b>📍 Stadium:</b><br>{match.get('stadium', 'World Cup Stadium')}</div>
                    <div class="details-item"><b>⭐ Player of Match:</b><br>{stats.get('player_of_the_match', 'N/A')}</div>
                </div>

                <div class="section-title">⚽ Goal Scorers</div>
                <ul class="scorers-list">
                    {scorers_list}
                </ul>

                <div class="section-title">📊 Match Statistics</div>
                <table class="stats-table">
                    <tr>
                        <td width="30%">{stats.get('possession_1', 50)}%</td>
                        <td class="stats-label" width="40%">Possession</td>
                        <td width="30%" align="right">{stats.get('possession_2', 50)}%</td>
                    </tr>
                    <tr>
                        <td>{stats.get('shots_1', 0)}</td>
                        <td class="stats-label">Shots (On Target)</td>
                        <td align="right">{stats.get('shots_2', 0)}</td>
                    </tr>
                    <tr>
                        <td>{stats.get('corners_1', 0)}</td>
                        <td class="stats-label">Corners</td>
                        <td align="right">{stats.get('corners_2', 0)}</td>
                    </tr>
                    <tr>
                        <td>{stats.get('yellow_cards_1', 0)} Y / {stats.get('red_cards_1', 0)} R</td>
                        <td class="stats-label">Cards</td>
                        <td align="right">{stats.get('yellow_cards_2', 0)} Y / {stats.get('red_cards_2', 0)} R</td>
                    </tr>
                    <tr>
                        <td>{stats.get('expected_goals_1', 0.0)}</td>
                        <td class="stats-label">Expected Goals (xG)</td>
                        <td align="right">{stats.get('expected_goals_2', 0.0)}</td>
                    </tr>
                </table>

                <div class="section-title">📈 Tournament Impact</div>
                <p style="font-size: 14px; margin-bottom: 20px;">
                    {summary.get('tournament_impact', 'Standings recalculated details updated in dashboard.')}
                </p>

                <div class="ai-box">
                    <div style="font-weight: 700; color: #007AFF; margin-bottom: 8px; font-size: 14px; display: flex; align-items: center;">
                        🤖 AI Match Analysis ({summary.get('language', 'English')})
                    </div>
                    <p style="margin: 0; font-size: 14px; line-height: 1.5; font-style: italic;">
                        "{summary.get('ai_summary', '')}"
                    </p>
                    <div style="margin-top: 12px; font-size: 12px; color: #6E6E73;">
                        <b>Key Storyline:</b> {summary.get('storyline', '')}<br/>
                        <b>Turning Point:</b> {summary.get('turning_points', '')}<br/>
                        <b>Tactics:</b> {summary.get('tactical_analysis', '')}
                    </div>
                </div>

                <div class="details-grid" style="background: rgba(52, 199, 89, 0.05); border: 1px solid rgba(52, 199, 89, 0.1);">
                    <div class="details-item" style="grid-column: span 2;">
                        <b>📅 Next Match:</b><br/>
                        {match['team_1']} vs France
                    </div>
                </div>

                <div class="footer">
                    Thank you for using ScoreSnap AI.<br/>
                    © 2026 ScoreSnap AI. Built for the FIFA World Cup 2026.
                </div>
            </div>
        </body>
        </html>
        """
        return cls.send_email(to_email, subject, html_content)

    @classmethod
    def send_daily_digest(cls, to_email: str, digest: Dict[str, Any], date_str: str) -> bool:
        """
        Agent 6 - Sends the morning digest overview.
        """
        subject = f"⚽ ScoreSnap AI | Daily Digest - {date_str}"
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{
                    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
                    background-color: #F5F5F7;
                    color: #1D1D1F;
                    margin: 0;
                    padding: 20px;
                }}
                .card {{
                    background: #ffffff;
                    border-radius: 20px;
                    padding: 30px;
                    box-shadow: 0 4px 30px rgba(0, 0, 0, 0.03);
                    border: 1px solid rgba(0, 0, 0, 0.05);
                    max-width: 600px;
                    margin: 0 auto;
                }}
                .header {{
                    text-align: center;
                    border-bottom: 1px solid #E5E5EA;
                    padding-bottom: 20px;
                    margin-bottom: 25px;
                }}
                .logo {{
                    font-weight: 700;
                    font-size: 24px;
                    color: #007AFF;
                    margin: 0;
                }}
                .tagline {{
                    color: #6E6E73;
                    font-size: 14px;
                    margin: 5px 0 0 0;
                }}
                .section-title {{
                    font-size: 16px;
                    font-weight: 700;
                    color: #1D1D1F;
                    margin-top: 25px;
                    margin-bottom: 10px;
                    border-left: 4px solid #007AFF;
                    padding-left: 10px;
                }}
                .ai-box {{
                    background: rgba(0, 122, 255, 0.05);
                    border: 1px solid rgba(0, 122, 255, 0.1);
                    border-radius: 12px;
                    padding: 20px;
                    margin-bottom: 25px;
                    font-size: 14px;
                    line-height: 1.5;
                }}
                .footer {{
                    text-align: center;
                    font-size: 12px;
                    color: #8E8E93;
                    margin-top: 30px;
                }}
            </style>
        </head>
        <body>
            <div class="card">
                <div class="header">
                    <div class="logo">ScoreSnap AI</div>
                    <div class="tagline">{digest.get('digest_title', 'ScoreSnap World Cup Morning Digest')}</div>
                </div>
                
                <p>Good Morning Football Fan,</p>
                
                <div class="ai-box">
                    <b>Overnight Action Summary:</b><br/>
                    {digest.get('overnight_summary', '')}
                </div>

                <div class="section-title">⭐ Biggest Upset</div>
                <p style="font-size: 14px;">{digest.get('biggest_upset', 'No upsets reported.')}</p>

                <div class="section-title">🔥 Match of the Day</div>
                <p style="font-size: 14px;">{digest.get('match_of_the_day', 'None.')}</p>

                <div class="section-title">⚽ Highest-Scoring Match</div>
                <p style="font-size: 14px;">{digest.get('highest_scoring_match', 'None.')}</p>

                <div class="section-title">👟 Golden Boot Digest</div>
                <p style="font-size: 14px;">{digest.get('top_scorers_digest', 'Golden Boot updates will appear as the tournament progresses.')}</p>

                <div class="section-title">📊 Standing Updates</div>
                <p style="font-size: 14px;">{digest.get('standings_insight', 'Standings updated.')}</p>

                <div class="footer">
                    Thank you for using ScoreSnap AI.<br/>
                    © 2026 ScoreSnap AI. Built for the FIFA World Cup 2026.
                </div>
            </div>
        </body>
        </html>
        """
        return cls.send_email(to_email, subject, html_content)

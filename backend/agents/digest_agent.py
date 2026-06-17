import datetime
from sqlalchemy.orm import Session
from database.models import User, Match, Standings, EmailLog
from services.gemini_service import GeminiService
from services.email_service import EmailService
from services.whatsapp_service import WhatsAppService

class DigestAgent:
    @staticmethod
    def generate_and_dispatch_digest(db: Session) -> None:
        """
        Agent 6 - Compiles the daily morning digest briefing and delivers it.
        Runs daily. Prevents sending multiple digests in a 12-hour window.
        """
        now = datetime.datetime.utcnow()
        twelve_hours_ago = now - datetime.timedelta(hours=12)
        
        # 1. Fetch matches completed in the last 24 hours
        one_day_ago = now - datetime.timedelta(hours=24)
        recent_matches = db.query(Match).filter(
            Match.status == "completed",
            Match.match_date >= one_day_ago
        ).all()

        # If no matches completed, we can still send a general digest or skip.
        # Let's send a summary if we have recent matches, otherwise log and skip
        # or grab the latest 3 matches as a fallback so the user always sees a digest!
        if not recent_matches:
            print("No matches completed in the last 24 hours. Falling back to latest 3 completed matches for demo.")
            recent_matches = db.query(Match).filter(
                Match.status == "completed"
            ).order_by(Match.match_date.desc()).limit(3).all()

        if not recent_matches:
            print("No completed matches found in database. Skipping daily digest.")
            return

        # 2. Get standings overview
        standings = db.query(Standings).order_by(Standings.group_name, Standings.points.desc()).all()
        standings_summary = [
            {
                "group": s.group_name,
                "team": s.team_name,
                "played": s.played,
                "points": s.points,
                "goal_diff": s.goals_for - s.goals_against
            } for s in standings
        ]

        # 3. Structure completed matches for Gemini
        completed_matches_data = [
            {
                "match_id": m.match_id,
                "teams": f"{m.team_1} vs {m.team_2}",
                "score": f"{m.score_1} - {m.score_2}",
                "stadium": m.stadium,
                "scorers": m.stats_json.get("scorers", []) if m.stats_json else []
            } for m in recent_matches
        ]

        print("Generating daily digest content via Gemini...")
        digest_content = GeminiService.generate_daily_digest(completed_matches_data, standings_summary)
        
        # Date string for subjects
        date_str = now.strftime("%d %B %Y")

        # 4. Dispatch to users
        users = db.query(User).filter(User.daily_digest_enabled == True).all()
        for user in users:
            # A. Email Digest
            if user.notifications_enabled:
                # Check for duplicate digest in last 12 hours
                dup_email = db.query(EmailLog).filter(
                    EmailLog.user_id == user.id,
                    EmailLog.email_type == "daily_digest",
                    EmailLog.sent_at >= twelve_hours_ago
                ).first()

                if not dup_email:
                    print(f"Sending Daily Digest Email to {user.email}...")
                    success = EmailService.send_daily_digest(user.email, digest_content, date_str)
                    
                    log_entry = EmailLog(
                        user_id=user.id,
                        sent_at=now,
                        delivery_status="sent" if success else "failed",
                        email_type="daily_digest"
                    )
                    db.add(log_entry)
                    db.commit()
                else:
                    print(f"Daily Digest Email already sent to {user.email} in last 12 hours. Skipping.")

            # B. WhatsApp Digest
            if user.whatsapp_enabled and user.whatsapp_phone and user.whatsapp_apikey:
                # Check for duplicate digest in last 12 hours
                dup_wa = db.query(EmailLog).filter(
                    EmailLog.user_id == user.id,
                    EmailLog.email_type == "whatsapp_digest",
                    EmailLog.sent_at >= twelve_hours_ago
                ).first()

                if not dup_wa:
                    print(f"Sending Daily Digest WhatsApp to {user.whatsapp_phone}...")
                    success = WhatsAppService.send_daily_digest(
                        phone=user.whatsapp_phone,
                        apikey=user.whatsapp_apikey,
                        digest=digest_content,
                        date_str=date_str
                    )
                    
                    log_entry = EmailLog(
                        user_id=user.id,
                        sent_at=now,
                        delivery_status="sent" if success else "failed",
                        email_type="whatsapp_digest"
                    )
                    db.add(log_entry)
                    db.commit()
                else:
                    print(f"Daily Digest WhatsApp already sent to {user.whatsapp_phone} in last 12 hours. Skipping.")

        print("Daily Digest dispatch process complete.")

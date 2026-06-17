import datetime
from sqlalchemy.orm import Session
from database.models import User, Match, Summary, EmailLog
from services.email_service import EmailService
from services.whatsapp_service import WhatsAppService
from typing import Dict, Any

class EmailAgent:
    @staticmethod
    def dispatch_notifications(db: Session, match_id: str) -> None:
        """
        Agent 4 - Sends exactly one email/WhatsApp per completed match to subscribed users.
        Prevents duplicate notifications by writing to EmailLog before/after sending.
        """
        match = db.query(Match).filter(Match.match_id == match_id).first()
        if not match:
            print(f"Error: Match {match_id} not found for notification dispatch.")
            return

        if match.status != "completed":
            print(f"Match {match_id} is not completed. Skipping notifications.")
            return

        # Fetch users
        users = db.query(User).all()
        if not users:
            print("No registered users to notify.")
            return

        print(f"Dispatching notifications for completed match {match_id} ({match.team_1} vs {match.team_2})...")

        for user in users:
            # Determine preferred language for the user
            lang = user.preferred_language or "English"
            
            # Fetch or generate summary in user's preferred language
            summary = db.query(Summary).filter(
                Summary.match_id == match_id,
                Summary.language == lang
            ).first()

            # Fallback to English if not found
            if not summary:
                summary = db.query(Summary).filter(
                    Summary.match_id == match_id,
                    Summary.language == "English"
                ).first()

            if not summary:
                print(f"No AI summary available for match {match_id}. Cannot send notifications yet.")
                continue

            # Structure data for formatting
            match_dict = {
                "team_1": match.team_1,
                "team_2": match.team_2,
                "score_1": match.score_1,
                "score_2": match.score_2,
                "stadium": match.stadium,
                "match_date": match.match_date,
                "stats_json": match.stats_json
            }
            summary_dict = {
                "ai_summary": summary.ai_summary,
                "storyline": summary.storyline,
                "turning_points": summary.turning_points,
                "tactical_analysis": summary.tactical_analysis,
                "best_player": summary.best_player,
                "tournament_impact": summary.tournament_impact,
                "language": summary.language
            }

            # 1. Handle Email Notifications
            if user.notifications_enabled:
                # Check for duplicate email
                dup_email = db.query(EmailLog).filter(
                    EmailLog.match_id == match_id,
                    EmailLog.user_id == user.id,
                    EmailLog.email_type == "match_report"
                ).first()

                if not dup_email:
                    print(f"Sending email notification to {user.email}...")
                    success = EmailService.send_match_summary(user.email, match_dict, summary_dict)
                    
                    # Log dispatch
                    log_entry = EmailLog(
                        match_id=match_id,
                        user_id=user.id,
                        sent_at=datetime.datetime.utcnow(),
                        delivery_status="sent" if success else "failed",
                        email_type="match_report"
                    )
                    db.add(log_entry)
                    db.commit()
                else:
                    print(f"Email notification already sent to {user.email} for match {match_id}. Skipping.")

            # 2. Handle WhatsApp Notifications
            if user.whatsapp_enabled and user.whatsapp_phone and user.whatsapp_apikey:
                # Check for duplicate WhatsApp message
                dup_wa = db.query(EmailLog).filter(
                    EmailLog.match_id == match_id,
                    EmailLog.user_id == user.id,
                    EmailLog.email_type == "whatsapp_report"
                ).first()

                if not dup_wa:
                    print(f"Sending WhatsApp notification to {user.whatsapp_phone}...")
                    success = WhatsAppService.send_match_summary(
                        phone=user.whatsapp_phone,
                        apikey=user.whatsapp_apikey,
                        match=match_dict,
                        summary=summary_dict
                    )
                    
                    # Log dispatch
                    log_entry = EmailLog(
                        match_id=match_id,
                        user_id=user.id,
                        sent_at=datetime.datetime.utcnow(),
                        delivery_status="sent" if success else "failed",
                        email_type="whatsapp_report"
                    )
                    db.add(log_entry)
                    db.commit()
                else:
                    print(f"WhatsApp notification already sent to {user.whatsapp_phone} for match {match_id}. Skipping.")
                    
        print(f"Notifications dispatch completed for match {match_id}.")

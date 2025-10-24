from datetime import datetime, timezone
from sqlmodel import Session, select
from user_agents import parse
import requests
from app.schemas.visitor import VisitorCreate, VisitorRead
from app.models.visitor import Visitor


class VisitorService:

    @staticmethod
    def extract_visitor_info(ip: str, user_agent_str: str) -> dict:
        ua = parse(user_agent_str)

        data = {
            "ip_address": ip,
            "user_agent": user_agent_str,
            "browser": ua.browser.family,
            "os": ua.os.family,
            "device_type": (
                "Mobile" if ua.is_mobile else
                "Tablet" if ua.is_tablet else
                "Bot" if ua.is_bot else
                "Desktop"
            ),
            "visited_at": datetime.now(timezone.utc),
        }

        try:
            res = requests.get(f"http://ip-api.com/json/{ip}?fields=status,message,lat,lon,city,country")
            data=res.json()
            print("info data", data)
            data.update({
                "country": data["country"],
                "city": data["city"],
                "latitude": str(data["lat"]),
                "longitude": str(data["lon"]),
            })
        except Exception:
            pass

        return data

    @staticmethod
    def create_or_update_visitor(
        session: Session,
        visitor_create: VisitorCreate
    ) -> VisitorRead:

        visitor_data = VisitorService.extract_visitor_info(
            visitor_create.ip_address,
            visitor_create.user_agent
        )
        

        existing_visitor = session.exec(
            select(Visitor).where(
                (Visitor.ip_address == visitor_create.ip_address) &
                (Visitor.user_agent == visitor_create.user_agent)
            )
        ).first()

        if existing_visitor:
            existing_visitor.visited_at = visitor_data["visited_at"]
            session.add(existing_visitor)
            session.commit()
            session.refresh(existing_visitor)
            return VisitorRead.from_orm(existing_visitor)

        # Create new visitor
        visitor = Visitor(**visitor_data)
        session.add(visitor)
        session.commit()
        session.refresh(visitor)
        return VisitorRead.from_orm(visitor)

"""
Campaign Calendar Manager
Manages scheduling of campaigns across different social media platforms
"""
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import json
from dataclasses import dataclass, asdict
from enum import Enum


class Platform(Enum):
    """Social media platforms"""
    LINKEDIN = "LinkedIn"
    TWITTER = "Twitter"
    INSTAGRAM = "Instagram"
    FACEBOOK = "Facebook"
    TIKTOK = "TikTok"


@dataclass
class CampaignEvent:
    """Represents a scheduled campaign event"""
    campaign_id: str
    platform: str
    title: str
    content: str
    scheduled_time: str
    status: str = "Scheduled"  # Scheduled, Executed, Delayed, Cancelled
    performance_metrics: Dict = None
    
    def __post_init__(self):
        if self.performance_metrics is None:
            self.performance_metrics = {}


class CampaignCalendar:
    """Manages campaign scheduling and calendar operations"""
    
    def __init__(self):
        self.events: List[CampaignEvent] = []
        self.campaign_metadata: Dict = {}
    
    def add_event(self, event: CampaignEvent) -> None:
        """Add a campaign event to the calendar"""
        self.events.append(event)
        print(f"✓ Added {event.platform} campaign: {event.title} on {event.scheduled_time}")
    
    def schedule_campaign_across_platforms(
        self, 
        campaign_id: str,
        campaign_title: str,
        platforms: List[str],
        content_per_platform: Dict[str, str],
        start_date: str,
        frequency: str = "once"  # once, daily, weekly
    ) -> List[CampaignEvent]:
        """Schedule a campaign across multiple platforms"""
        events = []
        start = datetime.fromisoformat(start_date)
        
        for platform in platforms:
            content = content_per_platform.get(platform, "")
            
            if frequency == "once":
                scheduled_time = start.isoformat()
                event = CampaignEvent(
                    campaign_id=campaign_id,
                    platform=platform,
                    title=campaign_title,
                    content=content,
                    scheduled_time=scheduled_time
                )
                self.add_event(event)
                events.append(event)
            
            elif frequency == "daily":
                for i in range(7):  # Schedule for 7 days
                    scheduled_time = (start + timedelta(days=i)).isoformat()
                    event = CampaignEvent(
                        campaign_id=f"{campaign_id}_day{i+1}",
                        platform=platform,
                        title=f"{campaign_title} - Day {i+1}",
                        content=content,
                        scheduled_time=scheduled_time
                    )
                    self.add_event(event)
                    events.append(event)
            
            elif frequency == "weekly":
                for i in range(4):  # Schedule for 4 weeks
                    scheduled_time = (start + timedelta(weeks=i)).isoformat()
                    event = CampaignEvent(
                        campaign_id=f"{campaign_id}_week{i+1}",
                        platform=platform,
                        title=f"{campaign_title} - Week {i+1}",
                        content=content,
                        scheduled_time=scheduled_time
                    )
                    self.add_event(event)
                    events.append(event)
        
        return events
    
    def get_upcoming_events(self, days: int = 7) -> List[CampaignEvent]:
        """Get upcoming events for the next N days"""
        now = datetime.now()
        future = now + timedelta(days=days)
        
        upcoming = [
            event for event in self.events
            if now <= datetime.fromisoformat(event.scheduled_time) <= future
        ]
        return sorted(upcoming, key=lambda x: x.scheduled_time)
    
    def execute_event(self, event: CampaignEvent) -> None:
        """Mark event as executed"""
        event.status = "Executed"
        event.performance_metrics = {
            "reach": 5000 + (hash(event.campaign_id) % 10000),
            "engagement": 250 + (hash(event.campaign_id) % 1000),
            "clicks": 50 + (hash(event.campaign_id) % 500),
            "conversions": 5 + (hash(event.campaign_id) % 50)
        }
        print(f"✓ Executed {event.platform} campaign: {event.title}")
    
    def get_calendar_view(self, start_date: Optional[str] = None, days: int = 7) -> str:
        """Get a text-based calendar view"""
        if start_date:
            start = datetime.fromisoformat(start_date)
        else:
            start = datetime.now()
        
        end = start + timedelta(days=days)
        events_in_range = [
            event for event in self.events
            if start <= datetime.fromisoformat(event.scheduled_time) <= end
        ]
        
        calendar_str = f"\n📅 Campaign Calendar ({start.date()} to {end.date()})\n"
        calendar_str += "=" * 80 + "\n"
        
        for event in sorted(events_in_range, key=lambda x: x.scheduled_time):
            event_date = datetime.fromisoformat(event.scheduled_time)
            calendar_str += f"{event_date.strftime('%Y-%m-%d %H:%M')} | {event.platform:10} | {event.title[:40]:40} | {event.status}\n"
        
        return calendar_str
    
    def export_calendar(self, filename: str) -> None:
        """Export calendar to JSON file"""
        data = {
            "exported_at": datetime.now().isoformat(),
            "total_campaigns": len(self.events),
            "events": [asdict(event) for event in self.events]
        }
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"✓ Calendar exported to {filename}")
    
    def get_platform_summary(self) -> Dict[str, int]:
        """Get summary of campaigns per platform"""
        summary = {}
        for event in self.events:
            summary[event.platform] = summary.get(event.platform, 0) + 1
        return summary

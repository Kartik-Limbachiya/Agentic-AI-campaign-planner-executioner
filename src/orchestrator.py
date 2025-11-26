"""
Main Orchestrator for Agentic AI Campaign Planner & Executioner
Coordinates all agents and manages the complete workflow
"""

import os
import sys
import json
from typing import Dict, List
from datetime import datetime, timedelta
from pathlib import Path

# Import all components
from .calendar_manager import CampaignCalendar, CampaignEvent, Platform
from .campaign_executor import CampaignExecutor as RealExecutor
from .performance_tracker import PerformanceAnalyzer


class CampaignOrchestrator:
    """Main orchestrator for managing the complete campaign lifecycle"""
    
    def __init__(self, api_key: str = None):
        """Initialize the orchestrator with all components"""
        self.calendar = CampaignCalendar()
        self.executor = CampaignExecutor()
        self.analyzer = PerformanceAnalyzer(api_key=api_key)
        self.campaigns = {}
        # Get the output directory
        import os
        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.output_dir = Path(current_dir) / "outputs"
        self.output_dir.mkdir(exist_ok=True)
    
    def plan_campaign(
        self,
        campaign_name: str,
        target_audience: str,
        campaign_goal: str,
        platforms: List[str],
        budget: str,
        duration_days: int = 28,
        start_date: str = None
    ) -> Dict:
        """
        Plan a social media campaign across multiple platforms
        
        Args:
            campaign_name: Name of the campaign
            target_audience: Target audience description
            campaign_goal: Goal of the campaign
            platforms: List of social media platforms
            budget: Budget allocation
            duration_days: Duration of campaign
            start_date: Start date (ISO format) or None for today
        
        Returns:
            Campaign plan with strategies
        """
        
        if start_date is None:
            start_date = datetime.now().isoformat()
        
        print(f"\n🎯 Planning campaign: {campaign_name}")
        print(f"   Audience: {target_audience}")
        print(f"   Goal: {campaign_goal}")
        print(f"   Platforms: {', '.join(platforms)}")
        print(f"   Duration: {duration_days} days")
        
        # Create sample campaign plan
        campaign_plan = {
            "campaign_id": f"camp_{datetime.now().timestamp()}",
            "name": campaign_name,
            "target_audience": target_audience,
            "goal": campaign_goal,
            "platforms": platforms,
            "budget": budget,
            "start_date": start_date,
            "duration_days": duration_days,
            "strategies": self._generate_platform_strategies(platforms, campaign_goal),
            "content": self._generate_platform_content(platforms, campaign_name, target_audience)
        }
        
        self.campaigns[campaign_plan["campaign_id"]] = campaign_plan
        print(f"✓ Campaign plan created with ID: {campaign_plan['campaign_id']}")
        
        return campaign_plan
    
    def _generate_platform_strategies(self, platforms: List[str], goal: str) -> Dict:
        """Generate platform-specific strategies"""
        strategies = {}
        
        platform_details = {
            "LinkedIn": {
                "frequency": "3-4 times per week",
                "content_type": "Articles, thought leadership, company updates",
                "kpis": ["Impressions", "Engagement rate", "Profile visits"]
            },
            "Twitter": {
                "frequency": "Daily (1-2 tweets)",
                "content_type": "News, hot takes, conversations, threads",
                "kpis": ["Retweets", "Likes", "Replies"]
            },
            "Instagram": {
                "frequency": "4-5 times per week",
                "content_type": "Reels, Stories, carousel posts, behind-the-scenes",
                "kpis": ["Reach", "Saves", "Shares", "Follower growth"]
            },
            "Facebook": {
                "frequency": "3-4 times per week",
                "content_type": "Community posts, videos, events",
                "kpis": ["Reach", "Video views", "Engagement"]
            },
            "TikTok": {
                "frequency": "Daily (2-3 videos)",
                "content_type": "Trends, challenges, educational content",
                "kpis": ["Views", "Watch time", "Shares"]
            }
        }
        
        for platform in platforms:
            details = platform_details.get(platform, {})
            strategies[platform] = {
                "posting_frequency": details.get("frequency", "Regular"),
                "content_type": details.get("content_type", "General"),
                "primary_kpis": details.get("kpis", []),
                "goal_alignment": f"Aligned with '{goal}'"
            }
        
        return strategies
    
    def _generate_platform_content(self, platforms: List[str], campaign_name: str, audience: str) -> Dict:
        """Generate sample content for each platform"""
        content = {}
        
        for platform in platforms:
            if platform == "LinkedIn":
                content[platform] = f"🎯 {campaign_name}\nExciting announcement for our {audience}! Learn more about how we're driving innovation. #LinkedInPost"
            elif platform == "Twitter":
                content[platform] = f"🚀 {campaign_name} is here! Perfect for {audience}. Check it out now! #SocialMedia #Campaign"
            elif platform == "Instagram":
                content[platform] = f"✨ {campaign_name} is live! 🎉 Designed for {audience} who want to stay ahead. Tap the link in bio! 📸 #InstagramReels"
            elif platform == "Facebook":
                content[platform] = f"📢 We're excited to introduce {campaign_name}! Created specifically for {audience}. Join our community and discover more!"
            elif platform == "TikTok":
                content[platform] = f"POV: {campaign_name} just changed everything for {audience} 🔥 #FYP #Trending #NewAnnouncement"
        
        return content
    
    def schedule_campaigns(self, campaign_id: str, frequency: str = "once") -> List[CampaignEvent]:
        """
        Schedule campaign across platforms
        
        Args:
            campaign_id: Campaign to schedule
            frequency: 'once', 'daily', or 'weekly'
        
        Returns:
            List of scheduled events
        """
        campaign = self.campaigns.get(campaign_id)
        if not campaign:
            print(f"❌ Campaign {campaign_id} not found")
            return []
        
        print(f"\n📅 Scheduling campaign: {campaign['name']}")
        print(f"   Frequency: {frequency}")
        
        events = self.calendar.schedule_campaign_across_platforms(
            campaign_id=campaign_id,
            campaign_title=campaign["name"],
            platforms=campaign["platforms"],
            content_per_platform=campaign["content"],
            start_date=campaign["start_date"],
            frequency=frequency
        )
        
        print(f"✓ Scheduled {len(events)} posts across {len(campaign['platforms'])} platforms")
        return events
    
    def execute_scheduled_campaigns(self) -> Dict:
        """Execute all scheduled campaigns"""
        print(f"\n🚀 Executing scheduled campaigns...")
        
        upcoming_events = self.calendar.get_upcoming_events(days=7)
        
        if not upcoming_events:
            print("   No campaigns scheduled for the next 7 days")
            return {"status": "no_campaigns"}
        
        execution_summary = {
            "timestamp": datetime.now().isoformat(),
            "total_posts_executed": 0,
            "platforms_covered": set(),
            "executions": []
        }
        
        for event in upcoming_events:
            # Execute the campaign
            result = self.executor.simulate_post_execution(event)
            execution_summary["executions"].append(result)
            execution_summary["total_posts_executed"] += 1
            execution_summary["platforms_covered"].add(event.platform)
            
            # Mark as executed
            self.calendar.execute_event(event)
        
        execution_summary["platforms_covered"] = list(execution_summary["platforms_covered"])
        print(f"✓ Executed {execution_summary['total_posts_executed']} posts on {len(execution_summary['platforms_covered'])} platforms")
        
        return execution_summary
    
    def track_performance(self) -> Dict:
        """Track campaign performance"""
        print(f"\n📊 Tracking campaign performance...")
        
        analytics = self.executor.simulator.get_all_analytics()
        
        return analytics
    
    def generate_performance_report(self) -> str:
        """Generate comprehensive performance report"""
        print(f"\n📈 Generating performance report...")
        
        analytics = self.track_performance()
        report = self.analyzer.generate_performance_report(analytics)
        
        # Save report
        report_path = self.output_dir / f"performance_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        self.analyzer.save_report(report, str(report_path))
        
        return report
    
    def export_calendar(self) -> str:
        """Export calendar to file"""
        calendar_path = self.output_dir / f"campaign_calendar_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        self.calendar.export_calendar(str(calendar_path))
        return str(calendar_path)
    
    def run_complete_workflow(
        self,
        campaign_name: str,
        target_audience: str,
        campaign_goal: str,
        platforms: List[str],
        budget: str
    ) -> Dict:
        """
        Run complete campaign workflow from planning to reporting
        
        Args:
            campaign_name: Name of campaign
            target_audience: Target audience
            campaign_goal: Campaign goal
            platforms: Social media platforms
            budget: Budget allocation
        
        Returns:
            Complete workflow results
        """
        
        print("\n" + "=" * 80)
        print("🤖 AGENTIC AI CAMPAIGN PLANNER & EXECUTIONER")
        print("=" * 80)
        
        # Step 1: Plan campaign
        campaign_plan = self.plan_campaign(
            campaign_name=campaign_name,
            target_audience=target_audience,
            campaign_goal=campaign_goal,
            platforms=platforms,
            budget=budget
        )
        
        # Step 2: Schedule campaigns
        events = self.schedule_campaigns(campaign_plan["campaign_id"], frequency="daily")
        
        # Step 3: View calendar
        calendar_view = self.calendar.get_calendar_view()
        print(calendar_view)
        
        # Step 4: Execute campaigns
        execution_result = self.execute_scheduled_campaigns()
        
        # Step 5: Track performance
        analytics = self.track_performance()
        
        # Step 6: Generate report
        report = self.generate_performance_report()
        
        # Step 7: Export calendar
        calendar_export_path = self.export_calendar()
        
        # Compile results
        workflow_result = {
            "campaign_id": campaign_plan["campaign_id"],
            "campaign_name": campaign_name,
            "workflow_status": "completed",
            "steps_completed": [
                "Campaign Planning",
                "Calendar Scheduling",
                "Campaign Execution",
                "Performance Tracking",
                "Report Generation"
            ],
            "stats": {
                "total_events_scheduled": len(events),
                "platforms_targeted": len(platforms),
                "posts_executed": execution_result.get("total_posts_executed", 0),
                "calendar_export": calendar_export_path
            },
            "analytics_summary": analytics,
            "report_preview": report[:500]  # First 500 chars of report
        }
        
        print("\n" + "=" * 80)
        print("✅ WORKFLOW COMPLETED SUCCESSFULLY")
        print("=" * 80)
        
        return workflow_result


# Backward compatibility for simulation
class CampaignExecutor:
    def __init__(self):
        self._executor = RealExecutor()
        self.simulator = self._executor.simulator
    
    def simulate_post_execution(self, event) -> Dict:
        """Simulate posting to platform"""
        return self.simulator.post_to_platform(event.platform, event.content, event.scheduled_time)

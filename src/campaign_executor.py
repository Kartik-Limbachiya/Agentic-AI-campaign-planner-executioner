"""
Campaign Execution Manager
Handles scheduling and execution of campaigns on social media platforms
"""
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import random
import json


class SocialMediaSimulator:
    """Simulates social media platform interactions for POC"""
    
    def __init__(self):
        self.executed_campaigns = []
        self.platform_configs = self._initialize_platforms()
    
    def _initialize_platforms(self) -> Dict:
        """Initialize platform-specific configurations"""
        return {
            "LinkedIn": {
                "base_reach": 10000,
                "engagement_rate": 0.025,
                "avg_followers": 5000
            },
            "Twitter": {
                "base_reach": 15000,
                "engagement_rate": 0.035,
                "avg_followers": 8000
            },
            "Instagram": {
                "base_reach": 20000,
                "engagement_rate": 0.045,
                "avg_followers": 12000
            },
            "Facebook": {
                "base_reach": 25000,
                "engagement_rate": 0.020,
                "avg_followers": 15000
            },
            "TikTok": {
                "base_reach": 30000,
                "engagement_rate": 0.055,
                "avg_followers": 20000
            }
        }
    
    def post_to_platform(self, platform: str, content: str, scheduled_time: str) -> Dict:
        """Simulate posting content to a platform"""
        post_id = f"{platform}_{datetime.now().timestamp()}"
        
        config = self.platform_configs.get(platform, {})
        base_reach = config.get("base_reach", 5000)
        engagement_rate = config.get("engagement_rate", 0.03)
        
        # Simulate performance metrics with some randomness
        reach = int(base_reach * (0.8 + random.random() * 0.4))
        engagements = int(reach * engagement_rate * (0.7 + random.random() * 0.6))
        clicks = int(engagements * 0.2 * (0.5 + random.random()))
        conversions = int(clicks * 0.05 * (0.3 + random.random()))
        
        post_data = {
            "post_id": post_id,
            "platform": platform,
            "content_preview": content[:100],
            "posted_at": datetime.now().isoformat(),
            "scheduled_time": scheduled_time,
            "status": "live",
            "metrics": {
                "reach": reach,
                "engagements": engagements,
                "likes": int(engagements * 0.7),
                "comments": int(engagements * 0.2),
                "shares": int(engagements * 0.1),
                "clicks": clicks,
                "conversions": conversions
            }
        }
        
        self.executed_campaigns.append(post_data)
        return post_data
    
    def schedule_post(self, platform: str, content: str, scheduled_time: str) -> Dict:
        """Schedule a post for future execution"""
        return {
            "platform": platform,
            "status": "scheduled",
            "content_preview": content[:100],
            "scheduled_time": scheduled_time,
            "message": f"Post scheduled on {platform} for {scheduled_time}"
        }
    
    def get_platform_analytics(self, platform: str, days: int = 7) -> Dict:
        """Get analytics for a specific platform"""
        platform_posts = [p for p in self.executed_campaigns if p["platform"] == platform]
        
        if not platform_posts:
            return {"platform": platform, "posts": 0, "total_reach": 0}
        
        total_reach = sum(p["metrics"]["reach"] for p in platform_posts)
        total_engagements = sum(p["metrics"]["engagements"] for p in platform_posts)
        total_clicks = sum(p["metrics"]["clicks"] for p in platform_posts)
        total_conversions = sum(p["metrics"]["conversions"] for p in platform_posts)
        
        return {
            "platform": platform,
            "posts_count": len(platform_posts),
            "total_reach": total_reach,
            "total_engagements": total_engagements,
            "avg_engagement_rate": (total_engagements / total_reach * 100) if total_reach > 0 else 0,
            "total_clicks": total_clicks,
            "total_conversions": total_conversions,
            "ctr": (total_clicks / total_reach * 100) if total_reach > 0 else 0,
            "conversion_rate": (total_conversions / total_clicks * 100) if total_clicks > 0 else 0
        }
    
    def get_all_analytics(self) -> Dict:
        """Get analytics across all platforms"""
        platforms = list(self.platform_configs.keys())
        analytics = {}
        
        for platform in platforms:
            analytics[platform] = self.get_platform_analytics(platform)
        
        return analytics


class CampaignExecutor:
    """Manages campaign execution workflow"""
    
    def __init__(self):
        self.simulator = SocialMediaSimulator()
        self.execution_log = []
    
    def execute_campaign(
        self,
        campaign_id: str,
        platforms: List[str],
        content_per_platform: Dict[str, str],
        start_time: Optional[str] = None
    ) -> Dict:
        """Execute a campaign across multiple platforms"""
        
        if start_time is None:
            start_time = datetime.now().isoformat()
        
        execution_result = {
            "campaign_id": campaign_id,
            "started_at": datetime.now().isoformat(),
            "platforms_targeted": platforms,
            "posts": []
        }
        
        for platform in platforms:
            content = content_per_platform.get(platform, "")
            if not content:
                continue
            
            result = self.simulator.post_to_platform(platform, content, start_time)
            execution_result["posts"].append(result)
            
            self.execution_log.append({
                "campaign_id": campaign_id,
                "platform": platform,
                "execution_time": datetime.now().isoformat(),
                "status": "executed"
            })
        
        return execution_result
    
    def get_execution_status(self, campaign_id: str) -> Dict:
        """Get execution status of a campaign"""
        campaign_logs = [log for log in self.execution_log if log["campaign_id"] == campaign_id]
        
        return {
            "campaign_id": campaign_id,
            "total_platforms": len(campaign_logs),
            "executions": campaign_logs,
            "status": "completed" if campaign_logs else "not_started"
        }
    
    def export_execution_report(self, filename: str) -> None:
        """Export execution report to file"""
        report = {
            "export_time": datetime.now().isoformat(),
            "total_campaigns_executed": len(set(log["campaign_id"] for log in self.execution_log)),
            "total_posts": len(self.simulator.executed_campaigns),
            "analytics": self.simulator.get_all_analytics(),
            "execution_log": self.execution_log
        }
        
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)

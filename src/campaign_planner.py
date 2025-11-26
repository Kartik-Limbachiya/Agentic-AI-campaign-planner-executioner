"""
Campaign Planning Agent
Uses CrewAI to plan social media campaigns across multiple platforms (if available)
"""
from typing import List, Dict
import json


class CampaignPlanner:
    """Agent-based campaign planner (with optional AI support)"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key
        self.platforms = ["LinkedIn", "Twitter", "Instagram", "Facebook", "TikTok"]
        self.use_ai = False
        
        # Try to import CrewAI if available and api_key is provided
        if api_key:
            try:
                from crewai import Agent, Task, Crew
                from langchain_openai import ChatOpenAI
                self.use_ai = True
                self.CrewAI_available = True
            except ImportError:
                self.CrewAI_available = False
        else:
            self.CrewAI_available = False
    
    def create_planning_agent(self):
        """Create the campaign planning agent (if CrewAI available)"""
        if not self.use_ai:
            return None
        
        from crewai import Agent
        from langchain_openai import ChatOpenAI
        
        llm = ChatOpenAI(model="gpt-4", api_key=self.api_key)
        return Agent(
            role="Campaign Strategist",
            goal="Create detailed, platform-specific social media campaign strategies",
            backstory="""You are an expert social media campaign strategist with 10+ years of experience.
            You understand each platform's unique audience, best practices, and content requirements.
            You create engaging, data-driven campaigns that drive real business results.""",
            llm=llm,
            verbose=True
        )
    
    def create_content_specialist_agent(self):
        """Create the content specialist agent (if CrewAI available)"""
        if not self.use_ai:
            return None
        
        from crewai import Agent
        from langchain_openai import ChatOpenAI
        
        llm = ChatOpenAI(model="gpt-4", api_key=self.api_key)
        return Agent(
            role="Content Specialist",
            goal="Create compelling platform-specific content for each social media channel",
            backstory="""You are a master content creator who excels at tailoring messages for different platforms.
            You understand that LinkedIn content differs from TikTok content, and you craft each message perfectly.""",
            llm=llm,
            verbose=True
        )
    
    def plan_campaign(
        self,
        campaign_name: str,
        target_audience: str,
        campaign_goal: str,
        budget: str,
        duration: str = "4 weeks"
    ) -> Dict:
        """Plan a complete social media campaign"""
        
        if not self.use_ai:
            # Return basic plan without AI
            return self._generate_basic_plan(campaign_name, target_audience, campaign_goal, budget, duration)
        
        try:
            from crewai import Agent, Task, Crew
            
            planner_agent = self.create_planning_agent()
            content_agent = self.create_content_specialist_agent()
            
            if not planner_agent or not content_agent:
                return self._generate_basic_plan(campaign_name, target_audience, campaign_goal, budget, duration)
            
            # Task 1: Strategy Planning
            strategy_task = Task(
                description=f"""Plan a comprehensive social media campaign with these details:
                - Campaign Name: {campaign_name}
                - Target Audience: {target_audience}
                - Campaign Goal: {campaign_goal}
                - Budget: {budget}
                - Duration: {duration}
                
                For each platform (LinkedIn, Twitter, Instagram, Facebook, TikTok), provide:
                1. Platform-specific strategy
                2. Posting frequency and best times
                3. Content themes and messaging angles
                4. KPIs to track
                5. Expected reach and engagement estimates
                
                Format as JSON with platform as keys.""",
                agent=planner_agent,
                expected_output="Detailed campaign strategy in JSON format"
            )
            
            # Task 2: Content Creation
            content_task = Task(
                description=f"""Based on the campaign strategy, create sample content for each platform:
                - Campaign Name: {campaign_name}
                - Target Audience: {target_audience}
                
                For each platform, create:
                1. 2-3 sample posts/content pieces
                2. Hashtags (3-5 per platform)
                3. Call-to-action
                4. Media/visual recommendations
                
                Tailor each piece to the platform's native format and audience.""",
                agent=content_agent,
                expected_output="Platform-specific content samples in JSON format"
            )
            
            # Create crew
            crew = Crew(
                agents=[planner_agent, content_agent],
                tasks=[strategy_task, content_task],
                verbose=True
            )
            
            # Execute
            result = crew.kickoff()
            
            return {
                "campaign_name": campaign_name,
                "target_audience": target_audience,
                "goal": campaign_goal,
                "budget": budget,
                "duration": duration,
                "planning_result": str(result)
            }
        except Exception as e:
            print(f"Warning: AI planning failed ({str(e)}), using basic planning")
            return self._generate_basic_plan(campaign_name, target_audience, campaign_goal, budget, duration)
    
    def _generate_basic_plan(self, campaign_name: str, target_audience: str, campaign_goal: str, budget: str, duration: str) -> Dict:
        """Generate basic campaign plan without AI"""
        return {
            "campaign_name": campaign_name,
            "target_audience": target_audience,
            "goal": campaign_goal,
            "budget": budget,
            "duration": duration,
            "strategies": self._generate_platform_strategies(self.platforms, campaign_goal),
            "content": self._generate_platform_content(self.platforms, campaign_name, target_audience)
        }
    
    def parse_campaign_plan(self, plan_text: str) -> Dict:
        """Parse campaign plan text into structured format"""
        try:
            # Try to extract JSON from the response
            if "{" in plan_text and "}" in plan_text:
                start = plan_text.find("{")
                end = plan_text.rfind("}") + 1
                json_str = plan_text[start:end]
                return json.loads(json_str)
        except (json.JSONDecodeError, ValueError):
            pass
        
        # Fallback: return structured format
        return {
            "strategy": plan_text,
            "platforms": self.platforms
        }
    
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
    
    def get_platform_content_template(self, platform: str) -> Dict:
        """Get content template for a specific platform"""
        templates = {
            "LinkedIn": {
                "character_limit": 3000,
                "tone": "Professional, thought-leadership",
                "content_types": ["Articles", "Case studies", "Industry insights", "Company updates"],
                "best_posting_times": "Tuesday-Thursday, 7-9 AM"
            },
            "Twitter": {
                "character_limit": 280,
                "tone": "Conversational, timely, trending",
                "content_types": ["News, Updates, Threads, Questions"],
                "best_posting_times": "Monday-Friday, 8-10 AM & 5-6 PM"
            },
            "Instagram": {
                "character_limit": 2200,
                "tone": "Visual, aspirational, engaging",
                "content_types": ["Photos, Reels, Stories, Carousels"],
                "best_posting_times": "Monday-Friday, 11 AM - 1 PM"
            },
            "Facebook": {
                "character_limit": 5000,
                "tone": "Community-focused, conversational",
                "content_types": ["Stories, Videos, Links, Events"],
                "best_posting_times": "Thursday-Friday, 1-4 PM"
            },
            "TikTok": {
                "character_limit": 150,
                "tone": "Trendy, authentic, entertaining",
                "content_types": ["Trends, Challenges, Behind-the-scenes, Educational"],
                "best_posting_times": "Tuesday-Thursday, 6-10 PM"
            }
        }
        return templates.get(platform, {})

"""
Performance Tracking and Analysis Agent
Monitors campaign performance and generates insights
"""
from typing import Dict, List
from datetime import datetime
import json


class PerformanceAnalyzer:
    """Analyzes campaign performance (with optional AI agent integration)"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key
        self.performance_data = {}
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
    
    def create_analytics_agent(self):
        """Create the analytics agent (if CrewAI available)"""
        if not self.use_ai:
            return None
        
        from crewai import Agent
        from langchain_openai import ChatOpenAI
        
        llm = ChatOpenAI(model="gpt-4", api_key=self.api_key)
        return Agent(
            role="Analytics Expert",
            goal="Analyze campaign performance data and extract actionable insights",
            backstory="""You are a data-driven marketing analyst with expertise in social media metrics.
            You understand engagement rates, reach, conversions, and can identify trends and opportunities.""",
            llm=llm,
            verbose=True
        )
    
    def create_insights_agent(self):
        """Create the insights agent (if CrewAI available)"""
        if not self.use_ai:
            return None
        
        from crewai import Agent
        from langchain_openai import ChatOpenAI
        
        llm = ChatOpenAI(model="gpt-4", api_key=self.api_key)
        return Agent(
            role="Strategic Insights Lead",
            goal="Provide strategic recommendations based on campaign performance",
            backstory="""You are a strategic marketing consultant who translates data into actionable recommendations.
            You understand what works, why it works, and how to optimize for better results.""",
            llm=llm,
            verbose=True
        )
    
    def analyze_campaign_performance(self, analytics_data: Dict) -> Dict:
        """Analyze campaign performance and generate insights"""
        
        if not self.use_ai:
            # Fallback to non-AI analysis
            return self._generate_basic_analysis(analytics_data)
        
        try:
            from crewai import Agent, Task, Crew
            
            analytics_agent = self.create_analytics_agent()
            insights_agent = self.create_insights_agent()
            
            if not analytics_agent or not insights_agent:
                return self._generate_basic_analysis(analytics_data)
            
            # Task 1: Analyze metrics
            analysis_task = Task(
                description=f"""Analyze the following campaign performance data:
                
                {json.dumps(analytics_data, indent=2)}
                
                Provide analysis for:
                1. Overall reach and engagement metrics
                2. Platform-by-platform performance comparison
                3. Conversion efficiency (conversions vs. reach)
                4. Best and worst performing platforms
                5. Engagement rate trends
                
                Format as JSON with clear metrics and insights.""",
                agent=analytics_agent,
                expected_output="Detailed performance analysis in JSON format"
            )
            
            # Task 2: Generate recommendations
            recommendations_task = Task(
                description=f"""Based on the campaign performance analysis, provide strategic recommendations:
                
                {json.dumps(analytics_data, indent=2)}
                
                Provide:
                1. What worked well and why
                2. What underperformed and potential reasons
                3. Platform-specific optimization recommendations
                4. Content strategy adjustments
                5. Budget allocation suggestions
                6. Next steps for campaign improvement
                
                Be specific and actionable.""",
                agent=insights_agent,
                expected_output="Strategic recommendations in JSON format"
            )
            
            # Create crew
            crew = Crew(
                agents=[analytics_agent, insights_agent],
                tasks=[analysis_task, recommendations_task],
                verbose=True
            )
            
            # Execute
            result = crew.kickoff()
            
            return {
                "analysis_timestamp": datetime.now().isoformat(),
                "performance_data": analytics_data,
                "analysis_result": str(result)
            }
        except Exception as e:
            print(f"Warning: AI analysis failed ({str(e)}), using basic analysis")
            return self._generate_basic_analysis(analytics_data)
    
    def _generate_basic_analysis(self, analytics_data: Dict) -> Dict:
        """Generate basic analysis without AI"""
        return {
            "analysis_timestamp": datetime.now().isoformat(),
            "performance_data": analytics_data,
            "analysis_type": "basic",
            "summary": "Campaign performance analysis generated"
        }
    
    def track_performance(self, campaign_id: str, metrics: Dict) -> None:
        """Store performance tracking data"""
        self.performance_data[campaign_id] = {
            "tracked_at": datetime.now().isoformat(),
            "metrics": metrics
        }
    
    def get_performance_summary(self, campaign_id: str) -> Dict:
        """Get performance summary for a campaign"""
        return self.performance_data.get(campaign_id, {})
    
    def generate_performance_report(self, analytics: Dict) -> str:
        """Generate a text-based performance report"""
        report = "\n" + "=" * 80 + "\n"
        report += "📊 CAMPAIGN PERFORMANCE REPORT\n"
        report += "=" * 80 + "\n\n"
        
        report += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        for platform, data in analytics.items():
            report += f"\n📱 {platform}\n"
            report += "-" * 40 + "\n"
            report += f"  Posts:             {data.get('posts_count', 0)}\n"
            report += f"  Total Reach:       {data.get('total_reach', 0):,}\n"
            report += f"  Engagements:       {data.get('total_engagements', 0):,}\n"
            report += f"  Engagement Rate:   {data.get('avg_engagement_rate', 0):.2f}%\n"
            report += f"  Clicks:            {data.get('total_clicks', 0):,}\n"
            report += f"  CTR:               {data.get('ctr', 0):.2f}%\n"
            report += f"  Conversions:       {data.get('total_conversions', 0):,}\n"
            if data.get('total_clicks', 0) > 0:
                report += f"  Conv. Rate:        {data.get('conversion_rate', 0):.2f}%\n"
        
        # Overall summary
        total_reach = sum(data.get('total_reach', 0) for data in analytics.values())
        total_engagements = sum(data.get('total_engagements', 0) for data in analytics.values())
        total_conversions = sum(data.get('total_conversions', 0) for data in analytics.values())
        
        report += "\n\n📈 OVERALL SUMMARY\n"
        report += "-" * 40 + "\n"
        report += f"  Total Reach:       {total_reach:,}\n"
        report += f"  Total Engagements: {total_engagements:,}\n"
        report += f"  Total Conversions: {total_conversions:,}\n"
        if total_reach > 0:
            report += f"  Avg Engagement %:  {(total_engagements/total_reach*100):.2f}%\n"
        
        report += "\n" + "=" * 80 + "\n"
        
        return report
    
    def save_report(self, report: str, filename: str) -> None:
        """Save report to file"""
        with open(filename, 'w') as f:
            f.write(report)
        print(f"✓ Report saved to {filename}")


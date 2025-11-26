#!/usr/bin/env python3
"""
Main Entry Point for Agentic AI Campaign Planner & Executioner POC
Provides both CLI and programmatic interfaces for campaign management
"""

import os
import sys
import json
import argparse
from typing import List, Dict
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.orchestrator import CampaignOrchestrator
from src.calendar_manager import CampaignCalendar
from src.campaign_executor import CampaignExecutor
from src.performance_tracker import PerformanceAnalyzer


def load_env():
    """Load environment variables"""
    env_path = Path(__file__).parent / '.env'
    if env_path.exists():
        load_dotenv(env_path)
    return os.getenv('OPENAI_API_KEY')


def demo_campaign_1():
    """Run demo: Tech Product Launch Campaign"""
    print("\n" + "🎬 " * 20)
    print("DEMO 1: TECH PRODUCT LAUNCH CAMPAIGN")
    print("🎬 " * 20)
    
    api_key = load_env()
    orchestrator = CampaignOrchestrator(api_key=api_key)
    
    result = orchestrator.run_complete_workflow(
        campaign_name="AI-Powered CRM Launch 2024",
        target_audience="Enterprise SaaS buyers and IT decision makers",
        campaign_goal="Generate awareness and drive product demo signups",
        platforms=["LinkedIn", "Twitter", "Facebook"],
        budget="$5,000"
    )
    
    return result


def demo_campaign_2():
    """Run demo: E-commerce Holiday Campaign"""
    print("\n" + "🎬 " * 20)
    print("DEMO 2: E-COMMERCE HOLIDAY CAMPAIGN")
    print("🎬 " * 20)
    
    api_key = load_env()
    orchestrator = CampaignOrchestrator(api_key=api_key)
    
    result = orchestrator.run_complete_workflow(
        campaign_name="Holiday Shopping Extravaganza 2024",
        target_audience="Online shoppers ages 25-55, interested in fashion and tech",
        campaign_goal="Maximize holiday sales and increase customer retention",
        platforms=["Instagram", "TikTok", "Facebook", "Twitter"],
        budget="$8,000"
    )
    
    return result


def interactive_campaign():
    """Run interactive campaign creation"""
    print("\n" + "=" * 80)
    print("INTERACTIVE CAMPAIGN CREATION")
    print("=" * 80)
    
    campaign_name = input("\n📝 Campaign Name: ").strip()
    target_audience = input("👥 Target Audience: ").strip()
    campaign_goal = input("🎯 Campaign Goal: ").strip()
    budget = input("💰 Budget: ").strip()
    
    print("\n📱 Available Platforms:")
    print("  1. LinkedIn")
    print("  2. Twitter")
    print("  3. Instagram")
    print("  4. Facebook")
    print("  5. TikTok")
    
    platforms_input = input("\nSelect platforms (comma-separated numbers, e.g., 1,3,4): ").strip()
    platform_map = {
        "1": "LinkedIn",
        "2": "Twitter",
        "3": "Instagram",
        "4": "Facebook",
        "5": "TikTok"
    }
    
    platforms = []
    for num in platforms_input.split(","):
        num = num.strip()
        if num in platform_map:
            platforms.append(platform_map[num])
    
    if not platforms:
        print("❌ No valid platforms selected")
        return None
    
    api_key = load_env()
    orchestrator = CampaignOrchestrator(api_key=api_key)
    
    result = orchestrator.run_complete_workflow(
        campaign_name=campaign_name,
        target_audience=target_audience,
        campaign_goal=campaign_goal,
        platforms=platforms,
        budget=budget
    )
    
    return result


def show_quick_example():
    """Show quick example without AI agents (for demo purposes)"""
    print("\n" + "=" * 80)
    print("⚡ QUICK EXAMPLE (No API Key Required)")
    print("=" * 80)
    
    orchestrator = CampaignOrchestrator()
    
    # Create campaign plan
    campaign_plan = orchestrator.plan_campaign(
        campaign_name="Social Media Awareness Campaign",
        target_audience="Tech enthusiasts and startups",
        campaign_goal="Build brand awareness and drive website traffic",
        platforms=["LinkedIn", "Twitter", "Instagram"],
        budget="$3,000",
        duration_days=14
    )
    
    print("\n📋 Campaign Plan:")
    print(json.dumps({
        "name": campaign_plan["name"],
        "audience": campaign_plan["target_audience"],
        "goal": campaign_plan["goal"],
        "platforms": campaign_plan["platforms"],
        "budget": campaign_plan["budget"]
    }, indent=2))
    
    # Schedule campaigns
    events = orchestrator.schedule_campaigns(campaign_plan["campaign_id"], frequency="daily")
    
    # Show calendar
    calendar_view = orchestrator.calendar.get_calendar_view()
    print(calendar_view)
    
    # Execute campaigns
    execution_result = orchestrator.execute_scheduled_campaigns()
    print(f"\n✅ Executed {execution_result['total_posts_executed']} posts")
    
    # Get analytics
    analytics = orchestrator.track_performance()
    
    print("\n📊 Performance Summary:")
    for platform, data in analytics.items():
        print(f"  {platform}:")
        print(f"    - Reach: {data.get('total_reach', 0):,}")
        print(f"    - Engagements: {data.get('total_engagements', 0):,}")
        print(f"    - Conversion Rate: {data.get('conversion_rate', 0):.2f}%")
    
    # Generate report
    report = orchestrator.generate_performance_report()
    print(report)
    
    # Export calendar
    calendar_export_path = orchestrator.export_calendar()
    
    return {
        "campaign": campaign_plan,
        "events_scheduled": len(events),
        "posts_executed": execution_result['total_posts_executed'],
        "analytics": analytics,
        "calendar_export": calendar_export_path
    }


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Agentic AI Campaign Planner & Executioner POC"
    )
    
    parser.add_argument(
        "mode",
        nargs="?",
        choices=["demo1", "demo2", "interactive", "quick"],
        default="quick",
        help="Run mode: demo1, demo2, interactive, or quick (default)"
    )
    
    parser.add_argument(
        "--api-key",
        help="OpenAI API key (or set OPENAI_API_KEY env variable)"
    )
    
    args = parser.parse_args()
    
    print("\n" + "🤖 " * 30)
    print("AGENTIC AI CAMPAIGN PLANNER & EXECUTIONER")
    print("POC Demo - December 2, 2024")
    print("🤖 " * 30)
    
    try:
        if args.mode == "demo1":
            result = demo_campaign_1()
        elif args.mode == "demo2":
            result = demo_campaign_2()
        elif args.mode == "interactive":
            result = interactive_campaign()
        else:  # quick
            result = show_quick_example()
        
        if result:
            print("\n" + "=" * 80)
            print("WORKFLOW SUMMARY")
            print("=" * 80)
            print(json.dumps(result, indent=2, default=str))
        
        print("\n✅ Campaign execution completed successfully!")
        print("📁 Check the outputs/ folder for generated reports and calendars")
        
    except KeyboardInterrupt:
        print("\n\n❌ Campaign execution cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        if "--debug" in sys.argv:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

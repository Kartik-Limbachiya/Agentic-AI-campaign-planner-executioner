"""
Agentic AI Campaign Planner & Executioner
A POC for autonomous social media campaign management using AI agents
"""

__version__ = "1.0.0"
__author__ = "Kartik Limbachiya"

from .orchestrator import CampaignOrchestrator
from .calendar_manager import CampaignCalendar, CampaignEvent, Platform
from .campaign_executor import CampaignExecutor
from .performance_tracker import PerformanceAnalyzer

__all__ = [
    "CampaignOrchestrator",
    "CampaignCalendar",
    "CampaignEvent",
    "Platform",
    "CampaignExecutor",
    "PerformanceAnalyzer"
]

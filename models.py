from dataclasses import dataclass
from typing import List, Optional, Dict
from datetime import datetime

@dataclass
class Scholarship:
    id: str
    title: str
    provider: str
    description: str
    amount: float
    deadline: datetime
    field_of_study: List[str]
    degree_level: str  # undergraduate, postgraduate, phd
    eligibility_criteria: Dict
    application_url: str
    country: str
    gpa_requirement: Optional[float] = None
    
@dataclass
class StudentProfile:
    name: str
    field_of_study: str
    degree_level: str
    gpa: float
    country: str
    financial_need: str
    achievements: List[str]
    interests: List[str] 
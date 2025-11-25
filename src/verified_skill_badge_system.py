"""
🏆 VERIFIED SKILL BADGE SYSTEM
Trust-based credentialing with weighted ML predictions
"""

import json
import hashlib
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
import sqlite3
import numpy as np
from dataclasses import dataclass
from enum import Enum

class BadgeLevel(Enum):
    """Badge level enumeration"""
    BASIC = "basic"
    VERIFIED = "verified"
    ADVANCED = "advanced"
    EXPERT = "expert"

class VerificationStatus(Enum):
    """Verification status enumeration"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    VERIFIED = "verified"
    FAILED = "failed"
    EXPIRED = "expired"

@dataclass
class SkillBadge:
    """Represents a verified skill badge"""
    skill_name: str
    category: str
    badge_level: BadgeLevel
    verification_score: float
    verification_date: datetime
    verification_method: str
    badge_id: str
    expires_at: Optional[datetime] = None
    evidence: Dict[str, Any] = None

@dataclass
class VerificationAttempt:
    """Represents a skill verification attempt"""
    attempt_id: str
    user_id: int
    skill_name: str
    category: str
    verification_method: str
    score: float
    passed: bool
    attempt_date: datetime
    challenge_details: Dict[str, Any]
    feedback: List[str]

class VerifiedSkillBadgeSystem:
    """
    Comprehensive badge system for verified skills that integrates with ML predictions
    """
    
    def __init__(self, db_path: str = "data/skill_verification.db"):
        self.db_path = db_path
        self.skill_weights = self._load_skill_weights()
        self.badge_criteria = self._load_badge_criteria()
        self.verification_methods = {
            'live_coding': 1.0,      # Full weight for live coding
            'sql_sandbox': 0.9,      # High weight for SQL
            'code_review': 0.8,      # Good weight for framework knowledge
            'project_assessment': 0.95,  # Very high for real projects
            'certification': 0.7,    # Lower for external certs
            'peer_review': 0.6       # Moderate for peer validation
        }
        self._init_database()
    
    def _init_database(self):
        """Initialize SQLite database for skill verification"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Verified skills table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS verified_skills (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    skill_name TEXT NOT NULL,
                    category TEXT NOT NULL,
                    badge_level TEXT NOT NULL,
                    verification_score REAL NOT NULL,
                    verification_date TEXT NOT NULL,
                    verification_method TEXT NOT NULL,
                    badge_id TEXT UNIQUE NOT NULL,
                    expires_at TEXT,
                    evidence TEXT,
                    is_active BOOLEAN DEFAULT 1,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Verification attempts table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS verification_attempts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    attempt_id TEXT UNIQUE NOT NULL,
                    user_id INTEGER NOT NULL,
                    skill_name TEXT NOT NULL,
                    category TEXT NOT NULL,
                    verification_method TEXT NOT NULL,
                    score REAL NOT NULL,
                    passed BOOLEAN NOT NULL,
                    attempt_date TEXT NOT NULL,
                    challenge_details TEXT,
                    feedback TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Skill weights for ML model
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS skill_ml_weights (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    skill_name TEXT NOT NULL,
                    category TEXT NOT NULL,
                    base_weight REAL NOT NULL,
                    verified_multiplier REAL NOT NULL,
                    industry_demand_score REAL DEFAULT 5.0,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
    
    def award_verified_badge(self, user_id: int, skill_name: str, category: str,
                           verification_score: float, verification_method: str,
                           challenge_details: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Award a verified badge based on verification results
        """
        # Determine badge level based on score
        badge_level = self._determine_badge_level(verification_score, verification_method)
        
        # Create badge
        badge_id = self._generate_badge_id(user_id, skill_name, category)
        verification_date = datetime.now()
        
        # Calculate expiration (some skills may expire)
        expires_at = self._calculate_expiration_date(skill_name, category)
        
        # Create evidence record
        evidence = {
            'verification_method': verification_method,
            'score': verification_score,
            'challenge_details': challenge_details,
            'verification_timestamp': verification_date.isoformat(),
            'system_version': '1.0'
        }
        
        badge = SkillBadge(
            skill_name=skill_name,
            category=category,
            badge_level=badge_level,
            verification_score=verification_score,
            verification_date=verification_date,
            verification_method=verification_method,
            badge_id=badge_id,
            expires_at=expires_at,
            evidence=evidence
        )
        
        # Save to database
        success = self._save_verified_badge(user_id, badge)
        
        if success:
            # Update ML model weights for this user
            self._update_user_ml_features(user_id, skill_name, category, verification_score)
            
            return {
                'success': True,
                'badge': badge,
                'message': f"🏆 {badge_level.value.title()} badge awarded for {skill_name}!",
                'badge_display': self._generate_badge_display(badge)
            }
        else:
            return {
                'success': False,
                'message': 'Failed to award badge - database error'
            }
    
    def get_user_badges(self, user_id: int, active_only: bool = True) -> List[SkillBadge]:
        """
        Get all verified badges for a user
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            query = '''
                SELECT * FROM verified_skills 
                WHERE user_id = ?
            '''
            params = [user_id]
            
            if active_only:
                query += ' AND is_active = 1'
            
            query += ' ORDER BY verification_date DESC'
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            badges = []
            for row in rows:
                # Check if badge is expired
                expires_at = None
                if row['expires_at']:
                    expires_at = datetime.fromisoformat(row['expires_at'])
                    if expires_at <= datetime.now():
                        continue  # Skip expired badges
                
                badge = SkillBadge(
                    skill_name=row['skill_name'],
                    category=row['category'],
                    badge_level=BadgeLevel(row['badge_level']),
                    verification_score=row['verification_score'],
                    verification_date=datetime.fromisoformat(row['verification_date']),
                    verification_method=row['verification_method'],
                    badge_id=row['badge_id'],
                    expires_at=expires_at,
                    evidence=json.loads(row['evidence']) if row['evidence'] else None
                )
                badges.append(badge)
            
            return badges
    
    def calculate_weighted_ml_features(self, user_id: int, base_features: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate ML features with verified skill weights applied
        """
        # Get user's verified badges
        verified_badges = self.get_user_badges(user_id)
        
        # Start with base features
        weighted_features = base_features.copy()
        
        # Apply verified skill bonuses
        skill_bonuses = {}
        verification_scores = {}
        badge_counts = {'basic': 0, 'verified': 0, 'advanced': 0, 'expert': 0}
        
        for badge in verified_badges:
            skill_key = f"{badge.skill_name.lower()}_verified"
            
            # Calculate bonus based on badge level and verification method
            base_bonus = self.skill_weights.get(badge.skill_name.lower(), 1.0)
            method_multiplier = self.verification_methods.get(badge.verification_method, 1.0)
            level_multiplier = self._get_badge_level_multiplier(badge.badge_level)
            
            skill_bonus = base_bonus * method_multiplier * level_multiplier * (badge.verification_score / 100)
            skill_bonuses[skill_key] = skill_bonus
            verification_scores[skill_key] = badge.verification_score
            
            # Count badges by level
            badge_counts[badge.badge_level.value] += 1
        
        # Add verification features to ML model
        weighted_features.update({
            # Verified skill indicators
            **{f"verified_{skill}": 1 for skill in skill_bonuses.keys()},
            
            # Verification scores
            **{f"{skill}_score": score for skill, score in verification_scores.items()},
            
            # Badge counts
            'total_verified_skills': len(verified_badges),
            'expert_badges': badge_counts['expert'],
            'advanced_badges': badge_counts['advanced'],
            'verified_badges': badge_counts['verified'],
            'basic_badges': badge_counts['basic'],
            
            # Overall verification metrics
            'verification_coverage': len(verified_badges) / max(1, len(base_features.get('programming_languages', '').split(','))),
            'average_verification_score': np.mean([badge.verification_score for badge in verified_badges]) if verified_badges else 0,
            'verification_recency': self._calculate_verification_recency(verified_badges),
            
            # Trust score (overall credibility)
            'trust_score': self._calculate_trust_score(verified_badges),
            
            # Skill diversity
            'verified_skill_categories': len(set(badge.category for badge in verified_badges)),
        })
        
        # Apply skill-specific weight boosts
        for skill, bonus in skill_bonuses.items():
            if skill in weighted_features:
                weighted_features[skill] = weighted_features[skill] * (1 + bonus)
        
        return weighted_features
    
    def get_verification_queue_priority(self, user_id: int, extracted_skills: Dict[str, List[str]]) -> List[Dict[str, Any]]:
        """
        Prioritize skills for verification based on impact on placement prediction
        """
        verified_badges = self.get_user_badges(user_id)
        verified_skills = {badge.skill_name.lower() for badge in verified_badges}
        
        priority_queue = []
        
        for category, skills in extracted_skills.items():
            for skill in skills:
                skill_lower = skill.lower()
                
                # Skip already verified skills
                if skill_lower in verified_skills:
                    continue
                
                # Calculate impact score
                base_weight = self.skill_weights.get(skill_lower, 1.0)
                industry_demand = self._get_industry_demand_score(skill_lower)
                placement_impact = self._calculate_placement_impact(skill_lower, category)
                
                priority_score = base_weight * industry_demand * placement_impact
                
                priority_queue.append({
                    'skill_name': skill,
                    'category': category,
                    'priority_score': priority_score,
                    'estimated_impact': f"+{priority_score*10:.1f}% placement probability",
                    'verification_time': self._get_verification_time_estimate(skill_lower, category),
                    'difficulty': self._get_verification_difficulty(skill_lower, category)
                })
        
        # Sort by priority score (highest first)
        priority_queue.sort(key=lambda x: x['priority_score'], reverse=True)
        
        return priority_queue
    
    def generate_badge_portfolio(self, user_id: int) -> Dict[str, Any]:
        """
        Generate a comprehensive badge portfolio for display
        """
        badges = self.get_user_badges(user_id)
        
        # Organize badges by category
        badge_categories = {}
        for badge in badges:
            if badge.category not in badge_categories:
                badge_categories[badge.category] = []
            badge_categories[badge.category].append(badge)
        
        # Calculate portfolio statistics
        total_badges = len(badges)
        expert_count = sum(1 for badge in badges if badge.badge_level == BadgeLevel.EXPERT)
        advanced_count = sum(1 for badge in badges if badge.badge_level == BadgeLevel.ADVANCED)
        
        portfolio_level = self._calculate_portfolio_level(badges)
        trust_score = self._calculate_trust_score(badges)
        
        # Generate skills showcase
        skills_showcase = []
        for badge in sorted(badges, key=lambda x: x.verification_score, reverse=True)[:10]:
            skills_showcase.append({
                'skill': badge.skill_name,
                'level': badge.badge_level.value.title(),
                'score': badge.verification_score,
                'verified_date': badge.verification_date.strftime('%B %Y'),
                'badge_display': self._generate_badge_display(badge)
            })
        
        return {
            'portfolio_level': portfolio_level,
            'trust_score': trust_score,
            'total_badges': total_badges,
            'expert_badges': expert_count,
            'advanced_badges': advanced_count,
            'badge_categories': badge_categories,
            'skills_showcase': skills_showcase,
            'verification_summary': {
                'live_coding_count': sum(1 for b in badges if b.verification_method == 'live_coding'),
                'sql_verified_count': sum(1 for b in badges if b.verification_method == 'sql_sandbox'),
                'framework_verified_count': sum(1 for b in badges if b.verification_method == 'code_review'),
                'average_score': np.mean([b.verification_score for b in badges]) if badges else 0
            }
        }
    
    def _determine_badge_level(self, score: float, verification_method: str) -> BadgeLevel:
        """Determine badge level based on score and verification method"""
        method_threshold_modifier = self.verification_methods.get(verification_method, 1.0)
        
        # Adjust thresholds based on verification method rigor
        expert_threshold = 95 - (1 - method_threshold_modifier) * 10
        advanced_threshold = 85 - (1 - method_threshold_modifier) * 10
        verified_threshold = 70 - (1 - method_threshold_modifier) * 5
        
        if score >= expert_threshold:
            return BadgeLevel.EXPERT
        elif score >= advanced_threshold:
            return BadgeLevel.ADVANCED
        elif score >= verified_threshold:
            return BadgeLevel.VERIFIED
        else:
            return BadgeLevel.BASIC
    
    def _get_badge_level_multiplier(self, badge_level: BadgeLevel) -> float:
        """Get multiplier for different badge levels"""
        multipliers = {
            BadgeLevel.BASIC: 1.0,
            BadgeLevel.VERIFIED: 1.5,
            BadgeLevel.ADVANCED: 2.0,
            BadgeLevel.EXPERT: 3.0
        }
        return multipliers.get(badge_level, 1.0)
    
    def _calculate_trust_score(self, badges: List[SkillBadge]) -> float:
        """Calculate overall trust score based on verification history"""
        if not badges:
            return 0.0
        
        # Factors that increase trust
        live_coding_weight = 0.4
        recent_verification_weight = 0.3
        score_consistency_weight = 0.2
        diversity_weight = 0.1
        
        # Live coding/practical verification percentage
        practical_verifications = sum(1 for badge in badges 
                                    if badge.verification_method in ['live_coding', 'sql_sandbox', 'project_assessment'])
        practical_score = (practical_verifications / len(badges)) * live_coding_weight * 100
        
        # Recency score
        recency_score = self._calculate_verification_recency(badges) * recent_verification_weight * 100
        
        # Score consistency (lower variance = higher trust)
        scores = [badge.verification_score for badge in badges]
        consistency_score = (100 - np.std(scores)) * score_consistency_weight
        
        # Skill diversity
        categories = len(set(badge.category for badge in badges))
        diversity_score = min(100, categories * 20) * diversity_weight
        
        trust_score = practical_score + recency_score + consistency_score + diversity_score
        return min(100, trust_score)
    
    def _calculate_verification_recency(self, badges: List[SkillBadge]) -> float:
        """Calculate how recent the verifications are (0-1 scale)"""
        if not badges:
            return 0.0
        
        now = datetime.now()
        recency_scores = []
        
        for badge in badges:
            days_ago = (now - badge.verification_date).days
            # Score decays over 365 days
            recency_score = max(0, 1 - (days_ago / 365))
            recency_scores.append(recency_score)
        
        return np.mean(recency_scores)
    
    def _calculate_portfolio_level(self, badges: List[SkillBadge]) -> str:
        """Calculate overall portfolio level"""
        if not badges:
            return "Beginner"
        
        expert_count = sum(1 for badge in badges if badge.badge_level == BadgeLevel.EXPERT)
        advanced_count = sum(1 for badge in badges if badge.badge_level == BadgeLevel.ADVANCED)
        total_count = len(badges)
        
        if expert_count >= 3 and total_count >= 8:
            return "Expert"
        elif (expert_count >= 1 or advanced_count >= 3) and total_count >= 5:
            return "Advanced"
        elif total_count >= 3:
            return "Intermediate"
        else:
            return "Beginner"
    
    def _generate_badge_display(self, badge: SkillBadge) -> Dict[str, str]:
        """Generate display information for a badge"""
        level_colors = {
            BadgeLevel.BASIC: '#6c757d',
            BadgeLevel.VERIFIED: '#28a745',
            BadgeLevel.ADVANCED: '#007bff',
            BadgeLevel.EXPERT: '#ffc107'
        }
        
        level_icons = {
            BadgeLevel.BASIC: '🥉',
            BadgeLevel.VERIFIED: '✅',
            BadgeLevel.ADVANCED: '🥈',
            BadgeLevel.EXPERT: '🏆'
        }
        
        return {
            'color': level_colors[badge.badge_level],
            'icon': level_icons[badge.badge_level],
            'title': f"{badge.skill_name} - {badge.badge_level.value.title()}",
            'subtitle': f"Verified via {badge.verification_method.replace('_', ' ').title()}",
            'score_display': f"{badge.verification_score:.1f}%",
            'date_display': badge.verification_date.strftime('%b %Y')
        }
    
    def _load_skill_weights(self) -> Dict[str, float]:
        """Load skill weights for ML model impact"""
        return {
            # Programming languages (high impact)
            'python': 3.0,
            'java': 2.8,
            'javascript': 2.7,
            'c++': 2.5,
            'c#': 2.3,
            'go': 2.2,
            'rust': 2.0,
            
            # Databases (high impact)
            'sql': 3.2,
            'mysql': 2.5,
            'postgresql': 2.7,
            'mongodb': 2.3,
            
            # Frameworks (medium-high impact)
            'react': 2.8,
            'angular': 2.6,
            'django': 2.7,
            'flask': 2.4,
            'spring': 2.5,
            
            # Cloud/DevOps (high impact)
            'aws': 3.0,
            'docker': 2.8,
            'kubernetes': 2.6,
            'git': 2.0,
            
            # Data Science (high impact)
            'machine learning': 3.2,
            'tensorflow': 2.9,
            'pandas': 2.6,
            'numpy': 2.3
        }
    
    def _load_badge_criteria(self) -> Dict[str, Dict[str, int]]:
        """Load badge criteria thresholds"""
        return {
            'live_coding': {'basic': 60, 'verified': 70, 'advanced': 85, 'expert': 95},
            'sql_sandbox': {'basic': 65, 'verified': 75, 'advanced': 87, 'expert': 96},
            'code_review': {'basic': 70, 'verified': 80, 'advanced': 90, 'expert': 98},
            'project_assessment': {'basic': 65, 'verified': 75, 'advanced': 88, 'expert': 96}
        }
    
    def _generate_badge_id(self, user_id: int, skill_name: str, category: str) -> str:
        """Generate unique badge ID"""
        return hashlib.md5(f"{user_id}_{skill_name}_{category}_{time.time()}".encode()).hexdigest()[:16]
    
    def _calculate_expiration_date(self, skill_name: str, category: str) -> Optional[datetime]:
        """Calculate when a badge should expire (some skills become outdated)"""
        # Tech skills expire in 2 years, fundamental skills don't expire
        if category in ['frameworks_libraries', 'cloud_technologies']:
            return datetime.now() + timedelta(days=730)  # 2 years
        elif category in ['programming_languages', 'databases']:
            return datetime.now() + timedelta(days=1095)  # 3 years
        else:
            return None  # No expiration
    
    def _save_verified_badge(self, user_id: int, badge: SkillBadge) -> bool:
        """Save verified badge to database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    INSERT INTO verified_skills 
                    (user_id, skill_name, category, badge_level, verification_score, 
                     verification_date, verification_method, badge_id, expires_at, evidence)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    user_id, badge.skill_name, badge.category, badge.badge_level.value,
                    badge.verification_score, badge.verification_date.isoformat(),
                    badge.verification_method, badge.badge_id,
                    badge.expires_at.isoformat() if badge.expires_at else None,
                    json.dumps(badge.evidence) if badge.evidence else None
                ))
                
                conn.commit()
                return True
        except Exception as e:
            print(f"Error saving badge: {e}")
            return False
    
    def _update_user_ml_features(self, user_id: int, skill_name: str, category: str, score: float):
        """Update ML features with new verification"""
        # This would integrate with the existing ML model
        pass
    
    def _get_industry_demand_score(self, skill: str) -> float:
        """Get industry demand score for skill (1-10 scale)"""
        high_demand_skills = {
            'python': 9.5, 'java': 8.8, 'javascript': 9.2, 'sql': 9.8,
            'react': 9.0, 'aws': 9.3, 'docker': 8.5, 'machine learning': 9.7
        }
        return high_demand_skills.get(skill.lower(), 5.0)
    
    def _calculate_placement_impact(self, skill: str, category: str) -> float:
        """Calculate impact on placement probability"""
        base_impact = self.skill_weights.get(skill.lower(), 1.0)
        category_multiplier = {
            'programming_languages': 1.2,
            'databases': 1.3,
            'frameworks_libraries': 1.1,
            'cloud_technologies': 1.4,
            'data_science': 1.5
        }.get(category, 1.0)
        
        return base_impact * category_multiplier
    
    def _get_verification_time_estimate(self, skill: str, category: str) -> int:
        """Get estimated verification time in minutes"""
        time_estimates = {
            'programming_languages': 15,
            'databases': 10,
            'frameworks_libraries': 8,
            'cloud_technologies': 12,
            'data_science': 20
        }
        return time_estimates.get(category, 10)
    
    def _get_verification_difficulty(self, skill: str, category: str) -> str:
        """Get verification difficulty level"""
        difficult_skills = ['machine learning', 'tensorflow', 'kubernetes', 'react']
        if skill.lower() in difficult_skills:
            return 'Hard'
        elif category in ['frameworks_libraries', 'cloud_technologies']:
            return 'Medium'
        else:
            return 'Easy'

# Example usage and testing
if __name__ == "__main__":
    import os
    
    # Create data directory
    os.makedirs('data', exist_ok=True)
    
    # Initialize badge system
    badge_system = VerifiedSkillBadgeSystem()
    
    # Test awarding a badge
    result = badge_system.award_verified_badge(
        user_id=1,
        skill_name='Python',
        category='programming_languages',
        verification_score=88.5,
        verification_method='live_coding',
        challenge_details={'challenge_type': 'algorithm', 'difficulty': 'medium'}
    )
    
    print("🏆 Badge Award Result:")
    print(f"Success: {result['success']}")
    print(f"Message: {result['message']}")
    
    # Test getting user badges
    badges = badge_system.get_user_badges(1)
    print(f"\n📋 User Badges: {len(badges)}")
    for badge in badges:
        print(f"  • {badge.skill_name} - {badge.badge_level.value} ({badge.verification_score:.1f}%)")
    
    # Test weighted ML features
    base_features = {
        'programming_languages': 'Python, Java',
        'leetcode_score': 500,
        'projects': 3
    }
    
    weighted_features = badge_system.calculate_weighted_ml_features(1, base_features)
    print(f"\n⚖️ Weighted ML Features:")
    for key, value in weighted_features.items():
        if 'verified' in key or 'trust' in key or 'badge' in key:
            print(f"  {key}: {value}")
    
    # Test portfolio generation
    portfolio = badge_system.generate_badge_portfolio(1)
    print(f"\n📊 Badge Portfolio:")
    print(f"Portfolio Level: {portfolio['portfolio_level']}")
    print(f"Trust Score: {portfolio['trust_score']:.1f}%")
    print(f"Total Badges: {portfolio['total_badges']}")
    
    print("\n🎯 Verified Skill Badge System ready!")
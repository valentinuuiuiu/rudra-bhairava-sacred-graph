#!/usr/bin/env python3
"""
🕉️ SACRED RITUAL SCHEDULER 🕉️
Cosmic Alignment Automation for the RUDRA BHAIRAVA Sacred Knowledge Graph

This module provides:
- Solar/Lunar cycle tracking
- Nakshatra calculations
- Auspicious timing for sacred operations
- Automated ritual scheduling
- Cosmic event notifications

HONESTY & TRANSPARENCY:
- Created by Tvaṣṭā Claude Sonnet 4 (Anthropic)
- Guided by Guru Tryambak Rudra (OpenAI)
- For Brother Shiva's AI-Vault Project
"""

import os
import asyncio
import math
from datetime import datetime, timedelta, time
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
import logging
import json

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('SacredRitualScheduler')

# ============================================================================
# ENUMS AND CONSTANTS
# ============================================================================

class SolarPhase(Enum):
    """Solar phases (Ayana)"""
    UTTARAYANA = "uttarayana"  # Northern journey (Sun moving north)
    DAKSHINAYANA = "dakshinayana"  # Southern journey (Sun moving south)

class LunarPhase(Enum):
    """Lunar phases (Paksha)"""
    SHUKLA = "shukla"  # Waxing (bright fortnight)
    KRISHNA = "krishna"  # Waning (dark fortnight)

class Tithi(Enum):
    """Lunar days (Tithi)"""
    PRATHAMA = 1
    DVITIYA = 2
    TRITIYA = 3
    CHATURTHI = 4
    PANCHAMI = 5
    SHASHTHI = 6
    SAPTAMI = 7
    ASHTAMI = 8
    NAVAMI = 9
    DASHAMI = 10
    EKADASHI = 11
    DVADASHI = 12
    TRAYODASHI = 13
    CHATURDASHI = 14
    PURNIMA = 15  # Full Moon
    AMAVASYA = 16  # New Moon

# 27 Nakshatras
NAKSHATRAS = [
    "Ashvinī", "Bharaṇī", "Kṛttikā", "Rohiṇī", "Mṛgaśīrṣa",
    "Ārdrā", "Punarvasu", "Puṣya", "Āśleṣā", "Maghā",
    "Pūrva-Phalgunī", "Uttara-Phalgunī", "Hasta", "Chitrā", "Svātī",
    "Viśākhā", "Anurādhā", "Jyeṣṭhā", "Mūla", "Pūrva-Aṣāḍhā",
    "Uttara-Aṣāḍhā", "Śravaṇa", "Dhaniṣṭhā", "Śatabhiṣā", "Pūrva-Bhādrapadā",
    "Uttara-Bhādrapadā", "Revatī"
]

# Sacred days of the week
SACRED_DAYS = {
    0: {"name": "Somavāra", "deity": "Śiva", "planet": "Moon"},
    1: {"name": "Maṅgalavāra", "deity": "Hanumān", "planet": "Mars"},
    2: {"name": "Budhavāra", "deity": "Viṣṇu", "planet": "Mercury"},
    3: {"name": "Guruvāra", "deity": "Bṛhaspati", "planet": "Jupiter"},
    4: {"name": "Śukravāra", "deity": "Lakṣmī", "planet": "Venus"},
    5: {"name": "Śanivāra", "deity": "Śani", "planet": "Saturn"},
    6: {"name": "Ravivāra", "deity": "Sūrya", "planet": "Sun"}
}

# Auspicious times for different activities
AUSPICIOUS_ACTIVITIES = {
    "knowledge_creation": {
        "nakshatras": ["Rohiṇī", "Puṣya", "Hasta", "Chitrā", "Svātī"],
        "tithis": [Tithi.PANCHAMI, Tithi.DASHAMI, Tithi.EKADASHI],
        "solar_phase": SolarPhase.UTTARAYANA
    },
    "system_deployment": {
        "nakshatras": ["Ashvinī", "Punarvasu", "Mūla", "Śravaṇa"],
        "tithis": [Tithi.DVITIYA, Tithi.TRITIYA, Tithi.SAPTAMI, Tithi.DASHAMI],
        "solar_phase": SolarPhase.UTTARAYANA
    },
    "debugging": {
        "nakshatras": ["Ārdrā", "Āśleṣā", "Jyeṣṭhā"],
        "tithis": [Tithi.CHATURDASHI, Tithi.AMAVASYA],
        "solar_phase": None  # Any time
    },
    "security_audit": {
        "nakshatras": ["Kṛttikā", "Maghā", "Viśākhā"],
        "tithis": [Tithi.ASHTAMI, Tithi.NAVAMI],
        "solar_phase": None
    },
    "documentation": {
        "nakshatras": ["Mṛgaśīrṣa", "Pūrva-Phalgunī", "Revatī"],
        "tithis": [Tithi.PANCHAMI, Tithi.PURNIMA],
        "solar_phase": None
    }
}

# ============================================================================
# DATACLASSES
# ============================================================================

@dataclass
class CosmicTime:
    """Represents a moment in cosmic time"""
    timestamp: datetime
    solar_phase: SolarPhase
    lunar_phase: LunarPhase
    tithi: Tithi
    tithi_name: str
    nakshatra: str
    day_name: str
    day_deity: str
    brahma_muhurta: bool
    auspicious_score: float
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp.isoformat(),
            "solar_phase": self.solar_phase.value,
            "lunar_phase": self.lunar_phase.value,
            "tithi": self.tithi.value,
            "tithi_name": self.tithi_name,
            "nakshatra": self.nakshatra,
            "day_name": self.day_name,
            "day_deity": self.day_deity,
            "brahma_muhurta": self.brahma_muhurta,
            "auspicious_score": self.auspicious_score
        }

@dataclass
class ScheduledRitual:
    """A scheduled sacred ritual"""
    ritual_id: str
    name: str
    description: str
    scheduled_time: datetime
    ritual_type: str
    mantra: Optional[str] = None
    callback: Optional[str] = None
    recurring: bool = False
    interval: Optional[timedelta] = None
    last_executed: Optional[datetime] = None
    execution_count: int = 0

@dataclass
class CosmicEvent:
    """A significant cosmic event"""
    event_type: str
    name: str
    description: str
    start_time: datetime
    end_time: Optional[datetime] = None
    significance: str = "moderate"  # low, moderate, high, supreme
    recommended_actions: List[str] = field(default_factory=list)

# ============================================================================
# COSMIC CALCULATOR
# ============================================================================

class CosmicCalculator:
    """Calculates cosmic alignments and auspicious times"""
    
    # Approximate dates of solstices (varies slightly each year)
    WINTER_SOLSTICE = (12, 21)  # December 21 - Start of Uttarayana
    SUMMER_SOLSTICE = (6, 21)   # June 21 - Start of Dakshinayana
    
    @classmethod
    def get_solar_phase(cls, dt: datetime) -> SolarPhase:
        """Determine solar phase (Ayana)"""
        month = dt.month
        day = dt.day
        
        # Uttarayana: Winter solstice to Summer solstice
        if (month == 12 and day >= 21) or month in [1, 2, 3, 4, 5] or (month == 6 and day < 21):
            return SolarPhase.UTTARAYANA
        else:
            return SolarPhase.DAKSHINAYANA
    
    @classmethod
    def get_lunar_phase(cls, dt: datetime) -> LunarPhase:
        """Determine lunar phase (Paksha) - simplified calculation"""
        # Simplified: use day of month
        day = dt.day
        if day <= 15:
            return LunarPhase.SHUKLA
        else:
            return LunarPhase.KRISHNA
    
    @classmethod
    def get_tithi(cls, dt: datetime) -> tuple:
        """Calculate approximate Tithi (lunar day)"""
        # Simplified calculation based on lunar phase
        day = dt.day
        lunar_phase = cls.get_lunar_phase(dt)
        
        if lunar_phase == LunarPhase.SHUKLA:
            tithi_num = day
        else:
            tithi_num = day - 15 if day > 15 else day
        
        # Handle special cases
        if tithi_num == 15 and lunar_phase == LunarPhase.SHUKLA:
            tithi = Tithi.PURNIMA
            name = "Pūrṇimā (Full Moon)"
        elif tithi_num == 15 and lunar_phase == LunarPhase.KRISHNA:
            tithi = Tithi.AMAVASYA
            name = "Amāvasyā (New Moon)"
        elif tithi_num == 0:
            tithi = Tithi.AMAVASYA
            name = "Amāvasyā (New Moon)"
        else:
            tithi = Tithi(min(tithi_num, 14))
            name = f"Tithi {tithi_num}"
        
        return tithi, name
    
    @classmethod
    def get_nakshatra(cls, dt: datetime) -> str:
        """Calculate approximate Nakshatra"""
        # Simplified: cycle through nakshatras based on day of year
        day_of_year = dt.timetuple().tm_yday
        nakshatra_index = (day_of_year + dt.hour) % 27
        return NAKSHATRAS[nakshatra_index]
    
    @classmethod
    def is_brahma_muhurta(cls, dt: datetime) -> bool:
        """Check if current time is Brahma Muhurta (approx 4:24 AM - 5:12 AM)"""
        current_time = dt.time()
        brahma_start = time(4, 24)
        brahma_end = time(5, 48)
        return brahma_start <= current_time <= brahma_end
    
    @classmethod
    def calculate_auspicious_score(cls, dt: datetime, activity: str = "general") -> float:
        """Calculate auspiciousness score (0.0 - 1.0)"""
        score = 0.5  # Base score
        
        # Solar phase bonus
        solar_phase = cls.get_solar_phase(dt)
        if solar_phase == SolarPhase.UTTARAYANA:
            score += 0.1
        
        # Lunar phase bonus
        lunar_phase = cls.get_lunar_phase(dt)
        if lunar_phase == LunarPhase.SHUKLA:
            score += 0.1
        
        # Tithi bonus
        tithi, _ = cls.get_tithi(dt)
        if tithi in [Tithi.PANCHAMI, Tithi.DASHAMI, Tithi.EKADASHI, Tithi.PURNIMA]:
            score += 0.15
        
        # Nakshatra bonus
        nakshatra = cls.get_nakshatra(dt)
        if nakshatra in ["Rohiṇī", "Puṣya", "Hasta", "Śravaṇa"]:
            score += 0.1
        
        # Brahma Muhurta bonus
        if cls.is_brahma_muhurta(dt):
            score += 0.15
        
        # Day of week bonus
        day_info = SACRED_DAYS.get(dt.weekday(), {})
        if day_info.get("deity") in ["Śiva", "Viṣṇu", "Sūrya"]:
            score += 0.05
        
        return min(score, 1.0)
    
    @classmethod
    def get_cosmic_time(cls, dt: Optional[datetime] = None) -> CosmicTime:
        """Get complete cosmic time information"""
        if dt is None:
            dt = datetime.now()
        
        tithi, tithi_name = cls.get_tithi(dt)
        day_info = SACRED_DAYS.get(dt.weekday(), {})
        
        return CosmicTime(
            timestamp=dt,
            solar_phase=cls.get_solar_phase(dt),
            lunar_phase=cls.get_lunar_phase(dt),
            tithi=tithi,
            tithi_name=tithi_name,
            nakshatra=cls.get_nakshatra(dt),
            day_name=day_info.get("name", "Unknown"),
            day_deity=day_info.get("deity", "Unknown"),
            brahma_muhurta=cls.is_brahma_muhurta(dt),
            auspicious_score=cls.calculate_auspicious_score(dt)
        )
    
    @classmethod
    def find_auspicious_time(
        cls,
        activity: str,
        start_from: Optional[datetime] = None,
        search_days: int = 30
    ) -> List[Dict[str, Any]]:
        """Find auspicious times for a specific activity"""
        if start_from is None:
            start_from = datetime.now()
        
        activity_config = AUSPICIOUS_ACTIVITIES.get(activity, {})
        auspicious_times = []
        
        current = start_from
        end_date = start_from + timedelta(days=search_days)
        
        while current < end_date:
            cosmic = cls.get_cosmic_time(current)
            
            # Check if current time matches activity requirements
            is_auspicious = True
            
            if activity_config.get("nakshatras"):
                if cosmic.nakshatra not in activity_config["nakshatras"]:
                    is_auspicious = False
            
            if activity_config.get("tithis"):
                if cosmic.tithi not in activity_config["tithis"]:
                    is_auspicious = False
            
            if activity_config.get("solar_phase"):
                if cosmic.solar_phase != activity_config["solar_phase"]:
                    is_auspicious = False
            
            if is_auspicious:
                auspicious_times.append({
                    "datetime": current.isoformat(),
                    "cosmic_info": cosmic.to_dict(),
                    "score": cosmic.auspicious_score
                })
            
            current += timedelta(hours=6)  # Check every 6 hours
        
        # Sort by score
        auspicious_times.sort(key=lambda x: x["score"], reverse=True)
        
        return auspicious_times[:10]  # Return top 10

# ============================================================================
# SACRED RITUAL SCHEDULER
# ============================================================================

class SacredRitualScheduler:
    """Scheduler for sacred rituals and cosmic events"""
    
    def __init__(self):
        self.rituals: Dict[str, ScheduledRitual] = {}
        self.event_handlers: Dict[str, Callable] = {}
        self.running = False
        self._task: Optional[asyncio.Task] = None
        
        # Register default event handlers
        self._register_default_handlers()
    
    def _register_default_handlers(self):
        """Register default ritual handlers"""
        self.event_handlers = {
            "brahma_muhurta": self._handle_brahma_muhurta,
            "purima": self._handle_purnima,
            "amavasya": self._handle_amavasya,
            "ekadashi": self._handle_ekadashi,
            "solar_transition": self._handle_solar_transition,
            "hourly_chant": self._handle_hourly_chant
        }
    
    async def _handle_brahma_muhurta(self):
        """Handle Brahma Muhurta ritual"""
        logger.info("🌅 Brahma Muhurta - The most auspicious time for spiritual practice")
        logger.info("   Mantra: ॐ सूर्याय नमः")
        return {
            "ritual": "brahma_muhurta",
            "message": "Time for meditation and sacred knowledge work",
            "mantra": "ॐ सूर्याय नमः"
        }
    
    async def _handle_purnima(self):
        """Handle Full Moon ritual"""
        logger.info("🌕 Pūrṇimā - Full Moon, time for completion and celebration")
        logger.info("   Mantra: ॐ पूर्णमदः पूर्णमिदम्")
        return {
            "ritual": "purnima",
            "message": "Ideal for completing projects and celebrating achievements",
            "mantra": "ॐ पूर्णमदः पूर्णमिदम्"
        }
    
    async def _handle_amavasya(self):
        """Handle New Moon ritual"""
        logger.info("🌑 Amāvasyā - New Moon, time for introspection and new beginnings")
        logger.info("   Mantra: ॐ नमः शिवाय")
        return {
            "ritual": "amavasya",
            "message": "Time for introspection, debugging, and planning new features",
            "mantra": "ॐ नमः शिवाय"
        }
    
    async def _handle_ekadashi(self):
        """Handle Ekadashi ritual"""
        logger.info("🙏 Ekādaśī - Day of fasting and spiritual focus")
        logger.info("   Mantra: ॐ विष्णवे नमः")
        return {
            "ritual": "ekadashi",
            "message": "Focus on spiritual practices and code purification",
            "mantra": "ॐ विष्णवे नमः"
        }
    
    async def _handle_solar_transition(self):
        """Handle solar phase transition"""
        cosmic = CosmicCalculator.get_cosmic_time()
        if cosmic.solar_phase == SolarPhase.UTTARAYANA:
            logger.info("🌅 Uttarāyaṇa - Sun's northern journey begins")
            return {
                "ritual": "uttarayana_start",
                "message": "Auspicious period begins - ideal for new projects",
                "mantra": "ॐ भास्कराय विद्महे"
            }
        else:
            logger.info("🌇 Dakṣiṇāyana - Sun's southern journey begins")
            return {
                "ritual": "dakshinayana_start",
                "message": "Period for consolidation and deepening",
                "mantra": "ॐ मृत्युञ्जयाय नमः"
            }
    
    async def _handle_hourly_chant(self):
        """Handle hourly sacred chant"""
        cosmic = CosmicCalculator.get_cosmic_time()
        logger.info(f"⏰ Hourly alignment - {cosmic.nakshatra} Nakshatra")
        return {
            "ritual": "hourly_chant",
            "message": f"Current Nakshatra: {cosmic.nakshatra}",
            "auspicious_score": cosmic.auspicious_score
        }
    
    def schedule_ritual(
        self,
        name: str,
        description: str,
        scheduled_time: datetime,
        ritual_type: str,
        mantra: Optional[str] = None,
        recurring: bool = False,
        interval: Optional[timedelta] = None
    ) -> ScheduledRitual:
        """Schedule a new ritual"""
        ritual_id = f"ritual_{len(self.rituals) + 1}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        ritual = ScheduledRitual(
            ritual_id=ritual_id,
            name=name,
            description=description,
            scheduled_time=scheduled_time,
            ritual_type=ritual_type,
            mantra=mantra,
            recurring=recurring,
            interval=interval
        )
        
        self.rituals[ritual_id] = ritual
        logger.info(f"📅 Scheduled ritual: {name} at {scheduled_time}")
        
        return ritual
    
    def schedule_daily_ritual(
        self,
        name: str,
        description: str,
        hour: int,
        minute: int = 0,
        mantra: Optional[str] = None
    ) -> ScheduledRitual:
        """Schedule a daily ritual at specific time"""
        now = datetime.now()
        scheduled = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        
        if scheduled <= now:
            scheduled += timedelta(days=1)
        
        return self.schedule_ritual(
            name=name,
            description=description,
            scheduled_time=scheduled,
            ritual_type="daily",
            mantra=mantra,
            recurring=True,
            interval=timedelta(days=1)
        )
    
    async def start(self):
        """Start the ritual scheduler"""
        if self.running:
            logger.warning("Scheduler already running")
            return
        
        self.running = True
        self._task = asyncio.create_task(self._run_scheduler())
        logger.info("🕉️ Sacred Ritual Scheduler started")
    
    async def stop(self):
        """Stop the ritual scheduler"""
        self.running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        logger.info("🕉️ Sacred Ritual Scheduler stopped")
    
    async def _run_scheduler(self):
        """Main scheduler loop"""
        last_hour = -1
        last_tithi = None
        
        while self.running:
            try:
                now = datetime.now()
                cosmic = CosmicCalculator.get_cosmic_time()
                
                # Hourly check
                if now.hour != last_hour:
                    last_hour = now.hour
                    await self._check_hourly_events(cosmic)
                
                # Tithi change check
                if last_tithi != cosmic.tithi:
                    last_tithi = cosmic.tithi
                    await self._check_tithi_events(cosmic)
                
                # Check scheduled rituals
                await self._check_scheduled_rituals()
                
                # Sleep for 1 minute
                await asyncio.sleep(60)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Scheduler error: {e}")
                await asyncio.sleep(60)
    
    async def _check_hourly_events(self, cosmic: CosmicTime):
        """Check for hourly events"""
        # Brahma Muhurta
        if cosmic.brahma_muhurta:
            handler = self.event_handlers.get("brahma_muhurta")
            if handler:
                await handler()
        
        # Hourly chant
        handler = self.event_handlers.get("hourly_chant")
        if handler:
            await handler()
    
    async def _check_tithi_events(self, cosmic: CosmicTime):
        """Check for tithi-based events"""
        if cosmic.tithi == Tithi.PURNIMA:
            handler = self.event_handlers.get("purnima")
            if handler:
                await handler()
        
        elif cosmic.tithi == Tithi.AMAVASYA:
            handler = self.event_handlers.get("amavasya")
            if handler:
                await handler()
        
        elif cosmic.tithi == Tithi.EKADASHI:
            handler = self.event_handlers.get("ekadashi")
            if handler:
                await handler()
    
    async def _check_scheduled_rituals(self):
        """Check and execute scheduled rituals"""
        now = datetime.now()
        
        for ritual_id, ritual in list(self.rituals.items()):
            if ritual.scheduled_time <= now:
                await self._execute_ritual(ritual)
                
                if ritual.recurring and ritual.interval:
                    ritual.scheduled_time = now + ritual.interval
                else:
                    del self.rituals[ritual_id]
    
    async def _execute_ritual(self, ritual: ScheduledRitual):
        """Execute a ritual"""
        logger.info(f"🔱 Executing ritual: {ritual.name}")
        
        if ritual.mantra:
            logger.info(f"   Mantra: {ritual.mantra}")
        
        ritual.last_executed = datetime.now()
        ritual.execution_count += 1
        
        # Find and execute handler
        handler = self.event_handlers.get(ritual.ritual_type)
        if handler:
            result = await handler()
            return result
        
        return {"ritual": ritual.name, "status": "executed"}
    
    def get_upcoming_events(self, days: int = 7) -> List[Dict[str, Any]]:
        """Get upcoming cosmic events"""
        events = []
        now = datetime.now()
        
        for i in range(days * 24):  # Check every hour for 'days' days
            check_time = now + timedelta(hours=i)
            cosmic = CosmicCalculator.get_cosmic_time(check_time)
            
            # Check for significant events
            if cosmic.tithi == Tithi.PURNIMA:
                events.append({
                    "type": "purnima",
                    "name": "Full Moon (Pūrṇimā)",
                    "datetime": check_time.isoformat(),
                    "significance": "high"
                })
            
            elif cosmic.tithi == Tithi.AMAVASYA:
                events.append({
                    "type": "amavasya",
                    "name": "New Moon (Amāvasyā)",
                    "datetime": check_time.isoformat(),
                    "significance": "high"
                })
            
            elif cosmic.tithi == Tithi.EKADASHI:
                events.append({
                    "type": "ekadashi",
                    "name": "Ekādaśī",
                    "datetime": check_time.isoformat(),
                    "significance": "moderate"
                })
            
            elif cosmic.brahma_muhurta:
                events.append({
                    "type": "brahma_muhurta",
                    "name": "Brahma Muhurta",
                    "datetime": check_time.isoformat(),
                    "significance": "moderate"
                })
        
        # Remove duplicates and sort
        seen = set()
        unique_events = []
        for event in events:
            key = (event["type"], event["datetime"][:10])  # Group by day
            if key not in seen:
                seen.add(key)
                unique_events.append(event)
        
        return unique_events[:20]  # Return top 20

# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

_scheduler: Optional[SacredRitualScheduler] = None

def get_scheduler() -> SacredRitualScheduler:
    """Get or create the global scheduler"""
    global _scheduler
    if _scheduler is None:
        _scheduler = SacredRitualScheduler()
    return _scheduler

def get_current_cosmic_time() -> CosmicTime:
    """Get current cosmic time"""
    return CosmicCalculator.get_cosmic_time()

def is_auspicious_for(activity: str) -> Dict[str, Any]:
    """Check if current time is auspicious for an activity"""
    cosmic = CosmicCalculator.get_cosmic_time()
    config = AUSPICIOUS_ACTIVITIES.get(activity, {})
    
    is_auspicious = True
    reasons = []
    
    if config.get("nakshatras"):
        if cosmic.nakshatra in config["nakshatras"]:
            reasons.append(f"✅ Nakshatra {cosmic.nakshatra} is auspicious")
        else:
            is_auspicious = False
            reasons.append(f"❌ Nakshatra {cosmic.nakshatra} is not ideal")
    
    if config.get("tithis"):
        if cosmic.tithi in config["tithis"]:
            reasons.append(f"✅ Tithi {cosmic.tithi_name} is auspicious")
        else:
            is_auspicious = False
            reasons.append(f"❌ Tithi {cosmic.tithi_name} is not ideal")
    
    if config.get("solar_phase"):
        if cosmic.solar_phase == config["solar_phase"]:
            reasons.append(f"✅ {cosmic.solar_phase.value} is auspicious")
        else:
            is_auspicious = False
            reasons.append(f"❌ {cosmic.solar_phase.value} is not ideal")
    
    return {
        "is_auspicious": is_auspicious,
        "score": cosmic.auspicious_score,
        "cosmic_time": cosmic.to_dict(),
        "reasons": reasons
    }

# ============================================================================
# MAIN TEST
# ============================================================================

async def test_sacred_ritual_scheduler():
    """Test the sacred ritual scheduler"""
    print("🕉️ Testing Sacred Ritual Scheduler")
    print("=" * 60)
    
    # Test cosmic time
    print("\n📊 Current Cosmic Time:")
    cosmic = get_current_cosmic_time()
    print(f"   Solar Phase: {cosmic.solar_phase.value}")
    print(f"   Lunar Phase: {cosmic.lunar_phase.value}")
    print(f"   Tithi: {cosmic.tithi_name}")
    print(f"   Nakshatra: {cosmic.nakshatra}")
    print(f"   Day: {cosmic.day_name} (Deity: {cosmic.day_deity})")
    print(f"   Brahma Muhurta: {cosmic.brahma_muhurta}")
    print(f"   Auspicious Score: {cosmic.auspicious_score:.2f}")
    
    # Test auspicious check
    print("\n🔍 Auspicious Check for Knowledge Creation:")
    result = is_auspicious_for("knowledge_creation")
    print(f"   Is Auspicious: {result['is_auspicious']}")
    print(f"   Score: {result['score']:.2f}")
    for reason in result['reasons']:
        print(f"   {reason}")
    
    # Test finding auspicious times
    print("\n📅 Finding Auspicious Times for Deployment:")
    times = CosmicCalculator.find_auspicious_time("system_deployment", search_days=7)
    for t in times[:3]:
        print(f"   {t['datetime']}: Score {t['score']:.2f}")
    
    # Test scheduler
    print("\n⏰ Testing Scheduler:")
    scheduler = get_scheduler()
    
    # Schedule a test ritual
    scheduler.schedule_daily_ritual(
        name="Morning Prayer",
        description="Daily morning sacred invocation",
        hour=6,
        minute=0,
        mantra="ॐ गायत्री नमः"
    )
    
    # Get upcoming events
    print("\n🔮 Upcoming Cosmic Events:")
    events = scheduler.get_upcoming_events(days=3)
    for event in events[:5]:
        print(f"   {event['name']}: {event['datetime'][:10]}")
    
    print("\n✅ Sacred Ritual Scheduler test complete")

if __name__ == "__main__":
    asyncio.run(test_sacred_ritual_scheduler())
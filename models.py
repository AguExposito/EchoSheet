import json
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional
from config import (
    MAX_LEVEL, MIN_LEVEL, MAX_ATTRIBUTE_POINTS, MIN_ATTRIBUTE_VALUE, 
    MAX_ATTRIBUTE_VALUE, POINT_BUY_COSTS, XP_THRESHOLDS, 
    CURRENCY_VALUES, DEFAULT_ITEM_WEIGHTS, HIT_DICE_BY_CLASS,
    BASE_HP_BY_CLASS, MOVEMENT_SPEED_BY_RACE, SPELLCASTING_ABILITIES,
    SAVING_THROW_PROFICIENCIES, COMBAT_ROLES
)


@dataclass
class Character:
    """Data model for a D&D character"""
    id: Optional[int] = None
    name: str = ""
    race: str = ""
    char_class: str = ""
    level: int = 1
    background: str = ""
    alignment: str = ""
    experience_points: int = 0
    
    # Physical Characteristics
    age: str = ""
    height: str = ""
    weight: str = ""
    eyes: str = ""
    skin: str = ""
    hair: str = ""
    
    # Combat Information
    hit_point_maximum: int = 0
    current_hit_points: int = 0
    temporary_hit_points: int = 0
    hit_dice: str = ""
    
    attributes: Dict[str, int] = field(default_factory=dict)  # STR, DEX, CON, INT, WIS, CHA
    skills: List[str] = field(default_factory=list)
    feats: List[str] = field(default_factory=list)
    spells: List[str] = field(default_factory=list)  # Combined list of cantrips and spells
    cantrips: List[str] = field(default_factory=list)  # Cantrips only
    spells_known: List[str] = field(default_factory=list)  # Spells only (not cantrips)
    
    # Personality Traits (D&D 5e standard)
    personality_traits: str = ""
    ideals: str = ""
    bonds: str = ""
    
    # Extended Personality (custom)
    background_story: str = ""
    short_term_goals: str = ""
    long_term_goals: str = ""
    personal_goals: str = ""
    personality_tags: List[str] = field(default_factory=list)
    flaws: str = ""
    
    currency: Dict[str, int] = field(default_factory=dict)  # {"cp": 0, "sp": 0, "ep": 0, "gp": 0, "pp": 0}
    items: List[str] = field(default_factory=list)
    item_weights: Dict[str, float] = field(default_factory=dict)  # Custom weights for items
    history_log: List[str] = field(default_factory=list)
    chat_history: List[Dict[str, str]] = field(default_factory=list)
    available_attribute_points: int = 27  # Point buy system
    available_skill_choices: int = 0  # Based on class and background
    
    def get_attribute_modifier(self, attribute: str) -> int:
        """Get attribute modifier"""
        if attribute not in self.attributes:
            return 0
        return (self.attributes[attribute] - 10) // 2
    
    def get_proficiency_bonus(self) -> int:
        """Get proficiency bonus based on level"""
        return (self.level - 1) // 4 + 2
    
    def get_skill_bonus(self, skill: str) -> int:
        """Get total skill bonus"""
        if skill not in self.skills:
            return 0
        
        # Skill to attribute mapping
        skill_attributes = {
            'Acrobatics': 'DEX',
            'Animal Handling': 'WIS',
            'Arcana': 'INT',
            'Athletics': 'STR',
            'Deception': 'CHA',
            'History': 'INT',
            'Insight': 'WIS',
            'Intimidation': 'CHA',
            'Investigation': 'INT',
            'Medicine': 'WIS',
            'Nature': 'INT',
            'Perception': 'WIS',
            'Performance': 'CHA',
            'Persuasion': 'CHA',
            'Religion': 'INT',
            'Sleight of Hand': 'DEX',
            'Stealth': 'DEX',
            'Survival': 'WIS'
        }
        
        attribute = skill_attributes.get(skill, 'STR')
        modifier = self.get_attribute_modifier(attribute)
        proficiency = self.get_proficiency_bonus() if skill in self.skills else 0
        
        return modifier + proficiency

    def validate_attributes(self) -> Dict[str, any]:
        """Validate attribute points and return validation info"""
        total_cost = 0
        errors = []
        
        for attr, value in self.attributes.items():
            if value < MIN_ATTRIBUTE_VALUE or value > MAX_ATTRIBUTE_VALUE:
                errors.append(f"{attr} must be between {MIN_ATTRIBUTE_VALUE} and {MAX_ATTRIBUTE_VALUE}")
            elif value in POINT_BUY_COSTS:
                total_cost += POINT_BUY_COSTS[value]
            else:
                errors.append(f"Invalid {attr} value: {value}")
        
        return {
            'valid': len(errors) == 0 and total_cost <= MAX_ATTRIBUTE_POINTS,
            'total_cost': total_cost,
            'remaining_points': MAX_ATTRIBUTE_POINTS - total_cost,
            'errors': errors
        }

    def get_available_skills(self) -> List[str]:
        """Get available skills based on class and background"""
        if not self.char_class:
            return []
        
        # Class skill options
        class_skills = {
            'Fighter': ['Acrobatics', 'Athletics', 'History', 'Insight', 'Intimidation', 'Perception', 'Survival'],
            'Wizard': ['Arcana', 'History', 'Insight', 'Investigation', 'Religion'],
            'Cleric': ['History', 'Insight', 'Medicine', 'Persuasion', 'Religion'],
            'Rogue': ['Acrobatics', 'Athletics', 'Deception', 'Insight', 'Intimidation', 'Investigation', 'Perception', 'Performance', 'Persuasion', 'Sleight of Hand', 'Stealth'],
            'Ranger': ['Animal Handling', 'Athletics', 'Insight', 'Investigation', 'Nature', 'Perception', 'Stealth', 'Survival'],
            'Paladin': ['Athletics', 'Insight', 'Intimidation', 'Medicine', 'Persuasion', 'Religion'],
            'Bard': ['Acrobatics', 'Animal Handling', 'Arcana', 'Athletics', 'Deception', 'History', 'Insight', 'Intimidation', 'Investigation', 'Medicine', 'Nature', 'Perception', 'Performance', 'Persuasion', 'Religion', 'Sleight of Hand', 'Stealth', 'Survival'],
            'Sorcerer': ['Arcana', 'Deception', 'Insight', 'Intimidation', 'Persuasion', 'Religion'],
            'Warlock': ['Arcana', 'Deception', 'History', 'Intimidation', 'Investigation', 'Nature', 'Religion'],
            'Monk': ['Acrobatics', 'Athletics', 'History', 'Insight', 'Religion', 'Stealth'],
            'Druid': ['Animal Handling', 'Arcana', 'Insight', 'Medicine', 'Nature', 'Perception', 'Religion', 'Survival'],
            'Barbarian': ['Animal Handling', 'Athletics', 'Intimidation', 'Nature', 'Perception', 'Survival']
        }
        
        return class_skills.get(self.char_class, [])

    def get_skill_choices_remaining(self) -> int:
        """Get remaining skill choices based on class and background"""
        if not self.char_class:
            return 0
        
        # Class skill choices
        class_choices = {
            'Fighter': 2, 'Wizard': 2, 'Cleric': 2, 'Rogue': 4,
            'Ranger': 3, 'Paladin': 2, 'Bard': 3, 'Sorcerer': 2,
            'Warlock': 2, 'Monk': 2, 'Druid': 2, 'Barbarian': 2
        }
        
        base_choices = class_choices.get(self.char_class, 0)
        background_choices = 2 if self.background else 0
        
        total_choices = base_choices + background_choices
        used_choices = len(self.skills)
        
        return max(0, total_choices - used_choices)
    
    def add_to_history(self, entry: str):
        """Agregar entrada al historial del personaje"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.history_log.append(f"[{timestamp}] {entry}")
    
    def to_dict(self) -> Dict:
        """Convertir personaje a diccionario para JSON"""
        return {
            'id': self.id,
            'name': self.name,
            'race': self.race,
            'char_class': self.char_class,
            'level': self.level,
            'background': self.background,
            'alignment': self.alignment,
            'experience_points': self.experience_points,
            'age': self.age,
            'height': self.height,
            'weight': self.weight,
            'eyes': self.eyes,
            'skin': self.skin,
            'hair': self.hair,
            'hit_point_maximum': self.hit_point_maximum,
            'current_hit_points': self.current_hit_points,
            'temporary_hit_points': self.temporary_hit_points,
            'hit_dice': self.hit_dice,
            'attributes': self.attributes,
            'skills': self.skills,
            'feats': self.feats,
            'spells': self.spells,
            'cantrips': self.cantrips,
            'spells_known': self.spells_known,
            'personality_traits': self.personality_traits,
            'ideals': self.ideals,
            'bonds': self.bonds,
            'background_story': self.background_story,
            'short_term_goals': self.short_term_goals,
            'long_term_goals': self.long_term_goals,
            'personal_goals': self.personal_goals,
            'personality_tags': self.personality_tags,
            'flaws': self.flaws,
            'currency': self.currency,
            'items': self.items,
            'item_weights': self.item_weights,
            'history_log': self.history_log,
            'chat_history': self.chat_history
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Character':
        """Crear personaje desde diccionario"""
        return cls(
            id=data.get('id'),
            name=data.get('name', ''),
            race=data.get('race', ''),
            char_class=data.get('char_class', ''),
            level=data.get('level', 1),
            background=data.get('background', ''),
            alignment=data.get('alignment', ''),
            experience_points=data.get('experience_points', 0),
            age=data.get('age', ''),
            height=data.get('height', ''),
            weight=data.get('weight', ''),
            eyes=data.get('eyes', ''),
            skin=data.get('skin', ''),
            hair=data.get('hair', ''),
            hit_point_maximum=data.get('hit_point_maximum', 0),
            current_hit_points=data.get('current_hit_points', 0),
            temporary_hit_points=data.get('temporary_hit_points', 0),
            hit_dice=data.get('hit_dice', ''),
            attributes=data.get('attributes', {}),
            skills=data.get('skills', []),
            feats=data.get('feats', []),
            spells=data.get('spells', []),
            cantrips=data.get('cantrips', []),
            spells_known=data.get('spells_known', []),
            personality_traits=data.get('personality_traits', ''),
            ideals=data.get('ideals', ''),
            bonds=data.get('bonds', ''),
            background_story=data.get('background_story', ''),
            short_term_goals=data.get('short_term_goals', ''),
            long_term_goals=data.get('long_term_goals', ''),
            personal_goals=data.get('personal_goals', ''),
            personality_tags=data.get('personality_tags', []),
            flaws=data.get('flaws', ''),
            currency=data.get('currency', {}),
            items=data.get('items', []),
            item_weights=data.get('item_weights', {}),
            history_log=data.get('history_log', []),
            chat_history=data.get('chat_history', [])
        )
    
    def get_spellcasting_ability(self) -> str:
        """Get the spellcasting ability for the character's class"""
        return SPELLCASTING_ABILITIES.get(self.char_class, 'None')
    
    def get_spell_save_dc(self) -> str:
        """Calculate spell save DC"""
        if not self.get_spellcasting_ability():
            return 'N/A'
        
        ability_modifier = self.get_attribute_modifier(self.get_spellcasting_ability()[:3])
        proficiency_bonus = self.get_proficiency_bonus()
        base_dc = 8 + ability_modifier + proficiency_bonus
        
        return f"{base_dc}"
    
    def get_spell_attack_bonus(self) -> str:
        """Calculate spell attack bonus"""
        if not self.get_spellcasting_ability():
            return 'N/A'
        
        ability_modifier = self.get_attribute_modifier(self.get_spellcasting_ability()[:3])
        proficiency_bonus = self.get_proficiency_bonus()
        attack_bonus = ability_modifier + proficiency_bonus
        
        return f"{'+' if attack_bonus >= 0 else ''}{attack_bonus}"
    
    def get_spell_slots(self, level: int) -> int:
        """Get number of spell slots for a given level"""
        if not self.get_spellcasting_ability():
            return 0
        
        # Spell slots by level for full casters (simplified for level 1)
        spell_slots = {
            1: {1: 2},  # Level 1 character has 2 1st-level slots
            2: {1: 3},
            3: {1: 4, 2: 2},
            4: {1: 4, 2: 3},
            5: {1: 4, 2: 3, 3: 2},
            6: {1: 4, 2: 3, 3: 3},
            7: {1: 4, 2: 3, 3: 3, 4: 1},
            8: {1: 4, 2: 3, 3: 3, 4: 2},
            9: {1: 4, 2: 3, 3: 3, 4: 3, 5: 1},
            10: {1: 4, 2: 3, 3: 3, 4: 3, 5: 2}
        }
        
        return spell_slots.get(self.level, {}).get(level, 0)
    
    def get_armor_class(self) -> int:
        """Calculate base armor class"""
        # Base AC calculation (simplified)
        dex_modifier = self.get_attribute_modifier('Dexterity')
        
        # Different base AC based on class
        if self.char_class in ['Monk', 'Barbarian']:
            # Unarmored Defense
            if self.char_class == 'Monk':
                wis_modifier = self.get_attribute_modifier('Wisdom')
                return 10 + dex_modifier + wis_modifier
            else:  # Barbarian
                con_modifier = self.get_attribute_modifier('Constitution')
                return 10 + dex_modifier + con_modifier
        else:
            # Standard armor (assuming light armor for most classes)
            return 11 + min(dex_modifier, 2)  # Light armor + Dex (max +2)
    
    def get_hit_points(self) -> int:
        """Calculate hit points"""
        con_modifier = self.get_attribute_modifier('Constitution')
        
        hit_die = BASE_HP_BY_CLASS.get(self.char_class, 8)
        base_hp = hit_die + con_modifier
        
        # Add HP for levels beyond 1st
        if self.level > 1:
            # Average HP per level (simplified)
            avg_hp_per_level = (hit_die // 2) + 1 + con_modifier
            additional_hp = avg_hp_per_level * (self.level - 1)
            base_hp += additional_hp
        
        return max(1, base_hp)  # Minimum 1 HP
    
    def get_speed(self) -> int:
        """Get movement speed"""
        return MOVEMENT_SPEED_BY_RACE.get(self.race, 30)
    
    def get_saving_throw_bonus(self, attribute: str) -> int:
        """Calculate saving throw bonus"""
        modifier = self.get_attribute_modifier(attribute)
        
        # Check if proficient in this saving throw
        proficiencies = SAVING_THROW_PROFICIENCIES.get(self.char_class, [])
        if attribute in proficiencies:
            modifier += self.get_proficiency_bonus()
        
        return modifier
    
    def get_combat_role(self) -> str:
        """Determine the character's primary combat role"""
        if not self.char_class:
            return "Undefined"
        
        return COMBAT_ROLES.get(self.char_class, "Versatile")
    
    def get_initiative(self) -> int:
        """Calculate initiative bonus"""
        return self.get_attribute_modifier('Dexterity')
    
    def get_passive_perception(self) -> int:
        """Calculate passive perception"""
        base = 10
        perception_bonus = self.get_skill_bonus('Perception')
        return base + perception_bonus
    
    def get_passive_investigation(self) -> int:
        """Calculate passive investigation"""
        base = 10
        investigation_bonus = self.get_skill_bonus('Investigation')
        return base + investigation_bonus
    
    def get_passive_insight(self) -> int:
        """Calculate passive insight"""
        base = 10
        insight_bonus = self.get_skill_bonus('Insight')
        return base + insight_bonus
    
    def get_hit_dice(self) -> str:
        """Get hit dice string based on class and level"""
        if not self.char_class:
            return ""
        
        dice_type = HIT_DICE_BY_CLASS.get(self.char_class, 'd8')
        return f"{self.level}{dice_type}"
    
    def get_experience_to_next_level(self) -> int:
        """Get experience points needed for next level"""
        if self.level >= MAX_LEVEL:
            return 0
        
        # Ensure experience_points is an integer
        current_xp = int(self.experience_points) if self.experience_points else 0
        next_level_xp = XP_THRESHOLDS.get(self.level + 1, 0)
        
        return max(0, next_level_xp - current_xp)
    
    def can_level_up(self) -> bool:
        """Check if character can level up"""
        if self.level >= MAX_LEVEL:
            return False
        
        # Ensure experience_points is an integer
        current_xp = int(self.experience_points) if self.experience_points else 0
        next_level_xp = XP_THRESHOLDS.get(self.level + 1, 0)
        return current_xp >= next_level_xp
    
    def get_current_level_xp_threshold(self) -> int:
        """Get XP threshold for current level"""
        return XP_THRESHOLDS.get(self.level, 0)
    
    def get_experience_progress(self) -> float:
        """Get experience progress as percentage to next level"""
        if self.level >= MAX_LEVEL:
            return 100.0
        
        current_level_xp = XP_THRESHOLDS.get(self.level, 0)
        next_level_xp = XP_THRESHOLDS.get(self.level + 1, current_level_xp)
        
        if next_level_xp == current_level_xp:
            return 100.0
        
        # Ensure experience_points is an integer
        current_xp = int(self.experience_points) if self.experience_points else 0
        progress = current_xp - current_level_xp
        total_needed = next_level_xp - current_level_xp
        
        return min(100.0, max(0.0, (progress / total_needed) * 100))
    
    def get_carrying_capacity(self) -> int:
        """Calculate carrying capacity based on Strength"""
        str_score = self.attributes.get('Strength', 10)
        return str_score * 15  # 15 pounds per point of Strength
    
    def get_push_drag_lift(self) -> int:
        """Calculate push, drag, or lift capacity"""
        str_score = self.attributes.get('Strength', 10)
        return str_score * 30  # 30 pounds per point of Strength
    
    def get_total_currency_value(self) -> int:
        """Get total currency value in copper pieces"""
        total_cp = 0
        
        for currency_type, amount in self.currency.items():
            if currency_type in CURRENCY_VALUES:
                total_cp += amount * CURRENCY_VALUES[currency_type]
        
        return total_cp
    
    def format_currency(self) -> str:
        """Format currency for display"""
        if not self.currency:
            return "0 cp"
        
        # Convert everything to copper first
        total_cp = self.get_total_currency_value()
        
        # Convert back to highest denominations
        pp = total_cp // 1000
        total_cp %= 1000
        gp = total_cp // 100
        total_cp %= 100
        ep = total_cp // 50
        total_cp %= 50
        sp = total_cp // 10
        total_cp %= 10
        cp = total_cp
        
        # Build formatted string
        parts = []
        if pp > 0:
            parts.append(f"{pp} pp")
        if gp > 0:
            parts.append(f"{gp} gp")
        if ep > 0:
            parts.append(f"{ep} ep")
        if sp > 0:
            parts.append(f"{sp} sp")
        if cp > 0:
            parts.append(f"{cp} cp")
        
        return ", ".join(parts) if parts else "0 cp"
    
    def get_estimated_weight(self) -> float:
        """Estimate total weight of items (simplified calculation)"""
        total_weight = 0
        
        # Calculate weight from items
        for item in self.items:
            found_weight = False
            
            # First check custom weights (exact match)
            if item in self.item_weights:
                total_weight += self.item_weights[item]
                found_weight = True
            else:
                # Then check default weights (partial match)
                item_lower = item.lower()
                for weight_item, weight in DEFAULT_ITEM_WEIGHTS.items():
                    if weight_item in item_lower:
                        total_weight += weight
                        found_weight = True
                        break
            
            # If no specific weight found, assume 1 pound
            if not found_weight:
                total_weight += 1
        
        # Add currency weight
        total_cp = self.get_total_currency_value()
        total_weight += total_cp * 0.02  # 50 coins = 1 pound
        
        return round(total_weight, 1)
    
    def get_item_weight(self, item_name: str) -> float:
        """Get the weight of a specific item"""
        # First check custom weights
        if item_name in self.item_weights:
            return self.item_weights[item_name]
        
        # Then check default weights
        item_lower = item_name.lower()
        for weight_item, weight in DEFAULT_ITEM_WEIGHTS.items():
            if weight_item in item_lower:
                return weight
        
        return 1.0  # Default weight 
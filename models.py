import json
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional


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
        
        # Point buy costs
        point_costs = {
            8: 0, 9: 1, 10: 2, 11: 3, 12: 4, 13: 5, 14: 7, 15: 9
        }
        
        for attr, value in self.attributes.items():
            if value < 8 or value > 15:
                errors.append(f"{attr} must be between 8 and 15")
            elif value in point_costs:
                total_cost += point_costs[value]
            else:
                errors.append(f"Invalid {attr} value: {value}")
        
        return {
            'valid': len(errors) == 0 and total_cost <= 27,
            'total_cost': total_cost,
            'remaining_points': 27 - total_cost,
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
        spellcasting_abilities = {
            'Wizard': 'Intelligence',
            'Cleric': 'Wisdom',
            'Bard': 'Charisma',
            'Sorcerer': 'Charisma',
            'Warlock': 'Charisma',
            'Druid': 'Wisdom',
            'Paladin': 'Charisma',
            'Ranger': 'Wisdom'
        }
        return spellcasting_abilities.get(self.char_class, 'None')
    
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
        
        # Hit die by class
        hit_dice = {
            'Barbarian': 12, 'Fighter': 10, 'Paladin': 10, 'Ranger': 10,
            'Bard': 8, 'Cleric': 8, 'Druid': 8, 'Monk': 8, 'Rogue': 8,
            'Sorcerer': 6, 'Warlock': 8, 'Wizard': 6
        }
        
        hit_die = hit_dice.get(self.char_class, 8)
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
        # Base speed by race (simplified)
        race_speeds = {
            'Human': 30, 'Elf': 30, 'Dwarf': 25, 'Halfling': 25,
            'Dragonborn': 30, 'Tiefling': 30, 'Half-Elf': 30, 'Half-Orc': 30,
            'Gnome': 25, 'Aarakocra': 25, 'Genasi': 30, 'Goliath': 30
        }
        
        return race_speeds.get(self.race, 30)
    
    def get_saving_throw_bonus(self, attribute: str) -> int:
        """Calculate saving throw bonus"""
        modifier = self.get_attribute_modifier(attribute)
        
        # Check if proficient in this saving throw
        saving_throw_proficiencies = {
            'Fighter': ['Strength', 'Constitution'],
            'Wizard': ['Intelligence', 'Wisdom'],
            'Cleric': ['Wisdom', 'Charisma'],
            'Rogue': ['Dexterity', 'Intelligence'],
            'Ranger': ['Strength', 'Dexterity'],
            'Paladin': ['Wisdom', 'Charisma'],
            'Bard': ['Dexterity', 'Charisma'],
            'Sorcerer': ['Constitution', 'Charisma'],
            'Warlock': ['Wisdom', 'Charisma'],
            'Monk': ['Strength', 'Dexterity'],
            'Druid': ['Intelligence', 'Wisdom'],
            'Barbarian': ['Strength', 'Constitution']
        }
        
        proficiencies = saving_throw_proficiencies.get(self.char_class, [])
        if attribute in proficiencies:
            modifier += self.get_proficiency_bonus()
        
        return modifier
    
    def get_combat_role(self) -> str:
        """Determine the character's primary combat role"""
        if not self.char_class:
            return "Undefined"
        
        # Combat roles by class
        combat_roles = {
            'Fighter': 'Frontline Defender',
            'Paladin': 'Frontline Defender',
            'Barbarian': 'Frontline Striker',
            'Ranger': 'Ranged Striker',
            'Rogue': 'Skirmisher',
            'Monk': 'Mobile Striker',
            'Wizard': 'Control Caster',
            'Sorcerer': 'Blaster Caster',
            'Warlock': 'Blaster Caster',
            'Cleric': 'Support Caster',
            'Druid': 'Control Caster',
            'Bard': 'Support Caster'
        }
        
        return combat_roles.get(self.char_class, "Versatile")
    
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
        
        # Hit dice by class
        hit_dice_types = {
            'Barbarian': 'd12',
            'Fighter': 'd10',
            'Paladin': 'd10',
            'Ranger': 'd10',
            'Bard': 'd8',
            'Cleric': 'd8',
            'Druid': 'd8',
            'Monk': 'd8',
            'Rogue': 'd8',
            'Sorcerer': 'd6',
            'Warlock': 'd8',
            'Wizard': 'd6'
        }
        
        dice_type = hit_dice_types.get(self.char_class, 'd8')
        return f"{self.level}{dice_type}"
    
    def get_experience_to_next_level(self) -> int:
        """Get experience points needed for next level"""
        # D&D 5e Experience Thresholds (official table)
        xp_thresholds = {
            1: 0, 2: 300, 3: 900, 4: 2700, 5: 6500,
            6: 14000, 7: 23000, 8: 34000, 9: 48000, 10: 64000,
            11: 85000, 12: 100000, 13: 120000, 14: 140000, 15: 165000,
            16: 195000, 17: 225000, 18: 265000, 19: 305000, 20: 355000
        }
        
        if self.level >= 20:
            return 0
        
        # Ensure experience_points is an integer
        current_xp = int(self.experience_points) if self.experience_points else 0
        next_level_xp = xp_thresholds.get(self.level + 1, 0)
        
        return max(0, next_level_xp - current_xp)
    
    def can_level_up(self) -> bool:
        """Check if character can level up"""
        if self.level >= 20:
            return False
        
        # Ensure experience_points is an integer
        current_xp = int(self.experience_points) if self.experience_points else 0
        xp_thresholds = {
            1: 0, 2: 300, 3: 900, 4: 2700, 5: 6500,
            6: 14000, 7: 23000, 8: 34000, 9: 48000, 10: 64000,
            11: 85000, 12: 100000, 13: 120000, 14: 140000, 15: 165000,
            16: 195000, 17: 225000, 18: 265000, 19: 305000, 20: 355000
        }
        
        next_level_xp = xp_thresholds.get(self.level + 1, 0)
        return current_xp >= next_level_xp
    
    def get_current_level_xp_threshold(self) -> int:
        """Get XP threshold for current level"""
        xp_thresholds = {
            1: 0, 2: 300, 3: 900, 4: 2700, 5: 6500,
            6: 14000, 7: 23000, 8: 34000, 9: 48000, 10: 64000,
            11: 85000, 12: 100000, 13: 120000, 14: 140000, 15: 165000,
            16: 195000, 17: 225000, 18: 265000, 19: 305000, 20: 355000
        }
        return xp_thresholds.get(self.level, 0)
    
    def get_experience_progress(self) -> float:
        """Get experience progress as percentage to next level"""
        if self.level >= 20:
            return 100.0
        
        xp_thresholds = {
            1: 0, 2: 300, 3: 900, 4: 2700, 5: 6500,
            6: 14000, 7: 23000, 8: 34000, 9: 48000, 10: 64000,
            11: 85000, 12: 100000, 13: 120000, 14: 140000, 15: 165000,
            16: 195000, 17: 225000, 18: 265000, 19: 305000, 20: 355000
        }
        
        current_level_xp = xp_thresholds.get(self.level, 0)
        next_level_xp = xp_thresholds.get(self.level + 1, current_level_xp)
        
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
        currency_values = {
            'cp': 1,      # Copper piece
            'sp': 10,     # Silver piece = 10 cp
            'ep': 50,     # Electrum piece = 50 cp
            'gp': 100,    # Gold piece = 100 cp
            'pp': 1000    # Platinum piece = 1000 cp
        }
        
        for currency_type, amount in self.currency.items():
            if currency_type in currency_values:
                total_cp += amount * currency_values[currency_type]
        
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
        # Base weight for common items (in pounds)
        default_item_weights = {
            'backpack': 5,
            'bedroll': 7,
            'rations': 2,
            'waterskin': 5,
            'torch': 1,
            'rope': 10,
            'tent': 20,
            'armor': 40,  # Average armor weight
            'weapon': 3,  # Average weapon weight
            'shield': 6,
            'potion': 0.5,
            'scroll': 0.1,
            'book': 5,
            'clothes': 3,
            'boots': 2,
            'helmet': 4,
            'gloves': 1,
            'belt': 1,
            'pouch': 1,
            'coin': 0.02  # Per coin
        }
        
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
                for weight_item, weight in default_item_weights.items():
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
        default_weights = {
            'backpack': 5, 'bedroll': 7, 'rations': 2, 'waterskin': 5,
            'torch': 1, 'rope': 10, 'tent': 20, 'armor': 40,
            'weapon': 3, 'shield': 6, 'potion': 0.5, 'scroll': 0.1,
            'book': 5, 'clothes': 3, 'boots': 2, 'helmet': 4,
            'gloves': 1, 'belt': 1, 'pouch': 1
        }
        
        item_lower = item_name.lower()
        for weight_item, weight in default_weights.items():
            if weight_item in item_lower:
                return weight
        
        return 1.0  # Default weight 
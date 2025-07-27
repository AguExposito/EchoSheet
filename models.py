from dataclasses import dataclass, field
from typing import Dict, List, Optional
from datetime import datetime

@dataclass
class Character:
    """Data model for a D&D character"""
    id: Optional[int] = None
    name: str = ""
    race: str = ""
    char_class: str = ""
    level: int = 1
    background: str = ""
    attributes: Dict[str, int] = field(default_factory=dict)  # STR, DEX, CON, INT, WIS, CHA
    skills: List[str] = field(default_factory=list)
    feats: List[str] = field(default_factory=list)
    spells: List[str] = field(default_factory=list)  # Combined list of cantrips and spells
    cantrips: List[str] = field(default_factory=list)  # Cantrips only
    spells_known: List[str] = field(default_factory=list)  # Spells only (not cantrips)
    personality_traits: str = ""
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
            'attributes': self.attributes,
            'skills': self.skills,
            'feats': self.feats,
            'spells': self.spells,
            'personality_traits': self.personality_traits,
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
            attributes=data.get('attributes', {}),
            skills=data.get('skills', []),
            feats=data.get('feats', []),
            spells=data.get('spells', []),
            cantrips=data.get('cantrips', []),
            spells_known=data.get('spells_known', []),
            personality_traits=data.get('personality_traits', ''),
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
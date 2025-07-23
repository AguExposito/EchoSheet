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
            personality_traits=data.get('personality_traits', ''),
            history_log=data.get('history_log', []),
            chat_history=data.get('chat_history', [])
        ) 
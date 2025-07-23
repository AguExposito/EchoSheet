import json
import random
from typing import Dict, List
from models import Character
from utils.spell_manager import SpellManager

class AutoFill:
    """Clase para autocompletar datos del personaje"""
    
    def __init__(self):
        self.load_data()
        self.spell_manager = SpellManager()
    
    def load_data(self):
        """Cargar datos de clases, razas y backgrounds"""
        # Datos básicos de D&D 5e (SRD only)
        self.races = {
            'Human': {'ability_bonus': {'STR': 1, 'DEX': 1, 'CON': 1, 'INT': 1, 'WIS': 1, 'CHA': 1}},
            'Elf': {'ability_bonus': {'DEX': 2}},
            'Dwarf': {'ability_bonus': {'CON': 2}},
            'Halfling': {'ability_bonus': {'DEX': 2}},
            'Dragonborn': {'ability_bonus': {'STR': 2, 'CHA': 1}},
            'Tiefling': {'ability_bonus': {'INT': 1, 'CHA': 2}},
            'Half-Elf': {'ability_bonus': {'CHA': 2}},
            'Half-Orc': {'ability_bonus': {'STR': 2, 'CON': 1}},
            'Gnome': {'ability_bonus': {'INT': 2}}
        }
        
        self.classes = {
            'Fighter': {
                'hit_die': 10,
                'primary_attributes': ['STR', 'CON'],
                'saving_throws': ['STR', 'CON'],
                'skill_choices': 2,
                'skill_options': ['Acrobatics', 'Athletics', 'History', 'Insight', 'Intimidation', 'Perception', 'Survival']
            },
            'Wizard': {
                'hit_die': 6,
                'primary_attributes': ['INT'],
                'saving_throws': ['INT', 'WIS'],
                'skill_choices': 2,
                'skill_options': ['Arcana', 'History', 'Insight', 'Investigation', 'Religion']
            },
            'Cleric': {
                'hit_die': 8,
                'primary_attributes': ['WIS'],
                'saving_throws': ['WIS', 'CHA'],
                'skill_choices': 2,
                'skill_options': ['History', 'Insight', 'Medicine', 'Persuasion', 'Religion']
            },
            'Rogue': {
                'hit_die': 8,
                'primary_attributes': ['DEX'],
                'saving_throws': ['DEX', 'INT'],
                'skill_choices': 4,
                'skill_options': ['Acrobatics', 'Athletics', 'Deception', 'Insight', 'Intimidation', 'Investigation', 'Perception', 'Performance', 'Persuasion', 'Sleight of Hand', 'Stealth']
            },
            'Ranger': {
                'hit_die': 10,
                'primary_attributes': ['STR', 'DEX', 'WIS'],
                'saving_throws': ['STR', 'DEX'],
                'skill_choices': 3,
                'skill_options': ['Animal Handling', 'Athletics', 'Insight', 'Investigation', 'Nature', 'Perception', 'Stealth', 'Survival']
            },
            'Paladin': {
                'hit_die': 10,
                'primary_attributes': ['STR', 'CHA'],
                'saving_throws': ['WIS', 'CHA'],
                'skill_choices': 2,
                'skill_options': ['Athletics', 'Insight', 'Intimidation', 'Medicine', 'Persuasion', 'Religion']
            },
            'Bard': {
                'hit_die': 8,
                'primary_attributes': ['CHA'],
                'saving_throws': ['DEX', 'CHA'],
                'skill_choices': 3,
                'skill_options': ['Acrobatics', 'Animal Handling', 'Arcana', 'Athletics', 'Deception', 'History', 'Insight', 'Intimidation', 'Investigation', 'Medicine', 'Nature', 'Perception', 'Performance', 'Persuasion', 'Religion', 'Sleight of Hand', 'Stealth', 'Survival']
            },
            'Sorcerer': {
                'hit_die': 6,
                'primary_attributes': ['CHA'],
                'saving_throws': ['CON', 'CHA'],
                'skill_choices': 2,
                'skill_options': ['Arcana', 'Deception', 'Insight', 'Intimidation', 'Persuasion', 'Religion']
            },
            'Warlock': {
                'hit_die': 8,
                'primary_attributes': ['CHA'],
                'saving_throws': ['WIS', 'CHA'],
                'skill_choices': 2,
                'skill_options': ['Arcana', 'Deception', 'History', 'Intimidation', 'Investigation', 'Nature', 'Religion']
            },
            'Monk': {
                'hit_die': 8,
                'primary_attributes': ['DEX', 'WIS'],
                'saving_throws': ['STR', 'DEX'],
                'skill_choices': 2,
                'skill_options': ['Acrobatics', 'Athletics', 'History', 'Insight', 'Religion', 'Stealth']
            },
            'Druid': {
                'hit_die': 8,
                'primary_attributes': ['WIS'],
                'saving_throws': ['INT', 'WIS'],
                'skill_choices': 2,
                'skill_options': ['Animal Handling', 'Arcana', 'Insight', 'Medicine', 'Nature', 'Perception', 'Religion', 'Survival']
            },
            'Barbarian': {
                'hit_die': 12,
                'primary_attributes': ['STR'],
                'saving_throws': ['STR', 'CON'],
                'skill_choices': 2,
                'skill_options': ['Animal Handling', 'Athletics', 'Intimidation', 'Nature', 'Perception', 'Survival']
            }
        }
        
        # Backgrounds del SRD (System Reference Document)
        self.backgrounds = {
            'Acolyte': {
                'skill_proficiencies': ['Insight', 'Religion'],
                'tool_proficiencies': [],
                'languages': 2,
                'equipment': ['Holy symbol', 'Prayer book', 'Incense', 'Vestments', 'Common clothes', '15 gp']
            },
            'Criminal': {
                'skill_proficiencies': ['Deception', 'Stealth'],
                'tool_proficiencies': ['Thieves\' tools', 'Gaming set'],
                'languages': 0,
                'equipment': ['Crowbar', 'Dark common clothes', '15 gp']
            },
            'Folk Hero': {
                'skill_proficiencies': ['Animal Handling', 'Survival'],
                'tool_proficiencies': ['Artisan\'s tools', 'Vehicles (land)'],
                'languages': 0,
                'equipment': ['Artisan\'s tools', 'Shovel', 'Iron pot', 'Common clothes', '10 gp']
            },
            'Noble': {
                'skill_proficiencies': ['History', 'Persuasion'],
                'tool_proficiencies': ['Gaming set'],
                'languages': 1,
                'equipment': ['Fine clothes', 'Signet ring', 'Scroll of pedigree', '25 gp']
            },
            'Sage': {
                'skill_proficiencies': ['Arcana', 'History'],
                'tool_proficiencies': [],
                'languages': 2,
                'equipment': ['Bottle of black ink', 'Quill', 'Small knife', 'Letter from dead colleague', 'Common clothes', '10 gp']
            },
            'Soldier': {
                'skill_proficiencies': ['Athletics', 'Intimidation'],
                'tool_proficiencies': ['Gaming set', 'Vehicles (land)'],
                'languages': 0,
                'equipment': ['Insignia of rank', 'Trophy from fallen enemy', 'Gaming set', 'Common clothes', '10 gp']
            },
            'Entertainer': {
                'skill_proficiencies': ['Acrobatics', 'Performance'],
                'tool_proficiencies': ['Disguise kit', 'Musical instrument'],
                'languages': 0,
                'equipment': ['Musical instrument', 'Costume', 'Admirer\'s favor', '15 gp']
            },
            'Guild Artisan': {
                'skill_proficiencies': ['Insight', 'Persuasion'],
                'tool_proficiencies': ['Artisan\'s tools'],
                'languages': 1,
                'equipment': ['Artisan\'s tools', 'Letter of introduction', 'Traveler\'s clothes', '15 gp']
            },
            'Hermit': {
                'skill_proficiencies': ['Medicine', 'Religion'],
                'tool_proficiencies': ['Herbalism kit'],
                'languages': 1,
                'equipment': ['Scroll case', 'Blanket', 'Winter clothes', 'Herbalism kit', '5 gp']
            },
            'Outlander': {
                'skill_proficiencies': ['Athletics', 'Survival'],
                'tool_proficiencies': ['Musical instrument'],
                'languages': 1,
                'equipment': ['Staff', 'Hunting trap', 'Trophy from animal', 'Traveler\'s clothes', '10 gp']
            },
            'Urchin': {
                'skill_proficiencies': ['Sleight of Hand', 'Stealth'],
                'tool_proficiencies': ['Disguise kit', 'Thieves\' tools'],
                'languages': 0,
                'equipment': ['Small knife', 'Map of home city', 'Pet mouse', 'Token from parents', 'Common clothes', '10 gp']
            }
        }
        
        # Hechizos del SRD por clase
        self.spells_by_class = {
            'Wizard': ['Magic Missile', 'Shield', 'Mage Armor', 'Detect Magic', 'Comprehend Languages'],
            'Cleric': ['Cure Wounds', 'Bless', 'Detect Magic', 'Guidance', 'Sacred Flame'],
            'Bard': ['Vicious Mockery', 'Cure Wounds', 'Disguise Self', 'Faerie Fire', 'Healing Word'],
            'Sorcerer': ['Fire Bolt', 'Shield', 'Mage Armor', 'Burning Hands', 'Charm Person'],
            'Warlock': ['Eldritch Blast', 'Armor of Agathys', 'Hex', 'Hellish Rebuke', 'Misty Step'],
            'Druid': ['Produce Flame', 'Cure Wounds', 'Entangle', 'Goodberry', 'Thunderwave'],
            'Paladin': ['Cure Wounds', 'Divine Favor', 'Bless', 'Detect Evil and Good', 'Shield of Faith'],
            'Ranger': ['Cure Wounds', 'Hunter\'s Mark', 'Goodberry', 'Speak with Animals', 'Animal Friendship']
        }
    
    def roll_attributes(self) -> Dict[str, int]:
        """Generate attributes using 4d6 drop lowest method"""
        attributes = {}
        for attr in ['STR', 'DEX', 'CON', 'INT', 'WIS', 'CHA']:
            rolls = [random.randint(1, 6) for _ in range(4)]
            rolls.remove(min(rolls))  # Drop lowest
            attributes[attr] = sum(rolls)
        return attributes

    def get_recommended_attributes(self, char_class: str, race: str = None) -> Dict[str, int]:
        """Get recommended attributes based on class and race"""
        # Point buy costs: 8=0, 9=1, 10=2, 11=3, 12=4, 13=5, 14=7, 15=9
        point_costs = {8: 0, 9: 1, 10: 2, 11: 3, 12: 4, 13: 5, 14: 7, 15: 9}
        
        # Standard Arrays from D&D 5e SRD
        standard_arrays = [
            {'STR': 15, 'DEX': 14, 'CON': 13, 'INT': 12, 'WIS': 10, 'CHA': 8},   # 9+7+5+4+2+0 = 27
            {'STR': 15, 'DEX': 13, 'CON': 14, 'INT': 12, 'WIS': 10, 'CHA': 8},   # 9+5+7+4+2+0 = 27
            {'STR': 15, 'DEX': 12, 'CON': 14, 'INT': 13, 'WIS': 10, 'CHA': 8},   # 9+4+7+5+2+0 = 27
            {'STR': 14, 'DEX': 15, 'CON': 13, 'INT': 12, 'WIS': 10, 'CHA': 8},   # 7+9+5+4+2+0 = 27
            {'STR': 14, 'DEX': 13, 'CON': 15, 'INT': 12, 'WIS': 10, 'CHA': 8},   # 7+5+9+4+2+0 = 27
            {'STR': 13, 'DEX': 15, 'CON': 14, 'INT': 12, 'WIS': 10, 'CHA': 8},   # 5+9+7+4+2+0 = 27
            {'STR': 12, 'DEX': 15, 'CON': 14, 'INT': 13, 'WIS': 10, 'CHA': 8},   # 4+9+7+5+2+0 = 27
            {'STR': 8, 'DEX': 15, 'CON': 14, 'INT': 15, 'WIS': 12, 'CHA': 10},   # 0+9+7+9+4+2 = 31 (Wizard)
            {'STR': 8, 'DEX': 12, 'CON': 15, 'INT': 15, 'WIS': 12, 'CHA': 10},   # 0+4+9+9+4+2 = 28 (Wizard)
            {'STR': 8, 'DEX': 12, 'CON': 14, 'INT': 15, 'WIS': 13, 'CHA': 10},   # 0+4+7+9+5+2 = 27 (Wizard)
        ]
        
        # Standard array presets for different playstyles (all use exactly 27 points)
        # These are BASE scores only - racial bonuses are applied separately
        presets = {
            'Fighter': {
                'balanced': {'STR': 15, 'DEX': 14, 'CON': 14, 'INT': 8, 'WIS': 10, 'CHA': 10},  # 9+7+7+0+2+2 = 27
                'strength': {'STR': 15, 'DEX': 14, 'CON': 14, 'INT': 8, 'WIS': 8, 'CHA': 12},  # 9+7+7+0+0+4 = 27
                'defensive': {'STR': 15, 'DEX': 12, 'CON': 15, 'INT': 8, 'WIS': 10, 'CHA': 11}  # 9+4+9+0+2+3 = 27
            },
            'Wizard': {
                'balanced': {'STR': 8, 'DEX': 12, 'CON': 14, 'INT': 15, 'WIS': 12, 'CHA': 11},  # 0+4+7+9+4+3 = 27
                'evoker': {'STR': 8, 'DEX': 10, 'CON': 14, 'INT': 15, 'WIS': 13, 'CHA': 12},    # 0+2+7+9+5+4 = 27
                'utility': {'STR': 8, 'DEX': 12, 'CON': 13, 'INT': 15, 'WIS': 12, 'CHA': 13}   # 0+4+5+9+4+5 = 27
            },
            'Cleric': {
                'balanced': {'STR': 12, 'DEX': 10, 'CON': 14, 'INT': 12, 'WIS': 15, 'CHA': 9},  # 4+2+7+4+9+1 = 27
                'healer': {'STR': 12, 'DEX': 10, 'CON': 14, 'INT': 12, 'WIS': 15, 'CHA': 9},    # 4+2+7+4+9+1 = 27
                'warrior': {'STR': 14, 'DEX': 10, 'CON': 14, 'INT': 8, 'WIS': 15, 'CHA': 10}     # 7+2+7+0+9+2 = 27
            },
            'Rogue': {
                'balanced': {'STR': 10, 'DEX': 15, 'CON': 13, 'INT': 12, 'WIS': 12, 'CHA': 11},  # 2+9+5+4+4+3 = 27
                'assassin': {'STR': 12, 'DEX': 15, 'CON': 13, 'INT': 13, 'WIS': 8, 'CHA': 12},   # 4+9+5+5+0+4 = 27
                'scout': {'STR': 8, 'DEX': 15, 'CON': 13, 'INT': 12, 'WIS': 12, 'CHA': 13}      # 0+9+5+4+4+5 = 27
            },
            'Ranger': {
                'balanced': {'STR': 12, 'DEX': 15, 'CON': 12, 'INT': 10, 'WIS': 13, 'CHA': 11},  # 4+9+4+2+5+3 = 27
                'archer': {'STR': 8, 'DEX': 15, 'CON': 13, 'INT': 12, 'WIS': 12, 'CHA': 13},    # 0+9+5+4+4+5 = 27
                'beastmaster': {'STR': 12, 'DEX': 12, 'CON': 13, 'INT': 10, 'WIS': 15, 'CHA': 11} # 4+4+5+2+9+3 = 27
            },
            'Paladin': {
                'balanced': {'STR': 15, 'DEX': 10, 'CON': 13, 'INT': 8, 'WIS': 12, 'CHA': 14},  # 9+2+5+0+4+7 = 27
                'tank': {'STR': 15, 'DEX': 8, 'CON': 14, 'INT': 10, 'WIS': 12, 'CHA': 13},      # 9+0+7+2+4+5 = 27
                'charismatic': {'STR': 13, 'DEX': 10, 'CON': 13, 'INT': 8, 'WIS': 12, 'CHA': 16} # 5+2+5+0+4+11 = 27
            },
            'Bard': {
                'balanced': {'STR': 8, 'DEX': 12, 'CON': 13, 'INT': 12, 'WIS': 11, 'CHA': 16},  # 0+4+5+4+3+11 = 27
                'lore': {'STR': 8, 'DEX': 12, 'CON': 12, 'INT': 13, 'WIS': 11, 'CHA': 16},      # 0+4+4+5+3+11 = 27
                'valor': {'STR': 12, 'DEX': 12, 'CON': 13, 'INT': 10, 'WIS': 9, 'CHA': 16}      # 4+4+5+2+1+11 = 27
            },
            'Sorcerer': {
                'balanced': {'STR': 8, 'DEX': 12, 'CON': 14, 'INT': 12, 'WIS': 11, 'CHA': 15},  # 0+4+7+4+3+9 = 27
                'damage': {'STR': 8, 'DEX': 12, 'CON': 14, 'INT': 10, 'WIS': 13, 'CHA': 15},    # 0+4+7+2+5+9 = 27
                'control': {'STR': 8, 'DEX': 12, 'CON': 13, 'INT': 12, 'WIS': 11, 'CHA': 16}    # 0+4+5+4+3+11 = 27
            },
            'Warlock': {
                'balanced': {'STR': 8, 'DEX': 12, 'CON': 14, 'INT': 12, 'WIS': 11, 'CHA': 15},  # 0+4+7+4+3+9 = 27
                'blaster': {'STR': 8, 'DEX': 12, 'CON': 14, 'INT': 10, 'WIS': 13, 'CHA': 15},   # 0+4+7+2+5+9 = 27
                'utility': {'STR': 8, 'DEX': 12, 'CON': 13, 'INT': 12, 'WIS': 11, 'CHA': 16}    # 0+4+5+4+3+11 = 27
            },
            'Monk': {
                'balanced': {'STR': 12, 'DEX': 15, 'CON': 13, 'INT': 10, 'WIS': 12, 'CHA': 11},  # 4+9+5+2+4+3 = 27
                'striker': {'STR': 12, 'DEX': 15, 'CON': 13, 'INT': 8, 'WIS': 12, 'CHA': 13},   # 4+9+5+0+4+5 = 27
                'defensive': {'STR': 10, 'DEX': 15, 'CON': 13, 'INT': 12, 'WIS': 12, 'CHA': 11}  # 2+9+5+4+4+3 = 27
            },
            'Druid': {
                'balanced': {'STR': 12, 'DEX': 12, 'CON': 14, 'INT': 10, 'WIS': 15, 'CHA': 9},  # 4+4+7+2+9+1 = 27
                'caster': {'STR': 8, 'DEX': 12, 'CON': 14, 'INT': 12, 'WIS': 15, 'CHA': 11},    # 0+4+7+4+9+3 = 27
                'shapeshifter': {'STR': 12, 'DEX': 12, 'CON': 14, 'INT': 10, 'WIS': 15, 'CHA': 9} # 4+4+7+2+9+1 = 27
            },
            'Barbarian': {
                'balanced': {'STR': 15, 'DEX': 14, 'CON': 14, 'INT': 8, 'WIS': 10, 'CHA': 10},  # 9+7+7+0+2+2 = 27
                'berserker': {'STR': 15, 'DEX': 14, 'CON': 14, 'INT': 8, 'WIS': 8, 'CHA': 12}, # 9+7+7+0+0+4 = 27
                'tank': {'STR': 15, 'DEX': 13, 'CON': 14, 'INT': 8, 'WIS': 10, 'CHA': 12}      # 9+5+7+0+2+4 = 27
            }
        }
        
        # Choose between standard arrays and presets
        if random.random() < 0.3:  # 30% chance to use standard array
            chosen_array = random.choice(standard_arrays)
            # Validate that the array uses exactly 27 points
            total_cost = sum(point_costs.get(value, 0) for value in chosen_array.values())
            if total_cost != 27:
                print(f"Warning: Standard array uses {total_cost} points instead of 27")
            
            return {
                'STR': chosen_array['STR'],
                'DEX': chosen_array['DEX'],
                'CON': chosen_array['CON'],
                'INT': chosen_array['INT'],
                'WIS': chosen_array['WIS'],
                'CHA': chosen_array['CHA']
            }
        
        if char_class in presets:
            # Choose a random preset for the class
            preset_names = list(presets[char_class].keys())
            chosen_preset = random.choice(preset_names)
            chosen_attributes = presets[char_class][chosen_preset]
            
            # Validate that the preset uses exactly 27 points
            total_cost = sum(point_costs.get(value, 0) for value in chosen_attributes.values())
            if total_cost != 27:
                print(f"Warning: {char_class} {chosen_preset} preset uses {total_cost} points instead of 27")
            
            # Return attributes in standard order: STR, DEX, CON, INT, WIS, CHA
            # These are BASE scores only - racial bonuses will be applied separately
            return {
                'STR': chosen_attributes['STR'],
                'DEX': chosen_attributes['DEX'],
                'CON': chosen_attributes['CON'],
                'INT': chosen_attributes['INT'],
                'WIS': chosen_attributes['WIS'],
                'CHA': chosen_attributes['CHA']
            }
        
        # Fallback to standard array if class not found
        return {'STR': 13, 'DEX': 13, 'CON': 13, 'INT': 12, 'WIS': 12, 'CHA': 12}
    
    def get_base_attributes(self, char_class: str, race: str = None) -> Dict[str, int]:
        """Get base attributes without racial bonuses"""
        return self.get_recommended_attributes(char_class, race)
    
    def fill_character(self, character: Character):
        """Autofill all character data"""
        # Generate attributes if not provided
        if not character.attributes:
            # Use recommended attributes instead of random rolls
            character.attributes = self.get_recommended_attributes(character.char_class, character.race)
        
        # Apply racial bonuses to existing attributes
        if character.race in self.races:
            race_bonuses = self.races[character.race]['ability_bonus']
            for attr, bonus in race_bonuses.items():
                if attr in character.attributes:
                    character.attributes[attr] += bonus
        
        # Select class skills if not provided
        if not character.skills and character.char_class in self.classes:
            class_data = self.classes[character.char_class]
            skill_options = class_data['skill_options']
            skill_choices = class_data['skill_choices']
            
            # Select skills randomly but in a consistent order
            selected_class_skills = random.sample(skill_options, min(skill_choices, len(skill_options)))
            
            # Add background skills first (they come first in the list)
            character.skills = []
            if character.background in self.backgrounds:
                background_skills = self.backgrounds[character.background]['skill_proficiencies']
                character.skills.extend(background_skills)
            
            # Then add class skills
            character.skills.extend(selected_class_skills)
        
        # Add spells if class has them and not provided
        if not character.spells and self.spell_manager.can_cast_spells(character.char_class):
            spell_suggestions = self.spell_manager.get_spell_suggestions(character.char_class)
            character.spells = spell_suggestions['cantrips'] + spell_suggestions['spells']
        
        # Generate personality traits if not provided
        if not character.personality_traits:
            character.personality_traits = self.generate_personality_traits(character)
    
    def generate_personality_traits(self, character: Character) -> str:
        """Generate personality traits based on class and race"""
        traits = []
        
        # Traits by class
        class_traits = {
            'Fighter': ['Brave', 'Disciplined', 'Protector'],
            'Wizard': ['Curious', 'Intellectual', 'Mysterious'],
            'Cleric': ['Devout', 'Compassionate', 'Inspiring'],
            'Rogue': ['Cunning', 'Independent', 'Opportunistic'],
            'Ranger': ['Observant', 'Practical', 'Nature protector'],
            'Paladin': ['Honorable', 'Just', 'Inspiring'],
            'Bard': ['Charismatic', 'Artistic', 'Sociable'],
            'Sorcerer': ['Mysterious', 'Charismatic', 'Unpredictable'],
            'Warlock': ['Mysterious', 'Ambitious', 'Pragmatic'],
            'Monk': ['Disciplined', 'Peaceful', 'Philosophical'],
            'Druid': ['Nature-connected', 'Wise', 'Protector'],
            'Barbarian': ['Fierce', 'Loyal', 'Direct']
        }
        
        # Traits by race
        race_traits = {
            'Human': ['Adaptable', 'Ambitious'],
            'Elf': ['Elegant', 'Long-lived', 'Magic-connected'],
            'Dwarf': ['Resilient', 'Hardworking', 'Honorable'],
            'Halfling': ['Optimistic', 'Agile', 'Sociable'],
            'Dragonborn': ['Proud', 'Brave', 'Honorable'],
            'Tiefling': ['Mysterious', 'Charismatic', 'Resilient'],
            'Half-Elf': ['Adaptable', 'Diplomatic'],
            'Half-Orc': ['Strong', 'Loyal', 'Direct'],
            'Gnome': ['Curious', 'Inventive', 'Cheerful']
        }
        
        # Select traits
        if character.char_class in class_traits:
            traits.extend(random.sample(class_traits[character.char_class], 2))
        
        if character.race in race_traits:
            traits.extend(random.sample(race_traits[character.race], 2))
        
        return ', '.join(traits) 

    def get_primary_attributes(self, char_class: str) -> Dict[str, str]:
        """Get primary attributes for each class with descriptions"""
        primary_attributes = {
            'Fighter': {
                'STR': 'Primary attack and damage',
                'CON': 'Hit points and survivability',
                'DEX': 'Armor class and initiative'
            },
            'Wizard': {
                'INT': 'Spellcasting and spell save DC',
                'CON': 'Hit points and concentration',
                'DEX': 'Armor class and initiative'
            },
            'Cleric': {
                'WIS': 'Spellcasting and spell save DC',
                'CON': 'Hit points and concentration',
                'STR': 'Melee combat and armor'
            },
            'Rogue': {
                'DEX': 'Attack, damage, armor class, and skills',
                'CON': 'Hit points and survivability',
                'INT': 'Skill checks and expertise'
            },
            'Ranger': {
                'DEX': 'Ranged combat and armor class',
                'WIS': 'Spellcasting and perception',
                'CON': 'Hit points and concentration'
            },
            'Paladin': {
                'STR': 'Melee combat and damage',
                'CHA': 'Spellcasting and class features',
                'CON': 'Hit points and survivability'
            },
            'Bard': {
                'CHA': 'Spellcasting and inspiration',
                'DEX': 'Armor class and initiative',
                'CON': 'Hit points and concentration'
            },
            'Sorcerer': {
                'CHA': 'Spellcasting and spell save DC',
                'CON': 'Hit points and concentration',
                'DEX': 'Armor class and initiative'
            },
            'Warlock': {
                'CHA': 'Spellcasting and spell save DC',
                'CON': 'Hit points and concentration',
                'DEX': 'Armor class and initiative'
            },
            'Monk': {
                'DEX': 'Attack, damage, and armor class',
                'WIS': 'Armor class and class features',
                'CON': 'Hit points and survivability'
            },
            'Druid': {
                'WIS': 'Spellcasting and spell save DC',
                'CON': 'Hit points and concentration',
                'DEX': 'Armor class and initiative'
            },
            'Barbarian': {
                'STR': 'Attack and damage',
                'CON': 'Hit points and rage benefits',
                'DEX': 'Armor class and initiative'
            }
        }
        
        return primary_attributes.get(char_class, {}) 

    def get_suggestions(self, char_class: str, background: str, race: str = None) -> Dict:
        """Get autofill suggestions that respect available skills"""
        # Get base attributes without racial bonuses
        base_attributes = self.get_recommended_attributes(char_class, race)
        
        # Get available skills for the class
        class_skills = []
        if char_class in self.classes:
            class_skills = self.classes[char_class]['skill_options']
        
        # Get background skills
        background_skills = []
        if background in self.backgrounds:
            background_skills = self.backgrounds[background]['skill_proficiencies']
        
        # Select class skills (excluding background skills to avoid duplicates)
        selected_class_skills = []
        if char_class in self.classes:
            class_data = self.classes[char_class]
            skill_choices = class_data['skill_choices']
            available_class_skills = [skill for skill in class_skills if skill not in background_skills]
            
            # Select skills that are available for the class
            if len(available_class_skills) >= skill_choices:
                selected_class_skills = random.sample(available_class_skills, skill_choices)
            else:
                selected_class_skills = available_class_skills
        
        # Combine background and class skills
        all_skills = background_skills + selected_class_skills
        
        # Get spells if applicable
        spells = []
        if self.spell_manager.can_cast_spells(char_class):
            spell_suggestions = self.spell_manager.get_spell_suggestions(char_class)
            spells = spell_suggestions['cantrips'] + spell_suggestions['spells']
        
        return {
            'attributes': base_attributes,
            'skills': all_skills,
            'spells': spells
        } 
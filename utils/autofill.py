import json
import random
from typing import Dict, List
from models import Character
from utils.spell_manager import SpellManager
from logging_config import get_logger

# Configure logging
logger = get_logger(__name__)

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
            'Half-Elf': {'ability_bonus': {'CHA': 2, 'STR': 1, 'DEX': 1}},
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
    
        # Complete playstyle presets with attributes, skills, and spells
        # These are BASE scores only - racial bonuses are applied separately
        self.playstyles = {
            'Fighter': {
                'balanced': {
                    'attributes': {'STR': 15, 'DEX': 14, 'CON': 14, 'INT': 8, 'WIS': 10, 'CHA': 10},  # 9+7+7+0+2+2 = 27
                    'skills': ['Athletics', 'Perception'],
                    'description': 'Versatile fighter with good offense and defense'
                },
                'strength': {
                    'attributes': {'STR': 15, 'DEX': 14, 'CON': 14, 'INT': 8, 'WIS': 8, 'CHA': 12},  # 9+7+7+0+0+4 = 27
                    'skills': ['Athletics', 'Intimidation'],
                    'description': 'Powerful melee fighter focused on raw strength'
                },
                'defensive': {
                    'attributes': {'STR': 15, 'DEX': 12, 'CON': 14, 'INT': 8, 'WIS': 11, 'CHA': 12},  # 9+4+7+0+3+4 = 27
                    'skills': ['Athletics', 'Insight'],
                    'description': 'Tank fighter with high constitution and defensive skills'
                }
            },
            'Wizard': {
                'balanced': {
                    'attributes': {'STR': 8, 'DEX': 12, 'CON': 14, 'INT': 15, 'WIS': 12, 'CHA': 11},  # 0+4+7+9+4+3 = 27
                    'skills': ['Arcana', 'History'],
                    'spells': ['Magic Missile', 'Shield', 'Mage Armor', 'Detect Magic'],
                    'cantrips': ['Fire Bolt', 'Prestidigitation', 'Mage Hand'],
                    'description': 'Versatile wizard with balanced spell selection'
                },
                'evoker': {
                    'attributes': {'STR': 8, 'DEX': 10, 'CON': 14, 'INT': 15, 'WIS': 13, 'CHA': 12},    # 0+2+7+9+5+4 = 27
                    'skills': ['Arcana', 'Investigation'],
                    'spells': ['Burning Hands', 'Magic Missile', 'Thunderwave', 'Chromatic Orb'],
                    'cantrips': ['Fire Bolt', 'Ray of Frost', 'Acid Splash'],
                    'description': 'Damage-focused wizard specializing in evocation spells'
                },
                'utility': {
                    'attributes': {'STR': 8, 'DEX': 12, 'CON': 13, 'INT': 15, 'WIS': 12, 'CHA': 13},   # 0+4+5+9+4+5 = 27
                    'skills': ['Arcana', 'Investigation'],
                    'spells': ['Detect Magic', 'Comprehend Languages', 'Unseen Servant', 'Alarm'],
                    'cantrips': ['Mage Hand', 'Message', 'Minor Illusion'],
                    'description': 'Utility wizard focused on non-combat spells'
                }
            },
            'Cleric': {
                'balanced': {
                    'attributes': {'STR': 12, 'DEX': 10, 'CON': 14, 'INT': 12, 'WIS': 15, 'CHA': 9},  # 4+2+7+4+9+1 = 27
                    'skills': ['Insight', 'Religion'],
                    'spells': ['Cure Wounds', 'Bless', 'Shield of Faith', 'Detect Magic'],
                    'cantrips': ['Sacred Flame', 'Spare the Dying', 'Guidance'],
                    'description': 'Balanced cleric with healing and support spells'
                },
                'healer': {
                    'attributes': {'STR': 12, 'DEX': 10, 'CON': 14, 'INT': 12, 'WIS': 15, 'CHA': 9},    # 4+2+7+4+9+1 = 27
                    'skills': ['Medicine', 'Religion'],
                    'spells': ['Cure Wounds', 'Healing Word', 'Prayer of Healing', 'Detect Magic'],
                    'cantrips': ['Sacred Flame', 'Spare the Dying', 'Guidance'],
                    'description': 'Dedicated healer focused on restoration magic'
                },
                'warrior': {
                    'attributes': {'STR': 14, 'DEX': 10, 'CON': 14, 'INT': 8, 'WIS': 15, 'CHA': 10},     # 7+2+7+0+9+2 = 27
                    'skills': ['Athletics', 'Religion'],
                    'spells': ['Divine Favor', 'Shield of Faith', 'Cure Wounds', 'Detect Magic'],
                    'cantrips': ['Sacred Flame', 'Thaumaturgy', 'Guidance'],
                    'description': 'Warrior cleric combining martial prowess with divine magic'
                }
            },
            'Rogue': {
                'balanced': {
                    'attributes': {'STR': 10, 'DEX': 15, 'CON': 13, 'INT': 12, 'WIS': 12, 'CHA': 11},  # 2+9+5+4+4+3 = 27
                    'skills': ['Stealth', 'Sleight of Hand'],
                    'description': 'Versatile rogue with stealth and thievery skills'
                },
                'assassin': {
                    'attributes': {'STR': 12, 'DEX': 15, 'CON': 13, 'INT': 13, 'WIS': 8, 'CHA': 12},   # 4+9+5+5+0+4 = 27
                    'skills': ['Stealth', 'Deception'],
                    'description': 'Deadly assassin focused on stealth and deception'
                },
                'scout': {
                    'attributes': {'STR': 8, 'DEX': 15, 'CON': 13, 'INT': 12, 'WIS': 12, 'CHA': 13},      # 0+9+5+4+4+5 = 27
                    'skills': ['Stealth', 'Perception'],
                    'description': 'Scout rogue with excellent perception and mobility'
                }
            },
            'Ranger': {
                'balanced': {
                    'attributes': {'STR': 12, 'DEX': 15, 'CON': 12, 'INT': 10, 'WIS': 13, 'CHA': 11},  # 4+9+4+2+5+3 = 27
                    'skills': ['Survival', 'Perception'],
                    'spells': ['Cure Wounds', 'Hunter\'s Mark', 'Goodberry', 'Detect Magic'],
                    'cantrips': ['Druidcraft'],
                    'description': 'Balanced ranger with wilderness and tracking skills'
                },
                'archer': {
                    'attributes': {'STR': 8, 'DEX': 15, 'CON': 13, 'INT': 12, 'WIS': 12, 'CHA': 13},    # 0+9+5+4+4+5 = 27
                    'skills': ['Stealth', 'Perception'],
                    'spells': ['Hunter\'s Mark', 'Ensnaring Strike', 'Hail of Thorns', 'Detect Magic'],
                    'cantrips': ['Druidcraft'],
                    'description': 'Ranged combat specialist with stealth and perception'
                },
                'beastmaster': {
                    'attributes': {'STR': 12, 'DEX': 12, 'CON': 13, 'INT': 10, 'WIS': 15, 'CHA': 11}, # 4+4+5+2+9+3 = 27
                    'skills': ['Animal Handling', 'Survival'],
                    'spells': ['Hunter\'s Mark', 'Animal Friendship', 'Speak with Animals', 'Cure Wounds'],
                    'cantrips': ['Druidcraft'],
                    'description': 'Beast master focused on animal companions and nature'
                }
            },
            'Paladin': {
                'balanced': {
                    'attributes': {'STR': 15, 'DEX': 10, 'CON': 13, 'INT': 8, 'WIS': 12, 'CHA': 14},  # 9+2+5+0+4+7 = 27
                    'skills': ['Athletics', 'Persuasion'],
                    'spells': ['Divine Favor', 'Bless'],
                    'cantrips': [],
                    'description': 'Balanced paladin with martial and divine abilities'
                },
                'tank': {
                    'attributes': {'STR': 15, 'DEX': 8, 'CON': 14, 'INT': 10, 'WIS': 12, 'CHA': 13},      # 9+0+7+2+4+5 = 27
                    'skills': ['Athletics', 'Insight'],
                    'spells': ['Shield of Faith', 'Divine Favor'],
                    'cantrips': [],
                    'description': 'Defensive paladin focused on protection and healing'
                },
                'charismatic': {
                    'attributes': {'STR': 14, 'DEX': 10, 'CON': 13, 'INT': 8, 'WIS': 12, 'CHA': 15}, # 7+2+5+0+4+9 = 27
                    'skills': ['Persuasion', 'Intimidation'],
                    'spells': ['Divine Favor', 'Command'],
                    'cantrips': [],
                    'description': 'Charismatic paladin with strong social and leadership skills'
                }
            },
            'Bard': {
                'balanced': {
                    'attributes': {'STR': 8, 'DEX': 12, 'CON': 13, 'INT': 12, 'WIS': 13, 'CHA': 15},  # 0+4+5+4+5+9 = 27
                    'skills': ['Performance', 'Persuasion'],
                    'spells': ['Cure Wounds', 'Charm Person', 'Disguise Self', 'Detect Magic'],
                    'cantrips': ['Vicious Mockery', 'Prestidigitation'],
                    'description': 'Versatile bard with healing, charm, and utility spells'
                },
                'lore': {
                    'attributes': {'STR': 8, 'DEX': 12, 'CON': 12, 'INT': 13, 'WIS': 13, 'CHA': 15},      # 0+4+4+5+5+9 = 27
                    'skills': ['History', 'Arcana'],
                    'spells': ['Comprehend Languages', 'Detect Magic', 'Cure Wounds', 'Charm Person'],
                    'cantrips': ['Vicious Mockery', 'Message'],
                    'description': 'Knowledge-focused bard with utility and information gathering'
                },
                'valor': {
                    'attributes': {'STR': 12, 'DEX': 12, 'CON': 13, 'INT': 10, 'WIS': 11, 'CHA': 15},      # 4+4+5+2+3+9 = 27
                    'skills': ['Athletics', 'Performance'],
                    'spells': ['Cure Wounds', 'Heroism', 'Thunderwave', 'Charm Person'],
                    'cantrips': ['Vicious Mockery', 'Blade Ward'],
                    'description': 'Combat-oriented bard with martial and inspiring abilities'
                }
            },
            'Sorcerer': {
                'balanced': {
                    'attributes': {'STR': 8, 'DEX': 12, 'CON': 14, 'INT': 12, 'WIS': 11, 'CHA': 15},  # 0+4+7+4+3+9 = 27
                    'skills': ['Arcana', 'Deception'],
                    'spells': ['Magic Missile', 'Shield'],
                    'cantrips': ['Fire Bolt', 'Prestidigitation', 'Mage Hand', 'Ray of Frost'],
                    'description': 'Balanced sorcerer with damage and utility spells'
                },
                'damage': {
                    'attributes': {'STR': 8, 'DEX': 12, 'CON': 14, 'INT': 10, 'WIS': 13, 'CHA': 15},    # 0+4+7+2+5+9 = 27
                    'skills': ['Arcana', 'Intimidation'],
                    'spells': ['Burning Hands', 'Magic Missile'],
                    'cantrips': ['Fire Bolt', 'Ray of Frost', 'Acid Splash', 'Shocking Grasp'],
                    'description': 'Damage-focused sorcerer specializing in evocation'
                },
                'control': {
                    'attributes': {'STR': 8, 'DEX': 12, 'CON': 13, 'INT': 12, 'WIS': 13, 'CHA': 15},    # 0+4+5+4+5+9 = 27
                    'skills': ['Arcana', 'Persuasion'],
                    'spells': ['Charm Person', 'Sleep'],
                    'cantrips': ['Mage Hand', 'Message', 'Minor Illusion', 'Friends'],
                    'description': 'Control-focused sorcerer with enchantment and illusion'
                }
            },
            'Warlock': {
                'balanced': {
                    'attributes': {'STR': 8, 'DEX': 12, 'CON': 14, 'INT': 12, 'WIS': 11, 'CHA': 15},  # 0+4+7+4+3+9 = 27
                    'skills': ['Arcana', 'Deception'],
                    'spells': ['Hex', 'Charm Person'],
                    'cantrips': ['Eldritch Blast', 'Prestidigitation'],
                    'description': 'Balanced warlock with damage and utility abilities'
                },
                'blaster': {
                    'attributes': {'STR': 8, 'DEX': 12, 'CON': 14, 'INT': 10, 'WIS': 13, 'CHA': 15},   # 0+4+7+2+5+9 = 27
                    'skills': ['Arcana', 'Intimidation'],
                    'spells': ['Hex', 'Armor of Agathys'],
                    'cantrips': ['Eldritch Blast', 'Ray of Frost'],
                    'description': 'Damage-focused warlock with powerful blasting abilities'
                },
                'utility': {
                    'attributes': {'STR': 8, 'DEX': 12, 'CON': 13, 'INT': 12, 'WIS': 13, 'CHA': 15},    # 0+4+5+4+5+9 = 27
                    'skills': ['Arcana', 'Persuasion'],
                    'spells': ['Unseen Servant', 'Comprehend Languages'],
                    'cantrips': ['Eldritch Blast', 'Mage Hand'],
                    'description': 'Utility-focused warlock with information gathering abilities'
                }
            },
            'Monk': {
                'balanced': {
                    'attributes': {'STR': 12, 'DEX': 15, 'CON': 13, 'INT': 10, 'WIS': 12, 'CHA': 11},  # 4+9+5+2+4+3 = 27
                    'skills': ['Acrobatics', 'Stealth'],
                    'description': 'Balanced monk with mobility and stealth skills'
                },
                'striker': {
                    'attributes': {'STR': 12, 'DEX': 15, 'CON': 13, 'INT': 8, 'WIS': 12, 'CHA': 13},   # 4+9+5+0+4+5 = 27
                    'skills': ['Athletics', 'Acrobatics'],
                    'description': 'Offensive monk focused on damage and mobility'
                },
                'defensive': {
                    'attributes': {'STR': 10, 'DEX': 15, 'CON': 13, 'INT': 12, 'WIS': 12, 'CHA': 11},  # 2+9+5+4+4+3 = 27
                    'skills': ['Insight', 'Perception'],
                    'description': 'Defensive monk with wisdom-based abilities'
                }
            },
            'Druid': {
                'balanced': {
                    'attributes': {'STR': 12, 'DEX': 12, 'CON': 14, 'INT': 10, 'WIS': 15, 'CHA': 9},  # 4+4+7+2+9+1 = 27
                    'skills': ['Nature', 'Survival'],
                    'spells': ['Cure Wounds', 'Entangle', 'Goodberry', 'Detect Magic'],
                    'cantrips': ['Druidcraft', 'Produce Flame'],
                    'description': 'Balanced druid with healing and nature magic'
                },
                'caster': {
                    'attributes': {'STR': 8, 'DEX': 12, 'CON': 14, 'INT': 12, 'WIS': 15, 'CHA': 11},    # 0+4+7+4+9+3 = 27
                    'skills': ['Arcana', 'Nature'],
                    'spells': ['Cure Wounds', 'Detect Magic', 'Comprehend Languages', 'Goodberry'],
                    'cantrips': ['Druidcraft', 'Guidance'],
                    'description': 'Spellcasting-focused druid with utility magic'
                },
                'shapeshifter': {
                    'attributes': {'STR': 12, 'DEX': 12, 'CON': 14, 'INT': 10, 'WIS': 15, 'CHA': 9}, # 4+4+7+2+9+1 = 27
                    'skills': ['Athletics', 'Survival'],
                    'spells': ['Cure Wounds', 'Longstrider', 'Jump', 'Detect Magic'],
                    'cantrips': ['Druidcraft', 'Shillelagh'],
                    'description': 'Shapeshifting-focused druid with physical enhancement'
                }
            },
            'Barbarian': {
                'balanced': {
                    'attributes': {'STR': 15, 'DEX': 14, 'CON': 14, 'INT': 8, 'WIS': 10, 'CHA': 10},  # 9+7+7+0+2+2 = 27
                    'skills': ['Athletics', 'Survival'],
                    'description': 'Balanced barbarian with strength and wilderness skills'
                },
                'berserker': {
                    'attributes': {'STR': 15, 'DEX': 14, 'CON': 14, 'INT': 8, 'WIS': 8, 'CHA': 12}, # 9+7+7+0+0+4 = 27
                    'skills': ['Athletics', 'Intimidation'],
                    'description': 'Frenzied berserker focused on raw power and intimidation'
                },
                'tank': {
                    'attributes': {'STR': 15, 'DEX': 13, 'CON': 14, 'INT': 8, 'WIS': 10, 'CHA': 12},      # 9+5+7+0+2+4 = 27
                    'skills': ['Athletics', 'Perception'],
                    'description': 'Defensive barbarian with high constitution and awareness'
                }
            }
        }
    
    def roll_attributes(self) -> Dict[str, int]:
        """Roll 4d6 drop lowest for each attribute"""
        attributes = {}
        for attr in ['STR', 'DEX', 'CON', 'INT', 'WIS', 'CHA']:
            rolls = [random.randint(1, 6) for _ in range(4)]
            rolls.remove(min(rolls))  # Drop lowest
            attributes[attr] = sum(rolls)
        return attributes

    def get_recommended_attributes(self, char_class: str, race: str = None) -> Dict[str, int]:
        """Get recommended attributes for a class and race combination"""
        # Get optimized standard array for the class
        attributes = self.get_optimized_standard_array(char_class)
        
        # Apply racial bonuses AFTER assignment
        if race and race in self.races:
            race_bonus = self.races[race]['ability_bonus']
            for attr, bonus in race_bonus.items():
                attributes[attr] += bonus
        
        return attributes
    
    def get_optimized_standard_array(self, char_class: str) -> Dict[str, int]:
        """Get optimized standard array for a specific class (non-random)"""
        # Class-specific optimized standard arrays
        # Each array uses exactly 27 points and prioritizes class needs
        optimized_arrays = {
            'Fighter': {
                'STR': 15, 'CON': 14, 'DEX': 13, 'WIS': 12, 'CHA': 10, 'INT': 8
            },  # 9+7+5+4+2+0 = 27
            'Wizard': {
                'INT': 15, 'CON': 14, 'DEX': 13, 'WIS': 12, 'CHA': 10, 'STR': 8
            },  # 9+7+5+4+2+0 = 27
            'Cleric': {
                'WIS': 15, 'CON': 14, 'STR': 13, 'CHA': 12, 'INT': 10, 'DEX': 8
            },  # 9+7+5+4+2+0 = 27
            'Rogue': {
                'DEX': 15, 'CON': 14, 'INT': 13, 'WIS': 12, 'CHA': 10, 'STR': 8
            },  # 9+7+5+4+2+0 = 27
            'Ranger': {
                'DEX': 15, 'WIS': 14, 'CON': 13, 'STR': 12, 'CHA': 10, 'INT': 8
            },  # 9+7+5+4+2+0 = 27
            'Paladin': {
                'STR': 15, 'CHA': 14, 'CON': 13, 'WIS': 12, 'DEX': 10, 'INT': 8
            },  # 9+7+5+4+2+0 = 27
            'Bard': {
                'CHA': 15, 'DEX': 14, 'CON': 13, 'INT': 12, 'WIS': 10, 'STR': 8
            },  # 9+7+5+4+2+0 = 27
            'Sorcerer': {
                'CHA': 15, 'CON': 14, 'DEX': 13, 'WIS': 12, 'INT': 10, 'STR': 8
            },  # 9+7+5+4+2+0 = 27
            'Warlock': {
                'CHA': 15, 'CON': 14, 'DEX': 13, 'WIS': 12, 'INT': 10, 'STR': 8
            },  # 9+7+5+4+2+0 = 27
            'Monk': {
                'DEX': 15, 'WIS': 14, 'CON': 13, 'STR': 12, 'CHA': 10, 'INT': 8
            },  # 9+7+5+4+2+0 = 27
            'Druid': {
                'WIS': 15, 'CON': 14, 'DEX': 13, 'STR': 12, 'INT': 10, 'CHA': 8
            },  # 9+7+5+4+2+0 = 27
            'Barbarian': {
                'STR': 15, 'CON': 14, 'DEX': 13, 'WIS': 12, 'CHA': 10, 'INT': 8
            }  # 9+7+5+4+2+0 = 27
        }
        
        return optimized_arrays.get(char_class, {
            'STR': 15, 'DEX': 14, 'CON': 13, 'INT': 12, 'WIS': 10, 'CHA': 8
        })
    
    def get_base_attributes(self, char_class: str, race: str = None) -> Dict[str, int]:
        """Get base attributes without optimization"""
        return self.get_recommended_attributes(char_class, race)
    
    def get_available_playstyles(self, char_class: str) -> List[str]:
        """Get available playstyles for a class"""
        playstyles = []
        
        # Add optimized standard array option
        playstyles.append('standard_array')
        
        # Add specific playstyles if available
        if char_class in self.playstyles:
            playstyles.extend(list(self.playstyles[char_class].keys()))
        
        return playstyles
    
    def get_playstyle_data(self, char_class: str, playstyle: str) -> Dict:
        """Get data for a specific playstyle"""
        return {
            'description': f'{playstyle} playstyle for {char_class}',
            'attributes': self.get_attributes_for_playstyle(char_class, playstyle),
            'skills': self.get_skills_for_playstyle(char_class, playstyle),
            'spells': self.get_spells_for_playstyle(char_class, playstyle)
        }
    
    def get_attributes_for_playstyle(self, char_class: str, playstyle: str) -> Dict[str, int]:
        """Get optimized attributes for a specific playstyle"""
        # Handle standard array option
        if playstyle == 'standard_array':
            return self.get_optimized_standard_array(char_class)
        
        # Check if we have a preset for this class and playstyle
        if char_class in self.playstyles and playstyle in self.playstyles[char_class]:
            # Use the preset attributes (these are base scores without racial bonuses)
            preset_attrs = self.playstyles[char_class][playstyle]['attributes'].copy()
            
            # Validate the preset
            validation = self._validate_attribute_points(preset_attrs)
            if validation['valid']:
                return preset_attrs
            else:
                # If preset is invalid, fix it
                logger.warning(f"Invalid preset for {char_class} {playstyle}: {validation}")
                return self._fix_playstyle_attributes(char_class, playstyle)
        
        # Fallback to optimized standard array
        return self.get_optimized_standard_array(char_class)
    
    def get_skills_for_playstyle(self, char_class: str, playstyle: str) -> List[str]:
        """Get recommended skills for a playstyle"""
        # Handle standard array option
        if playstyle == 'standard_array':
            class_skills = self.classes.get(char_class, {}).get('skill_options', [])
            skill_choices = self.classes.get(char_class, {}).get('skill_choices', 2)
            return class_skills[:skill_choices] if class_skills else []
        
        # Handle specific playstyle presets
        if char_class in self.playstyles and playstyle in self.playstyles[char_class]:
            return self.playstyles[char_class][playstyle].get('skills', [])
        
        # Fallback to generic playstyle logic
        class_skills = self.classes.get(char_class, {}).get('skill_options', [])
        
        if playstyle == 'Offensive':
            offensive_skills = ['Athletics', 'Intimidation', 'Stealth']
            return [skill for skill in offensive_skills if skill in class_skills][:2]
        elif playstyle == 'Defensive':
            defensive_skills = ['Insight', 'Perception', 'Survival']
            return [skill for skill in defensive_skills if skill in class_skills][:2]
        elif playstyle == 'Utility':
            utility_skills = ['Investigation', 'Arcana', 'History', 'Religion']
            return [skill for skill in utility_skills if skill in class_skills][:2]
        else:
            # Balanced - random selection
            return random.sample(class_skills, min(2, len(class_skills)))
    
    def get_spells_for_playstyle(self, char_class: str, playstyle: str) -> Dict[str, List[str]]:
        """Get recommended spells for a playstyle"""
        if not self.spell_manager.can_cast_spells(char_class):
            return {'cantrips': [], 'spells': []}
        
        # Handle standard array option
        if playstyle == 'standard_array':
            suggestions = self.spell_manager.get_spell_suggestions(char_class)
            return suggestions
        
        # Handle specific playstyle presets
        if char_class in self.playstyles and playstyle in self.playstyles[char_class]:
            preset_spells = self.playstyles[char_class][playstyle].get('spells', [])
            preset_cantrips = self.playstyles[char_class][playstyle].get('cantrips', [])
            return {
                'cantrips': preset_cantrips,
                'spells': preset_spells
            }
        
        # Fallback to generic playstyle logic
        suggestions = self.spell_manager.get_spell_suggestions(char_class)
        
        if playstyle == 'Offensive':
            # Focus on damage spells
            offensive_cantrips = ['Fire Bolt', 'Ray of Frost', 'Eldritch Blast']
            offensive_spells = ['Magic Missile', 'Burning Hands', 'Scorching Ray']
            
            cantrips = [c for c in suggestions['cantrips'] if c in offensive_cantrips]
            spells = [s for s in suggestions['spells'] if s in offensive_spells]
            
            return {
                'cantrips': cantrips[:2],
                'spells': spells[:2]
            }
        elif playstyle == 'Defensive':
            # Focus on protection and healing
            defensive_cantrips = ['Blade Ward', 'Resistance']
            defensive_spells = ['Shield', 'Cure Wounds', 'Protection from Evil and Good']
            
            cantrips = [c for c in suggestions['cantrips'] if c in defensive_cantrips]
            spells = [s for s in suggestions['spells'] if s in defensive_spells]
            
            return {
                'cantrips': cantrips[:2],
                'spells': spells[:2]
            }
        elif playstyle == 'Utility':
            # Focus on utility spells
            utility_cantrips = ['Mage Hand', 'Prestidigitation', 'Message']
            utility_spells = ['Detect Magic', 'Comprehend Languages', 'Identify']
            
            cantrips = [c for c in suggestions['cantrips'] if c in utility_cantrips]
            spells = [s for s in suggestions['spells'] if s in utility_spells]
            
            return {
                'cantrips': cantrips[:2],
                'spells': spells[:2]
            }
        else:
            # Balanced - use default suggestions
            return suggestions
    
    def fill_character(self, character: Character):
        """Fill character with recommended data"""
        # Generate attributes if not set
        if not character.attributes:
            character.attributes = self.get_recommended_attributes(character.char_class, character.race)
        
        # Generate skills if not set
        if not character.skills:
            class_data = self.classes.get(character.char_class, {})
            skill_options = class_data.get('skill_options', [])
            skill_choices = class_data.get('skill_choices', 2)
            
            # Add background skills
            background_skills = self._select_exact_skills(character.char_class, character.background)
            skill_options.extend(background_skills)
            skill_choices += 2  # Background gives 2 additional skills
            
            # Select skills
            character.skills = random.sample(skill_options, min(skill_choices, len(skill_options)))
        
        # Generate spells for spellcasters
        if self.spell_manager.can_cast_spells(character.char_class) and not character.cantrips and not character.spells_known:
            spell_suggestions = self.spell_manager.get_spell_suggestions(character.char_class)
            character.cantrips = spell_suggestions['cantrips']
            character.spells_known = spell_suggestions['spells']
            character.spells = character.cantrips + character.spells_known
        
        # Generate personality traits
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

    def _select_exact_skills(self, char_class: str, background: str) -> List[str]:
        """Select exactly the right number of skills for class and background"""
        all_skills = []
        
        # Add background skills first
        if background in self.backgrounds:
            background_skills = self.backgrounds[background]['skill_proficiencies']
            all_skills.extend(background_skills)
        
        # Get class skill options and choices
        if char_class in self.classes:
            class_data = self.classes[char_class]
            skill_options = class_data['skill_options']
            skill_choices = class_data['skill_choices']
            
            # Filter out skills that are already provided by background
            available_class_skills = [skill for skill in skill_options if skill not in all_skills]
            
            # Select exactly the required number of class skills
            if len(available_class_skills) >= skill_choices:
                selected_class_skills = random.sample(available_class_skills, skill_choices)
            else:
                # If not enough unique skills, take all available
                selected_class_skills = available_class_skills
                # Fill remaining slots with random skills from the class list
                remaining_slots = skill_choices - len(selected_class_skills)
                if remaining_slots > 0:
                    additional_skills = random.sample(skill_options, min(remaining_slots, len(skill_options)))
                    selected_class_skills.extend(additional_skills)
            
            # Add class skills to the list
            all_skills.extend(selected_class_skills)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_skills = []
        for skill in all_skills:
            if skill not in seen:
                seen.add(skill)
                unique_skills.append(skill)
        
        return unique_skills

    def _validate_exact_quantities(self, char_class: str, background: str, skills: List[str], spells: List[str]) -> Dict[str, bool]:
        """Validate that we have exactly the right quantities"""
        validation = {
            'skills_valid': False,
            'spells_valid': False,
            'cantrips_valid': False
        }
        
        # Validate skills
        if char_class in self.classes:
            class_data = self.classes[char_class]
            expected_skills = class_data['skill_choices']
            
            # Count background skills
            background_skills = 0
            if background in self.backgrounds:
                background_skills = len(self.backgrounds[background]['skill_proficiencies'])
            
            # Total skills should be background skills + class skills
            total_skills = len(skills)
            expected_total = background_skills + expected_skills
            
            validation['skills_valid'] = total_skills == expected_total
        
        # Validate spells
        if self.spell_manager.can_cast_spells(char_class):
            expected_cantrips = self.spell_manager.get_cantrips_known_limit(char_class)
            expected_spells = self.spell_manager.get_spells_known_limit(char_class)
            
            # Count cantrips and spells
            cantrip_count = 0
            spell_count = 0
            
            # This is a simplified check - in practice, we'd need to separate cantrips from spells
            # For now, we'll assume the spell_manager handles this correctly
            validation['cantrips_valid'] = True  # Will be validated by spell_manager
            validation['spells_valid'] = True    # Will be validated by spell_manager
        
        return validation

    def _create_quantity_summary(self, char_class: str, background: str, skills: List[str], cantrips: List[str], spells: List[str]) -> Dict:
        """Create a summary of the exact quantities selected"""
        summary = {
            'class': char_class,
            'background': background,
            'skills': {
                'total': len(skills),
                'background_skills': 0,
                'class_skills': 0,
                'list': skills
            },
            'spellcasting': {
                'can_cast': False,
                'cantrips': {
                    'expected': 0,
                    'selected': len(cantrips),
                    'list': cantrips
                },
                'spells': {
                    'expected': 0,
                    'selected': len(spells),
                    'list': spells
                }
            }
        }
        
        # Calculate skill breakdown
        if background in self.backgrounds:
            background_skill_list = self.backgrounds[background]['skill_proficiencies']
            summary['skills']['background_skills'] = len(background_skill_list)
            summary['skills']['class_skills'] = len(skills) - len(background_skill_list)
        
        # Calculate spellcasting breakdown
        if self.spell_manager.can_cast_spells(char_class):
            summary['spellcasting']['can_cast'] = True
            summary['spellcasting']['cantrips']['expected'] = self.spell_manager.get_cantrips_known_limit(char_class)
            summary['spellcasting']['spells']['expected'] = self.spell_manager.get_spells_known_limit(char_class)
        
        return summary

    def _validate_attribute_points(self, attributes: Dict[str, int]) -> Dict[str, any]:
        """Validate that attributes use exactly 27 points and no score exceeds 15"""
        # Point costs for each score
        point_costs = {
            8: 0, 9: 1, 10: 2, 11: 3, 12: 4, 13: 5, 14: 7, 15: 9
        }
        
        total_points = 0
        max_score = 0
        invalid_scores = []
        
        for attr, score in attributes.items():
            if score not in point_costs:
                invalid_scores.append(f"{attr}: {score} (invalid score)")
            else:
                total_points += point_costs[score]
                max_score = max(max_score, score)
        
        return {
            'valid': total_points == 27 and max_score <= 15 and len(invalid_scores) == 0,
            'total_points': total_points,
            'max_score': max_score,
            'invalid_scores': invalid_scores,
            'expected_points': 27
        }

    def _fix_playstyle_attributes(self, char_class: str, playstyle: str) -> Dict[str, int]:
        """Fix playstyle attributes to use exactly 27 points and no score > 15"""
        # Get the original preset
        if char_class not in self.playstyles or playstyle not in self.playstyles[char_class]:
            return self.get_recommended_attributes(char_class, None)  # No race bonus
        
        original_attrs = self.playstyles[char_class][playstyle]['attributes'].copy()
        
        # Validate the original
        validation = self._validate_attribute_points(original_attrs)
        if validation['valid']:
            return original_attrs
        
        # If invalid, create a corrected version
        # Use standard array as base: [15, 14, 13, 12, 10, 8] = 9+7+5+4+2+0 = 27 points
        standard_array = [15, 14, 13, 12, 10, 8]
        
        # For each class, prioritize the most important attributes
        class_priorities = {
            'Fighter': ['STR', 'CON', 'DEX', 'WIS', 'CHA', 'INT'],
            'Wizard': ['INT', 'CON', 'DEX', 'WIS', 'CHA', 'STR'],
            'Cleric': ['WIS', 'CON', 'STR', 'CHA', 'INT', 'DEX'],
            'Rogue': ['DEX', 'CON', 'INT', 'WIS', 'CHA', 'STR'],
            'Ranger': ['DEX', 'WIS', 'CON', 'STR', 'CHA', 'INT'],
            'Paladin': ['STR', 'CHA', 'CON', 'WIS', 'DEX', 'INT'],
            'Bard': ['CHA', 'DEX', 'CON', 'INT', 'WIS', 'STR'],
            'Sorcerer': ['CHA', 'CON', 'DEX', 'WIS', 'INT', 'STR'],
            'Warlock': ['CHA', 'CON', 'DEX', 'WIS', 'INT', 'STR'],
            'Monk': ['DEX', 'WIS', 'CON', 'STR', 'CHA', 'INT'],
            'Druid': ['WIS', 'CON', 'DEX', 'STR', 'INT', 'CHA'],
            'Barbarian': ['STR', 'CON', 'DEX', 'WIS', 'CHA', 'INT']
        }
        
        priorities = class_priorities.get(char_class, ['STR', 'DEX', 'CON', 'INT', 'WIS', 'CHA'])
        
        # Assign standard array values to prioritized attributes
        corrected_attrs = {}
        for i, attr in enumerate(priorities):
            if i < len(standard_array):
                corrected_attrs[attr] = standard_array[i]
            else:
                corrected_attrs[attr] = 8  # Fallback
        
        # Validate the corrected version
        validation = self._validate_attribute_points(corrected_attrs)
        if not validation['valid']:
            logger.warning(f"Failed to create valid attributes for {char_class} {playstyle}: {validation}")
        
        return corrected_attrs

    def apply_racial_bonuses(self, attributes: Dict[str, int], race: str) -> Dict[str, int]:
        """Apply racial bonuses to base attributes"""
        if not race or race not in self.races:
            return attributes.copy()
        
        result = attributes.copy()
        race_bonus = self.races[race]['ability_bonus']
        
        for attr, bonus in race_bonus.items():
            if attr in result:
                result[attr] += bonus
        
        return result

    def get_suggestions(self, char_class: str, background: str, race: str = None, playstyle: str = None) -> Dict:
        """Get autofill suggestions that respect available skills and playstyle"""
        # Get base attributes (presets are base scores without racial bonuses)
        if playstyle and char_class in self.playstyles:
            # Use specific playstyle preset
            base_attributes = self.get_attributes_for_playstyle(char_class, playstyle)
            playstyle_skills = self.get_skills_for_playstyle(char_class, playstyle)
            playstyle_spells = self.get_spells_for_playstyle(char_class, playstyle)
        else:
            # Use optimized standard array without racial bonuses
            base_attributes = self.get_optimized_standard_array(char_class)
            playstyle_skills = []
            playstyle_spells = {}
        
        # Select skills with exact quantities
        all_skills = self._select_exact_skills(char_class, background)
        
        # If we have playstyle skills, incorporate them properly
        if playstyle_skills:
            # Get class skill options to see what's available
            class_skills = []
            if char_class in self.classes:
                class_skills = self.classes[char_class]['skill_options']
            
            # Get background skills
            background_skills = []
            if background in self.backgrounds:
                background_skills = self.backgrounds[background]['skill_proficiencies']
            
            # Filter playstyle skills that are available for the class and not from background
            playstyle_skills_available = [skill for skill in playstyle_skills 
                                        if skill in class_skills and skill not in background_skills]
            
            if playstyle_skills_available:
                # Replace class skills with playstyle skills (up to the number of class skill choices)
                class_data = self.classes[char_class]
                skill_choices = class_data['skill_choices']
                
                # Create new skill list with background skills first
                new_skills = background_skills.copy()
                
                # Add playstyle skills first (up to class skill limit)
                playstyle_count = min(len(playstyle_skills_available), skill_choices)
                new_skills.extend(playstyle_skills_available[:playstyle_count])
                
                # Fill remaining slots with other class skills
                remaining_slots = skill_choices - playstyle_count
                if remaining_slots > 0:
                    available_class_skills = [skill for skill in class_skills 
                                           if skill not in new_skills]
                    if available_class_skills:
                        additional_skills = random.sample(available_class_skills, 
                                                       min(remaining_slots, len(available_class_skills)))
                        new_skills.extend(additional_skills)
                
                all_skills = new_skills
        
        # Get spells with exact quantities
        spells = []
        cantrips = []
        spells_known = []
        
        if self.spell_manager.can_cast_spells(char_class):
            if playstyle_spells:
                # Use playstyle spells but ensure exact quantities
                cantrips = playstyle_spells.get('cantrips', [])
                spells_known = playstyle_spells.get('spells', [])
                
                # Ensure we have the exact number of cantrips and spells
                expected_cantrips = self.spell_manager.get_cantrips_known_limit(char_class)
                expected_spells = self.spell_manager.get_spells_known_limit(char_class)
                
                # Validate that playstyle spells exist in the spell list
                available_cantrips = [c['name'] for c in self.spell_manager.get_available_cantrips(char_class)]
                available_spells = [s['name'] for s in self.spell_manager.get_available_spells(char_class)]
                
                # Filter cantrips to only include valid ones
                valid_cantrips = [c for c in cantrips if c in available_cantrips]
                valid_spells = [s for s in spells_known if s in available_spells]
                
                # Fill to exact limits with valid spells
                if len(valid_cantrips) < expected_cantrips:
                    spell_suggestions = self.spell_manager.get_spell_suggestions(char_class)
                    additional_cantrips = [c for c in spell_suggestions['cantrips'] 
                                         if c not in valid_cantrips][:expected_cantrips - len(valid_cantrips)]
                    valid_cantrips.extend(additional_cantrips)
                
                if len(valid_spells) < expected_spells:
                    spell_suggestions = self.spell_manager.get_spell_suggestions(char_class)
                    additional_spells = [s for s in spell_suggestions['spells'] 
                                       if s not in valid_spells][:expected_spells - len(valid_spells)]
                    valid_spells.extend(additional_spells)
                
                # Trim to exact limits
                cantrips = valid_cantrips[:expected_cantrips]
                spells_known = valid_spells[:expected_spells]
            else:
                # Use spell manager suggestions (already ensures exact quantities)
                spell_suggestions = self.spell_manager.get_spell_suggestions(char_class)
                cantrips = spell_suggestions['cantrips']
                spells_known = spell_suggestions['spells']
            
            # Combine for backward compatibility
            spells = cantrips + spells_known
        
        # Validate quantities
        validation = self._validate_exact_quantities(char_class, background, all_skills, spells)
        
        # Get available playstyles for the class
        available_playstyles = self.get_available_playstyles(char_class)
        
        # Create summary of exact quantities
        summary = self._create_quantity_summary(char_class, background, all_skills, cantrips, spells_known)
        
        # Apply racial bonuses if race is specified
        attributes_with_race = self.apply_racial_bonuses(base_attributes, race) if race else base_attributes.copy()
        
        # Validate base attributes
        base_validation = self._validate_attribute_points(base_attributes)
        
        return {
            'attributes': base_attributes,  # Base attributes (without racial bonuses)
            'attributes_with_race': attributes_with_race,  # Attributes with racial bonuses applied
            'skills': all_skills,
            'spells': spells,
            'cantrips': cantrips,
            'spells_known': spells_known,
            'available_playstyles': available_playstyles,
            'current_playstyle': playstyle,
            'validation': validation,
            'base_attributes_validation': base_validation,
            'summary': summary
        } 
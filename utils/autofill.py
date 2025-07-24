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
                    'attributes': {'STR': 15, 'DEX': 12, 'CON': 15, 'INT': 8, 'WIS': 10, 'CHA': 11},  # 9+4+9+0+2+3 = 27
                    'skills': ['Athletics', 'Insight'],
                    'description': 'Tank fighter with high constitution and defensive skills'
                }
            },
            'Wizard': {
                'balanced': {
                    'attributes': {'STR': 8, 'DEX': 12, 'CON': 14, 'INT': 15, 'WIS': 12, 'CHA': 11},  # 0+4+7+9+4+3 = 27
                    'skills': ['Arcana', 'History'],
                    'spells': ['Magic Missile', 'Shield', 'Mage Armor'],
                    'cantrips': ['Fire Bolt', 'Prestidigitation'],
                    'description': 'Versatile wizard with balanced spell selection'
                },
                'evoker': {
                    'attributes': {'STR': 8, 'DEX': 10, 'CON': 14, 'INT': 15, 'WIS': 13, 'CHA': 12},    # 0+2+7+9+5+4 = 27
                    'skills': ['Arcana', 'Investigation'],
                    'spells': ['Burning Hands', 'Magic Missile', 'Thunderwave'],
                    'cantrips': ['Fire Bolt', 'Ray of Frost'],
                    'description': 'Damage-focused wizard specializing in evocation spells'
                },
                'utility': {
                    'attributes': {'STR': 8, 'DEX': 12, 'CON': 13, 'INT': 15, 'WIS': 12, 'CHA': 13},   # 0+4+5+9+4+5 = 27
                    'skills': ['Arcana', 'Investigation'],
                    'spells': ['Detect Magic', 'Comprehend Languages', 'Unseen Servant'],
                    'cantrips': ['Mage Hand', 'Message'],
                    'description': 'Utility wizard focused on non-combat spells'
                }
            },
            'Cleric': {
                'balanced': {
                    'attributes': {'STR': 12, 'DEX': 10, 'CON': 14, 'INT': 12, 'WIS': 15, 'CHA': 9},  # 4+2+7+4+9+1 = 27
                    'skills': ['Insight', 'Religion'],
                    'spells': ['Cure Wounds', 'Bless', 'Shield of Faith'],
                    'cantrips': ['Sacred Flame', 'Spare the Dying'],
                    'description': 'Balanced cleric with healing and support spells'
                },
                'healer': {
                    'attributes': {'STR': 12, 'DEX': 10, 'CON': 14, 'INT': 12, 'WIS': 15, 'CHA': 9},    # 4+2+7+4+9+1 = 27
                    'skills': ['Medicine', 'Religion'],
                    'spells': ['Cure Wounds', 'Healing Word', 'Prayer of Healing'],
                    'cantrips': ['Sacred Flame', 'Spare the Dying'],
                    'description': 'Dedicated healer focused on restoration magic'
                },
                'warrior': {
                    'attributes': {'STR': 14, 'DEX': 10, 'CON': 14, 'INT': 8, 'WIS': 15, 'CHA': 10},     # 7+2+7+0+9+2 = 27
                    'skills': ['Athletics', 'Religion'],
                    'spells': ['Divine Favor', 'Shield of Faith', 'Cure Wounds'],
                    'cantrips': ['Sacred Flame', 'Thaumaturgy'],
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
                    'description': 'Balanced ranger with wilderness and tracking skills'
                },
                'archer': {
                    'attributes': {'STR': 8, 'DEX': 15, 'CON': 13, 'INT': 12, 'WIS': 12, 'CHA': 13},    # 0+9+5+4+4+5 = 27
                    'skills': ['Stealth', 'Perception'],
                    'description': 'Ranged combat specialist with stealth and perception'
                },
                'beastmaster': {
                    'attributes': {'STR': 12, 'DEX': 12, 'CON': 13, 'INT': 10, 'WIS': 15, 'CHA': 11}, # 4+4+5+2+9+3 = 27
                    'skills': ['Animal Handling', 'Survival'],
                    'description': 'Beast master focused on animal companions and nature'
                }
            },
            'Paladin': {
                'balanced': {
                    'attributes': {'STR': 15, 'DEX': 10, 'CON': 13, 'INT': 8, 'WIS': 12, 'CHA': 14},  # 9+2+5+0+4+7 = 27
                    'skills': ['Athletics', 'Persuasion'],
                    'spells': ['Divine Favor', 'Bless', 'Cure Wounds'],
                    'cantrips': ['Sacred Flame', 'Thaumaturgy'],
                    'description': 'Balanced paladin with martial and divine abilities'
                },
                'tank': {
                    'attributes': {'STR': 15, 'DEX': 8, 'CON': 14, 'INT': 10, 'WIS': 12, 'CHA': 13},      # 9+0+7+2+4+5 = 27
                    'skills': ['Athletics', 'Insight'],
                    'spells': ['Shield of Faith', 'Divine Favor', 'Cure Wounds'],
                    'cantrips': ['Sacred Flame', 'Thaumaturgy'],
                    'description': 'Defensive paladin focused on protection and healing'
                },
                'charismatic': {
                    'attributes': {'STR': 13, 'DEX': 10, 'CON': 13, 'INT': 8, 'WIS': 12, 'CHA': 15}, # 5+2+5+0+4+9 = 25
                    'skills': ['Persuasion', 'Intimidation'],
                    'spells': ['Command', 'Bless', 'Cure Wounds'],
                    'cantrips': ['Sacred Flame', 'Thaumaturgy'],
                    'description': 'Charismatic paladin with strong social and leadership skills'
                }
            },
            'Bard': {
                'balanced': {
                    'attributes': {'STR': 8, 'DEX': 12, 'CON': 13, 'INT': 12, 'WIS': 11, 'CHA': 15},  # 0+4+5+4+3+9 = 25
                    'skills': ['Performance', 'Persuasion'],
                    'spells': ['Cure Wounds', 'Charm Person', 'Disguise Self'],
                    'cantrips': ['Vicious Mockery', 'Prestidigitation'],
                    'description': 'Versatile bard with healing, charm, and utility spells'
                },
                'lore': {
                    'attributes': {'STR': 8, 'DEX': 12, 'CON': 12, 'INT': 13, 'WIS': 11, 'CHA': 15},      # 0+4+4+5+3+9 = 25 (adjusted)
                    'skills': ['History', 'Arcana'],
                    'spells': ['Comprehend Languages', 'Detect Magic', 'Cure Wounds'],
                    'cantrips': ['Vicious Mockery', 'Message'],
                    'description': 'Knowledge-focused bard with utility and information gathering'
                },
                'valor': {
                    'attributes': {'STR': 12, 'DEX': 12, 'CON': 13, 'INT': 10, 'WIS': 9, 'CHA': 15},      # 4+4+5+2+1+9 = 25 (adjusted)
                    'skills': ['Athletics', 'Performance'],
                    'spells': ['Cure Wounds', 'Heroism', 'Thunderwave'],
                    'cantrips': ['Vicious Mockery', 'Blade Ward'],
                    'description': 'Combat-oriented bard with martial and inspiring abilities'
                }
            },
            'Sorcerer': {
                'balanced': {
                    'attributes': {'STR': 8, 'DEX': 12, 'CON': 14, 'INT': 12, 'WIS': 11, 'CHA': 15},  # 0+4+7+4+3+9 = 27
                    'skills': ['Arcana', 'Deception'],
                    'spells': ['Magic Missile', 'Shield', 'Charm Person'],
                    'cantrips': ['Fire Bolt', 'Prestidigitation'],
                    'description': 'Balanced sorcerer with damage and utility spells'
                },
                'damage': {
                    'attributes': {'STR': 8, 'DEX': 12, 'CON': 14, 'INT': 10, 'WIS': 13, 'CHA': 15},    # 0+4+7+2+5+9 = 27
                    'skills': ['Arcana', 'Intimidation'],
                    'spells': ['Burning Hands', 'Magic Missile', 'Thunderwave'],
                    'cantrips': ['Fire Bolt', 'Ray of Frost'],
                    'description': 'Damage-focused sorcerer specializing in evocation'
                },
                'control': {
                    'attributes': {'STR': 8, 'DEX': 12, 'CON': 13, 'INT': 12, 'WIS': 11, 'CHA': 15},    # 0+4+5+4+3+9 = 25 (adjusted)
                    'skills': ['Arcana', 'Persuasion'],
                    'spells': ['Charm Person', 'Sleep', 'Suggestion'],
                    'cantrips': ['Mage Hand', 'Message'],
                    'description': 'Control-focused sorcerer with enchantment and illusion'
                }
            },
            'Warlock': {
                'balanced': {
                    'attributes': {'STR': 8, 'DEX': 12, 'CON': 14, 'INT': 12, 'WIS': 11, 'CHA': 15},  # 0+4+7+4+3+9 = 27
                    'skills': ['Arcana', 'Deception'],
                    'spells': ['Eldritch Blast', 'Hex', 'Charm Person'],
                    'cantrips': ['Eldritch Blast', 'Prestidigitation'],
                    'description': 'Balanced warlock with damage and utility abilities'
                },
                'blaster': {
                    'attributes': {'STR': 8, 'DEX': 12, 'CON': 14, 'INT': 10, 'WIS': 13, 'CHA': 15},   # 0+4+7+2+5+9 = 27
                    'skills': ['Arcana', 'Intimidation'],
                    'spells': ['Eldritch Blast', 'Hex', 'Armor of Agathys'],
                    'cantrips': ['Eldritch Blast', 'Ray of Frost'],
                    'description': 'Damage-focused warlock with powerful blasting abilities'
                },
                'utility': {
                    'attributes': {'STR': 8, 'DEX': 12, 'CON': 13, 'INT': 12, 'WIS': 11, 'CHA': 15},    # 0+4+5+4+3+9 = 25 (adjusted)
                    'skills': ['Arcana', 'Persuasion'],
                    'spells': ['Eldritch Blast', 'Unseen Servant', 'Comprehend Languages'],
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
                    'spells': ['Cure Wounds', 'Entangle', 'Goodberry'],
                    'cantrips': ['Druidcraft', 'Produce Flame'],
                    'description': 'Balanced druid with healing and nature magic'
                },
                'caster': {
                    'attributes': {'STR': 8, 'DEX': 12, 'CON': 14, 'INT': 12, 'WIS': 15, 'CHA': 11},    # 0+4+7+4+9+3 = 27
                    'skills': ['Arcana', 'Nature'],
                    'spells': ['Cure Wounds', 'Detect Magic', 'Comprehend Languages'],
                    'cantrips': ['Druidcraft', 'Guidance'],
                    'description': 'Spellcasting-focused druid with utility magic'
                },
                'shapeshifter': {
                    'attributes': {'STR': 12, 'DEX': 12, 'CON': 14, 'INT': 10, 'WIS': 15, 'CHA': 9}, # 4+4+7+2+9+1 = 27
                    'skills': ['Athletics', 'Survival'],
                    'spells': ['Cure Wounds', 'Longstrider', 'Jump'],
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
        
        # Standard Arrays from D&D 5e SRD (all using exactly 27 points)
        standard_arrays = [
            {'STR': 15, 'DEX': 14, 'CON': 13, 'INT': 12, 'WIS': 10, 'CHA': 8},   # 9+7+5+4+2+0 = 27
            {'STR': 15, 'DEX': 13, 'CON': 14, 'INT': 12, 'WIS': 10, 'CHA': 8},   # 9+5+7+4+2+0 = 27
            {'STR': 15, 'DEX': 12, 'CON': 14, 'INT': 13, 'WIS': 10, 'CHA': 8},   # 9+4+7+5+2+0 = 27
            {'STR': 14, 'DEX': 15, 'CON': 13, 'INT': 12, 'WIS': 10, 'CHA': 8},   # 7+9+5+4+2+0 = 27
            {'STR': 14, 'DEX': 13, 'CON': 15, 'INT': 12, 'WIS': 10, 'CHA': 8},   # 7+5+9+4+2+0 = 27
            {'STR': 13, 'DEX': 15, 'CON': 14, 'INT': 12, 'WIS': 10, 'CHA': 8},   # 5+9+7+4+2+0 = 27
            {'STR': 12, 'DEX': 15, 'CON': 14, 'INT': 13, 'WIS': 10, 'CHA': 8},   # 4+9+7+5+2+0 = 27
            {'STR': 8, 'DEX': 14, 'CON': 14, 'INT': 15, 'WIS': 12, 'CHA': 8},   # 0+7+7+9+4+0 = 27 (Wizard)
            {'STR': 8, 'DEX': 12, 'CON': 14, 'INT': 15, 'WIS': 12, 'CHA': 11},   # 0+4+7+9+4+3 = 27 (Wizard)
            {'STR': 8, 'DEX': 12, 'CON': 14, 'INT': 15, 'WIS': 13, 'CHA': 10},   # 0+4+7+9+5+2 = 27 (Wizard)
        ]
        
        # Choose between standard arrays and presets
        if random.random() < 0.3:  # 30% chance to use standard array
            chosen_array = random.choice(standard_arrays)
            
            # Validate that the array uses exactly 27 points and no value exceeds 15
            total_cost = sum(point_costs.get(value, 0) for value in chosen_array.values())
            max_value = max(chosen_array.values())
            
            if total_cost != 27:
                print(f"Warning: Standard array uses {total_cost} points instead of 27")
            if max_value > 15:
                print(f"Warning: Standard array has value {max_value} which exceeds 15")
                # Fallback to a safe array
                chosen_array = {'STR': 13, 'DEX': 13, 'CON': 13, 'INT': 12, 'WIS': 12, 'CHA': 12}
            
            return {
                'STR': chosen_array['STR'],
                'DEX': chosen_array['DEX'],
                'CON': chosen_array['CON'],
                'INT': chosen_array['INT'],
                'WIS': chosen_array['WIS'],
                'CHA': chosen_array['CHA']
            }
        
        if char_class in self.playstyles:
            # Choose a random playstyle for the class
            playstyle_names = list(self.playstyles[char_class].keys())
            chosen_playstyle = random.choice(playstyle_names)
            chosen_playstyle_data = self.playstyles[char_class][chosen_playstyle]
            chosen_attributes = chosen_playstyle_data['attributes']
            
            # Validate that the playstyle uses exactly 27 points and no value exceeds 15
            total_cost = sum(point_costs.get(value, 0) for value in chosen_attributes.values())
            max_value = max(chosen_attributes.values())
            
            if total_cost != 27:
                print(f"Warning: {char_class} {chosen_playstyle} playstyle uses {total_cost} points instead of 27")
            if max_value > 15:
                print(f"Warning: {char_class} {chosen_playstyle} playstyle has value {max_value} which exceeds 15")
                # Cap any value that exceeds 15 to 15
                for attr, value in chosen_attributes.items():
                    if value > 15:
                        print(f"Capping {attr} from {value} to 15")
                        chosen_attributes[attr] = 15
            
            # Rebalance if total cost is not 27
            if total_cost != 27:
                print(f"Rebalancing {char_class} {chosen_playstyle} from {total_cost} to 27 points")
                # Add points to primary attributes first
                primary_attrs = self.classes.get(char_class, {}).get('primary_attributes', [])
                
                # Calculate how many points we need to add
                points_needed = 27 - total_cost
                
                # Add points to primary attributes first, then others
                priority_attrs = primary_attrs + [attr for attr in ['STR', 'DEX', 'CON', 'INT', 'WIS', 'CHA'] if attr not in primary_attrs]
                
                for attr in priority_attrs:
                    if points_needed <= 0:
                        break
                    current_value = chosen_attributes[attr]
                    if current_value < 15:  # Don't exceed 15
                        # Calculate how many points we can add to this attribute
                        current_cost = point_costs.get(current_value, 0)
                        # Find the next value that would add points
                        for new_value in range(current_value + 1, 16):
                            new_cost = point_costs.get(new_value, 0)
                            if new_cost > current_cost:
                                points_to_add = new_cost - current_cost
                                if points_to_add <= points_needed:
                                    chosen_attributes[attr] = new_value
                                    points_needed -= points_to_add
                                    print(f"Added {points_to_add} points to {attr} (now {new_value})")
                                    break
            
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
    
    def get_available_playstyles(self, char_class: str) -> List[str]:
        """Get available playstyles for a class"""
        if char_class in self.playstyles:
            return list(self.playstyles[char_class].keys())
        return []
    
    def get_playstyle_data(self, char_class: str, playstyle: str) -> Dict:
        """Get complete data for a specific playstyle"""
        if char_class in self.playstyles and playstyle in self.playstyles[char_class]:
            return self.playstyles[char_class][playstyle]
        return None
    
    def get_attributes_for_playstyle(self, char_class: str, playstyle: str) -> Dict[str, int]:
        """Get attributes for a specific playstyle"""
        playstyle_data = self.get_playstyle_data(char_class, playstyle)
        if playstyle_data:
            return playstyle_data['attributes']
        return None
    
    def get_skills_for_playstyle(self, char_class: str, playstyle: str) -> List[str]:
        """Get recommended skills for a specific playstyle"""
        playstyle_data = self.get_playstyle_data(char_class, playstyle)
        if playstyle_data and 'skills' in playstyle_data:
            return playstyle_data['skills']
        return []
    
    def get_spells_for_playstyle(self, char_class: str, playstyle: str) -> Dict[str, List[str]]:
        """Get recommended spells for a specific playstyle"""
        playstyle_data = self.get_playstyle_data(char_class, playstyle)
        if playstyle_data:
            spells = {}
            if 'cantrips' in playstyle_data:
                spells['cantrips'] = playstyle_data['cantrips']
            if 'spells' in playstyle_data:
                spells['spells'] = playstyle_data['spells']
            return spells
        return {}
    
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

    def get_suggestions(self, char_class: str, background: str, race: str = None, playstyle: str = None) -> Dict:
        """Get autofill suggestions that respect available skills and playstyle"""
        # Get base attributes without racial bonuses
        if playstyle and char_class in self.playstyles and playstyle in self.playstyles[char_class]:
            # Use specific playstyle
            base_attributes = self.get_attributes_for_playstyle(char_class, playstyle)
            playstyle_skills = self.get_skills_for_playstyle(char_class, playstyle)
            playstyle_spells = self.get_spells_for_playstyle(char_class, playstyle)
        else:
            # Use random playstyle or standard array
        base_attributes = self.get_recommended_attributes(char_class, race)
            playstyle_skills = []
            playstyle_spells = {}
        
        # Get available skills for the class
        class_skills = []
        if char_class in self.classes:
            class_skills = self.classes[char_class]['skill_options']
        
        # Get background skills
        background_skills = []
        if background in self.backgrounds:
            background_skills = self.backgrounds[background]['skill_proficiencies']
        
        # Select class skills (prioritizing playstyle skills if available)
        selected_class_skills = []
        if char_class in self.classes:
            class_data = self.classes[char_class]
            skill_choices = class_data['skill_choices']
            available_class_skills = [skill for skill in class_skills if skill not in background_skills]
            
            # If we have playstyle skills, prioritize them
            if playstyle_skills:
                # Add playstyle skills that are available for the class
                for skill in playstyle_skills:
                    if skill in available_class_skills and len(selected_class_skills) < skill_choices:
                        selected_class_skills.append(skill)
                
                # Fill remaining slots with random skills
                remaining_slots = skill_choices - len(selected_class_skills)
                remaining_skills = [skill for skill in available_class_skills if skill not in selected_class_skills]
                if remaining_slots > 0 and remaining_skills:
                    additional_skills = random.sample(remaining_skills, min(remaining_slots, len(remaining_skills)))
                    selected_class_skills.extend(additional_skills)
            else:
                # Select skills randomly
            if len(available_class_skills) >= skill_choices:
                selected_class_skills = random.sample(available_class_skills, skill_choices)
            else:
                selected_class_skills = available_class_skills
        
        # Combine background and class skills
        all_skills = background_skills + selected_class_skills
        
        # Get spells if applicable
        spells = []
        if self.spell_manager.can_cast_spells(char_class):
            if playstyle_spells:
                # Use playstyle spells
                spells = playstyle_spells.get('cantrips', []) + playstyle_spells.get('spells', [])
            else:
                # Use random spell suggestions
            spell_suggestions = self.spell_manager.get_spell_suggestions(char_class)
            spells = spell_suggestions['cantrips'] + spell_suggestions['spells']
        
        # Get available playstyles for the class
        available_playstyles = self.get_available_playstyles(char_class)
        
        return {
            'attributes': base_attributes,
            'skills': all_skills,
            'spells': spells,
            'available_playstyles': available_playstyles,
            'current_playstyle': playstyle
        } 
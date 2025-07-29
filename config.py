"""
Configuration file for EchoSheet application
"""

import os

# Flask Configuration
SECRET_KEY = os.environ.get('SECRET_KEY', 'echo_sheet_secret_key')
DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'
HOST = os.environ.get('HOST', '0.0.0.0')
PORT = int(os.environ.get('PORT', 5000))

# Database Configuration
DATABASE_PATH = os.environ.get('DATABASE_PATH', 'db.sqlite')

# Application Constants
MAX_LEVEL = 20
MIN_LEVEL = 1
MAX_ATTRIBUTE_POINTS = 27
MIN_ATTRIBUTE_VALUE = 8
MAX_ATTRIBUTE_VALUE = 15

# Point Buy Costs (D&D 5e standard)
POINT_BUY_COSTS = {
    8: 0, 9: 1, 10: 2, 11: 3, 12: 4, 
    13: 5, 14: 7, 15: 9
}

# Experience Points Thresholds (D&D 5e)
XP_THRESHOLDS = {
    1: 0, 2: 300, 3: 900, 4: 2700, 5: 6500,
    6: 14000, 7: 23000, 8: 34000, 9: 48000, 10: 64000,
    11: 85000, 12: 100000, 13: 120000, 14: 140000, 15: 165000,
    16: 195000, 17: 225000, 18: 265000, 19: 305000, 20: 355000
}

# Available Classes
AVAILABLE_CLASSES = [
    'Fighter', 'Wizard', 'Cleric', 'Rogue', 'Ranger', 
    'Paladin', 'Bard', 'Sorcerer', 'Warlock', 'Monk', 
    'Druid', 'Barbarian'
]

# Available Races
AVAILABLE_RACES = [
    'Human', 'Elf', 'Dwarf', 'Halfling', 'Dragonborn', 
    'Tiefling', 'Half-Elf', 'Half-Orc', 'Gnome'
]

# Available Backgrounds
AVAILABLE_BACKGROUNDS = [
    'Acolyte', 'Criminal', 'Folk Hero', 'Noble', 'Sage', 
    'Soldier', 'Urchin', 'Charlatan', 'Entertainer', 'Guild Artisan',
    'Hermit', 'Outlander'
]

# Spellcasting Classes
SPELLCASTING_CLASSES = [
    'Wizard', 'Cleric', 'Bard', 'Sorcerer', 'Warlock', 
    'Druid', 'Paladin', 'Ranger'
]

# Class Skill Choices
CLASS_SKILL_CHOICES = {
    'Fighter': 2, 'Wizard': 2, 'Cleric': 2, 'Rogue': 4,
    'Ranger': 3, 'Paladin': 2, 'Bard': 3, 'Sorcerer': 2,
    'Warlock': 2, 'Monk': 2, 'Druid': 2, 'Barbarian': 2
}

# Background Skill Choices
BACKGROUND_SKILL_CHOICES = 2

# Currency Values (in copper pieces)
CURRENCY_VALUES = {
    'cp': 1,      # Copper piece
    'sp': 10,     # Silver piece = 10 cp
    'ep': 50,     # Electrum piece = 50 cp
    'gp': 100,    # Gold piece = 100 cp
    'pp': 1000    # Platinum piece = 1000 cp
}

# Default Item Weights (in pounds)
DEFAULT_ITEM_WEIGHTS = {
    'backpack': 5, 'bedroll': 7, 'rations': 2, 'waterskin': 5,
    'torch': 1, 'rope': 10, 'tent': 20, 'armor': 40,
    'weapon': 3, 'shield': 6, 'potion': 0.5, 'scroll': 0.1,
    'book': 5, 'clothes': 3, 'boots': 2, 'helmet': 4,
    'gloves': 1, 'belt': 1, 'pouch': 1, 'coin': 0.02
}

# Hit Dice by Class
HIT_DICE_BY_CLASS = {
    'Barbarian': 'd12', 'Fighter': 'd10', 'Paladin': 'd10', 'Ranger': 'd10',
    'Bard': 'd8', 'Cleric': 'd8', 'Druid': 'd8', 'Monk': 'd8', 'Rogue': 'd8',
    'Sorcerer': 'd6', 'Warlock': 'd8', 'Wizard': 'd6'
}

# Base Hit Points by Class
BASE_HP_BY_CLASS = {
    'Barbarian': 12, 'Fighter': 10, 'Paladin': 10, 'Ranger': 10,
    'Bard': 8, 'Cleric': 8, 'Druid': 8, 'Monk': 8, 'Rogue': 8,
    'Sorcerer': 6, 'Warlock': 8, 'Wizard': 6
}

# Movement Speed by Race
MOVEMENT_SPEED_BY_RACE = {
    'Human': 30, 'Elf': 30, 'Dwarf': 25, 'Halfling': 25,
    'Dragonborn': 30, 'Tiefling': 30, 'Half-Elf': 30, 'Half-Orc': 30,
    'Gnome': 25, 'Aarakocra': 25, 'Genasi': 30, 'Goliath': 30
}

# Spellcasting Abilities by Class
SPELLCASTING_ABILITIES = {
    'Wizard': 'Intelligence',
    'Cleric': 'Wisdom',
    'Bard': 'Charisma',
    'Sorcerer': 'Charisma',
    'Warlock': 'Charisma',
    'Druid': 'Wisdom',
    'Paladin': 'Charisma',
    'Ranger': 'Wisdom'
}

# Saving Throw Proficiencies by Class
SAVING_THROW_PROFICIENCIES = {
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

# Combat Roles by Class
COMBAT_ROLES = {
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
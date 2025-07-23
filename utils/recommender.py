from typing import Dict, List
from models import Character

class Recommender:
    """Clase para generar recomendaciones de mejoras para el personaje"""
    
    def __init__(self):
        self.load_recommendations()
    
    def load_recommendations(self):
        """Load recommendation data"""
        # Subclases del SRD por clase
        self.subclasses = {
            'Fighter': ['Champion', 'Battle Master', 'Eldritch Knight'],
            'Wizard': ['Evocation', 'Abjuration', 'Divination', 'Conjuration', 'Transmutation'],
            'Cleric': ['Life', 'Light', 'Nature', 'Tempest', 'Trickery', 'War'],
            'Rogue': ['Assassin', 'Thief', 'Arcane Trickster'],
            'Ranger': ['Hunter', 'Beast Master'],
            'Paladin': ['Devotion', 'Ancients', 'Vengeance'],
            'Bard': ['Lore', 'Valor'],
            'Sorcerer': ['Draconic', 'Wild Magic'],
            'Warlock': ['Fiend', 'Great Old One', 'Archfey'],
            'Monk': ['Open Hand', 'Shadow', 'Four Elements'],
            'Druid': ['Land', 'Moon'],
            'Barbarian': ['Berserker', 'Totem Warrior']
        }
        
        # Hechizos del SRD recomendados por nivel
        self.spell_recommendations = {
            'Wizard': {
                1: ['Magic Missile', 'Shield', 'Mage Armor'],
                2: ['Mirror Image', 'Misty Step', 'Web'],
                3: ['Fireball', 'Counterspell', 'Fly'],
                4: ['Polymorph', 'Wall of Fire', 'Dimension Door'],
                5: ['Cone of Cold', 'Teleportation Circle', 'Wall of Force']
            },
            'Cleric': {
                1: ['Cure Wounds', 'Bless', 'Sacred Flame'],
                2: ['Spiritual Weapon', 'Hold Person', 'Silence'],
                3: ['Spirit Guardians', 'Revivify', 'Dispel Magic'],
                4: ['Divination', 'Guardian of Faith', 'Death Ward'],
                5: ['Mass Cure Wounds', 'Commune', 'Flame Strike']
            },
            'Bard': {
                1: ['Vicious Mockery', 'Cure Wounds', 'Faerie Fire'],
                2: ['Suggestion', 'Invisibility', 'Heat Metal'],
                3: ['Hypnotic Pattern', 'Dispel Magic', 'Tiny Servant'],
                4: ['Polymorph', 'Greater Invisibility', 'Dimension Door'],
                5: ['Mass Suggestion', 'Otto\'s Irresistible Dance', 'Power Word Stun']
            },
            'Sorcerer': {
                1: ['Fire Bolt', 'Shield', 'Burning Hands'],
                2: ['Misty Step', 'Mirror Image', 'Scorching Ray'],
                3: ['Fireball', 'Counterspell', 'Fly'],
                4: ['Polymorph', 'Wall of Fire', 'Dimension Door'],
                5: ['Cone of Cold', 'Teleportation Circle', 'Wall of Force']
            },
            'Warlock': {
                1: ['Eldritch Blast', 'Hex', 'Armor of Agathys'],
                2: ['Misty Step', 'Mirror Image', 'Suggestion'],
                3: ['Counterspell', 'Dispel Magic', 'Fly'],
                4: ['Dimension Door', 'Wall of Fire', 'Banishment'],
                5: ['Teleportation Circle', 'Wall of Force', 'Mass Suggestion']
            },
            'Druid': {
                1: ['Produce Flame', 'Cure Wounds', 'Entangle'],
                2: ['Heat Metal', 'Spike Growth', 'Pass without Trace'],
                3: ['Call Lightning', 'Conjure Animals', 'Dispel Magic'],
                4: ['Polymorph', 'Wall of Fire', 'Conjure Minor Elementals'],
                5: ['Mass Cure Wounds', 'Commune with Nature', 'Insect Plague']
            },
            'Paladin': {
                1: ['Cure Wounds', 'Divine Favor', 'Bless'],
                2: ['Spiritual Weapon', 'Hold Person', 'Zone of Truth'],
                3: ['Crusader\'s Mantle', 'Revivify', 'Dispel Magic'],
                4: ['Divination', 'Guardian of Faith', 'Death Ward'],
                5: ['Mass Cure Wounds', 'Commune', 'Flame Strike']
            },
            'Ranger': {
                1: ['Cure Wounds', 'Hunter\'s Mark', 'Goodberry'],
                2: ['Spike Growth', 'Pass without Trace', 'Silence'],
                3: ['Conjure Animals', 'Lightning Arrow', 'Dispel Magic'],
                4: ['Guardian of Nature', 'Conjure Woodland Beings', 'Freedom of Movement'],
                5: ['Swift Quiver', 'Commune with Nature', 'Tree Stride']
            }
        }
        
        # Recommended skills by class
        self.skill_recommendations = {
            'Fighter': ['Athletics', 'Intimidation', 'Perception', 'Survival'],
            'Wizard': ['Arcana', 'History', 'Investigation', 'Religion'],
            'Cleric': ['Insight', 'Medicine', 'Persuasion', 'Religion'],
            'Rogue': ['Acrobatics', 'Deception', 'Stealth', 'Sleight of Hand'],
            'Ranger': ['Animal Handling', 'Nature', 'Perception', 'Survival'],
            'Paladin': ['Athletics', 'Insight', 'Intimidation', 'Persuasion'],
            'Bard': ['Deception', 'Performance', 'Persuasion', 'Stealth'],
            'Sorcerer': ['Arcana', 'Deception', 'Intimidation', 'Persuasion'],
            'Warlock': ['Arcana', 'Deception', 'Intimidation', 'Investigation'],
            'Monk': ['Acrobatics', 'Athletics', 'Insight', 'Stealth'],
            'Druid': ['Animal Handling', 'Insight', 'Medicine', 'Nature'],
            'Barbarian': ['Athletics', 'Intimidation', 'Nature', 'Perception']
        }
        
        # Recommended feats
        self.feat_recommendations = {
            'Fighter': ['Great Weapon Master', 'Polearm Master', 'Sentinel', 'Alert'],
            'Wizard': ['War Caster', 'Resilient (CON)', 'Alert', 'Lucky'],
            'Cleric': ['War Caster', 'Resilient (CON)', 'Alert', 'Healer'],
            'Rogue': ['Alert', 'Lucky', 'Mobile', 'Skulker'],
            'Ranger': ['Sharpshooter', 'Alert', 'Mobile', 'Skulker'],
            'Paladin': ['Great Weapon Master', 'Polearm Master', 'Sentinel', 'War Caster'],
            'Bard': ['War Caster', 'Alert', 'Lucky', 'Inspiring Leader'],
            'Sorcerer': ['War Caster', 'Resilient (CON)', 'Alert', 'Lucky'],
            'Warlock': ['War Caster', 'Resilient (CON)', 'Alert', 'Lucky'],
            'Monk': ['Mobile', 'Alert', 'Lucky', 'Sentinel'],
            'Druid': ['War Caster', 'Resilient (CON)', 'Alert', 'Mobile'],
            'Barbarian': ['Great Weapon Master', 'Polearm Master', 'Sentinel', 'Alert']
        }
    
    def get_recommendations(self, character: Character) -> Dict:
        """Get all recommendations for the character"""
        recommendations = {
            'subclass': self.get_subclass_recommendation(character),
            'spells': self.get_spell_recommendations(character),
            'skills': self.get_skill_recommendations(character),
            'feats': self.get_feat_recommendations(character),
            'next_level': self.get_next_level_recommendations(character)
        }
        
        return recommendations
    
    def get_subclass_recommendation(self, character: Character) -> Dict:
        """Recommend subclass based on class"""
        if character.char_class not in self.subclasses:
            return {'recommendations': [], 'reason': 'Class not supported'}
        
        available_subclasses = self.subclasses[character.char_class]
        
        # Simple logic: recommend based on primary attributes
        if character.char_class == 'Fighter':
            if character.attributes.get('STR', 0) > character.attributes.get('DEX', 0):
                recommended = 'Champion'
                reason = 'Your high Strength makes you ideal for melee combat'
            else:
                recommended = 'Battle Master'
                reason = 'Your dexterity allows for effective tactical maneuvers'
        elif character.char_class == 'Wizard':
            if character.attributes.get('INT', 0) >= 16:
                recommended = 'Evocation'
                reason = 'Tu alta Inteligencia maximiza el daño de hechizos ofensivos'
            else:
                recommended = 'Abjuration'
                reason = 'Protección y defensa para complementar tus atributos'
        else:
            recommended = available_subclasses[0]
            reason = f'Subclase estándar para {character.char_class}'
        
        return {
            'recommendations': available_subclasses,
            'recommended': recommended,
            'reason': reason
        }
    
    def get_spell_recommendations(self, character: Character) -> Dict:
        """Recomendar hechizos según nivel y clase"""
        if character.char_class not in self.spell_recommendations:
            return {'recommendations': [], 'reason': 'Clase no lanza hechizos'}
        
        spell_data = self.spell_recommendations[character.char_class]
        current_level = character.level
        
        # Encontrar hechizos para el nivel actual
        available_spells = []
        for level, spells in spell_data.items():
            if level <= current_level:
                available_spells.extend(spells)
        
        # Filtrar hechizos que ya tiene
        new_spells = [spell for spell in available_spells if spell not in character.spells]
        
        # Recomendar 2-3 hechizos
        recommended = new_spells[:3] if len(new_spells) >= 3 else new_spells
        
        return {
            'recommendations': recommended,
            'reason': f'Hechizos apropiados para nivel {current_level}',
            'all_available': available_spells
        }
    
    def get_skill_recommendations(self, character: Character) -> Dict:
        """Recomendar habilidades adicionales"""
        if character.char_class not in self.skill_recommendations:
            return {'recommendations': [], 'reason': 'No hay recomendaciones disponibles'}
        
        available_skills = self.skill_recommendations[character.char_class]
        current_skills = set(character.skills)
        
        # Encontrar habilidades que no tiene
        new_skills = [skill for skill in available_skills if skill not in current_skills]
        
        return {
            'recommendations': new_skills[:2],  # Recomendar 2 habilidades
            'reason': f'Habilidades complementarias para {character.char_class}',
            'all_available': available_skills
        }
    
    def get_feat_recommendations(self, character: Character) -> Dict:
        """Recomendar feats según la clase"""
        if character.char_class not in self.feat_recommendations:
            return {'recommendations': [], 'reason': 'No hay feats recomendados'}
        
        available_feats = self.feat_recommendations[character.char_class]
        
        # Lógica simple: recomendar basado en clase
        if character.char_class == 'Fighter':
            if character.attributes.get('STR', 0) > 14:
                recommended = 'Great Weapon Master'
                reason = 'Tu alta Fuerza maximiza el daño con armas pesadas'
            else:
                recommended = 'Alert'
                reason = 'Iniciativa mejorada para combate táctico'
        elif character.char_class in ['Wizard', 'Sorcerer', 'Warlock']:
            recommended = 'War Caster'
            reason = 'Ventajas para lanzar hechizos en combate'
        else:
            recommended = available_feats[0]
            reason = f'Feat estándar para {character.char_class}'
        
        return {
            'recommendations': available_feats,
            'recommended': recommended,
            'reason': reason
        }
    
    def get_next_level_recommendations(self, character: Character) -> Dict:
        """Recomendaciones para el próximo nivel"""
        next_level = character.level + 1
        
        recommendations = {
            'level': next_level,
            'proficiency_bonus': (next_level - 1) // 4 + 2,
            'suggestions': []
        }
        
        # Sugerencias específicas por nivel
        if next_level == 4:
            recommendations['suggestions'].append('Considera tomar un feat o mejorar tus atributos principales')
        elif next_level == 5:
            recommendations['suggestions'].append('Obtienes un ataque extra (Extra Attack) si eres luchador, paladín o ranger')
        elif next_level == 6:
            recommendations['suggestions'].append('Muchas clases obtienen características importantes en este nivel')
        elif next_level == 8:
            recommendations['suggestions'].append('Nivel ideal para mejorar atributos o tomar feats poderosos')
        
        return recommendations 
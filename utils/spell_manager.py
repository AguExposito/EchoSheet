import json
import os
from typing import Dict, List, Optional
from logging_config import get_logger

# Configure logging
logger = get_logger(__name__)

class SpellManager:
    """Manages spell selection and validation according to D&D 5e rules"""
    
    def __init__(self):
        self.load_spell_data()
    
    def load_spell_data(self):
        """Load spell data from JSON file"""
        try:
            with open('data/spells.json', 'r', encoding='utf-8') as f:
                self.spell_data = json.load(f)
        except FileNotFoundError:
            logger.warning("spells.json not found. Using empty spell data.")
            self.spell_data = {"cantrips": {}, "spells": {}, "spellcasting_rules": {}}
    
    def get_available_cantrips(self, char_class: str) -> List[Dict]:
        """Get available cantrips for a class (case-insensitive)"""
        cantrips_dict = self.spell_data.get("cantrips", {})
        for key in cantrips_dict:
            if key.lower() == char_class.lower():
                return cantrips_dict[key]
        return []
    
    def get_available_spells(self, char_class: str, spell_level: str = "1st") -> List[Dict]:
        """Get available spells for a class at a specific level (case-insensitive)"""
        spells_by_level = self.spell_data.get("spells", {}).get(spell_level, {})
        for key in spells_by_level:
            if key.lower() == char_class.lower():
                return spells_by_level[key]
        return []
    
    def get_spellcasting_rules(self, char_class: str) -> Dict:
        """Get spellcasting rules for a class (case-insensitive)"""
        rules_dict = self.spell_data.get("spellcasting_rules", {})
        for key in rules_dict:
            if key.lower() == char_class.lower():
                return rules_dict[key]
        return {}
    
    def get_cantrips_known_limit(self, char_class: str) -> int:
        """Get the number of cantrips a class can know at level 1"""
        rules = self.get_spellcasting_rules(char_class)
        return rules.get("cantrips_known", 0)
    
    def get_spells_known_limit(self, char_class: str) -> int:
        """Get the number of spells a class can know at level 1"""
        rules = self.get_spellcasting_rules(char_class)
        return rules.get("spells_known", 0)
    
    def get_spell_slots(self, char_class: str, level: int = 1) -> Dict[str, int]:
        """Get spell slots for a class at a specific level"""
        rules = self.get_spellcasting_rules(char_class)
        return rules.get("spell_slots", {})
    
    def validate_spell_selection(self, char_class: str, selected_cantrips: List[str], 
                               selected_spells: List[str]) -> Dict[str, any]:
        """Validate spell selection according to D&D 5e rules"""
        errors = []
        warnings = []
        
        # Get limits
        cantrip_limit = self.get_cantrips_known_limit(char_class)
        spell_limit = self.get_spells_known_limit(char_class)
        
        # Validate cantrips
        if len(selected_cantrips) > cantrip_limit:
            errors.append(f"Too many cantrips selected: {len(selected_cantrips)}. Maximum is {cantrip_limit}.")
        
        # Validate spells
        if len(selected_spells) > spell_limit:
            errors.append(f"Too many spells selected: {len(selected_spells)}. Maximum is {spell_limit}.")
        
        # Check if selected cantrips are available for the class
        available_cantrips = [spell["name"] for spell in self.get_available_cantrips(char_class)]
        for cantrip in selected_cantrips:
            if cantrip not in available_cantrips:
                errors.append(f"Cantrip '{cantrip}' is not available for {char_class}.")
        
        # Check if selected spells are available for the class
        available_spells = [spell["name"] for spell in self.get_available_spells(char_class)]
        for spell in selected_spells:
            if spell not in available_spells:
                errors.append(f"Spell '{spell}' is not available for {char_class}.")
        
        # Check for duplicates
        if len(selected_cantrips) != len(set(selected_cantrips)):
            errors.append("Duplicate cantrips selected.")
        
        if len(selected_spells) != len(set(selected_spells)):
            errors.append("Duplicate spells selected.")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings,
            'cantrip_limit': cantrip_limit,
            'spell_limit': spell_limit,
            'selected_cantrips': len(selected_cantrips),
            'selected_spells': len(selected_spells)
        }
    
    def get_spell_suggestions(self, char_class: str, num_cantrips: int = None, 
                            num_spells: int = None) -> Dict[str, List[str]]:
        """Get spell suggestions for a class"""
        available_cantrips = self.get_available_cantrips(char_class)
        available_spells = self.get_available_spells(char_class)
        
        # Use limits if not specified
        if num_cantrips is None:
            num_cantrips = self.get_cantrips_known_limit(char_class)
        if num_spells is None:
            num_spells = self.get_spells_known_limit(char_class)
        
        # Ensure we have the exact limits
        cantrip_limit = self.get_cantrips_known_limit(char_class)
        spell_limit = self.get_spells_known_limit(char_class)
        
        # Use the actual limits if not specified
        if num_cantrips is None:
            num_cantrips = cantrip_limit
        if num_spells is None:
            num_spells = spell_limit
        
        # Select cantrips - ALWAYS fill to the limit
        suggested_cantrips = []
        if available_cantrips and num_cantrips > 0:
            # Create a copy to avoid modifying the original list
            available_cantrips_copy = available_cantrips.copy()
            
            # Prioritize damage cantrips for spellcasters
            damage_cantrips = [c for c in available_cantrips_copy if any(keyword in c["name"].lower() 
                                                                       for keyword in ["fire", "ray", "bolt", "blast", "vicious"])]
            utility_cantrips = [c for c in available_cantrips_copy if c not in damage_cantrips]
            
            # Select damage cantrips first (up to half the slots)
            damage_slots = min(num_cantrips // 2, len(damage_cantrips))
            for i in range(damage_slots):
                if i < len(damage_cantrips):
                    suggested_cantrips.append(damage_cantrips[i]["name"])
            
            # Fill remaining slots with utility cantrips
            remaining_slots = num_cantrips - len(suggested_cantrips)
            for i in range(remaining_slots):
                if i < len(utility_cantrips):
                    suggested_cantrips.append(utility_cantrips[i]["name"])
            
            # If we still don't have enough, take any available cantrips
            if len(suggested_cantrips) < num_cantrips:
                all_cantrips = [c["name"] for c in available_cantrips_copy]
                for cantrip_name in all_cantrips:
                    if cantrip_name not in suggested_cantrips and len(suggested_cantrips) < num_cantrips:
                        suggested_cantrips.append(cantrip_name)
            
            # Ensure we have exactly the right number (no duplicates)
            suggested_cantrips = list(dict.fromkeys(suggested_cantrips))[:num_cantrips]
        
        # Select spells - ALWAYS fill to the limit
        suggested_spells = []
        if available_spells and num_spells > 0:
            # Create a copy to avoid modifying the original list
            available_spells_copy = available_spells.copy()
            
            # Prioritize based on class role
            if char_class in ["Wizard", "Sorcerer"]:
                # Prioritize damage and utility spells
                damage_spells = [s for s in available_spells_copy if any(keyword in s["name"].lower() 
                                                                      for keyword in ["fire", "magic missile", "burning", "ray"])]
                utility_spells = [s for s in available_spells_copy if s not in damage_spells]
                
                # Select damage spells first (up to half the slots)
                damage_slots = min(num_spells // 2, len(damage_spells))
                for i in range(damage_slots):
                    if i < len(damage_spells):
                        suggested_spells.append(damage_spells[i]["name"])
                
                # Fill remaining slots with utility spells
                remaining_slots = num_spells - len(suggested_spells)
                for i in range(remaining_slots):
                    if i < len(utility_spells):
                        suggested_spells.append(utility_spells[i]["name"])
                    
            elif char_class in ["Cleric", "Druid"]:
                # Prioritize healing and support spells
                healing_spells = [s for s in available_spells_copy if "cure" in s["name"].lower()]
                support_spells = [s for s in available_spells_copy if s not in healing_spells]
                
                # Select healing spells first (up to half the slots)
                healing_slots = min(num_spells // 2, len(healing_spells))
                for i in range(healing_slots):
                    if i < len(healing_spells):
                        suggested_spells.append(healing_spells[i]["name"])
                
                # Fill remaining slots with support spells
                remaining_slots = num_spells - len(suggested_spells)
                for i in range(remaining_slots):
                    if i < len(support_spells):
                        suggested_spells.append(support_spells[i]["name"])
                    
            elif char_class in ["Bard", "Warlock"]:
                # Balanced selection
                for i in range(min(num_spells, len(available_spells_copy))):
                    suggested_spells.append(available_spells_copy[i]["name"])
            else:
                # For other classes, just take the first available
                for i in range(min(num_spells, len(available_spells_copy))):
                    suggested_spells.append(available_spells_copy[i]["name"])
            
            # If we still don't have enough spells, take any available
            if len(suggested_spells) < num_spells:
                all_spells = [s["name"] for s in available_spells_copy]
                for spell_name in all_spells:
                    if spell_name not in suggested_spells and len(suggested_spells) < num_spells:
                        suggested_spells.append(spell_name)
            
                    # Ensure we have exactly the right number (no duplicates)
        suggested_spells = list(dict.fromkeys(suggested_spells))[:num_spells]
        
        # Final validation and adjustment
        if len(suggested_cantrips) < num_cantrips and available_cantrips:
            # Fill remaining cantrip slots
            remaining_cantrips = [c["name"] for c in available_cantrips if c["name"] not in suggested_cantrips]
            needed_cantrips = num_cantrips - len(suggested_cantrips)
            additional_cantrips = remaining_cantrips[:needed_cantrips]
            suggested_cantrips.extend(additional_cantrips)
        
        if len(suggested_spells) < num_spells and available_spells:
            # Fill remaining spell slots
            remaining_spells = [s["name"] for s in available_spells if s["name"] not in suggested_spells]
            needed_spells = num_spells - len(suggested_spells)
            additional_spells = remaining_spells[:needed_spells]
            suggested_spells.extend(additional_spells)
        
        # Final trim to exact limits
        suggested_cantrips = suggested_cantrips[:num_cantrips]
        suggested_spells = suggested_spells[:num_spells]
        
        return {
            'cantrips': suggested_cantrips,
            'spells': suggested_spells
        }
    
    def get_spell_info(self, spell_name: str) -> Optional[Dict]:
        """Get detailed information about a specific spell from all available spells"""
        # Search in all cantrips
        cantrips_dict = self.spell_data.get("cantrips", {})
        for class_name, cantrips in cantrips_dict.items():
            for cantrip in cantrips:
                if cantrip["name"] == spell_name:
                    return cantrip
        
        # Search in all spells
        spells_dict = self.spell_data.get("spells", {})
        for level, level_spells in spells_dict.items():
            for class_name, spells in level_spells.items():
                for spell in spells:
                    if spell["name"] == spell_name:
                        return spell
        
        return None
    
    def format_spell_description(self, spell: Dict) -> str:
        """Format spell information for display"""
        components = ", ".join(spell.get("components", []))
        return f"{spell['name']} ({spell['school']}) - {spell['casting_time']}, Range: {spell['range']}, Components: {components}, Duration: {spell['duration']}"
    
    def get_spellcasting_ability(self, char_class: str) -> str:
        """Get the spellcasting ability for a class"""
        rules = self.get_spellcasting_rules(char_class)
        return rules.get("spellcasting_ability", "")
    
    def can_cast_spells(self, char_class: str) -> bool:
        """Check if a class can cast spells at level 1"""
        rules = self.get_spellcasting_rules(char_class)
        return rules.get("spells_known", 0) > 0 or rules.get("cantrips_known", 0) > 0 
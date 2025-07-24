import json
import os
from typing import Dict, List, Optional

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
            print("Warning: spells.json not found. Using empty spell data.")
            self.spell_data = {"cantrips": {}, "spells": {}, "spellcasting_rules": {}}
    
    def get_available_cantrips(self, char_class: str) -> List[Dict]:
        """Get available cantrips for a class"""
        return self.spell_data.get("cantrips", {}).get(char_class, [])
    
    def get_available_spells(self, char_class: str, spell_level: str = "1st") -> List[Dict]:
        """Get available spells for a class at a specific level"""
        return self.spell_data.get("spells", {}).get(spell_level, {}).get(char_class, [])
    
    def get_spellcasting_rules(self, char_class: str) -> Dict:
        """Get spellcasting rules for a class"""
        return self.spell_data.get("spellcasting_rules", {}).get(char_class, {})
    
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
        
        print(f"Getting spell suggestions for {char_class}: {num_cantrips} cantrips, {num_spells} spells")
        print(f"Available cantrips: {len(available_cantrips)}, Available spells: {len(available_spells)}")
        
        # Debug: Print available cantrip names
        if available_cantrips:
            print(f"Available cantrip names: {[c['name'] for c in available_cantrips]}")
        if available_spells:
            print(f"Available spell names: {[s['name'] for s in available_spells]}")
        
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
        
        print(f"Selected {len(suggested_cantrips)} cantrips: {suggested_cantrips}")
        print(f"Selected {len(suggested_spells)} spells: {suggested_spells}")
        
        # Final validation
        if len(suggested_cantrips) != num_cantrips:
            print(f"WARNING: Cantrip count mismatch. Expected {num_cantrips}, got {len(suggested_cantrips)}")
        if len(suggested_spells) != num_spells:
            print(f"WARNING: Spell count mismatch. Expected {num_spells}, got {len(suggested_spells)}")
        
        # Check for duplicates
        if len(suggested_cantrips) != len(set(suggested_cantrips)):
            print(f"WARNING: Duplicate cantrips detected: {suggested_cantrips}")
        if len(suggested_spells) != len(set(suggested_spells)):
            print(f"WARNING: Duplicate spells detected: {suggested_spells}")
        
        return {
            'cantrips': suggested_cantrips,
            'spells': suggested_spells
        }
    
    def get_spell_info(self, spell_name: str, char_class: str) -> Optional[Dict]:
        """Get detailed information about a specific spell"""
        # Search in cantrips first
        available_cantrips = self.get_available_cantrips(char_class)
        for cantrip in available_cantrips:
            if cantrip["name"] == spell_name:
                return cantrip
        
        # Search in spells
        available_spells = self.get_available_spells(char_class)
        for spell in available_spells:
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
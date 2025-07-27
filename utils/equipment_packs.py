"""
D&D 5e Equipment Packs
Based on the Player's Handbook equipment packs
"""

EQUIPMENT_PACKS = {
    "Burglar's Pack": {
        "description": "Perfect for rogues and stealthy characters",
        "items": [
            "Backpack",
            "Bag of 1,000 ball bearings",
            "10 feet of string",
            "Bell",
            "5 candles",
            "Crowbar",
            "Hammer",
            "10 pitons",
            "Hooded lantern",
            "2 flasks of oil",
            "5 days of rations",
            "Tinderbox",
            "Waterskin",
            "50 feet of hempen rope"
        ],
        "item_weights": {
            "Backpack": 5.0,
            "Bag of 1,000 ball bearings": 2.0,
            "10 feet of string": 0.0,
            "Bell": 0.0,
            "5 candles": 0.0,
            "Crowbar": 5.0,
            "Hammer": 3.0,
            "10 pitons": 2.5,
            "Hooded lantern": 2.0,
            "2 flasks of oil": 2.0,
            "5 days of rations": 10.0,
            "Tinderbox": 1.0,
            "Waterskin": 5.0,
            "50 feet of hempen rope": 10.0
        },
        "currency": {"gp": 16}
    },
    
    "Diplomat's Pack": {
        "description": "Ideal for characters focused on social interaction",
        "items": [
            "Chest",
            "2 cases for maps and scrolls",
            "Fine clothes",
            "Bottle of ink",
            "Ink pen",
            "Lamp",
            "2 flasks of oil",
            "5 sheets of paper",
            "Vial of perfume",
            "Sealing wax",
            "Soap"
        ],
        "item_weights": {
            "Chest": 25.0,
            "2 cases for maps and scrolls": 1.0,
            "Fine clothes": 6.0,
            "Bottle of ink": 0.0,
            "Ink pen": 0.0,
            "Lamp": 1.0,
            "2 flasks of oil": 2.0,
            "5 sheets of paper": 0.0,
            "Vial of perfume": 0.0,
            "Sealing wax": 0.0,
            "Soap": 0.0
        },
        "currency": {"gp": 39}
    },
    
    "Dungeoneer's Pack": {
        "description": "Essential for exploring dungeons and caves",
        "items": [
            "Backpack",
            "Crowbar",
            "Hammer",
            "10 pitons",
            "10 torches",
            "Tinderbox",
            "10 days of rations",
            "Waterskin",
            "50 feet of hempen rope"
        ],
        "item_weights": {
            "Backpack": 5.0,
            "Crowbar": 5.0,
            "Hammer": 3.0,
            "10 pitons": 2.5,
            "10 torches": 10.0,
            "Tinderbox": 1.0,
            "10 days of rations": 20.0,
            "Waterskin": 5.0,
            "50 feet of hempen rope": 10.0
        },
        "currency": {"gp": 12}
    },
    
    "Entertainer's Pack": {
        "description": "Perfect for bards and performers",
        "items": [
            "Backpack",
            "Bedroll",
            "2 costumes",
            "5 candles",
            "5 days of rations",
            "Waterskin",
            "Disguise kit"
        ],
        "item_weights": {
            "Backpack": 5.0,
            "Bedroll": 7.0,
            "2 costumes": 8.0,
            "5 candles": 0.0,
            "5 days of rations": 10.0,
            "Waterskin": 5.0,
            "Disguise kit": 3.0
        },
        "currency": {"gp": 40}
    },
    
    "Explorer's Pack": {
        "description": "Great for wilderness exploration and survival",
        "items": [
            "Backpack",
            "Bedroll",
            "Mess kit",
            "Tinderbox",
            "10 torches",
            "10 days of rations",
            "Waterskin",
            "50 feet of hempen rope"
        ],
        "item_weights": {
            "Backpack": 5.0,
            "Bedroll": 7.0,
            "Mess kit": 1.0,
            "Tinderbox": 1.0,
            "10 torches": 10.0,
            "10 days of rations": 20.0,
            "Waterskin": 5.0,
            "50 feet of hempen rope": 10.0
        },
        "currency": {"gp": 10}
    },
    
    "Priest's Pack": {
        "description": "Ideal for clerics and religious characters",
        "items": [
            "Backpack",
            "Blanket",
            "10 candles",
            "Tinderbox",
            "Alms box",
            "2 blocks of incense",
            "Censer",
            "Vestments",
            "2 days of rations",
            "Waterskin"
        ],
        "item_weights": {
            "Backpack": 5.0,
            "Blanket": 3.0,
            "10 candles": 0.0,
            "Tinderbox": 1.0,
            "Alms box": 1.0,
            "2 blocks of incense": 0.0,
            "Censer": 1.0,
            "Vestments": 4.0,
            "2 days of rations": 4.0,
            "Waterskin": 5.0
        },
        "currency": {"gp": 19}
    },
    
    "Scholar's Pack": {
        "description": "Perfect for wizards and knowledge seekers",
        "items": [
            "Backpack",
            "Book of lore",
            "Bottle of ink",
            "Ink pen",
            "10 sheets of parchment",
            "Little bag of sand",
            "Small knife"
        ],
        "item_weights": {
            "Backpack": 5.0,
            "Book of lore": 5.0,
            "Bottle of ink": 0.0,
            "Ink pen": 0.0,
            "10 sheets of parchment": 0.0,
            "Little bag of sand": 1.0,
            "Small knife": 1.0
        },
        "currency": {"gp": 40}
    }
}

def get_pack_info(pack_name: str) -> dict:
    """Get information about a specific equipment pack"""
    return EQUIPMENT_PACKS.get(pack_name, {})

def get_all_packs() -> dict:
    """Get all available equipment packs"""
    return EQUIPMENT_PACKS

def calculate_pack_weight(pack_name: str) -> float:
    """Calculate the total weight of an equipment pack"""
    pack = get_pack_info(pack_name)
    if not pack:
        return 0.0
    
    total_weight = 0.0
    for item, weight in pack.get("item_weights", {}).items():
        total_weight += weight
    
    return round(total_weight, 1) 
from flask import Flask, render_template, request, jsonify, redirect, url_for
import sqlite3
import json
import os
from datetime import datetime
from models import Character
from utils.autofill import AutoFill
from utils.recommender import Recommender
from utils.chat_engine import ChatEngine
from utils.spell_manager import SpellManager

def init_db():
    """Initialize database"""
    conn = sqlite3.connect('db.sqlite')
    cursor = conn.cursor()
    
    # Check if table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='characters'")
    table_exists = cursor.fetchone()
    
    if not table_exists:
        # Create new table with optimized columns
        cursor.execute('''
            CREATE TABLE characters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            race TEXT NOT NULL,
            char_class TEXT NOT NULL,
            level INTEGER DEFAULT 1,
            background TEXT,
            attributes TEXT,
            skills TEXT,
            feats TEXT,
            cantrips TEXT,
            spells_known TEXT,
            personality_traits TEXT,
            history_log TEXT,
            chat_history TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
        print("Created new characters table")
    else:
        # Check existing columns and add missing ones
        cursor.execute("PRAGMA table_info(characters)")
        existing_columns = [column[1] for column in cursor.fetchall()]
        
        missing_columns = []
        required_columns = [
            'cantrips', 'spells_known', 'background_story', 'short_term_goals', 'long_term_goals', 
            'personal_goals', 'personality_tags', 'flaws', 'currency', 'items', 'item_weights',
            'alignment', 'experience_points', 'age', 'height', 'weight', 'eyes', 'skin', 'hair',
            'hit_point_maximum', 'current_hit_points', 'temporary_hit_points', 'hit_dice',
            'ideals', 'bonds'
        ]
        
        for column in required_columns:
            if column not in existing_columns:
                missing_columns.append(column)
        
        # Add missing columns
        for column in missing_columns:
            try:
                cursor.execute(f'ALTER TABLE characters ADD COLUMN {column} TEXT')
                print(f"Added missing column: {column}")
            except sqlite3.OperationalError as e:
                print(f"Error adding column {column}: {e}")
    
    conn.commit()
    conn.close()
    print("Database initialization completed")

app = Flask(__name__)
app.secret_key = 'echo_sheet_secret_key'

# Initialize database
init_db()

# Inicializar utilidades
autofill = AutoFill()
recommender = Recommender()
chat_engine = ChatEngine()
spell_manager = SpellManager()

@app.route('/')
def index():
    """Main page with character list"""
    conn = sqlite3.connect('db.sqlite')
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, race, char_class, level FROM characters ORDER BY created_at DESC')
    characters = cursor.fetchall()
    conn.close()
    
    return render_template('index.html', characters=characters)

@app.route('/create', methods=['GET', 'POST'])
def create_character():
    """Create new character"""
    if request.method == 'POST':
        try:
            data = request.get_json()
            print(f"Received data: {data}")
            
            # Validate required fields
            required_fields = ['name', 'race', 'char_class', 'background']
            for field in required_fields:
                if not data.get(field):
                    return jsonify({'success': False, 'error': f'Missing required field: {field}'})
        
        # Create character with basic data
            character = Character(
                name=data['name'],
                race=data['race'],
                char_class=data['char_class'],
                level=max(1, min(20, data.get('level', 1))),  # Cap level between 1-20
                background=data.get('background', '')
            )
        except Exception as e:
            print(f"Error processing request: {e}")
            return jsonify({'success': False, 'error': f'Error processing request: {str(e)}'})
        
        # Set custom attributes if provided
        if 'attributes' in data:
            # Validate attribute points
            point_costs = {8: 0, 9: 1, 10: 2, 11: 3, 12: 4, 13: 5, 14: 7, 15: 9}
            total_cost = 0
            
            for attr, value in data['attributes'].items():
                # Convert string to int if necessary
                try:
                    value = int(value)
                except (ValueError, TypeError):
                    return jsonify({'success': False, 'error': f'Invalid {attr} value: {value}. Must be a number between 8-15.'})
                
                if value < 8 or value > 15:
                    return jsonify({'success': False, 'error': f'Invalid {attr} value: {value}. Must be between 8-15.'})
                if value in point_costs:
                    total_cost += point_costs[value]
                else:
                    return jsonify({'success': False, 'error': f'Invalid {attr} value: {value}'})
            
            if total_cost > 27:
                return jsonify({'success': False, 'error': f'Too many attribute points used: {total_cost}. Maximum is 27.'})
            
            character.attributes = data['attributes']
        else:
            # Autofill data if no custom attributes
            autofill.fill_character(character)
        
        # Set custom skills if provided
        if 'skills' in data:
            # Validate skill count based on class and background
            char_class = data['char_class']
            background = data.get('background', '')
            
            # Expected skill choices
            class_choices = {
                'Fighter': 2, 'Wizard': 2, 'Cleric': 2, 'Rogue': 4,
                'Ranger': 3, 'Paladin': 2, 'Bard': 3, 'Sorcerer': 2,
                'Warlock': 2, 'Monk': 2, 'Druid': 2, 'Barbarian': 2
            }
            
            expected_choices = class_choices.get(char_class, 0) + 2  # +2 for background
            
            if len(data['skills']) != expected_choices:
                return jsonify({
                    'success': False, 
                    'error': f'Invalid number of skills: {len(data["skills"])}. Expected {expected_choices} for {char_class} with {background} background.'
                })
            
            character.skills = data['skills']
        elif not character.skills:
            # Generate skills if not provided
            autofill.fill_character(character)
        
        # Set custom spells if provided
        if 'spells' in data:
            spells_data = data['spells']
            cantrips = spells_data.get('cantrips', [])
            spells_known = spells_data.get('spells', [])
            
            # Validate spell selection
            validation = spell_manager.validate_spell_selection(
                character.char_class, cantrips, spells_known
            )
            
            if not validation['valid']:
                return jsonify({
                    'success': False,
                    'error': 'Invalid spell selection: ' + '; '.join(validation['errors'])
                })
            
            character.cantrips = cantrips
            character.spells_known = spells_known
            character.spells = cantrips + spells_known  # Combined list for compatibility
        else:
            # Always generate spells for spellcasters if not provided
            if spell_manager.can_cast_spells(character.char_class):
                autofill.fill_character(character)
                
                # If autofill didn't work, try direct spell generation
                if not character.cantrips and not character.spells_known:
                    suggestions = spell_manager.get_spell_suggestions(character.char_class)
                    character.cantrips = suggestions['cantrips']
                    character.spells_known = suggestions['spells']
                    character.spells = character.cantrips + character.spells_known
        
        # Save to database
        try:
            conn = sqlite3.connect('db.sqlite')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO characters (name, race, char_class, level, background, 
                                        attributes, skills, feats, cantrips, spells_known, personality_traits,
                                        background_story, short_term_goals, long_term_goals, personal_goals, personality_tags, flaws,
                                        currency, items, item_weights)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                character.name, character.race, character.char_class, character.level,
                character.background, json.dumps(character.attributes),
                json.dumps(character.skills), json.dumps(character.feats),
                    json.dumps(character.cantrips), json.dumps(character.spells_known), 
                character.personality_traits, character.background_story,
                character.short_term_goals, character.long_term_goals, character.personal_goals,
                json.dumps(character.personality_tags), character.flaws,
                json.dumps(character.currency), json.dumps(character.items), json.dumps(character.item_weights)
            ))
            character_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            print(f"Character created successfully with ID: {character_id}")
            return jsonify({'success': True, 'character_id': character_id})
        except Exception as e:
            print(f"Database error: {e}")
            return jsonify({'success': False, 'error': f'Database error: {str(e)}'})
    
    return render_template('create.html')

@app.route('/character/<int:character_id>')
def view_character(character_id):
    """View character sheet"""
    conn = sqlite3.connect('db.sqlite')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM characters WHERE id = ?', (character_id,))
    char_data = cursor.fetchone()
    conn.close()
    
    if not char_data:
        return redirect(url_for('index'))
    
    # Convert database data to Character object
    character = Character(
        id=char_data[0],
        name=char_data[1],
        race=char_data[2],
        char_class=char_data[3],
        level=char_data[4],
        background=char_data[5],
        alignment=char_data[25] if len(char_data) > 25 and char_data[25] else '',
        experience_points=char_data[26] if len(char_data) > 26 and char_data[26] else 0,
        age=char_data[27] if len(char_data) > 27 and char_data[27] else '',
        height=char_data[28] if len(char_data) > 28 and char_data[28] else '',
        weight=char_data[29] if len(char_data) > 29 and char_data[29] else '',
        eyes=char_data[30] if len(char_data) > 30 and char_data[30] else '',
        skin=char_data[31] if len(char_data) > 31 and char_data[31] else '',
        hair=char_data[32] if len(char_data) > 32 and char_data[32] else '',
        hit_point_maximum=char_data[33] if len(char_data) > 33 and char_data[33] else 0,
        current_hit_points=char_data[34] if len(char_data) > 34 and char_data[34] else 0,
        temporary_hit_points=char_data[35] if len(char_data) > 35 and char_data[35] else 0,
        hit_dice=char_data[36] if len(char_data) > 36 and char_data[36] else '',
        attributes=json.loads(char_data[6]) if char_data[6] and char_data[6].strip() else {},
        skills=json.loads(char_data[7]) if char_data[7] and char_data[7].strip() else [],
        feats=json.loads(char_data[8]) if char_data[8] and char_data[8].strip() else [],
        cantrips=json.loads(char_data[14]) if char_data[14] and char_data[14].strip() else [],
        spells_known=json.loads(char_data[15]) if char_data[15] and char_data[15].strip() else [],
        personality_traits=char_data[10] or '',
        ideals=char_data[37] if len(char_data) > 37 and char_data[37] else '',
        bonds=char_data[38] if len(char_data) > 38 and char_data[38] else '',
        background_story=char_data[16] if len(char_data) > 16 and char_data[16] else '',
        short_term_goals=char_data[17] if len(char_data) > 17 and char_data[17] else '',
        long_term_goals=char_data[18] if len(char_data) > 18 and char_data[18] else '',
        personal_goals=char_data[19] if len(char_data) > 19 and char_data[19] else '',
        personality_tags=json.loads(char_data[20]) if len(char_data) > 20 and char_data[20] and char_data[20].strip() else [],
        flaws=char_data[21] if len(char_data) > 21 and char_data[21] else '',
        currency=json.loads(char_data[22]) if len(char_data) > 22 and char_data[22] and char_data[22].strip() else {},
        items=json.loads(char_data[23]) if len(char_data) > 23 and char_data[23] and char_data[23].strip() else [],
        item_weights=json.loads(char_data[24]) if len(char_data) > 24 and char_data[24] and char_data[24].strip() else {}
    )
    
    # Combine cantrips and spells_known for backward compatibility
    character.spells = character.cantrips + character.spells_known
    
    # Get detailed spell information for display
    cantrips_info = []
    spells_info = []
    
    for cantrip_name in character.cantrips:
        spell_info = spell_manager.get_spell_info(cantrip_name)
        if spell_info:
            cantrips_info.append(spell_info)
    
    for spell_name in character.spells_known:
        spell_info = spell_manager.get_spell_info(spell_name)
        if spell_info:
            spells_info.append(spell_info)
    
    # Get recommendations
    recommendations = recommender.get_recommendations(character)
    
    return render_template('character.html', 
                         character=character, 
                         recommendations=recommendations,
                         cantrips_info=cantrips_info,
                         spells_info=spells_info)

@app.route('/character/<int:character_id>/chat', methods=['GET', 'POST'])
def chat_with_character(character_id):
    """Chat with character"""
    conn = sqlite3.connect('db.sqlite')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM characters WHERE id = ?', (character_id,))
    char_data = cursor.fetchone()
    conn.close()
    
    if not char_data:
        return redirect(url_for('index'))
    
    character = Character(
        id=char_data[0],
        name=char_data[1],
        race=char_data[2],
        char_class=char_data[3],
        level=char_data[4],
        background=char_data[5],
        alignment=char_data[25] if len(char_data) > 25 and char_data[25] else '',
        experience_points=char_data[26] if len(char_data) > 26 and char_data[26] else 0,
        age=char_data[27] if len(char_data) > 27 and char_data[27] else '',
        height=char_data[28] if len(char_data) > 28 and char_data[28] else '',
        weight=char_data[29] if len(char_data) > 29 and char_data[29] else '',
        eyes=char_data[30] if len(char_data) > 30 and char_data[30] else '',
        skin=char_data[31] if len(char_data) > 31 and char_data[31] else '',
        hair=char_data[32] if len(char_data) > 32 and char_data[32] else '',
        hit_point_maximum=char_data[33] if len(char_data) > 33 and char_data[33] else 0,
        current_hit_points=char_data[34] if len(char_data) > 34 and char_data[34] else 0,
        temporary_hit_points=char_data[35] if len(char_data) > 35 and char_data[35] else 0,
        hit_dice=char_data[36] if len(char_data) > 36 and char_data[36] else '',
        attributes=json.loads(char_data[6]) if char_data[6] and char_data[6].strip() else {},
        skills=json.loads(char_data[7]) if char_data[7] and char_data[7].strip() else [],
        feats=json.loads(char_data[8]) if char_data[8] and char_data[8].strip() else [],
        cantrips=json.loads(char_data[14]) if char_data[14] and char_data[14].strip() else [],
        spells_known=json.loads(char_data[15]) if char_data[15] and char_data[15].strip() else [],
        personality_traits=char_data[10] or '',
        ideals=char_data[37] if len(char_data) > 37 and char_data[37] else '',
        bonds=char_data[38] if len(char_data) > 38 and char_data[38] else '',
        background_story=char_data[16] if len(char_data) > 16 and char_data[16] else '',
        short_term_goals=char_data[17] if len(char_data) > 17 and char_data[17] else '',
        long_term_goals=char_data[18] if len(char_data) > 18 and char_data[18] else '',
        personal_goals=char_data[19] if len(char_data) > 19 and char_data[19] else '',
        personality_tags=json.loads(char_data[20]) if len(char_data) > 20 and char_data[20] and char_data[20].strip() else [],
        flaws=char_data[21] if len(char_data) > 21 and char_data[21] else '',
        currency=json.loads(char_data[22]) if len(char_data) > 22 and char_data[22] and char_data[22].strip() else {},
        items=json.loads(char_data[23]) if len(char_data) > 23 and char_data[23] and char_data[23].strip() else [],
        item_weights=json.loads(char_data[24]) if len(char_data) > 24 and char_data[24] and char_data[24].strip() else {},
        chat_history=json.loads(char_data[12]) if char_data[12] and char_data[12].strip() else []
    )
    
    # Combine cantrips and spells_known for backward compatibility
    character.spells = character.cantrips + character.spells_known
    
    if request.method == 'POST':
        data = request.get_json()
        user_message = data.get('message', '')
        
        # Generate character response
        response = chat_engine.get_response(character, user_message)
        
        # Save to history
        chat_entry = {
            'timestamp': datetime.now().isoformat(),
            'user': user_message,
            'character': response
        }
        character.chat_history.append(chat_entry)
        
        # Update database
        conn = sqlite3.connect('db.sqlite')
        cursor = conn.cursor()
        cursor.execute('UPDATE characters SET chat_history = ? WHERE id = ?',
                      (json.dumps(character.chat_history), character_id))
        conn.commit()
        conn.close()
        
        return jsonify({'response': response})
    
    return render_template('chat.html', character=character)

@app.route('/character/<int:character_id>/delete', methods=['POST'])
def delete_character(character_id):
    """Delete character with confirmation"""
    conn = sqlite3.connect('db.sqlite')
    cursor = conn.cursor()
    
    # Verify character exists
    cursor.execute('SELECT name FROM characters WHERE id = ?', (character_id,))
    char_data = cursor.fetchone()
    
    if not char_data:
        conn.close()
        return jsonify({'success': False, 'error': 'Character not found'})
    
    # Delete character
    cursor.execute('DELETE FROM characters WHERE id = ?', (character_id,))
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'message': f'Character "{char_data[0]}" deleted successfully'})

@app.route('/api/autofill', methods=['POST'])
def api_autofill():
    """API to autofill character data"""
    try:
        data = request.get_json()
        print(f"Received autofill request: {data}")
        
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'})
        
        char_class = data.get('char_class', '')
        background = data.get('background', '')
        race = data.get('race', '')
        playstyle = data.get('playstyle', '')
        
        print(f"Processing: class={char_class}, background={background}, race={race}, playstyle={playstyle}")
        
        if not char_class or not background:
            return jsonify({'success': False, 'error': 'Class and background are required'})
        
        # Get suggestions that respect available skills and playstyle
        suggestions = autofill.get_suggestions(char_class, background, race, playstyle)
        print(f"Generated suggestions: {suggestions}")
        
        return jsonify({
            'success': True,
            'attributes': suggestions['attributes'],
            'skills': suggestions['skills'],
            'spells': suggestions['spells'],
            'available_playstyles': suggestions['available_playstyles'],
            'current_playstyle': suggestions['current_playstyle']
        })
    except Exception as e:
        print(f"Error in autofill: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/spells/<char_class>', methods=['GET'])
def get_spells(char_class):
    """Get available spells for a class"""
    try:
        cantrips = spell_manager.get_available_cantrips(char_class)
        spells = spell_manager.get_available_spells(char_class)
        rules = spell_manager.get_spellcasting_rules(char_class)
        
        return jsonify({
            'success': True,
            'cantrips': cantrips,
            'spells': spells,
            'rules': rules
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/spells/validate', methods=['POST'])
def validate_spells():
    """Validate spell selection"""
    try:
        data = request.get_json()
        char_class = data.get('char_class', '')
        selected_cantrips = data.get('cantrips', [])
        selected_spells = data.get('spells', [])
        
        validation = spell_manager.validate_spell_selection(char_class, selected_cantrips, selected_spells)
        
        return jsonify({
            'success': True,
            'validation': validation
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/spells/suggestions/<char_class>', methods=['GET'])
def get_spell_suggestions(char_class):
    """Get spell suggestions for a class"""
    try:
        suggestions = spell_manager.get_spell_suggestions(char_class)
        
        return jsonify({
            'success': True,
            'suggestions': suggestions
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/playstyles/<char_class>', methods=['GET'])
def get_playstyles(char_class):
    """Get available playstyles for a class"""
    try:
        playstyles = autofill.get_available_playstyles(char_class)
        playstyle_data = {}
        
        for playstyle in playstyles:
            data = autofill.get_playstyle_data(char_class, playstyle)
            if data:
                playstyle_data[playstyle] = {
                    'description': data.get('description', ''),
                    'attributes': data.get('attributes', {}),
                    'skills': data.get('skills', []),
                    'spells': data.get('spells', []),
                    'cantrips': data.get('cantrips', [])
                }
        
        return jsonify({
            'success': True,
            'playstyles': playstyle_data
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/spell/<spell_name>', methods=['GET'])
def get_spell_info(spell_name):
    """Get detailed information for a specific spell"""
    try:
        spell_info = spell_manager.get_spell_info(spell_name)
        if spell_info:
            return jsonify({
                'success': True,
                'spell': spell_info
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Spell not found'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/character/<int:character_id>/personality', methods=['POST'])
def update_personality(character_id):
    """Update character personality fields"""
    try:
        data = request.get_json()
        
        # Get current character data
        conn = sqlite3.connect('db.sqlite')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM characters WHERE id = ?', (character_id,))
        char_data = cursor.fetchone()
        
        if not char_data:
            conn.close()
            return jsonify({'success': False, 'error': 'Character not found'}), 404
        
        # Update personality fields
        cursor.execute('''
            UPDATE characters SET 
                background_story = ?, 
                short_term_goals = ?, 
                long_term_goals = ?, 
                personal_goals = ?, 
                personality_traits = ?,
                ideals = ?,
                bonds = ?,
                personality_tags = ?, 
                flaws = ?
            WHERE id = ?
        ''', (
            data.get('background_story', ''),
            data.get('short_term_goals', ''),
            data.get('long_term_goals', ''),
            data.get('personal_goals', ''),
            data.get('personality_traits', ''),
            data.get('ideals', ''),
            data.get('bonds', ''),
            json.dumps(data.get('personality_tags', [])),
            data.get('flaws', ''),
            character_id
        ))
        
        conn.commit()
        conn.close()
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/character/<int:character_id>/inventory', methods=['POST'])
def update_inventory(character_id):
    """Update character inventory and currency"""
    try:
        data = request.get_json()
        
        # Get current character data
        conn = sqlite3.connect('db.sqlite')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM characters WHERE id = ?', (character_id,))
        char_data = cursor.fetchone()
        
        if not char_data:
            conn.close()
            return jsonify({'success': False, 'error': 'Character not found'}), 404
        
        # Update inventory fields
        cursor.execute('''
            UPDATE characters SET 
                currency = ?, 
                items = ?,
                item_weights = ?
            WHERE id = ?
        ''', (
            json.dumps(data.get('currency', {})),
            json.dumps(data.get('items', [])),
            json.dumps(data.get('item_weights', {})),
            character_id
        ))
        
        conn.commit()
        conn.close()
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/character/<int:character_id>/apply-pack', methods=['POST'])
def apply_equipment_pack(character_id):
    """Apply an equipment pack to a character"""
    try:
        from utils.equipment_packs import get_pack_info
        
        data = request.get_json()
        pack_name = data.get('pack_name')
        
        if not pack_name:
            return jsonify({'success': False, 'error': 'Pack name is required'}), 400
        
        # Get pack information
        pack_info = get_pack_info(pack_name)
        if not pack_info:
            return jsonify({'success': False, 'error': 'Pack not found'}), 404
        
        # Get current character data
        conn = sqlite3.connect('db.sqlite')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM characters WHERE id = ?', (character_id,))
        char_data = cursor.fetchone()
        
        if not char_data:
            conn.close()
            return jsonify({'success': False, 'error': 'Character not found'}), 404
        
        # Get current inventory
        current_items = json.loads(char_data[23]) if len(char_data) > 23 and char_data[23] and char_data[23].strip() else []
        current_currency = json.loads(char_data[22]) if len(char_data) > 22 and char_data[22] and char_data[22].strip() else {}
        current_weights = json.loads(char_data[24]) if len(char_data) > 24 and char_data[24] and char_data[24].strip() else {}
        
        # Add pack items (avoid duplicates)
        new_items = current_items.copy()
        for item in pack_info['items']:
            if item not in new_items:
                new_items.append(item)
        
        # Add pack weights
        new_weights = current_weights.copy()
        new_weights.update(pack_info['item_weights'])
        
        # Add pack currency
        new_currency = current_currency.copy()
        for currency_type, amount in pack_info['currency'].items():
            new_currency[currency_type] = new_currency.get(currency_type, 0) + amount
        
        # Update character
        cursor.execute('''
            UPDATE characters SET 
                currency = ?, 
                items = ?,
                item_weights = ?
            WHERE id = ?
        ''', (
            json.dumps(new_currency),
            json.dumps(new_items),
            json.dumps(new_weights),
            character_id
        ))
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'pack_name': pack_name,
            'items_added': pack_info['items'],
            'currency_added': pack_info['currency'],
            'total_weight': sum(pack_info['item_weights'].values())
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/character/<int:character_id>/basic-info', methods=['POST'])
def update_basic_info(character_id):
    """Update character basic information"""
    try:
        data = request.get_json()
        
        # Get current character data
        conn = sqlite3.connect('db.sqlite')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM characters WHERE id = ?', (character_id,))
        char_data = cursor.fetchone()
        
        if not char_data:
            conn.close()
            return jsonify({'success': False, 'error': 'Character not found'}), 404
        
        # Update basic info fields
        cursor.execute('''
            UPDATE characters SET 
                alignment = ?, 
                experience_points = ?
            WHERE id = ?
        ''', (
            data.get('alignment', ''),
            data.get('experience_points', 0),
            character_id
        ))
        
        conn.commit()
        conn.close()
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/character/<int:character_id>/physical-info', methods=['POST'])
def update_physical_info(character_id):
    """Update character physical characteristics"""
    try:
        data = request.get_json()
        
        # Get current character data
        conn = sqlite3.connect('db.sqlite')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM characters WHERE id = ?', (character_id,))
        char_data = cursor.fetchone()
        
        if not char_data:
            conn.close()
            return jsonify({'success': False, 'error': 'Character not found'}), 404
        
        # Update physical info fields
        cursor.execute('''
            UPDATE characters SET 
                age = ?, 
                height = ?, 
                weight = ?, 
                eyes = ?, 
                skin = ?, 
                hair = ?
            WHERE id = ?
        ''', (
            data.get('age', ''),
            data.get('height', ''),
            data.get('weight', ''),
            data.get('eyes', ''),
            data.get('skin', ''),
            data.get('hair', ''),
            character_id
        ))
        
        conn.commit()
        conn.close()
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/character/<int:character_id>/hit-points', methods=['POST'])
def update_hit_points(character_id):
    """Update character hit points"""
    try:
        data = request.get_json()
        
        # Get current character data
        conn = sqlite3.connect('db.sqlite')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM characters WHERE id = ?', (character_id,))
        char_data = cursor.fetchone()
        
        if not char_data:
            conn.close()
            return jsonify({'success': False, 'error': 'Character not found'}), 404
        
        # Update hit points fields
        cursor.execute('''
            UPDATE characters SET 
                hit_point_maximum = ?, 
                current_hit_points = ?, 
                temporary_hit_points = ?
            WHERE id = ?
        ''', (
            data.get('hit_point_maximum', 0),
            data.get('current_hit_points', 0),
            data.get('temporary_hit_points', 0),
            character_id
        ))
        
        conn.commit()
        conn.close()
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500



@app.route('/api/character/<int:character_id>/level-up', methods=['POST'])
def level_up_character(character_id):
    """Level up character"""
    try:
        # Get current character data
        conn = sqlite3.connect('db.sqlite')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM characters WHERE id = ?', (character_id,))
        char_data = cursor.fetchone()
        
        if not char_data:
            conn.close()
            return jsonify({'success': False, 'error': 'Character not found'}), 404
        
        # Load character from database data
        character = Character(
            id=char_data[0],
            name=char_data[1],
            race=char_data[2],
            char_class=char_data[3],
            level=char_data[4],
            background=char_data[5],
            alignment=char_data[25] if len(char_data) > 25 and char_data[25] else '',
            experience_points=char_data[26] if len(char_data) > 26 and char_data[26] else 0,
            age=char_data[27] if len(char_data) > 27 and char_data[27] else '',
            height=char_data[28] if len(char_data) > 28 and char_data[28] else '',
            weight=char_data[29] if len(char_data) > 29 and char_data[29] else '',
            eyes=char_data[30] if len(char_data) > 30 and char_data[30] else '',
            skin=char_data[31] if len(char_data) > 31 and char_data[31] else '',
            hair=char_data[32] if len(char_data) > 32 and char_data[32] else '',
            hit_point_maximum=char_data[33] if len(char_data) > 33 and char_data[33] else 0,
            current_hit_points=char_data[34] if len(char_data) > 34 and char_data[34] else 0,
            temporary_hit_points=char_data[35] if len(char_data) > 35 and char_data[35] else 0,
            hit_dice=char_data[36] if len(char_data) > 36 and char_data[36] else '',
            attributes=json.loads(char_data[6]) if char_data[6] and char_data[6].strip() else {},
            skills=json.loads(char_data[7]) if char_data[7] and char_data[7].strip() else [],
            feats=json.loads(char_data[8]) if char_data[8] and char_data[8].strip() else [],
            cantrips=json.loads(char_data[14]) if char_data[14] and char_data[14].strip() else [],
            spells_known=json.loads(char_data[15]) if char_data[15] and char_data[15].strip() else [],
            personality_traits=char_data[10] or '',
            ideals=char_data[37] if len(char_data) > 37 and char_data[37] else '',
            bonds=char_data[38] if len(char_data) > 38 and char_data[38] else '',
            background_story=char_data[16] if len(char_data) > 16 and char_data[16] else '',
            short_term_goals=char_data[17] if len(char_data) > 17 and char_data[17] else '',
            long_term_goals=char_data[18] if len(char_data) > 18 and char_data[18] else '',
            personal_goals=char_data[19] if len(char_data) > 19 and char_data[19] else '',
            personality_tags=json.loads(char_data[20]) if len(char_data) > 20 and char_data[20] and char_data[20].strip() else [],
            flaws=char_data[21] if len(char_data) > 21 and char_data[21] else '',
            currency=json.loads(char_data[22]) if len(char_data) > 22 and char_data[22] and char_data[22].strip() else {},
            items=json.loads(char_data[23]) if len(char_data) > 23 and char_data[23] and char_data[23].strip() else [],
            item_weights=json.loads(char_data[24]) if len(char_data) > 24 and char_data[24] and char_data[24].strip() else {}
        )
        
        # Check if character can level up
        if not character.can_level_up():
            conn.close()
            # Add debug information
            current_xp = int(character.experience_points) if character.experience_points else 0
            xp_needed = character.get_experience_to_next_level()
            return jsonify({
                'success': False, 
                'error': f'Character cannot level up yet. Current XP: {current_xp}, XP needed: {xp_needed}'
            }), 400
        
        # Level up
        new_level = character.level + 1
        
        # Keep the current XP (don't reset it)
        current_xp = int(character.experience_points) if character.experience_points else 0
        
        # Update character level (keep current XP)
        cursor.execute('''
            UPDATE characters SET 
                level = ?
            WHERE id = ?
        ''', (new_level, character_id))
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True, 
            'new_level': new_level,
            'message': f'Character leveled up to level {new_level}!'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500



if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000))) 
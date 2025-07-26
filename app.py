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
        required_columns = ['cantrips', 'spells_known']
        
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
        elif not character.spells:
            # Generate spells if not provided
            autofill.fill_character(character)
        
        # Save to database
        try:
            conn = sqlite3.connect('db.sqlite')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO characters (name, race, char_class, level, background, 
                                        attributes, skills, feats, cantrips, spells_known, personality_traits)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                character.name, character.race, character.char_class, character.level,
                character.background, json.dumps(character.attributes),
                json.dumps(character.skills), json.dumps(character.feats),
                    json.dumps(character.cantrips), json.dumps(character.spells_known), 
                    character.personality_traits
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
        attributes=json.loads(char_data[6]) if char_data[6] else {},
        skills=json.loads(char_data[7]) if char_data[7] else [],
        feats=json.loads(char_data[8]) if char_data[8] else [],
        cantrips=json.loads(char_data[9]) if char_data[9] else [],
        spells_known=json.loads(char_data[10]) if char_data[10] else [],
        personality_traits=char_data[11] or ''
    )
    
    # Combine cantrips and spells_known for backward compatibility
    character.spells = character.cantrips + character.spells_known
    
    # Get recommendations
    recommendations = recommender.get_recommendations(character)
    
    return render_template('character.html', character=character, recommendations=recommendations)

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
        attributes=json.loads(char_data[6]) if char_data[6] else {},
        skills=json.loads(char_data[7]) if char_data[7] else [],
        feats=json.loads(char_data[8]) if char_data[8] else [],
        cantrips=json.loads(char_data[9]) if char_data[9] else [],
        spells_known=json.loads(char_data[10]) if char_data[10] else [],
        personality_traits=char_data[11] or '',
        chat_history=json.loads(char_data[13]) if char_data[13] else []
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

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000))) 
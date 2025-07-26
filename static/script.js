// Funcionalidad principal de EchoSheet

document.addEventListener('DOMContentLoaded', function() {
    // Inicializar funcionalidades según la página
    if (document.getElementById('character-form')) {
        initCharacterCreation();
    }
    
    if (document.getElementById('chat-form')) {
        initChat();
    }
    
    // Inicializar botones de preguntas sugeridas
    initSuggestedQuestions();
    
    // Inicializar funcionalidad de eliminación de personajes
    initCharacterDeletion();
});

// Character creation functionality
function initCharacterCreation() {
    const form = document.getElementById('character-form');
    const autofillBtn = document.getElementById('autofill-btn');
    const applyBtn = document.getElementById('apply-btn');
    
    // Initialize character counter
    const nameInput = document.getElementById('name');
    const charCounter = document.querySelector('.char-counter');
    
    if (nameInput && charCounter) {
        nameInput.addEventListener('input', function() {
            const currentLength = this.value.length;
            const maxLength = this.maxLength;
            charCounter.textContent = `${currentLength}/${maxLength} characters`;
            
            // Change color when approaching limit
            if (currentLength >= maxLength * 0.9) {
                charCounter.style.color = '#e74c3c';
            } else if (currentLength >= maxLength * 0.7) {
                charCounter.style.color = '#f39c12';
            } else {
                charCounter.style.color = '#95a5a6';
            }
            
            // Only hide suggestions when name changes, not the preview
            const applyBtn = document.getElementById('apply-btn');
            if (applyBtn) {
                applyBtn.style.display = 'none';
            }
            
            // Update preview with new name
            updatePreview();
        });
    }
    

    
    // Track if suggestions are valid
    let suggestionsValid = false;
    

    let lastFormData = null;
    
    // Function to check if form data has changed (excluding name)
    function hasFormDataChanged() {
        const currentData = getFormData();
        if (!lastFormData) return false;
        
        // Compare all fields except name
        const fieldsToCompare = ['race', 'char_class', 'level', 'background'];
        for (const field of fieldsToCompare) {
            if (currentData[field] !== lastFormData[field]) {
                return true;
            }
        }
        return false;
    }
    
    // Function to hide suggestions
    function hideSuggestions() {
        if (previewSection) {
            previewSection.style.display = 'none';
        }
        if (applyBtn) {
            applyBtn.style.display = 'none';
        }
        suggestionsValid = false;
    }
    
    // Function to show suggestions

    
    // Monitor form changes
    form.addEventListener('change', function(e) {
        // If any field other than name changes, hide suggestions
        if (e.target.id !== 'name') {
            if (suggestionsValid) {
                hideSuggestions();
                showNotification('Suggestions hidden - form data has changed', 'info');
            }
            
            // Check if we should show spells section
            const charClass = document.getElementById('char_class').value;
            const background = document.getElementById('background').value;
            
            if (charClass && background) {
                // Check if class can cast spells
                checkSpellcasting();
            }
        }
    });
    
    // Initialize attribute controls
    initAttributeControls();
    
    // Initialize skill selection
    initSkillSelection();
    
    // Initialize spell selection
    initSpellSelection();
    
    // Autofill button
    autofillBtn.addEventListener('click', function() {
        const formData = getFormData();
        
        if (!formData.name || !formData.race || !formData.char_class || !formData.background) {
            showNotification('Please complete name, race, class and background before autofilling.', 'error');
            return;
        }
        
        autofillCharacter(formData);
        lastFormData = formData;
        showSuggestions();
    });
    
    // Apply suggestions button
    if (applyBtn) {
        applyBtn.addEventListener('click', function() {
            // Check if preview section is visible and has data
            const previewSection = document.getElementById('preview-section');
            if (!previewSection || previewSection.style.display === 'none') {
                showNotification('No suggestions available. Please generate suggestions first.', 'error');
                return;
            }
            
            // Check if there are attributes in the preview
            const previewAttributes = document.querySelectorAll('#preview-attributes .attribute-card');
            if (previewAttributes.length === 0) {
                showNotification('No attribute suggestions found. Please regenerate suggestions.', 'error');
                return;
            }
            
            applyAutofillSuggestions();
        });
    }
    
    // Form submission
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const formData = getFormData();
        
        if (!validateForm(formData)) {
            return;
        }
        
        createCharacter(formData);
    });
    
    // Update preview when form changes
    const formInputs = form.querySelectorAll('input, select');
    formInputs.forEach(input => {
        input.addEventListener('change', updatePreview);
        input.addEventListener('input', updatePreview);
    });
    
    // Add race change listener for racial bonuses
    const raceSelect = document.getElementById('race');
    if (raceSelect) {
        raceSelect.addEventListener('change', updateRacialBonuses);
    }
    
    // Add background change listener for skill updates
    const backgroundSelectForSkills = document.getElementById('background');
    if (backgroundSelectForSkills) {
        backgroundSelectForSkills.addEventListener('change', updateSkillSelection);
    }
    
    // Show attribute section when class is selected
    const charClassSelect = document.getElementById('char_class');
    if (charClassSelect) {
        charClassSelect.addEventListener('change', function() {
            const attributesSection = document.querySelector('.attributes-section');
            if (attributesSection) {
                attributesSection.style.display = this.value ? 'block' : 'none';
                if (this.value) {
                    initAttributeControls();
                }
            }
        });
    }
    
    // Show skill section when background is selected
    const backgroundSelect = document.getElementById('background');
    if (backgroundSelect) {
        backgroundSelect.addEventListener('change', function() {
            if (this.value && document.getElementById('char_class').value) {
                document.getElementById('skills-section').style.display = 'block';
                updateSkillSelection();
                
                // Check if class can cast spells
                checkSpellcasting();
            }
        });
    }
    
    // Show spells section when class changes
    const classSelect = document.getElementById('char_class');
    if (classSelect) {
        classSelect.addEventListener('change', function() {
            if (this.value && document.getElementById('background').value) {
                // Show skills section
                document.getElementById('skills-section').style.display = 'block';
                updateSkillSelection();
                
                // Check if class can cast spells
                checkSpellcasting();
            }
        });
    }
    
    // Initialize preview if basic info is already present
    const formData = getFormData();
    if (formData && formData.race && formData.char_class && formData.background) {
        updatePreview();
    }
}

// Function to show suggestions (global scope)
function showSuggestions() {
    const previewSection = document.getElementById('preview-section');
    const applyBtn = document.getElementById('apply-btn');
    
    // Only show suggestions if we have valid data
    if (suggestionsValid && previewSection) {
        previewSection.style.display = 'block';
    }
    if (applyBtn) {
        applyBtn.style.display = 'block';
    }
}

// Function to show playstyle selector in preview
function showPlaystyleSelector(availablePlaystyles, currentPlaystyle) {
    const playstyleSelector = document.querySelector('.playstyle-selector');
    const playstyleSelect = document.getElementById('preview-playstyle-select');
    const changePlaystyleBtn = document.getElementById('change-playstyle-btn');
    
    if (!playstyleSelector || !playstyleSelect) return;
    
    // Clear current options
    playstyleSelect.innerHTML = '<option value="">Random / Standard Array</option>';
    
    // Add playstyle options
    availablePlaystyles.forEach(playstyle => {
        const option = document.createElement('option');
        option.value = playstyle;
        option.textContent = playstyle.charAt(0).toUpperCase() + playstyle.slice(1);
        playstyleSelect.appendChild(option);
    });
    
    // Set current playstyle if available
    if (currentPlaystyle) {
        playstyleSelect.value = currentPlaystyle;
    }
    
    // Show the selector
    playstyleSelector.style.display = 'block';
    
    // Add event listener for change playstyle button
    if (changePlaystyleBtn) {
        // Ensure the button has the correct content
        if (!changePlaystyleBtn.innerHTML.includes('🔄')) {
            changePlaystyleBtn.innerHTML = '<span class="btn-icon">🔄</span>Change Playstyle';
        }
        
        // Store the original content
        const originalContent = changePlaystyleBtn.innerHTML;
        
        // Remove existing event listeners by cloning
        const newBtn = changePlaystyleBtn.cloneNode(true);
        changePlaystyleBtn.parentNode.replaceChild(newBtn, changePlaystyleBtn);
        
        // Restore the original content
        newBtn.innerHTML = originalContent;
        
        // Add new event listener
        newBtn.onclick = function() {
            const selectedPlaystyle = playstyleSelect.value;
            if (selectedPlaystyle) {
                regenerateWithPlaystyle(selectedPlaystyle);
            }
        };
    }
}

// Function to regenerate suggestions with specific playstyle
async function regenerateWithPlaystyle(playstyle) {
    const formData = getFormData();
    if (!formData) return;
    
    try {
        showLoading(document.getElementById('change-playstyle-btn'));
        
        const response = await fetch('/api/autofill', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                ...formData,
                playstyle: playstyle
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            updatePreviewWithData(data);
            suggestionsValid = true;
            showNotification(`Regenerated with ${playstyle} playstyle!`, 'success');
            
            // Update the playstyle selector without re-initializing
            const playstyleSelect = document.getElementById('preview-playstyle-select');
            if (playstyleSelect && data.current_playstyle) {
                playstyleSelect.value = data.current_playstyle;
            }
            
            // Ensure the button has correct content after regeneration
            const changePlaystyleBtn = document.getElementById('change-playstyle-btn');
            if (changePlaystyleBtn && !changePlaystyleBtn.innerHTML.includes('🔄')) {
                changePlaystyleBtn.innerHTML = '<span class="btn-icon">🔄</span>Change Playstyle';
            }
        } else {
            showNotification('Error regenerating suggestions: ' + data.error, 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        showNotification('Error regenerating suggestions: ' + error.message, 'error');
    } finally {
        hideLoading(document.getElementById('change-playstyle-btn'));
    }
}

function getFormData() {
    const formData = {
        name: document.getElementById('name').value,
        race: document.getElementById('race').value,
        char_class: document.getElementById('char_class').value,
        level: parseInt(document.getElementById('level').value) || 1,
        background: document.getElementById('background').value,

        attributes: getAttributes(),
        skills: getSelectedSkills(),
        spells: getSelectedSpells()
    };
    
    console.log('Form data collected:', formData);
    
    // Validate required fields
    if (!formData.name || !formData.race || !formData.char_class || !formData.background) {
        console.error('Missing required fields:', {
            name: !!formData.name,
            race: !!formData.race,
            char_class: !!formData.char_class,
            background: !!formData.background
        });
        return null;
    }
    
    // Validate attributes
    if (!formData.attributes || Object.keys(formData.attributes).length === 0) {
        console.error('No attributes found');
        return null;
    }
    
    // Validate skills
    if (!formData.skills || formData.skills.length === 0) {
        console.error('No skills selected');
        return null;
    }
    
    return formData;
}

function getAttributes() {
    return {
        STR: parseInt(document.getElementById('str').value) || 8,
        DEX: parseInt(document.getElementById('dex').value) || 8,
        CON: parseInt(document.getElementById('con').value) || 8,
        INT: parseInt(document.getElementById('int').value) || 8,
        WIS: parseInt(document.getElementById('wis').value) || 8,
        CHA: parseInt(document.getElementById('cha').value) || 8
    };
}

function getSelectedSkills() {
    const selectedSkills = [];
    const selectedSkillItems = document.querySelectorAll('.skill-item.selected');
    
    console.log('Found selected skill items:', selectedSkillItems.length);
    
    selectedSkillItems.forEach(skillItem => {
        const skillName = skillItem.getAttribute('data-skill');
        if (skillName) {
            selectedSkills.push(skillName);
            console.log('Selected skill:', skillName);
        } else {
            console.warn('Skill item without data-skill attribute:', skillItem);
        }
    });
    
    console.log('Total selected skills:', selectedSkills);
    return selectedSkills;
}

function getClassSkills(charClass) {
    const classSkills = {
        'Fighter': ['Acrobatics', 'Athletics', 'History', 'Insight', 'Intimidation', 'Perception', 'Survival'],
        'Wizard': ['Arcana', 'History', 'Insight', 'Investigation', 'Religion'],
        'Cleric': ['History', 'Insight', 'Medicine', 'Persuasion', 'Religion'],
        'Rogue': ['Acrobatics', 'Athletics', 'Deception', 'Insight', 'Intimidation', 'Investigation', 'Perception', 'Performance', 'Persuasion', 'Sleight of Hand', 'Stealth'],
        'Ranger': ['Animal Handling', 'Athletics', 'Insight', 'Investigation', 'Nature', 'Perception', 'Stealth', 'Survival'],
        'Paladin': ['Athletics', 'Insight', 'Intimidation', 'Medicine', 'Persuasion', 'Religion'],
        'Bard': ['Acrobatics', 'Animal Handling', 'Arcana', 'Athletics', 'Deception', 'History', 'Insight', 'Intimidation', 'Investigation', 'Medicine', 'Nature', 'Perception', 'Performance', 'Persuasion', 'Religion', 'Sleight of Hand', 'Stealth', 'Survival'],
        'Sorcerer': ['Arcana', 'Deception', 'Insight', 'Intimidation', 'Persuasion', 'Religion'],
        'Warlock': ['Arcana', 'Deception', 'History', 'Intimidation', 'Investigation', 'Nature', 'Religion'],
        'Monk': ['Acrobatics', 'Athletics', 'History', 'Insight', 'Religion', 'Stealth'],
        'Druid': ['Animal Handling', 'Arcana', 'Insight', 'Medicine', 'Nature', 'Perception', 'Religion', 'Survival'],
        'Barbarian': ['Animal Handling', 'Athletics', 'Intimidation', 'Nature', 'Perception', 'Survival']
    };
    
    return classSkills[charClass] || [];
}

function getBackgroundSkills() {
    const background = document.getElementById('background').value;
    if (!background) return [];
    
    const backgroundSkills = {
        'Acolyte': ['Insight', 'Religion'],
        'Criminal': ['Deception', 'Stealth'],
        'Folk Hero': ['Animal Handling', 'Survival'],
        'Noble': ['History', 'Persuasion'],
        'Sage': ['Arcana', 'History'],
        'Soldier': ['Athletics', 'Intimidation'],
        'Entertainer': ['Acrobatics', 'Performance'],
        'Guild Artisan': ['Insight', 'Persuasion'],
        'Hermit': ['Medicine', 'Religion'],
        'Outlander': ['Athletics', 'Survival'],
        'Urchin': ['Sleight of Hand', 'Stealth']
    };
    
    return backgroundSkills[background] || [];
}

// Initialize attribute controls
function initAttributeControls() {
    // Initialize all attributes
    const attributes = ['str', 'dex', 'con', 'int', 'wis', 'cha'];
    attributes.forEach(attr => {
        updateAttributeModifier(attr);
        updatePointCost(attr);
    });
    updatePointBuy();
    updateButtons();
    updateRacialBonuses();
}

function changeAttribute(attr, change) {
    const input = document.getElementById(attr);
    const currentValue = parseInt(input.value);
    const newValue = currentValue + change;
    
    // Check if base value would exceed 15 (point buy limit)
    if (newValue >= 8 && newValue <= 15) {
        input.value = newValue;
        updateAttributeModifier(attr);
        updatePointCost(attr);
        updatePointBuy();
        updateButtons();
        updateTotalScore(attr);
    } else if (newValue < 8) {
        showNotification(`Cannot decrease ${attr.toUpperCase()}: minimum base score is 8`, 'error');
    } else if (newValue > 15) {
        showNotification(`Cannot increase ${attr.toUpperCase()}: maximum base score is 15`, 'error');
    }
}

function updateAttributeModifier(attr) {
    const input = document.getElementById(attr);
    const value = parseInt(input.value);
    const modifier = Math.floor((value - 10) / 2);
    const modifierElement = document.getElementById(`modifier-${attr}`);
    
    if (modifierElement) {
        modifierElement.textContent = modifier >= 0 ? `+${modifier}` : `${modifier}`;
    }
}

function updatePointCost(attr) {
    const input = document.getElementById(attr);
    const value = parseInt(input.value);
    const pointCosts = {8: 0, 9: 1, 10: 2, 11: 3, 12: 4, 13: 5, 14: 7, 15: 9};
    const cost = pointCosts[value] || 0;
    
    const costElement = document.getElementById(`cost-${attr}`);
    if (costElement) {
        costElement.textContent = cost;
    }
}

function updateTotalScore(attr) {
    const input = document.getElementById(attr);
    const baseValue = parseInt(input.value);
    const racialBonus = getRacialBonus(attr);
    const totalValue = baseValue + racialBonus;
    
    const totalElement = document.getElementById(`total-${attr}`);
    if (totalElement) {
        totalElement.textContent = totalValue;
    }
    
    // Update modifier based on total score
    const modifier = Math.floor((totalValue - 10) / 2);
    const modifierElement = document.getElementById(`modifier-${attr}`);
    if (modifierElement) {
        modifierElement.textContent = modifier >= 0 ? `+${modifier}` : `${modifier}`;
    }
}

function getRacialBonus(attr) {
    const race = document.getElementById('race').value;
    if (!race) return 0;
    
    const racialBonuses = {
        'Human': {str: 1, dex: 1, con: 1, int: 1, wis: 1, cha: 1},
        'Elf': {dex: 2},
        'Dwarf': {con: 2},
        'Halfling': {dex: 2},
        'Dragonborn': {str: 2, cha: 1},
        'Tiefling': {int: 1, cha: 2},
        'Half-Elf': {cha: 2, str: 1, dex: 1},
        'Half-Orc': {str: 2, con: 1},
        'Gnome': {int: 2}
    };
    
    return racialBonuses[race]?.[attr] || 0;
}

function updateRacialBonuses() {
    const attributes = ['str', 'dex', 'con', 'int', 'wis', 'cha'];
    attributes.forEach(attr => {
        const bonus = getRacialBonus(attr);
        const bonusElement = document.getElementById(`racial-${attr}`);
        if (bonusElement) {
            bonusElement.textContent = bonus > 0 ? `+${bonus}` : '+0';
        }
        updateTotalScore(attr);
    });
}

// Update point buy system
function updatePointBuy() {
    const attributes = ['str', 'dex', 'con', 'int', 'wis', 'cha'];
    const pointCosts = {8: 0, 9: 1, 10: 2, 11: 3, 12: 4, 13: 5, 14: 7, 15: 9};
    
    let totalCost = 0;
    attributes.forEach(attr => {
        const input = document.getElementById(attr);
        const value = parseInt(input.value);
        totalCost += pointCosts[value] || 0;
    });
    
    const remainingPoints = 27 - totalCost;
    const remainingElement = document.getElementById('remaining-points');
    if (remainingElement) {
        remainingElement.textContent = remainingPoints;
    }
    
    return remainingPoints;
}

// Update button states
function updateButtons() {
    const attributes = ['str', 'dex', 'con', 'int', 'wis', 'cha'];
    const remainingPoints = updatePointBuy();
    
    attributes.forEach(attr => {
        const input = document.getElementById(attr);
        const value = parseInt(input.value);
        const pointCosts = {8: 0, 9: 1, 10: 2, 11: 3, 12: 4, 13: 5, 14: 7, 15: 9};
        
        // Find buttons for this attribute
        const buttons = input.parentElement.querySelectorAll('.attr-btn');
        const decreaseBtn = buttons[0];
        const increaseBtn = buttons[1];
        
        // Disable decrease button if at minimum
        if (decreaseBtn) {
            decreaseBtn.disabled = value <= 8;
        }
        
        // Disable increase button if at maximum or not enough points
        if (increaseBtn) {
            const nextValue = value + 1;
            const additionalCost = pointCosts[nextValue] - pointCosts[value];
            increaseBtn.disabled = value >= 15 || remainingPoints < additionalCost;
        }
    });
}

// Initialize skill selection
function initSkillSelection() {
    updateSkillSelection();
}

// Update skill selection based on class and background
function updateSkillSelection() {
    const charClass = document.getElementById('char_class').value;
    const background = document.getElementById('background').value;
    
    if (!charClass || !background) {
        document.getElementById('skills-section').style.display = 'none';
        return;
    }
    
    document.getElementById('skills-section').style.display = 'block';
    
    const skillsContainer = document.getElementById('skills-container');
    skillsContainer.innerHTML = '';
    
    // Get class skills
    const classSkills = getClassSkills(charClass);
    
    // Get background skills
    const backgroundSkills = getBackgroundSkills();
    
    // Create a set of all available skills (class + background)
    const allAvailableSkills = new Set([...classSkills, ...backgroundSkills]);
    
    // Create skill items for ALL available skills
    allAvailableSkills.forEach(skill => {
        const isBackgroundSkill = backgroundSkills.includes(skill);
        const isClassSkill = classSkills.includes(skill);
        const skillType = isBackgroundSkill ? 'background' : 'class';
        const skillItem = createSkillItem(skill, skillType, isBackgroundSkill);
        skillsContainer.appendChild(skillItem);
    });
    
    // Update remaining skills count
    const classChoices = {
        'Fighter': 2, 'Wizard': 2, 'Cleric': 2, 'Rogue': 4,
        'Ranger': 3, 'Paladin': 2, 'Bard': 3, 'Sorcerer': 2,
        'Warlock': 2, 'Monk': 2, 'Druid': 2, 'Barbarian': 2
    };
    
    const totalChoices = classChoices[charClass] || 0;
    const backgroundSkillCount = backgroundSkills.length;
    const remainingChoices = Math.max(0, totalChoices);
    
    document.getElementById('remaining-skills').textContent = remainingChoices;
    
    // Update skill selection logic
    updateSkillSelectionLogic(remainingChoices);
}

// Create skill item element
function createSkillItem(skillName, type, selected = false) {
    const skillItem = document.createElement('div');
    skillItem.className = 'skill-item';
    skillItem.setAttribute('data-skill', skillName);
    skillItem.setAttribute('data-type', type);
    
    if (selected) {
        skillItem.classList.add('selected');
    }
    
    if (type === 'background') {
        skillItem.classList.add('disabled');
        skillItem.classList.add('selected'); // Background skills are always selected
    }
    
    skillItem.innerHTML = `
        <div class="skill-indicator ${selected || type === 'background' ? 'selected' : ''}"></div>
        <span class="skill-name">${skillName}</span>
        ${type === 'background' ? '<span class="skill-type">(Background)</span>' : ''}
    `;
    
    if (type !== 'background') {
        skillItem.addEventListener('click', () => toggleSkillSelection(skillItem));
    }
    
    return skillItem;
}

// Toggle skill selection
function toggleSkillSelection(skillItem) {
    // Don't allow interaction with background skills
    if (skillItem.classList.contains('disabled')) {
        return;
    }
    
    const isSelected = skillItem.classList.contains('selected');
    const indicator = skillItem.querySelector('.skill-indicator');
    const remainingSkills = parseInt(document.getElementById('remaining-skills').textContent);
    
    if (isSelected) {
        // Deselect skill
        skillItem.classList.remove('selected');
        indicator.classList.remove('selected');
        document.getElementById('remaining-skills').textContent = remainingSkills + 1;
    } else if (remainingSkills > 0) {
        // Select skill
        skillItem.classList.add('selected');
        indicator.classList.add('selected');
        document.getElementById('remaining-skills').textContent = remainingSkills - 1;
    }
    
    updateSkillSelectionLogic(remainingSkills + (isSelected ? 1 : -1));
}

// Update skill selection logic
function updateSkillSelectionLogic(remainingChoices) {
    const skillItems = document.querySelectorAll('.skill-item:not(.selected)');
    
    skillItems.forEach(item => {
        if (remainingChoices <= 0) {
            item.classList.add('disabled');
        } else {
            item.classList.remove('disabled');
        }
    });
}

// Validation functions
function validateForm(formData) {
    if (!formData.name || !formData.race || !formData.char_class || !formData.background) {
        showNotification('Please complete all required fields.', 'error');
        return false;
    }
    
    // Validate attributes
    if (!validateAttributes()) {
        showNotification('Please fix attribute point allocation.', 'error');
        return false;
    }
    
    // Validate skills
    if (!validateSkills()) {
        showNotification('Please select the correct number of skills.', 'error');
        return false;
    }
    
    // Validate spells
    if (!validateSpells()) {
        showNotification('Please fix spell selection.', 'error');
        return false;
    }
    
    return true;
}

function validateAttributes() {
    const remainingPoints = parseInt(document.getElementById('remaining-points').textContent);
    return remainingPoints === 0;
}

function validateSkills() {
    const remainingSkills = parseInt(document.getElementById('remaining-skills').textContent);
    return remainingSkills === 0;
}

function validateSpells() {
    const charClass = document.getElementById('char_class').value;
    if (!charClass) return true; // No class selected, skip validation
    
    const selectedSpells = getSelectedSpells();
    const cantripLimit = parseInt(document.getElementById('cantrips-limit').textContent) || 0;
    const spellLimit = parseInt(document.getElementById('spells-limit').textContent) || 0;
    
    // If class can't cast spells, validation passes
    if (cantripLimit === 0 && spellLimit === 0) return true;
    
    // Validate cantrips
    if (selectedSpells.cantrips.length > cantripLimit) {
        return false;
    }
    
    // Validate spells
    if (selectedSpells.spells.length > spellLimit) {
        return false;
    }
    
    return true;
}

function autofillCharacter(formData) {
    console.log('Starting autofill with data:', formData);
    
    fetch('/api/autofill', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
    })
    .then(response => {
        console.log('Response status:', response.status);
        return response.json();
    })
    .then(data => {
        console.log('Autofill response:', data);
        if (data.success) {
            updatePreviewWithData(data);
            
            // Mark suggestions as valid
            suggestionsValid = true;
            
            // Show suggestions and preview
            showSuggestions();
            showPreview();
            
            // Show apply button after autofill
            const applyBtn = document.getElementById('apply-btn');
            if (applyBtn) {
                applyBtn.style.display = 'inline-block';
            }
            
                // Show playstyle selector if playstyles are available
    if (data.available_playstyles && data.available_playstyles.length > 0) {
        showPlaystyleSelector(data.available_playstyles, data.current_playstyle);
    } else {
        // Hide playstyle selector if no playstyles available
        const playstyleSelector = document.querySelector('.playstyle-selector');
        if (playstyleSelector) {
            playstyleSelector.style.display = 'none';
        }
    }
        } else {
            const errorMessage = data.error || 'Unknown error occurred';
            showNotification('Error generating suggestions: ' + errorMessage, 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('Error generating suggestions: ' + error.message, 'error');
    });
}

function applyAutofillSuggestions() {
    const formData = getFormData();
    if (!formData.name || !formData.race || !formData.char_class || !formData.background) {
        showNotification('Please complete name, race, class and background before applying suggestions.', 'error');
        return;
    }
    
    // Clear any previous application state to prevent inconsistencies
    console.log('=== CLEARING PREVIOUS STATE ===');
    const previousSelectedSkills = document.querySelectorAll('.skill-item.selected');
    console.log(`Clearing ${previousSelectedSkills.length} previously selected skills`);
    
    // Get the current preview data instead of making a new API call
    const previewSection = document.getElementById('preview-section');
    if (!previewSection || previewSection.style.display === 'none') {
        showNotification('No suggestions available. Please generate suggestions first.', 'error');
        return;
    }
    
    // Check if there are attributes in the preview
    const previewAttributeElements = document.querySelectorAll('#preview-attributes .attribute-card');
    if (previewAttributeElements.length === 0) {
        showNotification('No attribute suggestions found. Please regenerate suggestions.', 'error');
        return;
    }
    
    // Store current playstyle for debugging
    const currentPlaystyle = document.getElementById('preview-playstyle')?.textContent || 'Unknown';
    console.log(`Applying suggestions for playstyle: ${currentPlaystyle}`);
    
    // Extract attributes from the preview (now showing base values)
    const previewAttributes = {};
    const attributeElements = document.querySelectorAll('#preview-attributes .attribute-card');
    attributeElements.forEach(element => {
        const attrName = element.querySelector('.attribute-name').textContent;
        const attrValue = parseInt(element.querySelector('.attribute-value').textContent);
        if (attrName && !isNaN(attrValue)) {
            // Convert attribute name to uppercase for consistency
            const attrKey = attrName.toUpperCase();
            // The preview now shows base values directly
            previewAttributes[attrKey] = attrValue;
        }
    });
    
    // Extract skills from the preview
    const previewSkills = [];
    const skillElements = document.querySelectorAll('#preview-skills .skill-item');
    skillElements.forEach(element => {
        const skillName = element.textContent.trim();
        if (skillName) {
            previewSkills.push(skillName);
        }
    });
    
    console.log('Applying preview data:', { attributes: previewAttributes, skills: previewSkills });
    
    // Apply suggested attributes exactly as shown in preview
    if (Object.keys(previewAttributes).length > 0) {
        Object.keys(previewAttributes).forEach(attr => {
            const input = document.getElementById(attr.toLowerCase());
            if (input) {
                // Apply the base value directly from preview
                const baseValue = previewAttributes[attr];
                input.value = baseValue;
                updateAttributeModifier(attr.toLowerCase());
                updatePointCost(attr.toLowerCase());
                updateTotalScore(attr.toLowerCase());
            }
        });
        updatePointBuy();
        updateButtons();
        updateRacialBonuses();
    }
    
            // Apply suggested skills exactly as shown in the preview
        if (previewSkills.length > 0) {
            console.log('=== SKILL APPLICATION DEBUG ===');
            console.log('Preview skills received:', previewSkills);
            
            // First, deselect ALL skills (including background skills)
            const allSkillItems = document.querySelectorAll('.skill-item');
            console.log(`Found ${allSkillItems.length} total skill items`);
            
            allSkillItems.forEach(item => {
                item.classList.remove('selected');
                const indicator = item.querySelector('.skill-indicator');
                if (indicator) {
                    indicator.classList.remove('selected');
                }
            });
            
            // Reset remaining skills count to initial value
            const charClass = document.getElementById('char_class').value;
            const classChoices = {
                'Fighter': 2, 'Wizard': 2, 'Cleric': 2, 'Rogue': 4,
                'Ranger': 3, 'Paladin': 2, 'Bard': 3, 'Sorcerer': 2,
                'Warlock': 2, 'Monk': 2, 'Druid': 2, 'Barbarian': 2
            };
            const totalChoices = classChoices[charClass] || 0;
            const remainingSkillsElement = document.getElementById('remaining-skills');
            if (remainingSkillsElement) {
                remainingSkillsElement.textContent = totalChoices;
            }
            
            console.log(`Class: ${charClass}, Total choices: ${totalChoices}`);
            
            // Get background skills that should always be selected
            const backgroundSkills = getBackgroundSkills();
            
            // Apply suggested spells if available
            const previewSpells = [];
            const spellElements = document.querySelectorAll('#preview-spells .spell-item');
            spellElements.forEach(element => {
                const spellName = element.textContent.trim();
                if (spellName) {
                    previewSpells.push(spellName);
                }
            });
            
            // Apply suggested spells
            if (previewSpells.length > 0) {
                console.log('=== SPELL APPLICATION DEBUG ===');
                console.log('Preview spells received:', previewSpells);
                
                // First, deselect ALL spells
                const allSpellItems = document.querySelectorAll('.spell-item');
                console.log(`Found ${allSpellItems.length} total spell items`);
                
                allSpellItems.forEach(item => {
                    item.classList.remove('selected');
                    const indicator = item.querySelector('.spell-indicator');
                    if (indicator) {
                        indicator.classList.remove('selected');
                    }
                });
                
                // Select suggested spells
                let spellsSelected = 0;
                previewSpells.forEach(spellName => {
                    // Try multiple selectors to find the spell
                    let spellItem = document.querySelector(`.spell-item[data-spell="${spellName}"]`);
                    if (!spellItem) {
                        // Try case-insensitive search
                        spellItem = document.querySelector(`.spell-item[data-spell*="${spellName.toLowerCase()}" i]`);
                    }
                    if (!spellItem) {
                        // Try finding by text content
                        const allSpellItems = document.querySelectorAll('.spell-item');
                        spellItem = Array.from(allSpellItems).find(item => 
                            item.textContent.trim().toLowerCase() === spellName.toLowerCase()
                        );
                    }
                    if (!spellItem) {
                        // Try partial match
                        const allSpellItems = document.querySelectorAll('.spell-item');
                        spellItem = Array.from(allSpellItems).find(item => 
                            item.textContent.trim().toLowerCase().includes(spellName.toLowerCase()) ||
                            spellName.toLowerCase().includes(item.textContent.trim().toLowerCase())
                        );
                    }
                    
                    if (spellItem) {
                        spellItem.classList.add('selected');
                        const indicator = spellItem.querySelector('.spell-indicator');
                        if (indicator) {
                            indicator.classList.add('selected');
                        }
                        spellsSelected++;
                        console.log(`Selected spell: ${spellName}`);
                    } else {
                        console.warn(`Spell not found: ${spellName}`);
                        // Try to find similar spells
                        const allSpells = Array.from(document.querySelectorAll('.spell-item')).map(item => item.textContent.trim());
                        console.log('Available spells:', allSpells);
                    }
                });
                
                console.log(`Successfully selected ${spellsSelected} out of ${previewSpells.length} suggested spells`);
                updateSpellCounts();
            }
        
        // First, select background skills (these are guaranteed)
        backgroundSkills.forEach(skillName => {
            const skillItem = document.querySelector(`[data-skill="${skillName}"]`);
            if (skillItem) {
                skillItem.classList.add('selected');
                skillItem.classList.add('disabled');
                const indicator = skillItem.querySelector('.skill-indicator');
                if (indicator) {
                    indicator.classList.add('selected');
                }
                console.log(`Selected background skill: ${skillName} (disabled)`);
            } else {
                console.warn(`Background skill not found: ${skillName}`);
            }
        });
        
        // Now select ONLY the suggested class skills (excluding background skills)
        let skillsSelected = 0;
        let remainingSkills = totalChoices;
        
        console.log('Suggested skills:', previewSkills);
        console.log(`Background skills: ${backgroundSkills}`);
        console.log(`Initial remaining skills: ${remainingSkills}`);
        
        // Create a list of skills to select (excluding background skills)
        const skillsToSelect = previewSkills.filter(skill => !backgroundSkills.includes(skill));
        console.log('Skills to select (excluding background):', skillsToSelect);
        console.log('Background skills that will be auto-selected:', backgroundSkills);
        
        // More robust skill selection
        for (let index = 0; index < skillsToSelect.length && remainingSkills > 0; index++) {
            const skillName = skillsToSelect[index];
            
            // Try multiple selectors to find the skill
            let skillItem = document.querySelector(`[data-skill="${skillName}"]`);
            if (!skillItem) {
                // Try case-insensitive search
                skillItem = document.querySelector(`[data-skill*="${skillName.toLowerCase()}" i]`);
            }
            if (!skillItem) {
                // Try finding by text content
                const allSkillItems = document.querySelectorAll('.skill-item');
                skillItem = Array.from(allSkillItems).find(item => 
                    item.textContent.trim().toLowerCase() === skillName.toLowerCase()
                );
            }
            if (!skillItem) {
                // Try partial match
                const allSkillItems = document.querySelectorAll('.skill-item');
                skillItem = Array.from(allSkillItems).find(item => 
                    item.textContent.trim().toLowerCase().includes(skillName.toLowerCase()) ||
                    skillName.toLowerCase().includes(item.textContent.trim().toLowerCase())
                );
            }
            
            if (skillItem && remainingSkills > 0) {
                // Select the class skill
                skillItem.classList.add('selected');
                skillItem.classList.remove('disabled');
                const indicator = skillItem.querySelector('.skill-indicator');
                if (indicator) {
                    indicator.classList.add('selected');
                }
                skillsSelected++;
                remainingSkills--;
                console.log(`Selected class skill: ${skillName}, remaining: ${remainingSkills}`);
                
                // Update remaining skills count
                if (remainingSkillsElement) {
                    remainingSkillsElement.textContent = remainingSkills;
                }
            } else if (skillItem) {
                console.log(`No skill points remaining, cannot select ${skillName}`);
            } else {
                console.warn(`Skill not found: ${skillName}`);
                // Try to find similar skills
                const allSkills = Array.from(document.querySelectorAll('.skill-item')).map(item => item.textContent.trim());
                console.log('Available skills:', allSkills);
            }
        }
        
        console.log(`Total selected: ${skillsSelected} class skills`);
        console.log(`Final remaining skills: ${remainingSkills}`);
        
        // If we still have remaining skills, try to fill them with available class skills
        if (remainingSkills > 0) {
            console.log(`Attempting to fill remaining ${remainingSkills} skills with available class skills`);
            const availableClassSkills = getClassSkills(charClass);
            const unselectedSkills = availableClassSkills.filter(skill => {
                const skillItem = document.querySelector(`[data-skill="${skill}"]`);
                return skillItem && !skillItem.classList.contains('selected');
            });
            
            for (let i = 0; i < Math.min(remainingSkills, unselectedSkills.length); i++) {
                const skillName = unselectedSkills[i];
                const skillItem = document.querySelector(`[data-skill="${skillName}"]`);
                if (skillItem) {
                    skillItem.classList.add('selected');
                    skillItem.classList.remove('disabled');
                    const indicator = skillItem.querySelector('.skill-indicator');
                    if (indicator) {
                        indicator.classList.add('selected');
                    }
                    remainingSkills--;
                    console.log(`Auto-filled remaining skill: ${skillName}`);
                }
            }
            
            // Update remaining skills count
            if (remainingSkillsElement) {
                remainingSkillsElement.textContent = remainingSkills;
            }
        }
        
        // Update skill selection logic
        updateSkillSelectionLogic(remainingSkills);
        
        // Final validation - check if all skills were applied correctly
        const finalSelectedSkills = document.querySelectorAll('.skill-item.selected');
        const expectedTotalSkills = backgroundSkills.length + skillsToSelect.length;
        
        console.log('=== FINAL VALIDATION ===');
        console.log(`Expected total skills: ${expectedTotalSkills} (${backgroundSkills.length} background + ${skillsToSelect.length} class)`);
        console.log(`Actually selected: ${finalSelectedSkills.length}`);
        
        if (finalSelectedSkills.length !== expectedTotalSkills) {
            console.warn('⚠️ SKILL COUNT MISMATCH DETECTED!');
            console.warn('Selected skills:', Array.from(finalSelectedSkills).map(item => item.getAttribute('data-skill')));
            console.warn('Expected skills:', [...backgroundSkills, ...skillsToSelect]);
        }
    }
    
    showNotification('Suggestions applied successfully!', 'success');
}

function updatePreviewWithData(data) {
    const formData = getFormData();
    
    // Actualizar información básica
    document.getElementById('preview-name').textContent = formData.name || 'Nombre del Personaje';
    document.getElementById('preview-level').textContent = `Nivel ${formData.level}`;
    document.getElementById('preview-race-class').textContent = 
        `${formData.race || 'Raza'} • ${formData.char_class || 'Clase'}`;
    document.getElementById('preview-background').textContent = formData.background || 'Sin trasfondo';
    
    // Mostrar información del playstyle si está disponible
    const playstyleInfo = document.getElementById('preview-playstyle');
    if (playstyleInfo) {
        if (data.current_playstyle) {
            playstyleInfo.textContent = `Playstyle: ${data.current_playstyle.charAt(0).toUpperCase() + data.current_playstyle.slice(1)}`;
            playstyleInfo.style.display = 'block';
        } else {
            playstyleInfo.textContent = 'Playstyle: Random / Standard Array';
            playstyleInfo.style.display = 'block';
        }
    }
    
    // Actualizar atributos en orden estándar
    const attributesGrid = document.getElementById('preview-attributes');
    attributesGrid.innerHTML = '';
    
    if (data.attributes) {
        // Definir el orden estándar de atributos
        const attributeOrder = ['STR', 'DEX', 'CON', 'INT', 'WIS', 'CHA'];
        
        attributeOrder.forEach(attr => {
            if (data.attributes[attr] !== undefined) {
                const baseValue = data.attributes[attr];
                const racialBonus = getRacialBonus(attr.toLowerCase());
                const totalValue = baseValue + racialBonus;
                const modifier = Math.floor((totalValue - 10) / 2);
                const modifierText = modifier >= 0 ? `+${modifier}` : `${modifier}`;
                
                // Show base value in preview (not total) to be consistent with point buy system
                attributesGrid.innerHTML += `
                    <div class="attribute-card">
                        <div class="attribute-name">${attr}</div>
                        <div class="attribute-value">${baseValue}</div>
                        <div class="attribute-modifier">${modifierText}</div>
                        ${racialBonus > 0 ? `<div class="attribute-racial">+${racialBonus}</div>` : ''}
                    </div>
                `;
            }
        });
    }
    
    // Actualizar habilidades
    const skillsList = document.getElementById('preview-skills');
    skillsList.innerHTML = '';
    
    if (data.skills && data.skills.length > 0) {
        data.skills.forEach(skill => {
            skillsList.innerHTML += `<span class="skill-item">${skill}</span>`;
        });
    }
    
    // Actualizar hechizos
    const spellsSection = document.getElementById('preview-spells-section');
    const spellsList = document.getElementById('preview-spells');
    spellsList.innerHTML = '';
    
    if (data.spells && data.spells.length > 0) {
        data.spells.forEach(spell => {
            spellsList.innerHTML += `<span class="spell-item">${spell}</span>`;
        });
        spellsSection.style.display = 'block';
    } else {
        spellsSection.style.display = 'none';
    }
}

function updatePreview() {
    const formData = getFormData();
    
    document.getElementById('preview-name').textContent = formData.name || 'Nombre del Personaje';
    document.getElementById('preview-level').textContent = `Nivel ${formData.level}`;
    document.getElementById('preview-race-class').textContent = 
        `${formData.race || 'Raza'} • ${formData.char_class || 'Clase'}`;
    document.getElementById('preview-background').textContent = formData.background || 'Sin trasfondo';
    
    // Show preview if we have basic info (except name)
    if (formData.race && formData.char_class && formData.background) {
        showPreview();
    }
}

function showPreview() {
    const previewSection = document.getElementById('preview-section');
    previewSection.style.display = 'block';
    previewSection.scrollIntoView({ behavior: 'smooth' });
}

function createCharacter(formData) {
    console.log('Creating character with data:', formData);
    
    // Validate form data before sending
    if (!validateForm(formData)) {
        console.error('Form validation failed');
        return;
    }
    
    fetch('/create', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
    })
    .then(response => {
        console.log('Response status:', response.status);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        console.log('Server response:', data);
        if (data.success) {
            showNotification('¡Personaje creado exitosamente!', 'success');
            window.location.href = `/character/${data.character_id}`;
        } else {
            const errorMessage = data.error || 'Error desconocido al crear el personaje';
            console.error('Server error:', errorMessage);
            showNotification('Error al crear el personaje: ' + errorMessage, 'error');
        }
    })
    .catch(error => {
        console.error('Network or parsing error:', error);
        showNotification('Error de conexión al crear el personaje: ' + error.message, 'error');
    });
}

// Funcionalidad del chat
function initChat() {
    const chatForm = document.getElementById('chat-form');
    const messageInput = document.getElementById('message-input');
    const chatMessages = document.getElementById('chat-messages');
    
    chatForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const message = messageInput.value.trim();
        if (!message) return;
        
        // Agregar mensaje del usuario
        addMessage('Tú', message, 'user');
        messageInput.value = '';
        
        // Enviar mensaje al servidor
        sendMessage(message);
    });
    
    // Auto-scroll al último mensaje
    function scrollToBottom() {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    // Observar cambios en los mensajes para auto-scroll
    const observer = new MutationObserver(scrollToBottom);
    observer.observe(chatMessages, { childList: true });
}

function addMessage(sender, text, type = 'character') {
    const chatMessages = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}-message`;
    
    const avatar = type === 'user' ? '👤' : '👤';
    const avatarClass = type === 'user' ? 'user-avatar' : 'character-avatar';
    
    messageDiv.innerHTML = `
        <div class="message-avatar ${avatarClass}">${avatar}</div>
        <div class="message-content">
            <div class="message-sender">${sender}</div>
            <div class="message-text">${text}</div>
        </div>
    `;
    
    chatMessages.appendChild(messageDiv);
}

function sendMessage(message) {
    const characterId = window.location.pathname.split('/')[2];
    
    fetch(`/character/${characterId}/chat`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: message })
    })
    .then(response => response.json())
    .then(data => {
        // Agregar respuesta del personaje
        const characterName = document.querySelector('.character-info h2').textContent.replace('💬 Conversando con ', '');
        addMessage(characterName, data.response, 'character');
    })
    .catch(error => {
        console.error('Error:', error);
        addMessage('Sistema', 'Lo siento, hubo un error al procesar tu mensaje.', 'character');
    });
}

// Funcionalidad de preguntas sugeridas
function initSuggestedQuestions() {
    const questionButtons = document.querySelectorAll('.question-btn');
    
    questionButtons.forEach(button => {
        button.addEventListener('click', function() {
            const question = this.getAttribute('data-question');
            const messageInput = document.getElementById('message-input');
            
            if (messageInput) {
                messageInput.value = question;
                messageInput.focus();
            }
        });
    });
}

// Funcionalidad de eliminación de personajes
function initCharacterDeletion() {
    const deleteButtons = document.querySelectorAll('.delete-character-btn');
    
    deleteButtons.forEach(button => {
        button.addEventListener('click', function() {
            const characterId = this.getAttribute('data-character-id');
            const characterName = this.getAttribute('data-character-name');
            confirmDeleteCharacter(characterId, characterName);
        });
    });
}

function confirmDeleteCharacter(characterId, characterName) {
    const message = `Are you sure you want to delete the character "${characterName}"?\n\nThis action cannot be undone.`;
    
    if (confirm(message)) {
        deleteCharacter(characterId, characterName);
    }
}

function deleteCharacter(characterId, characterName) {
    fetch(`/character/${characterId}/delete`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showNotification(data.message, 'success');
            // Redirigir a la página principal después de un breve delay
            setTimeout(() => {
                window.location.href = '/';
            }, 1500);
        } else {
            showNotification(data.error || 'Error deleting character', 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('Error deleting character', 'error');
    });
}

// Funcionalidades adicionales
function showLoading(element) {
    // Store original content before showing loading
    element.setAttribute('data-original-content', element.innerHTML);
    element.innerHTML = '<div class="loading">Cargando...</div>';
}

function hideLoading(element) {
    const loading = element.querySelector('.loading');
    if (loading) {
        loading.remove();
    }
    
    // Restore original content
    const originalContent = element.getAttribute('data-original-content');
    if (originalContent) {
        element.innerHTML = originalContent;
        element.removeAttribute('data-original-content');
    }
}

// Utilidades
function formatModifier(value) {
    const modifier = Math.floor((value - 10) / 2);
    return modifier >= 0 ? `+${modifier}` : `${modifier}`;
}

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Animaciones suaves
function smoothScrollTo(element) {
    element.scrollIntoView({ 
        behavior: 'smooth', 
        block: 'start' 
    });
}

// Notificaciones
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.classList.add('show');
    }, 100);
    
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, 3000);
}

// Estilos para notificaciones
const notificationStyles = `
    .notification {
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        color: white;
        font-weight: 600;
        z-index: 1000;
        transform: translateX(100%);
        transition: transform 0.3s ease;
    }
    
    .notification.show {
        transform: translateX(0);
    }
    
    .notification-info {
        background: linear-gradient(135deg, #3498db, #2980b9);
    }
    
    .notification-success {
        background: linear-gradient(135deg, #27ae60, #229954);
    }
    
    .notification-error {
        background: linear-gradient(135deg, #e74c3c, #c0392b);
    }
`;

// Spell selection functionality
function initSpellSelection() {
    // This will be called when the page loads
    // Spell selection will be initialized when class and background are selected
}

function checkSpellcasting() {
    const charClass = document.getElementById('char_class').value;
    const background = document.getElementById('background').value;
    
    if (!charClass || !background) return;
    
    fetch(`/api/spells/${charClass}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const rules = data.rules;
                const cantripLimit = rules.cantrips_known || 0;
                const spellLimit = rules.spells_known || 0;
                
                if (cantripLimit > 0 || spellLimit > 0) {
                    document.getElementById('spells-section').style.display = 'block';
                    document.getElementById('spellcasting-ability').textContent = rules.spellcasting_ability || 'None';
                    document.getElementById('cantrips-limit').textContent = cantripLimit;
                    document.getElementById('spells-limit').textContent = spellLimit;
                    
                    updateSpellSelection(data);
                } else {
                    document.getElementById('spells-section').style.display = 'none';
                }
            }
        })
        .catch(error => {
            console.error('Error loading spells:', error);
        });
}

function updateSpellSelection(spellData) {
    // Update cantrips
    const cantripsContainer = document.getElementById('cantrips-container');
    cantripsContainer.innerHTML = '';
    
    spellData.cantrips.forEach(cantrip => {
        const cantripItem = createSpellItem(cantrip, 'cantrip');
        cantripsContainer.appendChild(cantripItem);
    });
    
    // Update spells
    const spellsContainer = document.getElementById('spells-container');
    spellsContainer.innerHTML = '';
    
    spellData.spells.forEach(spell => {
        const spellItem = createSpellItem(spell, 'spell');
        spellsContainer.appendChild(spellItem);
    });
    
    updateSpellCounts();
}

function createSpellItem(spell, type) {
    const spellItem = document.createElement('div');
    spellItem.className = 'spell-item';
    spellItem.setAttribute('data-spell', spell.name);
    spellItem.setAttribute('data-type', type);
    
    // Create source badge if available
    const sourceBadge = spell.source ? `<span class="spell-source ${spell.source.toLowerCase()}">${spell.source}</span>` : '';
    
    spellItem.innerHTML = `
        <div class="spell-indicator"></div>
        <div class="spell-info">
            <span class="spell-name">${spell.name}</span>
            <span class="spell-school">(${spell.school})</span>
        </div>
        <div class="spell-details">
            <span class="spell-casting-time">${spell.casting_time}</span>
            <span class="spell-range">Range: ${spell.range}</span>
        </div>
        <button class="spell-info-btn" title="View spell details">📖</button>
        ${sourceBadge}
    `;
    
    spellItem.addEventListener('click', (e) => {
        if (!e.target.classList.contains('spell-info-btn')) {
            toggleSpellSelection(spellItem);
        }
    });
    
    // Add spell info functionality
    const infoBtn = spellItem.querySelector('.spell-info-btn');
    infoBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        showSpellInfo(spell);
    });
    
    return spellItem;
}

function toggleSpellSelection(spellItem) {
    const isSelected = spellItem.classList.contains('selected');
    const indicator = spellItem.querySelector('.spell-indicator');
    const type = spellItem.getAttribute('data-type');
    
    if (isSelected) {
        // Deselect spell
        spellItem.classList.remove('selected');
        indicator.classList.remove('selected');
    } else {
        // Check if we can select more spells of this type
        const currentCount = document.querySelectorAll(`.spell-item.selected[data-type="${type}"]`).length;
        const limit = type === 'cantrip' ? 
            parseInt(document.getElementById('cantrips-limit').textContent) :
            parseInt(document.getElementById('spells-limit').textContent);
        
        if (currentCount < limit) {
            // Select spell
            spellItem.classList.add('selected');
            indicator.classList.add('selected');
        } else {
            showNotification(`Cannot select more ${type}s. Limit is ${limit}.`, 'error');
            return;
        }
    }
    
    updateSpellCounts();
}

function updateSpellCounts() {
    const selectedCantrips = document.querySelectorAll('.spell-item.selected[data-type="cantrip"]').length;
    const selectedSpells = document.querySelectorAll('.spell-item.selected[data-type="spell"]').length;
    
    document.getElementById('cantrips-known').textContent = selectedCantrips;
    document.getElementById('spells-known').textContent = selectedSpells;
}

function getSelectedSpells() {
    const selectedCantrips = [];
    const selectedSpells = [];
    
    const cantripItems = document.querySelectorAll('.spell-item.selected[data-type="cantrip"]');
    const spellItems = document.querySelectorAll('.spell-item.selected[data-type="spell"]');
    
    console.log('Found selected cantrips:', cantripItems.length);
    console.log('Found selected spells:', spellItems.length);
    
    cantripItems.forEach(item => {
        const spellName = item.getAttribute('data-spell');
        if (spellName) {
            selectedCantrips.push(spellName);
            console.log('Selected cantrip:', spellName);
        }
    });
    
    spellItems.forEach(item => {
        const spellName = item.getAttribute('data-spell');
        if (spellName) {
            selectedSpells.push(spellName);
            console.log('Selected spell:', spellName);
        }
    });
    
    const result = {
        cantrips: selectedCantrips,
        spells: selectedSpells
    };
    
    console.log('Total selected spells:', result);
    return result;
}

function showSpellInfo(spell) {
    // Remove existing spell info modal if any
    const existingModal = document.getElementById('spell-info-modal');
    if (existingModal) {
        existingModal.remove();
    }
    
    // Create modal
    const modal = document.createElement('div');
    modal.id = 'spell-info-modal';
    modal.className = 'spell-info-modal';
    
    // Format components
    const components = spell.components.join(', ');
    
    // Create source badge for modal if available
    const sourceBadge = spell.source ? `<span class="spell-source ${spell.source.toLowerCase()}">${spell.source}</span>` : '';
    
    // Create modal content
    modal.innerHTML = `
        <div class="spell-info-content">
            <div class="spell-info-header">
                <h3 class="spell-info-title">
                    ${spell.name}
                    ${sourceBadge}
                </h3>
                <button class="spell-info-close" onclick="closeSpellInfo()">×</button>
            </div>
            <div class="spell-info-body">
                <div class="spell-info-grid">
                    <div class="spell-info-item">
                        <strong>School:</strong> ${spell.school}
                    </div>
                    <div class="spell-info-item">
                        <strong>Casting Time:</strong> ${spell.casting_time}
                    </div>
                    <div class="spell-info-item">
                        <strong>Range:</strong> ${spell.range}
                    </div>
                    <div class="spell-info-item">
                        <strong>Components:</strong> ${components}
                    </div>
                    <div class="spell-info-item">
                        <strong>Duration:</strong> ${spell.duration}
                    </div>
                    ${spell.source ? `<div class="spell-info-item">
                        <strong>Source:</strong> ${spell.source}
                    </div>` : ''}
                </div>
                <div class="spell-info-description">
                    <strong>Description:</strong>
                    <p>${spell.description}</p>
                </div>
            </div>
        </div>
    `;
    
    // Add modal to page
    document.body.appendChild(modal);
    
    // Add backdrop click to close
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            closeSpellInfo();
        }
    });
    
    // Add escape key to close
    document.addEventListener('keydown', function escapeHandler(e) {
        if (e.key === 'Escape') {
            closeSpellInfo();
            document.removeEventListener('keydown', escapeHandler);
        }
    });
    
    // Focus modal for accessibility
    modal.focus();
}

function closeSpellInfo() {
    const modal = document.getElementById('spell-info-modal');
    if (modal) {
        modal.remove();
    }
}

// Agregar estilos de notificaciones si no existen
if (!document.querySelector('#notification-styles')) {
    const style = document.createElement('style');
    style.id = 'notification-styles';
    style.textContent = notificationStyles;
    document.head.appendChild(style);
} 
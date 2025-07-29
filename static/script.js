// Funcionalidad principal de EchoSheet

document.addEventListener('DOMContentLoaded', function() {
    // Inicializar funcionalidades según la página
    if (document.getElementById('character-form')) {
        initCharacterCreation();
    }
    
    if (document.getElementById('chat-form')) {
        initChat();
    }
    
    // Inicializar funcionalidades de character sheet
    if (document.querySelector('.character-sheet')) {
        initPersonalityEditor();
        initInventorySystem();
        initCharacterInfoEditors();
        initLevelUp();
        initPersonalityTags();
        initExperienceTracking();
    }
    
    // Inicializar botones de preguntas sugeridas
    initSuggestedQuestions();
    
    // Inicializar funcionalidad de eliminación de personajes
    initCharacterDeletion();
    
    // Inicializar botones de descarga PDF
    initPdfDownload();
    
    // Initialize level up functionality
    initLevelUp();
    
    // Enhanced Personality Tags System
    initPersonalityTags();
    
    // Initialize experience tracking
    initExperienceTracking();
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
    playstyleSelect.innerHTML = '';
    
    // Add playstyle options
    availablePlaystyles.forEach(playstyle => {
        const option = document.createElement('option');
        option.value = playstyle;
        
        // Format playstyle names nicely
        let displayName = playstyle;
        if (playstyle === 'standard_array') {
            displayName = 'Standard Array';
        } else {
            displayName = playstyle.charAt(0).toUpperCase() + playstyle.slice(1);
        }
        
        option.textContent = displayName;
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
            let playstyleDisplay = data.current_playstyle;
            if (data.current_playstyle === 'standard_array') {
                playstyleDisplay = 'Standard Array';
            } else {
                playstyleDisplay = data.current_playstyle.charAt(0).toUpperCase() + data.current_playstyle.slice(1);
            }
            playstyleInfo.textContent = `Playstyle: ${playstyleDisplay}`;
            playstyleInfo.style.display = 'block';
        } else {
            playstyleInfo.textContent = 'Playstyle: Standard Array';
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

// PDF Download functionality
function initPdfDownload() {
    const downloadButtons = document.querySelectorAll('.download-pdf-btn');
    
    downloadButtons.forEach(button => {
        button.addEventListener('click', function() {
            const characterId = this.getAttribute('data-character-id');
            const characterName = this.getAttribute('data-character-name');
            
            // Show notification that PDF download is coming soon
            showNotification('PDF download feature coming soon!', 'info');
            
            // PDF generation feature coming soon
            // This will be implemented in a future update
            console.log('PDF download requested for character:', characterName, 'ID:', characterId);
        });
    });
}

// Agregar estilos de notificaciones si no existen
if (!document.querySelector('#notification-styles')) {
    const style = document.createElement('style');
    style.id = 'notification-styles';
    style.textContent = notificationStyles;
    document.head.appendChild(style);
} 

// Personality Editor Functionality
function initPersonalityEditor() {
    const personalityTab = document.getElementById('personality-tab');
    if (!personalityTab) return;
    
    // Initialize character counters
    initCharacterCounters();
    
    // Initialize tags system
    initTagsSystem();
    
    // Initialize save functionality
    initPersonalitySave();
}

function initCharacterCounters() {
    const textareas = document.querySelectorAll('.personality-textarea');
    
    textareas.forEach(textarea => {
        const counterId = textarea.id + '-count';
        const counter = document.getElementById(counterId);
        
        if (counter) {
            // Update counter on input
            textarea.addEventListener('input', function() {
                const currentLength = this.value.length;
                const maxLength = this.maxLength;
                counter.textContent = currentLength;
                
                // Change color when approaching limit
                if (currentLength >= maxLength * 0.9) {
                    counter.style.color = '#e74c3c';
                } else if (currentLength >= maxLength * 0.7) {
                    counter.style.color = '#f39c12';
                } else {
                    counter.style.color = '#f4d03f';
                }
            });
        }
    });
}

function initTagsSystem() {
    const tagsInput = document.getElementById('personality-tags-input');
    const tagsDisplay = document.getElementById('personality-tags-display');
    
    if (!tagsInput || !tagsDisplay) return;
    
    // Handle input events
    tagsInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' || e.key === ' ' || e.key === ',') {
            e.preventDefault();
            addTag(this.value.trim());
            this.value = '';
        }
    });
    
    // Handle paste events
    tagsInput.addEventListener('paste', function(e) {
        e.preventDefault();
        const pastedText = (e.clipboardData || window.clipboardData).getData('text');
        const tags = pastedText.split(/[\s,]+/).filter(tag => tag.trim());
        
        tags.forEach(tag => {
            if (tag.trim()) {
                addTag(tag.trim());
            }
        });
    });
    
    // Handle blur event
    tagsInput.addEventListener('blur', function() {
        if (this.value.trim()) {
            addTag(this.value.trim());
            this.value = '';
        }
    });
}

function addTag(tagText) {
    if (!tagText || tagText.length === 0) return;
    
    // Clean the tag text (single word, no spaces)
    const cleanTag = tagText.toLowerCase().replace(/[^a-z0-9]/g, '');
    if (!cleanTag) return;
    
    // Capitalize first letter
    const displayTag = cleanTag.charAt(0).toUpperCase() + cleanTag.slice(1);
    
    // Check if tag already exists
    const existingTags = document.querySelectorAll('#personality-tags-display .tag');
    for (let tag of existingTags) {
        if (tag.getAttribute('data-tag').toLowerCase() === cleanTag) {
            return; // Tag already exists
        }
    }
    
    // Create new tag element
    const tagElement = document.createElement('span');
    tagElement.className = 'tag';
    tagElement.setAttribute('data-tag', cleanTag);
    tagElement.innerHTML = `
        ${displayTag}
        <button type="button" class="tag-remove" onclick="removeTag(this)">×</button>
    `;
    
    // Add to display
    const tagsDisplay = document.getElementById('personality-tags-display');
    tagsDisplay.appendChild(tagElement);
    
    // Trigger save
    debouncedSavePersonality();
}

function removeTag(button) {
    const tag = button.parentElement;
    tag.style.animation = 'tagSlideOut 0.3s ease';
    
    setTimeout(() => {
        tag.remove();
        debouncedSavePersonality();
    }, 300);
}

// Debounced save function
const debouncedSavePersonality = debounce(savePersonality, 1000);

function initPersonalitySave() {
    const saveBtn = document.getElementById('save-personality-btn');
    if (!saveBtn) return;
    
    saveBtn.addEventListener('click', function() {
        savePersonality();
    });
    
    // Auto-save on input changes
    const textareas = document.querySelectorAll('.personality-textarea');
    textareas.forEach(textarea => {
        textarea.addEventListener('input', debouncedSavePersonality);
    });
}

function savePersonality() {
    const characterId = getCharacterIdFromUrl();
    if (!characterId) return;
    
    const saveBtn = document.getElementById('save-personality-btn');
    const saveStatus = document.getElementById('save-status');
    
    // Show saving state
    if (saveBtn) {
        saveBtn.disabled = true;
        saveBtn.innerHTML = '💾 Saving...';
    }
    if (saveStatus) {
        saveStatus.textContent = 'Saving...';
        saveStatus.className = 'save-status saving';
    }
    
    // Collect data
    const data = {
        background_story: document.getElementById('background-story')?.value || '',
        short_term_goals: document.getElementById('short-term-goals')?.value || '',
        long_term_goals: document.getElementById('long-term-goals')?.value || '',
        personal_goals: document.getElementById('personal-goals')?.value || '',
        personality_traits: document.getElementById('personality-traits')?.value || '',
        ideals: document.getElementById('ideals')?.value || '',
        bonds: document.getElementById('bonds')?.value || '',
        personality_tags: getPersonalityTags(),
        flaws: document.getElementById('flaws')?.value || ''
    };
    
    // Send to server
    fetch(`/api/character/${characterId}/personality`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        if (result.success) {
            if (saveStatus) {
                saveStatus.textContent = 'Saved successfully!';
                saveStatus.className = 'save-status success';
            }
            showNotification('Personality saved successfully!', 'success');
        } else {
            if (saveStatus) {
                saveStatus.textContent = 'Error saving';
                saveStatus.className = 'save-status error';
            }
            showNotification('Error saving personality: ' + (result.error || 'Unknown error'), 'error');
        }
    })
    .catch(error => {
        console.error('Error saving personality:', error);
        if (saveStatus) {
            saveStatus.textContent = 'Error saving';
            saveStatus.className = 'save-status error';
        }
        showNotification('Error saving personality: ' + error.message, 'error');
    })
    .finally(() => {
        if (saveBtn) {
            saveBtn.disabled = false;
            saveBtn.innerHTML = '💾 Save Personality';
        }
        
        // Clear status after 3 seconds
        setTimeout(() => {
            if (saveStatus) {
                saveStatus.textContent = '';
                saveStatus.className = 'save-status';
            }
        }, 3000);
    });
}

function getPersonalityTags() {
    const tags = document.querySelectorAll('#personality-tags-display .tag');
    return Array.from(tags).map(tag => tag.getAttribute('data-tag'));
}

function getCharacterIdFromUrl() {
    const urlParts = window.location.pathname.split('/');
    const characterIndex = urlParts.indexOf('character');
    if (characterIndex !== -1 && urlParts[characterIndex + 1]) {
        return urlParts[characterIndex + 1];
    }
    return null;
}

// Add slide out animation for tags
const personalityStyles = document.createElement('style');
personalityStyles.textContent = `
    @keyframes tagSlideOut {
        from {
            opacity: 1;
            transform: translateY(0) scale(1);
        }
        to {
            opacity: 0;
            transform: translateY(-10px) scale(0.8);
        }
    }
`;
document.head.appendChild(personalityStyles);

// Initialize personality editor when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize personality editor if on character page
    if (document.getElementById('personality-tab')) {
        initPersonalityEditor();
    }
    
    // Initialize inventory system if on character page
    if (document.getElementById('inventory-tab')) {
        initInventorySystem();
    }
});

// Inventory System Functionality
function initInventorySystem() {
    const inventoryTab = document.getElementById('inventory-tab');
    if (!inventoryTab) return;
    
    // Initialize currency system
    initCurrencySystem();
    
    // Initialize items system
    initItemsSystem();
    
    // Initialize equipment packs
    initEquipmentPacks();
    
    // Initialize save functionality
    initInventorySave();
}

function initCurrencySystem() {
    const currencyInputs = document.querySelectorAll('.currency-input');
    
    currencyInputs.forEach(input => {
        input.addEventListener('input', function() {
            updateCurrencyTotal();
            debouncedSaveInventory();
        });
    });
}

function updateCurrencyTotal() {
    const currencyValues = {
        'cp': 1,
        'sp': 10,
        'ep': 50,
        'gp': 100,
        'pp': 1000
    };
    
    let totalCp = 0;
    
    // Calculate total in copper pieces
    for (const [type, value] of Object.entries(currencyValues)) {
        const input = document.getElementById(`${type}-amount`);
        if (input) {
            const amount = parseInt(input.value) || 0;
            totalCp += amount * value;
        }
    }
    
    // Convert back to highest denominations
    const pp = Math.floor(totalCp / 1000);
    totalCp %= 1000;
    const gp = Math.floor(totalCp / 100);
    totalCp %= 100;
    const ep = Math.floor(totalCp / 50);
    totalCp %= 50;
    const sp = Math.floor(totalCp / 10);
    totalCp %= 10;
    const cp = totalCp;
    
    // Build formatted string
    const parts = [];
    if (pp > 0) parts.push(`${pp} pp`);
    if (gp > 0) parts.push(`${gp} gp`);
    if (ep > 0) parts.push(`${ep} ep`);
    if (sp > 0) parts.push(`${sp} sp`);
    if (cp > 0) parts.push(`${cp} cp`);
    
    const totalDisplay = parts.length > 0 ? parts.join(', ') : '0 cp';
    const totalElement = document.getElementById('currency-total');
    if (totalElement) {
        totalElement.textContent = totalDisplay;
    }
}

function initItemsSystem() {
    const itemsInput = document.getElementById('items-input');
    const itemsDisplay = document.getElementById('items-display');
    const clearAllBtn = document.getElementById('clear-all-items-btn');
    
    if (!itemsInput || !itemsDisplay) return;
    
    // Handle input events
    itemsInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' || e.key === ' ' || e.key === ',') {
            e.preventDefault();
            addItem(this.value.trim());
            this.value = '';
        }
    });
    
    // Handle paste events
    itemsInput.addEventListener('paste', function(e) {
        e.preventDefault();
        const pastedText = (e.clipboardData || window.clipboardData).getData('text');
        const items = pastedText.split(/[\s,]+/).filter(item => item.trim());
        
        items.forEach(item => {
            if (item.trim()) {
                addItem(item.trim());
            }
        });
    });
    
    // Handle blur event
    itemsInput.addEventListener('blur', function() {
        if (this.value.trim()) {
            addItem(this.value.trim());
            this.value = '';
        }
    });
    
    // Handle clear all items
    if (clearAllBtn) {
        clearAllBtn.addEventListener('click', function() {
            if (confirm('Are you sure you want to remove all items? This action cannot be undone.')) {
                clearAllItems();
            }
        });
    }
}

function addItem(itemText) {
    if (!itemText || itemText.length === 0) return;
    
    // Clean the item text
    const cleanItem = itemText.trim();
    if (!cleanItem) return;
    
    // Check if item already exists
    const existingItems = document.querySelectorAll('#items-display .item-tag');
    for (let item of existingItems) {
        if (item.getAttribute('data-item').toLowerCase() === cleanItem.toLowerCase()) {
            return; // Item already exists
        }
    }
    
    // Create new item element
    const itemElement = document.createElement('span');
    itemElement.className = 'item-tag';
    itemElement.setAttribute('data-item', cleanItem);
    itemElement.innerHTML = `
        <div class="item-content">
            <span class="item-name">${cleanItem}</span>
            <span class="item-weight" data-item="${cleanItem}">1.0 lbs</span>
        </div>
        <button type="button" class="item-edit-weight" onclick="editItemWeight('${cleanItem}')" title="Edit weight">⚖️</button>
        <button type="button" class="item-remove" onclick="removeItem(this)">×</button>
    `;
    
    // Add to display
    const itemsDisplay = document.getElementById('items-display');
    itemsDisplay.appendChild(itemElement);
    
    // Update weight calculation
    updateWeightCalculation();
    
    // Trigger save
    debouncedSaveInventory();
}

function removeItem(button) {
    const item = button.parentElement;
    item.style.animation = 'tagSlideOut 0.3s ease';
    
    setTimeout(() => {
        item.remove();
        updateWeightCalculation();
        debouncedSaveInventory();
    }, 300);
}

function updateWeightCalculation() {
    // Calculate weight from displayed weights
    const items = document.querySelectorAll('#items-display .item-tag');
    let estimatedWeight = 0;
    
    items.forEach(item => {
        const weightElement = item.querySelector('.item-weight');
        if (weightElement) {
            const weight = parseFloat(weightElement.textContent.replace(' lbs', ''));
            estimatedWeight += weight;
        }
    });
    
    // Add currency weight (50 coins = 1 pound)
    const currencyInputs = document.querySelectorAll('.currency-input');
    let totalCoins = 0;
    currencyInputs.forEach(input => {
        totalCoins += parseInt(input.value) || 0;
    });
    estimatedWeight += totalCoins * 0.02;
    
    // Update display
    const weightElement = document.getElementById('current-weight');
    if (weightElement) {
        weightElement.textContent = `${Math.round(estimatedWeight * 10) / 10} lbs`;
    }
    
    // Update weight status
    updateWeightStatus(estimatedWeight);
}

function updateCurrencyFromPack(currencyAdded) {
    // Update currency inputs with new values
    for (const [currencyType, amount] of Object.entries(currencyAdded)) {
        const input = document.getElementById(`${currencyType}-amount`);
        if (input) {
            const currentValue = parseInt(input.value) || 0;
            input.value = currentValue + amount;
        }
    }
    
    // Update currency total display
    updateCurrencyTotal();
}

function addItemsFromPack(itemsAdded, packName) {
    const itemsDisplay = document.getElementById('items-display');
    if (!itemsDisplay) return;
    
    // Get pack weights from the equipment packs data
    const packWeights = getPackWeights(packName);
    
    itemsAdded.forEach(item => {
        // Check if item already exists
        const existingItem = document.querySelector(`[data-item="${item}"]`);
        if (!existingItem) {
            // Get weight for this item from pack data
            const weight = packWeights[item] || 1.0;
            
            // Create new item element
            const itemElement = document.createElement('span');
            itemElement.className = 'item-tag';
            itemElement.setAttribute('data-item', item);
            itemElement.innerHTML = `
                <div class="item-content">
                    <span class="item-name">${item}</span>
                    <span class="item-weight" data-item="${item}">${weight} lbs</span>
                </div>
                <button type="button" class="item-edit-weight" onclick="editItemWeight('${item}')" title="Edit weight">⚖️</button>
                <button type="button" class="item-remove" onclick="removeItem(this)">×</button>
            `;
            
            // Add to display with animation
            itemElement.style.animation = 'tagSlideIn 0.3s ease';
            itemsDisplay.appendChild(itemElement);
        }
    });
}

function getPackWeights(packName) {
    // This would ideally come from the server, but for now we'll use a simplified version
    const packWeights = {
        "Burglar's Pack": {
            "Backpack": 5.0, "Bag of 1,000 ball bearings": 2.0, "10 feet of string": 0.0,
            "Bell": 0.0, "5 candles": 0.0, "Crowbar": 5.0, "Hammer": 3.0, "10 pitons": 2.5,
            "Hooded lantern": 2.0, "2 flasks of oil": 2.0, "5 days of rations": 10.0,
            "Tinderbox": 1.0, "Waterskin": 5.0, "50 feet of hempen rope": 10.0
        },
        "Diplomat's Pack": {
            "Chest": 25.0, "2 cases for maps and scrolls": 1.0, "Fine clothes": 6.0,
            "Bottle of ink": 0.0, "Ink pen": 0.0, "Lamp": 1.0, "2 flasks of oil": 2.0,
            "5 sheets of paper": 0.0, "Vial of perfume": 0.0, "Sealing wax": 0.0, "Soap": 0.0
        },
        "Dungeoneer's Pack": {
            "Backpack": 5.0, "Crowbar": 5.0, "Hammer": 3.0, "10 pitons": 2.5,
            "10 torches": 10.0, "Tinderbox": 1.0, "10 days of rations": 20.0,
            "Waterskin": 5.0, "50 feet of hempen rope": 10.0
        },
        "Entertainer's Pack": {
            "Backpack": 5.0, "Bedroll": 7.0, "2 costumes": 8.0, "5 candles": 0.0,
            "5 days of rations": 10.0, "Waterskin": 5.0, "Disguise kit": 3.0
        },
        "Explorer's Pack": {
            "Backpack": 5.0, "Bedroll": 7.0, "Mess kit": 1.0, "Tinderbox": 1.0,
            "10 torches": 10.0, "10 days of rations": 20.0, "Waterskin": 5.0,
            "50 feet of hempen rope": 10.0
        },
        "Priest's Pack": {
            "Backpack": 5.0, "Blanket": 3.0, "10 candles": 0.0, "Tinderbox": 1.0,
            "Alms box": 1.0, "2 blocks of incense": 0.0, "Censer": 1.0,
            "Vestments": 4.0, "2 days of rations": 4.0, "Waterskin": 5.0
        },
        "Scholar's Pack": {
            "Backpack": 5.0, "Book of lore": 5.0, "Bottle of ink": 0.0, "Ink pen": 0.0,
            "10 sheets of parchment": 0.0, "Little bag of sand": 1.0, "Small knife": 1.0
        }
    };
    
    return packWeights[packName] || {};
}

function updateWeightStatus(weight) {
    const statusElement = document.getElementById('weight-status');
    if (!statusElement) return;
    
    // Get carrying capacity (simplified - would need to get from character data)
    const capacity = 150; // Default capacity, should be calculated from Strength
    
    let statusHtml = '';
    if (weight > capacity) {
        statusHtml = '<span class="weight-warning">⚠️ Overloaded! Reduce weight to avoid penalties.</span>';
    } else if (weight > capacity * 0.8) {
        statusHtml = '<span class="weight-caution">⚡ Heavy load - movement may be affected.</span>';
    } else {
        statusHtml = '<span class="weight-ok">✅ Weight is manageable.</span>';
    }
    
    statusElement.innerHTML = statusHtml;
}

// Debounced save function for inventory
const debouncedSaveInventory = debounce(saveInventory, 1000);

function initInventorySave() {
    const saveBtn = document.getElementById('save-inventory-btn');
    if (!saveBtn) return;
    
    saveBtn.addEventListener('click', function() {
        saveInventory();
    });
}

function saveInventory() {
    const characterId = getCharacterIdFromUrl();
    if (!characterId) return;
    
    const saveBtn = document.getElementById('save-inventory-btn');
    const saveStatus = document.getElementById('inventory-save-status');
    
    // Show saving state
    if (saveBtn) {
        saveBtn.disabled = true;
        saveBtn.innerHTML = '💾 Saving...';
    }
    if (saveStatus) {
        saveStatus.textContent = 'Saving...';
        saveStatus.className = 'save-status saving';
    }
    
    // Collect currency data
    const currency = {};
    const currencyTypes = ['cp', 'sp', 'ep', 'gp', 'pp'];
    currencyTypes.forEach(type => {
        const input = document.getElementById(`${type}-amount`);
        if (input) {
            currency[type] = parseInt(input.value) || 0;
        }
    });
    
    // Collect items data
    const items = getInventoryItems();
    
    // Collect item weights
    const itemWeights = {};
    items.forEach(item => {
        const weightElement = document.querySelector(`[data-item="${item}"] .item-weight`);
        if (weightElement) {
            const weight = parseFloat(weightElement.textContent.replace(' lbs', ''));
            if (!isNaN(weight)) {
                itemWeights[item] = weight;
            }
        }
    });
    
    // Collect data
    const data = {
        currency: currency,
        items: items,
        item_weights: itemWeights
    };
    
    // Send to server
    fetch(`/api/character/${characterId}/inventory`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        if (result.success) {
            if (saveStatus) {
                saveStatus.textContent = 'Saved successfully!';
                saveStatus.className = 'save-status success';
            }
            showNotification('Inventory saved successfully!', 'success');
        } else {
            if (saveStatus) {
                saveStatus.textContent = 'Error saving';
                saveStatus.className = 'save-status error';
            }
            showNotification('Error saving inventory: ' + (result.error || 'Unknown error'), 'error');
        }
    })
    .catch(error => {
        console.error('Error saving inventory:', error);
        if (saveStatus) {
            saveStatus.textContent = 'Error saving';
            saveStatus.className = 'save-status error';
        }
        showNotification('Error saving inventory: ' + error.message, 'error');
    })
    .finally(() => {
        if (saveBtn) {
            saveBtn.disabled = false;
            saveBtn.innerHTML = '💾 Save Inventory';
        }
        
        // Clear status after 3 seconds
        setTimeout(() => {
            if (saveStatus) {
                saveStatus.textContent = '';
                saveStatus.className = 'save-status';
            }
        }, 3000);
    });
}

function getInventoryItems() {
    const items = document.querySelectorAll('#items-display .item-tag');
    return Array.from(items).map(item => item.getAttribute('data-item'));
}

function clearAllItems() {
    const itemsDisplay = document.getElementById('items-display');
    if (!itemsDisplay) return;
    
    // Remove all items with animation
    const items = itemsDisplay.querySelectorAll('.item-tag');
    items.forEach((item, index) => {
        setTimeout(() => {
            item.style.animation = 'tagSlideOut 0.3s ease';
            setTimeout(() => {
                item.remove();
                // Update weight calculation after all items are removed
                if (index === items.length - 1) {
                    updateWeightCalculation();
                    debouncedSaveInventory();
                }
            }, 300);
        }, index * 50); // Stagger the animations
    });
    
    showNotification('All items removed successfully!', 'success');
}

// Equipment Packs Functionality
function initEquipmentPacks() {
    const packButtons = document.querySelectorAll('.pack-btn');
    
    packButtons.forEach(button => {
        button.addEventListener('click', function() {
            const packName = this.getAttribute('data-pack');
            applyEquipmentPack(packName);
        });
    });
}

function applyEquipmentPack(packName) {
    const characterId = getCharacterIdFromUrl();
    if (!characterId) return;
    
    const statusElement = document.getElementById('pack-status');
    
    // Show loading state
    if (statusElement) {
        statusElement.textContent = `Applying ${packName}...`;
        statusElement.className = 'pack-status';
    }
    
    // Send request to server
    fetch(`/api/character/${characterId}/apply-pack`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ pack_name: packName })
    })
    .then(response => response.json())
            .then(result => {
            if (result.success) {
                if (statusElement) {
                    statusElement.textContent = `✅ ${packName} applied successfully! Added ${result.items_added.length} items and ${Object.values(result.currency_added)[0]} gp`;
                    statusElement.className = 'pack-status pack-success';
                }
                
                // Update currency display
                updateCurrencyFromPack(result.currency_added);
                
                // Add new items to display
                addItemsFromPack(result.items_added, result.pack_name);
                
                // Update weight calculation
                updateWeightCalculation();
                
                // Auto-save the changes
                debouncedSaveInventory();
                
                showNotification(`${packName} applied successfully!`, 'success');
                
                // Clear status after 5 seconds
                setTimeout(() => {
                    if (statusElement) {
                        statusElement.textContent = '';
                        statusElement.className = 'pack-status';
                    }
                }, 5000);
            } else {
                if (statusElement) {
                    statusElement.textContent = `❌ Error: ${result.error}`;
                    statusElement.className = 'pack-status pack-error';
                }
                showNotification('Error applying pack: ' + (result.error || 'Unknown error'), 'error');
            }
        })
    .catch(error => {
        console.error('Error applying pack:', error);
        if (statusElement) {
            statusElement.textContent = '❌ Error applying pack';
            statusElement.className = 'pack-status pack-error';
        }
        showNotification('Error applying pack: ' + error.message, 'error');
    });
}

// Item Weight Editing Functionality
function editItemWeight(itemName) {
    const currentWeight = getItemWeightFromDisplay(itemName);
    const newWeight = prompt(`Enter new weight for "${itemName}" (in pounds):`, currentWeight);
    
    if (newWeight !== null && newWeight !== '') {
        const weight = parseFloat(newWeight);
        if (isNaN(weight) || weight < 0) {
            showNotification('Please enter a valid positive number for weight', 'error');
            return;
        }
        
        updateItemWeight(itemName, weight);
        debouncedSaveInventory();
    }
}

function getItemWeightFromDisplay(itemName) {
    const weightElement = document.querySelector(`[data-item="${itemName}"] .item-weight`);
    if (weightElement) {
        return parseFloat(weightElement.textContent.replace(' lbs', ''));
    }
    return 1.0;
}

function updateItemWeight(itemName, weight) {
    // Update display
    const weightElement = document.querySelector(`[data-item="${itemName}"] .item-weight`);
    if (weightElement) {
        weightElement.textContent = `${weight} lbs`;
    }
    
    // Update weight calculation
    updateWeightCalculation();
}

function updateWeightCalculation() {
    // This is a simplified weight calculation
    // In a full implementation, you'd have a database of item weights
    const items = document.querySelectorAll('#items-display .item-tag');
    let estimatedWeight = 0;
    
    // Calculate weight from displayed weights
    items.forEach(item => {
        const weightElement = item.querySelector('.item-weight');
        if (weightElement) {
            const weight = parseFloat(weightElement.textContent.replace(' lbs', ''));
            estimatedWeight += weight;
        }
    });
    
    // Add currency weight (50 coins = 1 pound)
    const currencyInputs = document.querySelectorAll('.currency-input');
    let totalCoins = 0;
    currencyInputs.forEach(input => {
        totalCoins += parseInt(input.value) || 0;
    });
    estimatedWeight += totalCoins * 0.02;
    
    // Update display
    const weightElement = document.getElementById('current-weight');
    if (weightElement) {
        weightElement.textContent = `${Math.round(estimatedWeight * 10) / 10} lbs`;
    }
    
    // Update weight status
    updateWeightStatus(estimatedWeight);
}

// Initialize character info editors
function initCharacterInfoEditors() {
    initBasicInfoEditor();
    initPhysicalInfoEditor();
    initHitPointsEditor();
}

function initBasicInfoEditor() {
    const saveBtn = document.getElementById('save-basic-info-btn');
    if (!saveBtn) return;
    
    saveBtn.addEventListener('click', saveBasicInfo);
}

function initPhysicalInfoEditor() {
    const saveBtn = document.getElementById('save-physical-btn');
    if (!saveBtn) return;
    
    saveBtn.addEventListener('click', savePhysicalInfo);
}

function initHitPointsEditor() {
    const saveBtn = document.getElementById('save-hp-btn');
    if (!saveBtn) return;
    
    saveBtn.addEventListener('click', saveHitPoints);
    
    // Initialize HP tracking
    initHPTracking();
}

function saveBasicInfo() {
    const characterId = getCharacterIdFromUrl();
    if (!characterId) return;
    
    const saveBtn = document.getElementById('save-basic-info-btn');
    
    // Show saving state
    if (saveBtn) {
        saveBtn.disabled = true;
        saveBtn.innerHTML = '💾 Saving...';
    }
    
    // Collect data
    const data = {
        alignment: document.getElementById('alignment-select')?.value || '',
        experience_points: parseInt(document.getElementById('experience-points')?.value || '0')
    };
    
    // Send to server
    fetch(`/api/character/${characterId}/basic-info`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        if (result.success) {
            showNotification('Basic information saved successfully!', 'success');
            // Update progress bar and level up button
            updateExperienceDisplay();
        } else {
            showNotification('Error saving basic information: ' + (result.error || 'Unknown error'), 'error');
        }
    })
    .catch(error => {
        console.error('Error saving basic info:', error);
        showNotification('Error saving basic information: ' + error.message, 'error');
    })
    .finally(() => {
        if (saveBtn) {
            saveBtn.disabled = false;
            saveBtn.innerHTML = '💾 Save Basic Info';
        }
    });
}

function updateExperienceDisplay() {
    // Update the experience progress display after saving
    updateExperienceProgress();
    
    // Show a brief success message without reloading
    showNotification('Experience updated successfully!', 'success');
}

function savePhysicalInfo() {
    const characterId = getCharacterIdFromUrl();
    if (!characterId) return;
    
    const saveBtn = document.getElementById('save-physical-btn');
    
    // Show saving state
    if (saveBtn) {
        saveBtn.disabled = true;
        saveBtn.innerHTML = '💾 Saving...';
    }
    
    // Collect data
    const data = {
        age: document.getElementById('age-input')?.value || '',
        height: document.getElementById('height-input')?.value || '',
        weight: document.getElementById('weight-input')?.value || '',
        eyes: document.getElementById('eyes-input')?.value || '',
        skin: document.getElementById('skin-input')?.value || '',
        hair: document.getElementById('hair-input')?.value || ''
    };
    
    // Send to server
    fetch(`/api/character/${characterId}/physical-info`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        if (result.success) {
            showNotification('Physical information saved successfully!', 'success');
        } else {
            showNotification('Error saving physical information: ' + (result.error || 'Unknown error'), 'error');
        }
    })
    .catch(error => {
        console.error('Error saving physical info:', error);
        showNotification('Error saving physical information: ' + error.message, 'error');
    })
    .finally(() => {
        if (saveBtn) {
            saveBtn.disabled = false;
            saveBtn.innerHTML = '💾 Save Physical Info';
        }
    });
}

function saveHitPoints() {
    const characterId = getCharacterIdFromUrl();
    if (!characterId) return;
    
    const saveBtn = document.getElementById('save-hp-btn');
    
    // Show saving state
    if (saveBtn) {
        saveBtn.disabled = true;
        saveBtn.innerHTML = '💾 Saving...';
    }
    
    // Collect data
    const data = {
        hit_point_maximum: parseInt(document.getElementById('hp-maximum')?.value || '0'),
        current_hit_points: parseInt(document.getElementById('hp-current')?.value || '0'),
        temporary_hit_points: parseInt(document.getElementById('hp-temporary')?.value || '0')
    };
    
    // Validate data
    if (data.hit_point_maximum < 1) {
        showNotification('Hit Point Maximum must be at least 1', 'error');
        if (saveBtn) {
            saveBtn.disabled = false;
            saveBtn.innerHTML = '💾 Save HP';
        }
        return;
    }
    
    if (data.current_hit_points < 0) {
        showNotification('Current Hit Points cannot be negative', 'error');
        if (saveBtn) {
            saveBtn.disabled = false;
            saveBtn.innerHTML = '💾 Save HP';
        }
        return;
    }
    
    if (data.temporary_hit_points < 0) {
        showNotification('Temporary Hit Points cannot be negative', 'error');
        if (saveBtn) {
            saveBtn.disabled = false;
            saveBtn.innerHTML = '💾 Save HP';
        }
        return;
    }
    
    // Send to server
    fetch(`/api/character/${characterId}/hit-points`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        if (result.success) {
            showNotification('Hit Points saved successfully!', 'success');
            // Update visual bar after saving
            updateHPVisualBar();
        } else {
            showNotification('Error saving hit points: ' + (result.error || 'Unknown error'), 'error');
        }
    })
    .catch(error => {
        console.error('Error saving hit points:', error);
        showNotification('Error saving hit points: ' + error.message, 'error');
    })
    .finally(() => {
        if (saveBtn) {
            saveBtn.disabled = false;
            saveBtn.innerHTML = '💾 Save HP';
        }
    });
} 

// Initialize level up functionality
function initLevelUp() {
    const levelUpBtn = document.getElementById('level-up-btn');
    if (!levelUpBtn) return;
    
    levelUpBtn.addEventListener('click', performLevelUp);
    

}

function performLevelUp() {
    const characterId = getCharacterIdFromUrl();
    if (!characterId) return;
    
    const levelUpBtn = document.getElementById('level-up-btn');
    
    // Show loading state
    if (levelUpBtn) {
        levelUpBtn.disabled = true;
        levelUpBtn.innerHTML = '💾 Saving XP...';
    }
    
    // First, save the current XP
    const expInput = document.getElementById('experience-points');
    const currentXP = expInput ? parseInt(expInput.value) || 0 : 0;
    
    // Save XP first
    fetch(`/api/character/${characterId}/basic-info`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            experience_points: currentXP
        })
    })
    .then(response => response.json())
    .then(saveResult => {
        if (!saveResult.success) {
            throw new Error('Failed to save XP: ' + (saveResult.error || 'Unknown error'));
        }
        
        // Update button text to show leveling up
        if (levelUpBtn) {
            levelUpBtn.innerHTML = '🎯 Leveling Up...';
        }
        
        // Now send level up request
        return fetch(`/api/character/${characterId}/level-up`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        });
    })
    .then(response => response.json())
    .then(result => {
        if (result.success) {
            showNotification(result.message, 'success');
            
            // Update the level display
            const levelDisplay = document.getElementById('character-level');
            if (levelDisplay) {
                levelDisplay.textContent = result.new_level;
            }
            
            // Update experience progress after level up
            updateExperienceProgress();
            
            // Hide level up button if character can't level up anymore
            const levelUpContainer = document.getElementById('level-up-container');
            if (levelUpContainer) {
                levelUpContainer.style.display = 'none';
            }
        } else {
            showNotification('Error leveling up: ' + (result.error || 'Unknown error'), 'error');
        }
    })
    .catch(error => {
        console.error('Error leveling up:', error);
        showNotification('Error leveling up: ' + error.message, 'error');
    })
    .finally(() => {
        if (levelUpBtn) {
            levelUpBtn.disabled = false;
            levelUpBtn.innerHTML = '🎯 Level Up!';
        }
    });
}

// Enhanced Personality Tags System
function initPersonalityTags() {
    const tagsInput = document.getElementById('personality-tags');
    const tagsContainer = document.getElementById('personality-tags-container');
    
    if (!tagsInput || !tagsContainer) return;
    
    // Handle input events
    tagsInput.addEventListener('keydown', handleTagInput);
    tagsInput.addEventListener('paste', handleTagPaste);
    tagsInput.addEventListener('blur', handleTagBlur);
    
    // Initialize existing tags
    updateTagsFromInput();
}

function handleTagInput(event) {
    if (event.key === 'Enter' || event.key === ' ' || event.key === ',') {
        event.preventDefault();
        addTagFromInput();
    }
}

function handleTagPaste(event) {
    setTimeout(() => {
        addTagFromInput();
    }, 10);
}

function handleTagBlur() {
    addTagFromInput();
}

function addTagFromInput() {
    const tagsInput = document.getElementById('personality-tags');
    const tagsContainer = document.getElementById('personality-tags-container');
    
    if (!tagsInput || !tagsContainer) return;
    
    const inputValue = tagsInput.value.trim();
    if (!inputValue) return;
    
    // Split by spaces and commas
    const newTags = inputValue.split(/[\s,]+/).filter(tag => tag.trim());
    
    // Get existing tags
    const existingTags = Array.from(tagsContainer.querySelectorAll('.tag')).map(tag => tag.dataset.tag);
    
    // Add new tags
    newTags.forEach(tag => {
        const cleanTag = tag.trim().toLowerCase();
        if (cleanTag && !existingTags.includes(cleanTag)) {
            addPersonalityTag(cleanTag);
        }
    });
    
    // Clear input
    tagsInput.value = '';
}

function addPersonalityTag(tagText) {
    const tagsContainer = document.getElementById('personality-tags-container');
    if (!tagsContainer) return;
    
    const tagElement = document.createElement('span');
    tagElement.className = 'tag';
    tagElement.dataset.tag = tagText;
    tagElement.innerHTML = `
        ${tagText}
        <button class="tag-remove" onclick="removePersonalityTag(this)">×</button>
    `;
    
    tagsContainer.appendChild(tagElement);
    
    // Trigger save
    debouncedSavePersonality();
}

function removePersonalityTag(button) {
    const tag = button.parentElement;
    tag.style.animation = 'tagDisappear 0.3s ease-out';
    
    setTimeout(() => {
        tag.remove();
        debouncedSavePersonality();
    }, 300);
}

function updateTagsFromInput() {
    const tagsInput = document.getElementById('personality-tags');
    const tagsContainer = document.getElementById('personality-tags-container');
    
    if (!tagsInput || !tagsContainer) return;
    
    // Clear existing tags
    tagsContainer.innerHTML = '';
    
    // Add tags from input value
    const inputValue = tagsInput.value.trim();
    if (inputValue) {
        const tags = inputValue.split(/[\s,]+/).filter(tag => tag.trim());
        tags.forEach(tag => {
            addPersonalityTag(tag.trim().toLowerCase());
        });
    }
}

function getPersonalityTags() {
    const tagsContainer = document.getElementById('personality-tags-container');
    if (!tagsContainer) return [];
    
    return Array.from(tagsContainer.querySelectorAll('.tag')).map(tag => tag.dataset.tag);
}

// Initialize experience tracking
function initExperienceTracking() {
    const expInput = document.getElementById('experience-points');
    if (!expInput) return;
    
    // Update on every input change for real-time feedback
    expInput.addEventListener('input', updateExperienceProgress);
    expInput.addEventListener('change', updateExperienceProgress);
    expInput.addEventListener('keyup', updateExperienceProgress);
    
    // Initial update
    updateExperienceProgress();
}

function updateExperienceProgress() {
    const expInput = document.getElementById('experience-points');
    const progressFill = document.getElementById('experience-progress-fill');
    const progressText = document.getElementById('experience-progress-text');
    const levelUpBtn = document.getElementById('level-up-btn');
    const expToNextDisplay = document.getElementById('experience-to-next-level');
    
    if (!expInput) return;
    
    const currentXP = parseInt(expInput.value) || 0;
    const characterLevel = parseInt(document.getElementById('character-level')?.textContent) || 1;
    
    // D&D 5e Experience Thresholds (corrected from official table)
    const xpThresholds = {
        1: 0, 2: 300, 3: 900, 4: 2700, 5: 6500,
        6: 14000, 7: 23000, 8: 34000, 9: 48000, 10: 64000,
        11: 85000, 12: 100000, 13: 120000, 14: 140000, 15: 165000,
        16: 195000, 17: 225000, 18: 265000, 19: 305000, 20: 355000
    };
    
    const currentLevelXP = xpThresholds[characterLevel] || 0;
    const nextLevelXP = xpThresholds[characterLevel + 1] || currentLevelXP;
    
    if (nextLevelXP === currentLevelXP) {
        // Max level (20)
        if (progressFill) progressFill.style.width = '100%';
        if (progressText) progressText.textContent = '100.0%';
        if (levelUpBtn) levelUpBtn.style.display = 'none';
        if (expToNextDisplay) expToNextDisplay.textContent = '0 XP';
        return;
    }
    
    // Calculate experience needed for next level
    const expToNext = Math.max(0, nextLevelXP - currentXP);
    
    // Calculate progress percentage (based on XP progress within current level)
    const progressPercent = nextLevelXP > currentLevelXP ? 
        Math.min(100.0, Math.max(0.0, ((currentXP - currentLevelXP) / (nextLevelXP - currentLevelXP)) * 100)) : 100.0;
    
    // Update progress bar
    if (progressFill) {
        progressFill.style.width = progressPercent + '%';
    }
    
    // Update progress text
    if (progressText) {
        progressText.textContent = progressPercent.toFixed(1) + '%';
    }
    
    // Update "Experience to Next Level" display
    if (expToNextDisplay) {
        expToNextDisplay.textContent = expToNext + ' XP';
    }
    
    // Show/hide level up button
    const levelUpContainer = document.getElementById('level-up-container');
    if (levelUpBtn && levelUpContainer) {
        if (currentXP >= nextLevelXP && characterLevel < 20) {
            levelUpContainer.style.display = 'block';
            levelUpBtn.disabled = false;
        } else {
            levelUpContainer.style.display = 'none';
            levelUpBtn.disabled = true;
        }
    }
}

// Initialize HP tracking
function initHPTracking() {
    const hpMaximum = document.getElementById('hp-maximum');
    const hpCurrent = document.getElementById('hp-current');
    const hpTemporary = document.getElementById('hp-temporary');
    
    if (hpMaximum) hpMaximum.addEventListener('input', updateHPVisualBar);
    if (hpCurrent) hpCurrent.addEventListener('input', updateHPVisualBar);
    if (hpTemporary) hpTemporary.addEventListener('input', updateHPVisualBar);
    
    // Initial update
    updateHPVisualBar();
}

function updateHPVisualBar() {
    const hpMaximum = parseInt(document.getElementById('hp-maximum')?.value || '0');
    const hpCurrent = parseInt(document.getElementById('hp-current')?.value || '0');
    const hpTemporary = parseInt(document.getElementById('hp-temporary')?.value || '0');
    
    const barMaximum = document.getElementById('hp-bar-maximum');
    const barCurrent = document.getElementById('hp-bar-current');
    const barTemporary = document.getElementById('hp-bar-temporary');
    
    if (!barMaximum || !barCurrent || !barTemporary) return;
    
    // Calculate percentages based on maximum HP
    const maxHP = Math.max(hpMaximum, hpCurrent, hpTemporary);
    if (maxHP <= 0) {
        barMaximum.style.width = '0%';
        barCurrent.style.width = '0%';
        barTemporary.style.width = '0%';
        return;
    }
    
    const maxPercent = (hpMaximum / maxHP) * 100;
    const currentPercent = (hpCurrent / maxHP) * 100;
    const tempPercent = (hpTemporary / maxHP) * 100;
    
    // Update bar widths
    barMaximum.style.width = maxPercent + '%';
    barCurrent.style.width = Math.min(currentPercent, maxPercent) + '%';
    barTemporary.style.width = Math.min(tempPercent, maxPercent) + '%';
    
    // Update labels with actual values
    const labelMaximum = document.querySelector('.hp-label-maximum');
    const labelCurrent = document.querySelector('.hp-label-current');
    const labelTemporary = document.querySelector('.hp-label-temporary');
    
    if (labelMaximum) labelMaximum.textContent = `Maximum: ${hpMaximum}`;
    if (labelCurrent) labelCurrent.textContent = `Current: ${hpCurrent}`;
    if (labelTemporary) labelTemporary.textContent = `Temporary: ${hpTemporary}`;
}
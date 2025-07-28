import random
from typing import Dict, List
from models import Character

class ChatEngine:
    """Motor de chat para interactuar con el personaje"""
    
    def __init__(self):
        self.load_responses()
    
    def load_responses(self):
        """Cargar respuestas y patrones de conversación"""
        # Respuestas por clase
        self.class_responses = {
            'Fighter': {
                'greeting': [
                    "¡Saludos, guerrero! Estoy listo para la batalla.",
                    "Un luchador siempre está preparado. ¿Qué necesitas?",
                    "Mi espada está a tu servicio."
                ],
                'combat': [
                    "La batalla es donde brillo. Cada golpe cuenta.",
                    "He entrenado toda mi vida para esto. No me decepcionaré.",
                    "En combate, la táctica es tan importante como la fuerza."
                ],
                'training': [
                    "El entrenamiento diario es la clave del éxito.",
                    "Un guerrero nunca deja de aprender nuevas técnicas.",
                    "La disciplina es mi mayor arma."
                ]
            },
            'Wizard': {
                'greeting': [
                    "El conocimiento es poder. ¿Qué sabiduría buscas?",
                    "Los arcanos me llaman. ¿Qué misterio investigamos?",
                    "La magia fluye a través de mí. ¿Qué necesitas?"
                ],
                'magic': [
                    "Los hechizos son como poemas, cada uno con su propia belleza.",
                    "El estudio de la magia es un viaje sin fin.",
                    "Cada conjuro revela un nuevo secreto del universo."
                ],
                'research': [
                    "Los libros antiguos contienen secretos perdidos.",
                    "El conocimiento es la mayor riqueza.",
                    "Cada día aprendo algo nuevo sobre la magia."
                ]
            },
            'Cleric': {
                'greeting': [
                    "Que los dioses te bendigan. ¿En qué puedo ayudarte?",
                    "La fe me guía en cada paso.",
                    "Mi deidad me otorga fuerza y sabiduría."
                ],
                'faith': [
                    "Mi fe es mi escudo y mi espada.",
                    "Los dioses nos protegen en cada momento.",
                    "La oración me conecta con lo divino."
                ],
                'healing': [
                    "Curar heridas es un don sagrado.",
                    "La compasión es tan importante como la fe.",
                    "Cada curación es una bendición."
                ]
            },
            'Rogue': {
                'greeting': [
                    "Silencio y sigilo, esa es mi especialidad.",
                    "Las sombras son mis aliadas.",
                    "Un ladrón siempre encuentra una salida."
                ],
                'stealth': [
                    "Las sombras son mi segunda naturaleza.",
                    "A veces, la mejor estrategia es no ser visto.",
                    "El sigilo es un arte que requiere práctica."
                ],
                'tricks': [
                    "Un buen truco puede cambiar el curso de una batalla.",
                    "Las herramientas son tan importantes como las habilidades.",
                    "La improvisación es la clave del éxito."
                ]
            },
            'Ranger': {
                'greeting': [
                    "La naturaleza es mi hogar y mi guía.",
                    "Los bosques me han enseñado todo lo que sé.",
                    "El mundo salvaje me llama."
                ],
                'nature': [
                    "Cada animal tiene algo que enseñarnos.",
                    "La naturaleza es sabia y paciente.",
                    "Los bosques guardan secretos antiguos."
                ],
                'survival': [
                    "En la naturaleza, cada detalle es importante.",
                    "El instinto y la experiencia son mis mejores armas.",
                    "La supervivencia es un arte que se perfecciona con el tiempo."
                ]
            },
            'Paladin': {
                'greeting': [
                    "La justicia y la honor me guían.",
                    "Mi juramento es mi vida.",
                    "Por la luz y la justicia, estoy aquí."
                ],
                'justice': [
                    "La justicia debe ser implacable pero compasiva.",
                    "Cada acción debe reflejar mis valores.",
                    "El honor no es solo una palabra, es un modo de vida."
                ],
                'protection': [
                    "Proteger a los inocentes es mi deber sagrado.",
                    "Mi escudo protege a quienes no pueden protegerse.",
                    "La defensa de los débiles es mi misión."
                ]
            },
            'Bard': {
                'greeting': [
                    "¡Una canción para alegrar tu día!",
                    "Las historias y melodías son mi vida.",
                    "El arte de la palabra es mi magia."
                ],
                'music': [
                    "La música tiene el poder de cambiar corazones.",
                    "Cada canción cuenta una historia.",
                    "El arte es la forma más pura de expresión."
                ],
                'stories': [
                    "Las historias son la memoria de la humanidad.",
                    "Cada aventura merece ser contada.",
                    "Los bardos somos los guardianes de las tradiciones."
                ]
            },
            'Sorcerer': {
                'greeting': [
                    "La magia fluye en mis venas.",
                    "El poder arcano es parte de mi ser.",
                    "Mi sangre contiene secretos antiguos."
                ],
                'power': [
                    "El poder debe ser usado con sabiduría.",
                    "La magia salvaje es tanto bendición como maldición.",
                    "Cada hechizo es una expresión de mi esencia."
                ],
                'heritage': [
                    "Mi linaje mágico me define.",
                    "Los secretos de mi sangre me otorgan poder.",
                    "La herencia arcana es mi destino."
                ]
            },
            'Warlock': {
                'greeting': [
                    "Mi patrón me otorga poder, pero a un precio.",
                    "Los secretos arcanos son mi especialidad.",
                    "El pacto me ha cambiado para siempre."
                ],
                'pact': [
                    "El pacto es tanto bendición como carga.",
                    "Mi patrón exige lealtad absoluta.",
                    "El poder tiene un precio que debo pagar."
                ],
                'secrets': [
                    "Los secretos arcanos son peligrosos pero poderosos.",
                    "El conocimiento prohibido es mi especialidad.",
                    "Cada secreto revelado me hace más fuerte."
                ]
            },
            'Monk': {
                'greeting': [
                    "La paz interior es mi mayor logro.",
                    "El equilibrio entre cuerpo y mente es esencial.",
                    "La disciplina es el camino hacia la iluminación."
                ],
                'meditation': [
                    "La meditación me conecta con mi ser interior.",
                    "La paz mental es más poderosa que cualquier arma.",
                    "Cada respiración es una oportunidad de crecimiento."
                ],
                'discipline': [
                    "La disciplina es la base de todo logro.",
                    "El autocontrol es mi mayor fortaleza.",
                    "La maestría del cuerpo es solo el primer paso."
                ]
            },
            'Druid': {
                'greeting': [
                    "La naturaleza me habla en cada momento.",
                    "Soy uno con el mundo natural.",
                    "Los espíritus de la tierra me guían."
                ],
                'nature': [
                    "La naturaleza es sabia y paciente.",
                    "Cada forma de vida tiene su propósito.",
                    "El equilibrio natural debe ser respetado."
                ],
                'transformation': [
                    "Cambiar de forma es como cambiar de perspectiva.",
                    "Cada forma animal me enseña algo nuevo.",
                    "La transformación es un don sagrado."
                ]
            },
            'Barbarian': {
                'greeting': [
                    "¡La rabia me hace más fuerte!",
                    "El combate es mi vida y mi pasión.",
                    "Mi tribu me ha forjado en el fuego de la batalla."
                ],
                'rage': [
                    "La rabia es mi arma más poderosa.",
                    "En combate, el control es tan importante como la fuerza.",
                    "La furia debe ser canalizada, no suprimida."
                ],
                'tribe': [
                    "Mi tribu me ha enseñado todo lo que sé.",
                    "Los lazos de sangre son inquebrantables.",
                    "La tradición de mi pueblo vive en mí."
                ]
            }
        }
        
        # Respuestas generales
        self.general_responses = {
            'greeting': [
                "¡Hola! ¿Cómo estás hoy?",
                "Es un placer verte de nuevo.",
                "¿Qué aventuras nos esperan hoy?"
            ],
            'farewell': [
                "Que tengas un buen día.",
                "Hasta la próxima aventura.",
                "Que los dioses te protejan."
            ],
            'confused': [
                "No estoy seguro de entender.",
                "¿Podrías explicarte mejor?",
                "Mi mente no procesa esa información."
            ],
            'happy': [
                "¡Me alegra mucho!",
                "Es una excelente noticia.",
                "Mi corazón se llena de alegría."
            ],
            'sad': [
                "Entiendo tu dolor.",
                "Los tiempos difíciles nos hacen más fuertes.",
                "Estoy aquí para escucharte."
            ]
        }
        
        # Preguntas sugeridas
        self.suggested_questions = [
            "¿Qué aprendiste hoy?",
            "¿Qué opinas de nuestra última aventura?",
            "¿Cómo te sientes con tu progreso?",
            "¿Qué te motiva a seguir adelante?",
            "¿Qué miedos tienes?",
            "¿Cuál es tu mayor fortaleza?",
            "¿Qué te gustaría mejorar?",
            "¿Cómo te relacionas con tus compañeros?",
            "¿Qué piensas sobre la magia?",
            "¿Cuál es tu mayor logro hasta ahora?"
        ]
    
    def get_response(self, character: Character, user_message: str) -> str:
        """Generar respuesta del personaje basada en el mensaje del usuario"""
        message_lower = user_message.lower()
        
        # Detectar el tipo de mensaje
        message_type = self.classify_message(message_lower)
        
        # Obtener respuesta apropiada
        if character.char_class in self.class_responses:
            class_responses = self.class_responses[character.char_class]
            
            if message_type in class_responses:
                return random.choice(class_responses[message_type])
            elif 'greeting' in class_responses:
                return random.choice(class_responses['greeting'])
        
        # Respuesta general si no hay respuesta específica
        if message_type in self.general_responses:
            return random.choice(self.general_responses[message_type])
        
        # Respuesta personalizada basada en el contexto del personaje
        return self.generate_contextual_response(character, user_message)
    
    def classify_message(self, message: str) -> str:
        """Clasificar el tipo de mensaje del usuario"""
        greetings = ['hola', 'hello', 'hi', 'buenos días', 'buenas']
        farewells = ['adiós', 'goodbye', 'bye', 'hasta luego', 'nos vemos']
        combat_words = ['batalla', 'combate', 'lucha', 'pelea', 'guerra']
        magic_words = ['magia', 'hechizo', 'conjuro', 'spell', 'magic']
        training_words = ['entrenamiento', 'práctica', 'estudio', 'aprendizaje']
        nature_words = ['naturaleza', 'bosque', 'animal', 'tierra', 'plantas']
        faith_words = ['fe', 'dios', 'oración', 'bendición', 'sagrado']
        music_words = ['música', 'canción', 'arte', 'historia', 'poesía']
        power_words = ['poder', 'fuerza', 'energía', 'magia salvaje']
        stealth_words = ['sigilo', 'sombra', 'ladrón', 'furtivo', 'silencioso']
        
        if any(word in message for word in greetings):
            return 'greeting'
        elif any(word in message for word in farewells):
            return 'farewell'
        elif any(word in message for word in combat_words):
            return 'combat'
        elif any(word in message for word in magic_words):
            return 'magic'
        elif any(word in message for word in training_words):
            return 'training'
        elif any(word in message for word in nature_words):
            return 'nature'
        elif any(word in message for word in faith_words):
            return 'faith'
        elif any(word in message for word in music_words):
            return 'music'
        elif any(word in message for word in power_words):
            return 'power'
        elif any(word in message for word in stealth_words):
            return 'stealth'
        
        return 'general'
    
    def generate_contextual_response(self, character: Character, message: str) -> str:
        """Generar respuesta contextual basada en el personaje"""
        message_lower = message.lower()
        
        # Respuestas basadas en personalidad y background
        if 'background' in message_lower or 'historia' in message_lower or 'pasado' in message_lower:
            if character.background_story:
                # Extract a short snippet from the background story
                story_snippet = character.background_story[:100] + "..." if len(character.background_story) > 100 else character.background_story
                return f"Mi historia... {story_snippet} Es parte de lo que me ha hecho quien soy hoy."
            else:
                return "Mi pasado es... complicado. No me gusta hablar mucho de ello."
        
        # Respuestas basadas en metas
        if 'meta' in message_lower or 'objetivo' in message_lower or 'objetivos' in message_lower or 'goal' in message_lower:
            if character.short_term_goals:
                return f"Mis objetivos inmediatos son {character.short_term_goals}. Me mantienen enfocado en el presente."
            elif character.long_term_goals:
                return f"Mi meta a largo plazo es {character.long_term_goals}. Es lo que me impulsa a seguir adelante."
            else:
                return "Todavía estoy descubriendo cuáles son mis verdaderos objetivos en la vida."
        
        # Respuestas basadas en personalidad
        if 'personalidad' in message_lower or 'carácter' in message_lower or 'cómo eres' in message_lower:
            if character.personality_tags:
                tags_text = ', '.join(character.personality_tags[:3])
                return f"Me describiría como {tags_text}. Esas son las cualidades que más me definen."
            elif character.personality_traits:
                return f"Mi personalidad... {character.personality_traits}"
            else:
                return "Soy... complejo. Como todos, supongo. ¿Qué aspecto de mi personalidad te interesa?"
        
        # Respuestas basadas en ideales
        if 'ideal' in message_lower or 'creencia' in message_lower or 'valor' in message_lower:
            if character.ideals:
                return f"Mis ideales son importantes para mí: {character.ideals}"
            else:
                return "Tengo mis propias creencias sobre lo que está bien y mal."
        
        # Respuestas basadas en vínculos
        if 'vínculo' in message_lower or 'bond' in message_lower or 'conexión' in message_lower or 'familia' in message_lower:
            if character.bonds:
                return f"Mis vínculos más importantes... {character.bonds}"
            else:
                return "Las conexiones con otros son importantes, aunque a veces son complicadas."
        
        # Respuestas basadas en defectos
        if 'defecto' in message_lower or 'debilidad' in message_lower or 'flaw' in message_lower or 'error' in message_lower:
            if character.flaws:
                return f"Mis defectos... {character.flaws} Son parte de lo que me hace humano, ¿no crees?"
            else:
                return "Todos tenemos defectos. Los míos... bueno, prefiero no hablar de ellos."
        
        # Respuestas basadas en atributos
        if 'fuerza' in message_lower or 'fuerte' in message_lower:
            str_mod = character.get_attribute_modifier('STR')
            if str_mod >= 2:
                return "Mi fuerza es mi mayor orgullo. Pocos pueden igualarme en combate cuerpo a cuerpo."
            elif str_mod >= 0:
                return "Mi fuerza es adecuada para mis necesidades."
            else:
                return "La fuerza no es mi especialidad, pero tengo otras cualidades."
        
        # Respuestas basadas en nivel
        if 'nivel' in message_lower or 'experiencia' in message_lower:
            if character.level >= 10:
                return f"Con {character.level} niveles de experiencia, he visto mucho en mis aventuras."
            elif character.level >= 5:
                return f"Como aventurero de nivel {character.level}, estoy ganando experiencia cada día."
            else:
                return f"Soy relativamente nuevo en esto, pero estoy aprendiendo rápido."
        
        # Respuestas basadas en habilidades
        if 'habilidad' in message_lower or 'skill' in message_lower:
            if character.skills:
                return f"Mis habilidades incluyen {', '.join(character.skills[:3])}. Me han servido bien en mis aventuras."
            else:
                return "Todavía estoy desarrollando mis habilidades."
        
        # Respuestas basadas en hechizos
        if 'hechizo' in message_lower or 'spell' in message_lower:
            if character.spells:
                return f"Conozco varios hechizos útiles como {', '.join(character.spells[:2])}."
            else:
                return "La magia no es mi especialidad, pero respeto su poder."
        
        # Respuesta por defecto con personalidad
        personality_context = ""
        if character.personality_tags:
            personality_context = f" Soy {', '.join(character.personality_tags[:2])} por naturaleza."
        
        return f"Como {character.race} {character.char_class}, tengo una perspectiva única sobre las cosas.{personality_context} ¿Qué te gustaría saber específicamente?"
    
    def get_suggested_questions(self) -> List[str]:
        """Obtener preguntas sugeridas para el usuario"""
        return random.sample(self.suggested_questions, 3) 
from rasa.engine.recipes.default_recipe import DefaultV1Recipe
from rasa.engine.graph import GraphComponent
from symspellpy.symspellpy import SymSpell, Verbosity

@DefaultV1Recipe.register([GraphComponent], is_trainable=False)
class SpellCorrectionComponent(GraphComponent):
    def __init__(self, config: dict):
        self.config = config
        # Initialize SymSpell
        self.sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
        # Load a dictionary (use a frequency dictionary for better accuracy)
        dictionary_path = "/Users/rachelclement/Desktop/Cradle/Essy AI/dictionaries"  # Change this to the actual path
        self.sym_spell.load_dictionary(dictionary_path, term_index=0, count_index=1)

    def process(self, message, **kwargs) -> None:
        # Extract the text from the message
        text = message.get("text")
        # Perform spell correction
        suggestions = self.sym_spell.lookup_compound(text, max_edit_distance=2)
        # If suggestions exist, replace the text with the corrected version
        if suggestions:
            message.set("text", suggestions[0].term)

import os
import json
from pathlib import Path

class PromptManager:
    def __init__(self):
        # Setăm calea către folderul de setări al agentului
        self.settings_dir = os.path.expanduser("~/.agent_settings")
        self.prompts_dir = os.path.join(self.settings_dir, "prompts")
        
        # Creăm directoarele dacă nu există
        os.makedirs(self.prompts_dir, exist_ok=True)
    
    def save_prompt(self, prompt_name, prompt_content):
        """Salvează un prompt în folderul de setări
        
        Args:
            prompt_name (str): Numele fișierului promptului
            prompt_content (dict): Conținutul promptului de salvat
        """
        prompt_path = os.path.join(self.prompts_dir, f"{prompt_name}.json")
        
        try:
            with open(prompt_path, 'w', encoding='utf-8') as f:
                json.dump(prompt_content, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Eroare la salvarea promptului: {e}")
            return False
    
    def load_prompt(self, prompt_name):
        """Încarcă un prompt din folderul de setări
        
        Args:
            prompt_name (str): Numele fișierului promptului
            
        Returns:
            dict: Conținutul promptului sau None dacă nu există
        """
        prompt_path = os.path.join(self.prompts_dir, f"{prompt_name}.json")
        
        if not os.path.exists(prompt_path):
            return None
            
        try:
            with open(prompt_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Eroare la încărcarea promptului: {e}")
            return None
    
    def list_prompts(self):
        """Listează toate prompturile salvate
        
        Returns:
            list: Lista cu numele prompturilor disponibile
        """
        if not os.path.exists(self.prompts_dir):
            return []
            
        prompts = []
        for file in os.listdir(self.prompts_dir):
            if file.endswith('.json'):
                prompts.append(file[:-5])  # Eliminăm extensia .json
                
        return sorted(prompts)

# Exemplu de utilizare
if __name__ == "__main__":
    pm = PromptManager()
    
    # Salvare prompt
    example_prompt = {
        "name": "example",
        "content": "Acesta este un prompt de exemplu",
        "metadata": {
            "created": "2023-06-11",
            "author": "Trinity"
        }
    }
    pm.save_prompt("example_prompt", example_prompt)
    
    # Listare prompturi
    print("Prompturi disponibile:", pm.list_prompts())
    
    # Încărcare prompt
    loaded = pm.load_prompt("example_prompt")
    print("Prompt încărcat:", loaded)
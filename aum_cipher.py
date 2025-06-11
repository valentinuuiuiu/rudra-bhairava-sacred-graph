from cryptography.fernet import Fernet
from mantras import generate_seed_from_mantra, validate_mantra_purity
import base64
from typing import Optional

class AumCipher:
    """Sacred encryption system using mantra-derived keys with 108-fold transformation"""
    
    def __init__(self, mantra: str = "Om Namah Shivaya"):
        if not validate_mantra_purity(mantra):
            raise ValueError("Mantra contains non-sacred syllables")
        
        self.mantra = mantra
        self.seed = generate_seed_from_mantra(mantra)
        self.key = base64.urlsafe_b64encode(self.seed[:32])
        self.cipher = Fernet(self.key)
    
    def encrypt(self, plaintext: str) -> bytes:
        """Encrypt sacred knowledge with mantra power"""
        return self.cipher.encrypt(plaintext.encode())
    
    def decrypt(self, ciphertext: bytes) -> str:
        """Decrypt with same mantra vibration"""
        return self.cipher.decrypt(ciphertext).decode()
    
    def rotate_mantra(self, new_mantra: str) -> None:
        """Perform sacred key rotation ceremony"""
        if not validate_mantra_purity(new_mantra):
            raise ValueError("New mantra lacks sacred purity")
        self.__init__(new_mantra)

class TantricAccess:
    """Spiritual access control based on enlightenment levels"""
    
    ENLIGHTENMENT_LEVELS = {
        'sadhu': 1,
        'siddha': 2, 
        'avadhuta': 3
    }
    
    def __init__(self, user_level: str = 'sadhu'):
        self.level = self.ENLIGHTENMENT_LEVELS.get(user_level.lower(), 0)
    
    def check_access(self, required_level: str) -> bool:
        """Verify user has sufficient spiritual attainment"""
        return self.level >= self.ENLIGHTENMENT_LEVELS.get(required_level.lower(), 0)
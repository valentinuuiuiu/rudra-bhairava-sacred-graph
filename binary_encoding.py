"""
Chanda Shastra Binary Encoding System for Rudra Bhairava Graph
Implements Vedic binary encoding patterns for agent nodes
"""

class ChandaShastraEncoder:
    """
    Implements the Vedic binary encoding system based on Chanda Shastra metrics
    """
    
    # Core node mappings (10 nodes total)
    NODE_MAPPINGS = {
        'user': 0b00000001,
        'rudra_agent': 0b00000010,
        'bhairava_agent': 0b00000100,
        'vedic_math_agent': 0b00001000,
        'tantra_agent': 0b00010000,
        'jyotish_agent': 0b00100000,
        'mantra_agent': 0b01000000,
        'yantra_agent': 0b10000000,
        'integration_agent': 0b11000000,
        'orchestrator': 0b11100000
    }

    @staticmethod
    def encode_node(node_name: str) -> int:
        """
        Encodes a node name into its binary representation
        Args:
            node_name: Name of the node to encode
        Returns:
            Binary encoded value (int)
        Raises:
            ValueError: If node name is not recognized
        """
        if node_name not in ChandaShastraEncoder.NODE_MAPPINGS:
            raise ValueError(f"Unknown node: {node_name}")
        return ChandaShastraEncoder.NODE_MAPPINGS[node_name]

    @staticmethod
    def decode_node(binary_value: int) -> str:
        """
        Decodes a binary value back to node name
        Args:
            binary_value: Encoded binary value
        Returns:
            Original node name
        Raises:
            ValueError: If binary value doesn't match any node
        """
        for name, val in ChandaShastraEncoder.NODE_MAPPINGS.items():
            if val == binary_value:
                return name
        raise ValueError(f"Invalid binary value: {bin(binary_value)}")

    @staticmethod
    def validate_encoding(binary_value: int) -> bool:
        """
        Validates if binary encoding follows Chanda Shastra rules
        Args:
            binary_value: Value to validate
        Returns:
            True if valid, False otherwise
        """
        return binary_value in ChandaShastraEncoder.NODE_MAPPINGS.values()


# Example usage
if __name__ == "__main__":
    print("Testing Chanda Shastra Encoding:")
    test_node = "rudra_agent"
    encoded = ChandaShastraEncoder.encode_node(test_node)
    decoded = ChandaShastraEncoder.decode_node(encoded)
    print(f"Node: {test_node} → Encoded: {bin(encoded)} → Decoded: {decoded}")
    print(f"Validation: {ChandaShastraEncoder.validate_encoding(encoded)}")
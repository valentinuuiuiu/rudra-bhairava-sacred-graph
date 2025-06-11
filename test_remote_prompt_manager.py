import asyncio
from agent_settings.remote_prompt_manager import RemotePromptManager

async def test_remote_prompt_manager():
    # Initialize with test MCP server URL (adjust as needed)
    manager = RemotePromptManager(
        mcp_server_url="http://localhost:8000",
        auth_token="test_token"
    )
    
    print("\n=== Testing Connection ===")
    is_connected = await manager.test_connection()
    print(f"Connection test: {'SUCCESS' if is_connected else 'FAILED'}")
    
    print("\n=== Testing Prompt Management ===")
    test_prompt = {
        "name": "test_prompt",
        "instructions": "Test instructions",
        "examples": ["example1", "example2"]
    }
    
    # Test saving prompt
    save_result = await manager.save_prompt("test_prompt", test_prompt)
    print(f"Save prompt: {'SUCCESS' if save_result else 'FAILED'}")
    
    # Test loading prompt
    loaded_prompt = await manager.load_prompt("test_prompt")
    print(f"Load prompt: {'SUCCESS' if loaded_prompt else 'FAILED'}")
    if loaded_prompt:
        print(f"Prompt content: {loaded_prompt}")
    
    # Test listing prompts
    prompts = await manager.list_prompts()
    print(f"Available prompts: {prompts}")
    
    print("\n=== Testing Web Content Fetching ===")
    test_urls = [
        "https://example.com",  # Should work
        "https://invalid.url.that.does.not.exist",  # Should fail
        "https://google.com"  # Should work but may be truncated
    ]
    
    for url in test_urls:
        print(f"\nFetching: {url}")
        content = await manager.fetch_web_content(url)
        if content:
            print(f"Success! Content length: {len(content)}")
            print(f"First 100 chars: {content[:100]}...")
        else:
            print("Failed to fetch content")

if __name__ == "__main__":
    asyncio.run(test_remote_prompt_manager())
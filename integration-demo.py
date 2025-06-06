"""
Integration example: Using the Advertising Helper Agent with the Django app
This shows how the Django marketplace can integrate with our MCP advertising tools.
"""

import json
import httpx
import asyncio
from pathlib import Path

# Sample data that would come from the Django marketplace
SAMPLE_LISTINGS = [
    {
        "id": 1,
        "title": "Apartament 2 camere",
        "category": "imobiliare",
        "location": "București",
        "price": 85000,
        "condition": "nou",
        "description": "Apartament nou în zona centrală"
    },
    {
        "id": 2, 
        "title": "iPhone 13",
        "category": "electronice",
        "location": "Cluj-Napoca",
        "price": 2500,
        "condition": "foarte bună",
        "description": "Telefon în stare perfectă"
    },
    {
        "id": 3,
        "title": "Volkswagen Golf",
        "category": "auto", 
        "location": "Timișoara",
        "price": 15000,
        "condition": "bună",
        "description": "Mașină cu service la zi"
    }
]

async def process_listing_with_advertising_helper(listing):
    """
    Process a listing using the advertising helper tools.
    In a real implementation, this would call the MCP server.
    """
    
    print(f"\n🎯 Processing listing: {listing['title']}")
    print("-" * 50)
    
    # Simulate title optimization
    print("📝 Optimized title suggestions:")
    if listing['category'] == 'imobiliare':
        suggestions = [
            f"🏠 {listing['title']} {listing['location']} - Zonă premium",
            f"✨ {listing['title']} nou - {listing['location']}",
            f"🔑 {listing['title']} modern - Vezi detalii"
        ]
    elif listing['category'] == 'auto':
        suggestions = [
            f"🚗 {listing['title']} - Stare {listing['condition']}",
            f"🔥 {listing['title']} urgent - {listing['location']}",
            f"💎 {listing['title']} service la zi"
        ]
    else:
        suggestions = [
            f"📱 {listing['title']} - {listing['condition']}",
            f"✨ {listing['title']} premium",
            f"🔥 {listing['title']} - Ofertă specială"
        ]
    
    for i, suggestion in enumerate(suggestions, 1):
        print(f"  {i}. {suggestion}")
    
    # Simulate pricing strategy
    print(f"\n💰 Pricing analysis for {listing['price']} RON:")
    
    # Simple pricing logic based on category and condition
    condition_multipliers = {
        "nou": 1.0,
        "foarte bună": 0.85,
        "bună": 0.70
    }
    
    multiplier = condition_multipliers.get(listing['condition'], 0.8)
    base_price = listing['price']
    
    strategies = [
        ("Premium pricing", int(base_price * 1.1)),
        ("Competitive pricing", int(base_price)),
        ("Quick sale", int(base_price * 0.9))
    ]
    
    for strategy, price in strategies:
        print(f"  • {strategy}: {price:,} RON")
    
    # Simulate social media content
    print(f"\n📱 Social media content:")
    
    facebook_post = f"""🔥 {listing['title']} - {listing['location']}

💰 {listing['price']:,} RON
📍 {listing['location']}
✨ {listing['description']}

👉 Contactează-mă pentru detalii
📞 Răspuns rapid garantat

#{listing['category'].lower()} #{listing['location'].lower().replace('-', '').replace(' ', '')} #romania #calitate"""
    
    print("Facebook post preview:")
    print(facebook_post[:150] + "...")
    
    # Simulate posting schedule
    print(f"\n⏰ Best posting times for {listing['category']}:")
    
    schedules = {
        "imobiliare": "Joi-Duminică, 18:00-20:00 (vizionări weekend)",
        "auto": "Sâmbătă-Duminică, 10:00-12:00 (test drive weekend)",
        "electronice": "Luni-Miercuri, 19:00-21:00 (după program)"
    }
    
    schedule = schedules.get(listing['category'], "Standard business hours")
    print(f"  📅 {schedule}")
    
    return {
        "listing_id": listing['id'],
        "optimized_title": suggestions[0],
        "recommended_price": strategies[1][1],
        "social_content": facebook_post,
        "best_posting_time": schedule
    }

async def main():
    """Main integration demo"""
    
    print("🚀 Piața.ro + Advertising Helper Integration Demo")
    print("=" * 60)
    
    print("\n📊 Processing marketplace listings with AI advertising assistance...")
    
    # Process all sample listings
    results = []
    for listing in SAMPLE_LISTINGS:
        result = await process_listing_with_advertising_helper(listing)
        results.append(result)
    
    # Summary
    print("\n" + "=" * 60)
    print("📈 Integration Summary")
    print("-" * 25)
    
    print(f"✅ Processed {len(results)} listings")
    print("🎯 Features demonstrated:")
    print("   • Title optimization with emoji and keywords")
    print("   • Dynamic pricing strategies")
    print("   • Social media content generation")
    print("   • Category-specific posting schedules")
    print("   • Romanian marketplace best practices")
    
    print("\n🔗 Integration Benefits:")
    print("   • Automated listing optimization")
    print("   • Increased visibility and engagement")
    print("   • Data-driven pricing recommendations")
    print("   • Multi-platform content generation")
    print("   • Cultural and behavioral insights")
    
    print("\n📋 Next Steps:")
    print("   1. Start the MCP server: ./start-advertising-agent.sh")
    print("   2. Integrate MCP calls into Django views")
    print("   3. Add advertising dashboard to admin panel")
    print("   4. Set up automated A/B testing")
    print("   5. Monitor performance metrics")
    
    print("\n🎯 The advertising helper agent is ready to boost your marketplace!")

if __name__ == "__main__":
    asyncio.run(main())

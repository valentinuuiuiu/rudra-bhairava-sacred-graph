"""
Advertising Helper MCP Server for Piata.ro Project
A Model Context Protocol server that provides specialized tools for Romanian marketplace advertising, 
marketing optimization, and seller assistance.
"""

import os
import asyncio
import json
import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from pathlib import Path
import random

from fastmcp import FastMCP
from pydantic import BaseModel
import sqlite3
import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Load environment variables
load_dotenv()

# Initialize FastMCP server for advertising helper
mcp = FastMCP("Piața.ro Advertising Helper Agent")

# Create FastAPI app for REST endpoints
rest_app = FastAPI(title="Piața.ro Advertising Helper API")

# Add CORS middleware
rest_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic models for data validation
class ListingData(BaseModel):
    title: str
    description: str
    price: float
    category: str
    location: str
    contact_info: str

class SearchQuery(BaseModel):
    query: str
    category: Optional[str] = None
    location: Optional[str] = None
    max_price: Optional[float] = None
    min_price: Optional[float] = None

# Database connection helper
def get_db_connection():
    """Get SQLite database connection"""
    db_path = os.getenv('DATABASE_PATH', 'db.sqlite3')
    return sqlite3.connect(db_path)

# Health check endpoint
@mcp.tool()
def health_check() -> str:
    """Health check endpoint for monitoring"""
    return json.dumps({
        "status": "healthy", 
        "timestamp": datetime.now().isoformat(),
        "service": "advertising-agent"
    })

# Romanian marketplace categories for advertising optimization
ROMANIAN_CATEGORIES = {
    "imobiliare": ["apartament", "casă", "teren", "comercial", "închiriere"],
    "auto": ["mașină", "motocicletă", "piese auto", "service auto"],
    "electronice": ["telefon", "laptop", "televizor", "console", "audio"],
    "casa_gradina": ["mobilă", "electrocasnice", "grădină", "decorațiuni"],
    "fashion": ["îmbrăcăminte", "pantofi", "accesorii", "bijuterii"],
    "locuri_munca": ["full-time", "part-time", "freelance", "stagii"],
    "servicii": ["reparații", "construcții", "curățenie", "transport"],
    "animale": ["câini", "pisici", "accesorii animale", "hrană animale"],
    "hobby_sport": ["fitness", "biciclete", "camping", "instrumente muzicale"],
    "copii_bebelusi": ["jucării", "haine copii", "cărucior", "pătuț"]
}

# Romanian cities for location targeting
MAJOR_ROMANIAN_CITIES = [
    "București", "Cluj-Napoca", "Timișoara", "Iași", "Constanța", 
    "Craiova", "Brașov", "Galați", "Ploiești", "Oradea"
]

# Advertising keywords in Romanian
ADVERTISING_KEYWORDS = {
    "urgency": ["urgent", "rapid", "astăzi", "imediat", "limitată"],
    "quality": ["calitate", "premium", "profesional", "garantat", "verificat"],
    "price": ["preț mic", "ofertă", "reducere", "promoție", "avantajos"],
    "location": ["zonă centrală", "aproape de", "acces ușor", "transport"]
}

@mcp.tool()
def optimize_listing_title(title: str, category: str, location: str) -> Dict[str, Any]:
    """
    Optimize a listing title for better visibility and engagement in Romanian marketplace.
    
    Args:
        title: Original listing title
        category: Product/service category
        location: Location of the listing
    
    Returns:
        Optimized title suggestions with SEO improvements
    """
    try:
        suggestions = []
        original_title = title.strip()
        
        # Add location if not present
        if location and location not in original_title:
            suggestions.append(f"{original_title} - {location}")
        
        # Add category-specific keywords
        if category.lower() in ROMANIAN_CATEGORIES:
            keywords = ROMANIAN_CATEGORIES[category.lower()]
            for keyword in keywords[:2]:  # Use first 2 relevant keywords
                if keyword not in original_title.lower():
                    suggestions.append(f"{original_title} {keyword}")
        
        # Add urgency/quality keywords
        quality_words = ADVERTISING_KEYWORDS["quality"]
        urgency_words = ADVERTISING_KEYWORDS["urgency"]
        
        suggestions.append(f"{original_title} - Calitate Garantată")
        suggestions.append(f"🔥 {original_title} - Ofertă Limitată")
        suggestions.append(f"✨ {original_title} Premium")
        
        # SEO optimized version
        seo_title = f"{original_title} {category} {location}".replace("  ", " ").strip()
        suggestions.append(seo_title)
        
        return {
            "original_title": original_title,
            "optimized_suggestions": suggestions[:5],
            "tips": [
                "Folosește emoji pentru a atrage atenția (🔥✨💎)",
                "Include cuvinte cheie din categoria produsului",
                "Menționează localitatea pentru căutări locale",
                "Păstrează titlul sub 60 de caractere pentru SEO"
            ]
        }
        
    except Exception as e:
        return {"error": f"Title optimization error: {str(e)}"}

@mcp.tool()
def generate_description_template(category: str, product_type: str, selling_points: List[str]) -> Dict[str, Any]:
    """
    Generate professional description template for Romanian marketplace listings.
    
    Args:
        category: Product category
        product_type: Specific product type
        selling_points: List of key selling points
    
    Returns:
        Professional description template with Romanian marketplace best practices
    """
    try:
        templates = {
            "imobiliare": f"""
🏠 **{product_type} de Vânzare/Închiriere**

📍 **Locație**: [Adaugă zona exactă]
📐 **Suprafață**: [mp]
🏗️ **An construcție**: [anul]

✨ **Caracteristici principale**:
{chr(10).join([f"• {point}" for point in selling_points])}

💰 **Preț**: [sumă] RON {'(negociabil)' if 'negociabil' in str(selling_points).lower() else ''}

📞 **Contact**: [telefon/email]
⏰ **Program vizionări**: Luni-Vineri 9-18

#imobiliare #{category.lower()} #bucuresti #vanzare
            """,
            
            "auto": f"""
🚗 **{product_type} - Stare Impecabilă**

🔧 **Specificații tehnice**:
{chr(10).join([f"• {point}" for point in selling_points])}

✅ **Avantaje**:
• ITP valabil
• Service la zi
• Istoric complet
• Fără accidente

💰 **Preț**: [sumă] RON
🔄 **Schimb posibil**: [Da/Nu]

📞 **Contact direct**: [telefon]
📍 **Locație**: [oraș]

#auto #masina #{category.lower()} #piatauto
            """,
            
            "default": f"""
🌟 **{product_type} Premium**

📋 **Descriere**:
{chr(10).join([f"• {point}" for point in selling_points])}

✨ **De ce să alegi acest produs**:
• Calitate garantată
• Preț competitiv
• Livrare rapidă
• Garanție

💰 **Preț**: [sumă] RON
🚚 **Livrare**: [detalii transport]
📞 **Contact**: [telefon/email]

#{category.lower()} #calitate #oferta
            """
        }
        
        template = templates.get(category.lower(), templates["default"])
        
        return {
            "template": template.strip(),
            "seo_tips": [
                "Folosește hashtag-uri relevante la sfârșit",
                "Include cuvinte cheie în primele 2 rânduri",
                "Adaugă emoji pentru vizibilitate",
                "Menționează garanția/calitatea",
                "Include informații de contact clare"
            ],
            "engagement_boosters": [
                "🔥 Ofertă limitată",
                "✨ Calitate premium", 
                "📞 Răspuns rapid",
                "🚚 Livrare gratuită",
                "💎 Stare impecabilă"
            ]
        }
        
    except Exception as e:
        return {"error": f"Template generation error: {str(e)}"}

@mcp.tool()
def suggest_pricing_strategy(category: str, product_condition: str, market_price: float) -> Dict[str, Any]:
    """
    Suggest optimal pricing strategy for Romanian marketplace based on category and condition.
    
    Args:
        category: Product category
        product_condition: Condition (nou/folosit/deteriorat)
        market_price: Current market price reference
    
    Returns:
        Pricing recommendations and strategies
    """
    try:
        condition_multipliers = {
            "nou": 1.0,
            "ca nou": 0.85,
            "foarte bună": 0.75,
            "bună": 0.65,
            "acceptabilă": 0.45,
            "pentru piese": 0.25
        }
        
        base_multiplier = condition_multipliers.get(product_condition.lower(), 0.7)
        
        # Category-specific adjustments
        category_adjustments = {
            "electronice": -0.1,  # Electronics depreciate faster
            "auto": -0.05,        # Cars hold value better
            "imobiliare": 0.0,    # Real estate stable
            "fashion": -0.15,     # Fashion depreciates quickly
            "mobilă": -0.08       # Furniture moderate depreciation
        }
        
        adjustment = category_adjustments.get(category.lower(), 0)
        final_multiplier = max(0.2, base_multiplier + adjustment)
        
        recommended_price = market_price * final_multiplier
        
        pricing_strategies = [
            {
                "strategy": "Preț fix premium",
                "price": round(recommended_price * 1.1, -1),
                "description": "Pentru produse de calitate superioară"
            },
            {
                "strategy": "Preț competitiv",
                "price": round(recommended_price, -1),
                "description": "Echilibru între profit și vânzare rapidă"
            },
            {
                "strategy": "Vânzare rapidă",
                "price": round(recommended_price * 0.9, -1),
                "description": "Pentru vânzare în maximum 1 săptămână"
            }
        ]
        
        return {
            "recommended_price": round(recommended_price, -1),
            "price_range": {
                "min": round(recommended_price * 0.85, -1),
                "max": round(recommended_price * 1.15, -1)
            },
            "strategies": pricing_strategies,
            "tips": [
                f"Pentru {category}, prețurile variază cu {abs(adjustment)*100:.0f}% față de media pieței",
                "Lasă marge de negociere de 10-15%",
                "Monitorizează concurența săptămânal",
                "Consideră oferte în lot pentru discount"
            ]
        }
        
    except Exception as e:
        return {"error": f"Pricing strategy error: {str(e)}"}

@mcp.tool()
def generate_promotional_content(listing_title: str, category: str, special_offer: str = "") -> Dict[str, Any]:
    """
    Generate promotional content for social media and advertising campaigns.
    
    Args:
        listing_title: Title of the listing
        category: Product category
        special_offer: Any special offer or discount
    
    Returns:
        Ready-to-use promotional content for various platforms
    """
    try:
        base_content = {
            "facebook_post": f"""
🔥 OFERTĂ SPECIALĂ! 🔥

{listing_title}

{special_offer if special_offer else '✨ Calitate garantată la preț avantajos!'}

👉 Vezi detalii pe Piata.ro
📞 Contact direct pentru informații

#{category.lower()} #romania #piata #oferta #calitate
            """,
            
            "instagram_story": f"""
🌟 {listing_title}

{special_offer if special_offer else '💎 Produsul tău perfect te așteaptă!'}

📲 Swipe up pentru detalii
💬 DM pentru întrebări

#{category} #Shopping #Romania
            """,
            
            "whatsapp_message": f"""
Salut! 👋

Am văzut că te-ar putea interesa:
*{listing_title}*

{special_offer if special_offer else 'Produsul este în stare excelentă și la un preț foarte bun.'}

Îți pot trimite poze și detalii complete.
Când ai timp să vorbim? 📞
            """,
            
            "email_template": f"""
Subiect: {listing_title} - Ofertă specială pentru tine

Salut,

Îți scriu în legătură cu {listing_title}.

{special_offer if special_offer else 'Am acest produs de calitate la un preț foarte avantajos.'}

Detalii complete:
- [Adaugă specificații]
- [Adaugă fotografii]
- [Adaugă preț și condiții]

Pentru întrebări sau programarea unei întâlniri, te rog să mă contactezi.

Cu stimă,
[Numele tău]
[Telefon]
            """
        }
        
        return {
            "promotional_content": base_content,
            "hashtags_by_platform": {
                "facebook": f"#{category.lower()} #romania #piata #vanzare #calitate",
                "instagram": f"#{category} #Romania #Shopping #Sale #Quality #Piata",
                "tiktok": f"#{category}RO #PiataRomania #Shopping #Oferta"
            },
            "engagement_tips": [
                "Postează în intervalul 18:00-21:00 pentru engagement maxim",
                "Folosește întrebări pentru a genera comentarii",
                "Răspunde rapid la mesaje și comentarii",
                "Adaugă povești personale despre produs"
            ]
        }
        
    except Exception as e:
        return {"error": f"Promotional content error: {str(e)}"}

@mcp.tool()
def analyze_competitor_pricing(category: str, location: str, product_keywords: List[str]) -> Dict[str, Any]:
    """
    Analyze competitor pricing and market trends for better positioning.
    
    Args:
        category: Product category
        location: Geographic location
        product_keywords: Keywords describing the product
    
    Returns:
        Market analysis and competitive pricing insights
    """
    try:
        # Simulated market data (in real implementation, this would connect to actual APIs)
        market_data = {
            "auto": {"avg_price": 15000, "listings_count": 1250, "trend": "stable"},
            "imobiliare": {"avg_price": 85000, "listings_count": 890, "trend": "rising"},
            "electronice": {"avg_price": 1200, "listings_count": 2100, "trend": "declining"},
            "mobilă": {"avg_price": 800, "listings_count": 650, "trend": "stable"}
        }
        
        base_data = market_data.get(category.lower(), {"avg_price": 500, "listings_count": 100, "trend": "stable"})
        
        # Location-based price adjustments
        city_multipliers = {
            "București": 1.2,
            "Cluj-Napoca": 1.15,
            "Timișoara": 1.1,
            "Iași": 1.05,
            "Constanța": 1.05
        }
        
        location_multiplier = city_multipliers.get(location, 1.0)
        adjusted_avg_price = base_data["avg_price"] * location_multiplier
        
        analysis = {
            "market_overview": {
                "average_price": round(adjusted_avg_price, -1),
                "total_listings": base_data["listings_count"],
                "trend": base_data["trend"],
                "location_factor": f"{(location_multiplier-1)*100:+.0f}%" if location_multiplier != 1 else "Standard"
            },
            "pricing_recommendations": {
                "competitive_price": round(adjusted_avg_price * 0.95, -1),
                "premium_price": round(adjusted_avg_price * 1.1, -1),
                "budget_price": round(adjusted_avg_price * 0.8, -1)
            },
            "market_insights": [
                f"În {location}, prețurile pentru {category} sunt {'mai mari' if location_multiplier > 1 else 'standard'} cu {abs((location_multiplier-1)*100):.0f}%",
                f"Trend de piață: {base_data['trend']} - {'recomandăm prudență în pricing' if base_data['trend'] == 'declining' else 'oportunitate bună de vânzare'}",
                f"Există {base_data['listings_count']} anunțuri similare - {'piață competitivă' if base_data['listings_count'] > 500 else 'piață cu oportunități'}"
            ],
            "competitive_advantages": [
                "Oferă garanție extinsă pentru diferențiere",
                "Include servicii de livrare gratuită",
                "Prezintă istoricul/documentația completă",
                "Organizează demonstrații/teste gratuite"
            ]
        }
        
        return analysis
        
    except Exception as e:
        return {"error": f"Competitor analysis error: {str(e)}"}

@mcp.tool()
def suggest_best_posting_times(category: str, target_audience: str) -> Dict[str, Any]:
    """
    Suggest optimal posting times for maximum visibility based on Romanian user behavior.
    
    Args:
        category: Product category
        target_audience: Target audience (tineri/adulti/familii/profesionisti)
    
    Returns:
        Optimal posting schedule and audience insights
    """
    try:
        # Romanian user behavior patterns
        audience_patterns = {
            "tineri": {
                "peak_hours": ["19:00-22:00", "12:00-14:00"],
                "peak_days": ["Vineri", "Sâmbătă", "Duminică"],
                "social_platforms": ["Instagram", "TikTok", "Facebook"]
            },
            "adulti": {
                "peak_hours": ["18:00-20:00", "07:00-09:00"],
                "peak_days": ["Marți", "Miercuri", "Joi"],
                "social_platforms": ["Facebook", "WhatsApp", "Email"]
            },
            "familii": {
                "peak_hours": ["20:00-22:00", "10:00-12:00"],
                "peak_days": ["Sâmbătă", "Duminică"],
                "social_platforms": ["Facebook", "WhatsApp"]
            },
            "profesionisti": {
                "peak_hours": ["07:00-09:00", "17:00-19:00"],
                "peak_days": ["Luni", "Marți", "Miercuri"],
                "social_platforms": ["LinkedIn", "Email", "Facebook"]
            }
        }
        
        category_adjustments = {
            "auto": "Weekend dimineața pentru test-drive",
            "imobiliare": "Joi-Duminică pentru vizionări",
            "electronice": "Seara după program și weekend",
            "servicii": "Luni-Miercuri pentru planificare",
            "fashion": "Joi-Sâmbătă pentru shopping weekend"
        }
        
        audience_data = audience_patterns.get(target_audience.lower(), audience_patterns["adulti"])
        
        schedule = {
            "optimal_posting_times": {
                "zilnic": audience_data["peak_hours"],
                "saptamanal": audience_data["peak_days"],
                "categorie_specifica": category_adjustments.get(category.lower(), "Standard business hours")
            },
            "platform_strategy": {
                "recommended_platforms": audience_data["social_platforms"],
                "posting_frequency": {
                    "Facebook": "1-2 posturi/zi",
                    "Instagram": "1 post + 2-3 stories/zi",
                    "TikTok": "3-5 posturi/săptămână",
                    "WhatsApp": "Direct messaging only"
                }
            },
            "content_calendar": {
                "Luni": "Produse noi + Start săptămână",
                "Marți": "Oferte speciale",
                "Miercuri": "Testimoniale + Reviews",
                "Joi": "Behind the scenes",
                "Vineri": "Weekend deals",
                "Sâmbătă": "Lifestyle content",
                "Duminică": "Recap săptămână + Preview"
            },
            "romanian_specific_tips": [
                "Evită postările în timpul meselor (12:00-14:00, 19:00-20:00)",
                "Weekend-ul este ideal pentru produse de lux/hobby",
                "Lunea dimineața este bună pentru servicii B2B",
                "Evită sărbătorile religioase majore",
                "Vara, postează mai devreme (18:00 vs 19:00)"
            ]
        }
        
        return schedule
        
    except Exception as e:
        return {"error": f"Posting schedule error: {str(e)}"}

@mcp.resource("advertising://templates")
def get_advertising_templates() -> str:
    """
    Resource that provides advertising templates and best practices for Romanian marketplace.
    """
    try:
        content = """
# 📈 Piața.ro Advertising Templates & Best Practices

## 🎯 Title Optimization Templates

### Imobiliare
- **Apartament 2 camere, zona centrală [Oraș] - Vedere deosebită**
- **🏠 Casă nouă [Orașe] - Grădină mare, finisaje premium**
- **🔑 Închirez apartament modern [Oraș] - Utilat complet**

### Auto
- **🚗 [Marca Model] [An] - Stare impecabilă, service la zi**
- **Mașină [Marca] [An] - [Km] km, proprietar unic**
- **🔥 [Model] urgent de vânzare - Preț negociabil**

### Electronice
- **📱 [Model] nou-nouț - Sigilat, garanție 2 ani**
- **💻 Laptop [Marca] - Perfect pentru birou/gaming**
- **📺 TV [Mărime] [Marca] - Smart TV, 4K HDR**

## 💡 Description Frameworks

### AIDA Framework (Attention-Interest-Desire-Action)
1. **Atenție**: Emoji + Beneficiul principal
2. **Interes**: Specificații tehnice + Puncte forte
3. **Dorință**: Testimoniale + Garanții
4. **Acțiune**: Call-to-action clar + Contact

### Problem-Solution-Benefit
1. **Problema**: Ce problemă rezolvă produsul
2. **Soluția**: Cum o rezolvă produsul tău
3. **Beneficiul**: Ce câștigi alegând produsul

## 🏷️ Pricing Psychology

### Preț ancoră
- Afișează prețul original ~~1000 RON~~
- Arată noul preț: **800 RON**
- Evidențiază economisirea: *Economisești 200 RON!*

### Preț psihologic
- Folosește 999 RON în loc de 1000 RON
- 1.999 RON pare mai mic decât 2.000 RON
- Subliniază valoarea: "Doar 50 RON/lună"

## 📱 Social Media Copy Templates

### Facebook Post
```
🌟 [TITLU PRODUS]

✨ [Beneficiul principal]
📍 [Locația]
💰 [Preț] RON

👉 Detalii în comentarii
📞 [Contact]

#[categorie] #[oraș] #romania #calitate
```

### Instagram Story
```
🔥 DEAL ALERT!

[Emoji] [Titlu scurt]
[Preț] RON

Swipe up 👆
sau DM pentru detalii

#[categoria] #Romania
```

## 🎯 Target Audience Messaging

### Pentru Tineri (18-30)
- Folosește limbaj casual și emoji
- Evidențiază trendul și style-ul
- Menționează compatibilitatea cu tehnologia
- "Perfect pentru lifestyle-ul tău activ"

### Pentru Familii (30-50)
- Subliniază siguranța și calitatea
- Menționează beneficiile pentru copii
- Evidențiază economisirea pe termen lung
- "Investiție sigură pentru familia ta"

### Pentru Seniori (50+)
- Limbaj formal și respectuos
- Evidențiază durabilitatea și fiabilitatea
- Menționează garanțiile și service-ul
- "Produs de încredere cu istoric dovedit"

## 📞 Contact & Call-to-Action Templates

### Urgență
- "Sună acum - doar 3 bucăți în stoc!"
- "Primul venit, primul servit"
- "Oferta se încheie duminică!"

### Încredere
- "Garanție de rambursare 30 zile"
- "Vezi produsul înainte să plătești"
- "Service autorizat inclus"

### Comoditate
- "Livrare gratuită în [oraș]"
- "Programare flexibilă - și în weekend"
- "Plată în rate fără dobândă"

## 🏆 Success Metrics

### Urmărește:
- **CTR (Click-Through Rate)**: >3% pentru anunțuri
- **Engagement Rate**: >5% pentru postări sociale
- **Conversion Rate**: >10% din vizualizări la contacte
- **Response Time**: <2ore pentru mesaje

### Optimizează pentru:
- Numărul de vizualizări unice
- Timpul petrecut pe anunț
- Numărul de contacte primite
- Rata de vânzare finală

---
*Actualizat: {datetime.now().strftime('%d.%m.%Y')}*
        """
        
        return content.strip()
        
    except Exception as e:
        return f"Error generating advertising templates: {str(e)}"

@mcp.resource("advertising://analytics")
def get_advertising_analytics() -> str:
    """
    Resource that provides advertising analytics and performance insights.
    """
    try:
        # Simulated analytics data
        analytics_data = f"""
# 📊 Advertising Analytics Dashboard

## 🎯 Current Performance (Last 30 Days)

### Top Performing Categories
1. **Imobiliare**: 45% of total conversions
2. **Auto**: 25% of total conversions  
3. **Electronice**: 20% of total conversions
4. **Servicii**: 10% of total conversions

### Geographic Performance
- **București**: 35% conversions, 28% traffic
- **Cluj-Napoca**: 15% conversions, 18% traffic
- **Timișoara**: 12% conversions, 15% traffic
- **Iași**: 10% conversions, 12% traffic

### Best Posting Times (Romanian Users)
- **Weekdays**: 18:00-20:00 (peak engagement)
- **Weekends**: 10:00-12:00 (browsing peak)
- **Tuesday**: Best day for B2B services
- **Saturday**: Best day for consumer products

### Price Performance Analysis
- **Under 100 RON**: 60% inquiry rate
- **100-1000 RON**: 35% inquiry rate
- **1000-10000 RON**: 20% inquiry rate
- **Over 10000 RON**: 10% inquiry rate

## 📈 Optimization Recommendations

### Title Optimization
- Use numbers: "5 reasons why..." (+40% engagement)
- Include location: "Available in București" (+25% local traffic)
- Add urgency: "Limited time offer" (+30% click-through)
- Use emoji: "🔥" or "✨ " (+15% visibility)

### Description Optimization
- First 50 characters are crucial for mobile
- Include 3-5 bullet points for key features
- End with clear call-to-action
- Use social proof when available

### Pricing Strategy
- Show original price with discount
- Use psychological pricing (999 vs 1000)
- Offer payment plans for expensive items
- Bundle complementary products

### Visual Content
- High-resolution photos increase inquiries by 80%
- Multiple angles boost conversion by 45%
- Video content gets 300% more engagement
- Lifestyle shots outperform product-only shots

## 🎯 A/B Testing Results

### Subject Lines
- ✅ "🔥 Special offer just for you" (12% open rate)
- ❌ "Product update newsletter" (3% open rate)

### Call-to-Actions
- ✅ "Contact me now" (25% click rate)
- ❌ "Get more information" (8% click rate)

### Posting Schedule
- ✅ Tuesday 19:00 (highest engagement)
- ❌ Monday 08:00 (lowest engagement)

---
*Data generated: {datetime.now().strftime('%d.%m.%Y %H:%M')}*
        """
        
        return analytics_data.strip()
        
    except Exception as e:
        return f"Error generating analytics: {str(e)}"

# REST API endpoints for tool calls
@rest_app.post("/call")
async def call_tool(request: dict):
    """REST endpoint to call MCP tools"""
    try:
        method = request.get("method")
        params = request.get("params", {})
        
        if method != "tools/call":
            raise HTTPException(status_code=400, detail="Only tools/call method supported")
        
        tool_name = params.get("name")
        tool_args = params.get("arguments", {})
        
        # Get the tool from MCP server and call it properly
        available_tools = await mcp.get_tools()
        
        if tool_name not in available_tools:
            raise HTTPException(status_code=400, detail=f"Unknown tool: {tool_name}")
        
        # Call the tool function directly (since they're decorated functions)
        tool_function = available_tools[tool_name].fn
        result = tool_function(**tool_args)
        
        return {
            "jsonrpc": "2.0",
            "id": request.get("id"),
            "result": result
        }
        
    except Exception as e:
        return {
            "jsonrpc": "2.0",
            "id": request.get("id"),
            "error": {
                "code": -1,
                "message": str(e)
            }
        }

@rest_app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy", "service": "advertising-agent"}

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Piața.ro Advertising Helper Agent')
    parser.add_argument('--port', type=int, default=8001, help='Port to run the MCP server on')
    parser.add_argument('--host', type=str, default='0.0.0.0', help='Host to bind the MCP server to')
    args = parser.parse_args()
    
    print(f"🚀 Starting Piața.ro Advertising Helper Agent on {args.host}:{args.port}")
    
    # Create a combined app that serves both MCP SSE and REST API
    from fastapi import FastAPI
    from fastapi.responses import StreamingResponse
    import threading
    
    # Mount the MCP server as SSE endpoint
    @rest_app.get("/sse")
    async def sse_endpoint():
        """SSE endpoint for MCP protocol"""
        # This would need proper SSE implementation
        return {"message": "SSE endpoint for MCP protocol"}
    
    # Run the REST API server
    uvicorn.run(rest_app, host=args.host, port=args.port)

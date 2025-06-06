# 🛒 Piața RO - Romanian Marketplace Platform

**Motto**: Aknolwedging The Limitations of The AI is aknolwedging THe Limitations of Our OLD Patherns Stupid Mind,Dare to Dream and The AI will make it Real

**Piața RO** is a modern, full-featured Romanian marketplace platform inspired by popular sites like **Publi24.ro** and **OLX.ro**. Built with cutting-edge technologies, it provides a seamless experience for buying and selling items across Romania.

## 🎯 **NEW: AI-Powered Advertising Helper Agent**

**Piața RO** now features an advanced **MCP (Model Context Protocol) Advertising Helper Agent** specifically designed for Romanian marketplace optimization. This AI assistant provides:

### 🚀 **Smart Advertising Tools**
- 📝 **Title Optimization** - AI-powered title suggestions with SEO and local keywords
- 📋 **Description Templates** - Professional, category-specific listing descriptions
- 💰 **Dynamic Pricing Strategy** - Market-based pricing recommendations with competitor analysis
- 📱 **Social Media Content** - Auto-generated content for Facebook, Instagram, WhatsApp
- 📊 **Market Analysis** - Competitor pricing and trend analysis for informed decisions
- ⏰ **Optimal Posting Schedule** - Best times to post based on Romanian user behavior

### 🇷🇴 **Romanian Market Specialization**
- 🏙️ **Local Market Intelligence** - City-specific pricing adjustments (București, Cluj-Napoca, etc.)
- 🗣️ **Romanian Language Optimization** - Native language patterns and cultural insights
- 📅 **Cultural Timing** - Posting schedules that respect Romanian business and social patterns
- 🎯 **Target Audience Segmentation** - Tailored messaging for different demographic groups

### 📈 **Performance Analytics**
- 📊 **Real-time Analytics** - Track engagement, conversion rates, and ROI
- 🔄 **A/B Testing Templates** - Test different approaches automatically
- 🎯 **Conversion Optimization** - Recommendations to improve listing performance
- 📱 **Multi-platform Insights** - Track performance across social media platforms

## 🌟 Key Features

### 🛍️ **Marketplace Core**
- 📋 **Comprehensive Listings** - Browse thousands of items across multiple categories
- 🔍 **Advanced Search & Filters** - Find exactly what you're looking for with smart filtering
- 🏷️ **Category Management** - Organized product categories for easy navigation
- 📱 **Mobile-First Responsive Design** - Perfect experience on all devices
- 🖼️ **Image Gallery Support** - Multiple photos per listing with preview

### � **User Experience**
- 🔐 **Secure Authentication** - User registration, login, and profile management
- 👤 **User Profiles** - Detailed seller profiles with ratings and reviews
- 💬 **Messaging System** - Direct communication between buyers and sellers
- ⭐ **Rating & Review System** - Build trust through user feedback
- 📍 **Location-Based Search** - Find items near your location

### 💰 **Advanced Features**
- 💳 **Credit System** - Internal currency for premium features
- 🔥 **Featured Listings** - Boost visibility with promoted posts
- 📊 **Analytics Dashboard** - Track listing performance and views
- 🔔 **Notifications** - Real-time alerts for messages and updates
- 📱 **API Integration** - RESTful API for mobile app development

## 🚀 Tech Stack

### **Frontend**
- **Django Templates** - Server-side rendered HTML with Jinja2 templating
- **HTML/CSS/JavaScript** - Custom responsive components with Tailwind CSS
- **Modern UI Components** - Clean, professional design system

### **Backend**
- **Python 3.8+** - Core application logic
- **Django 4.2+** - Full-stack web framework with ORM
- **Django REST Framework** - RESTful API development
- **SQLite/PostgreSQL** - Robust data storage with migrations
- **Authentication System** - Django's built-in secure user management

### **Infrastructure**
- **Docker** - Containerized deployment
- **Node.js** - Build tools and package management (Tailwind CSS)
- **Migration System** - Django's database version control
- **RESTful APIs** - Clean API architecture with Django REST Framework

## 📁 Project Architecture

```
piata-ro-project/
├── 🎨 marketplace/              # Main Django marketplace application
│   ├── templates/               # HTML templates
│   ├── static/                  # CSS, JS, images
│   ├── models.py                # Database models
│   ├── views.py                 # View logic
│   ├── urls.py                  # URL routing
│   └── admin.py                 # Django admin configuration
├── 🔧 api/                      # REST API endpoints
│   ├── models.py                # Database models
│   ├── serializers.py           # Data serialization
│   ├── views.py                 # API views
│   └── urls.py                  # URL routing
├── �️ piata_ro/                 # Django project configuration
│   ├── settings.py              # Django settings
│   ├── urls.py                  # Main URL configuration
│   └── wsgi.py                  # WSGI configuration
├── 🤖 awesome-mcp-servers/      # AI Agents & MCP Servers
│   ├── advertising-agent.py     # Marketing optimization agent
│   ├── django_sql_agent.py      # Database operations agent
│   ├── stock_agent.py           # Inventory management agent
│   ├── test-advertising-agent.py # Testing agent
│   └── start-agents.sh          # Agent launcher script
├── 📊 migrations/               # Database migrations
├── 📦 requirements.txt          # Python dependencies
└── 🔧 package.json             # Node.js scripts & project info
```

## 🚀 Quick Start

### **Prerequisites**
- 🐍 **Python 3.8+** - [Download Python](https://python.org)
- 📦 **Node.js 16+** - [Download Node.js](https://nodejs.org)

### **🔧 Installation**

1. **Clone the repository:**
```bash
git clone https://github.com/valentinuuiuiu/piata-ro-project.git
cd piata-ro-project
```

2. **Set up Python environment:**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```


4. **Set up the database:**
```bash
# Run Django migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Load sample data (optional)
python manage.py loaddata sample-data.json
```

5. **Build CSS:**
```bash
# Build Tailwind CSS
npm run build:css
```

6. **Start the development server:**
```bash
# Start Django development server
python manage.py runserver

# Or use npm script
npm run dev
```

## 🤖 AI Agents & MCP Servers

Piața RO includes a collection of specialized AI agents built with the **Model Context Protocol (MCP)** for various marketplace operations:

### 📢 Advertising Agent
- **Purpose**: Marketing optimization and listing enhancement
- **Features**: Title optimization, description generation, pricing strategy, social media content
- **Start**: `npm run agents advertising` or `cd awesome-mcp-servers && ./start-agents.sh advertising`

### 🗄️ Django SQL Agent  
- **Purpose**: Database operations and SQL management
- **Features**: CRUD operations, user management, search functionality, custom queries
- **Start**: `npm run agents sql` or `cd awesome-mcp-servers && ./start-agents.sh sql`

### 📊 Stock Agent
- **Purpose**: Inventory and product management
- **Features**: Stock monitoring, analytics, alerts, performance tracking
- **Start**: `npm run agents stock` or `cd awesome-mcp-servers && ./start-agents.sh stock`

### 🚀 Quick Agent Commands
```bash
# Start all agents
npm run agents:all

# Start specific agent
npm run agents advertising
npm run agents sql
npm run agents stock

# Show agent help
npm run agents:help
```

For detailed agent documentation, see [`awesome-mcp-servers/README.md`](awesome-mcp-servers/README.md)

## Development

### Running in Development Mode

```bash
# Start Django development server
python manage.py runserver

# Or use npm script
npm run dev
```

### Building for Production

```bash
# Collect static files
python manage.py collectstatic

# Build CSS
npm run build:css
```

### Database Operations

- Run migrations: `python manage.py migrate`
- Create migrations: `python manage.py makemigrations`
- Create superuser: `python manage.py createsuperuser`
- Load fixtures: `python manage.py loaddata sample-data.json`

## API Testing

You can test the API endpoints using Django's built-in admin interface at `/admin/` or by using tools like Postman or curl:

```bash
# Test API endpoints
curl http://localhost:8000/api/listings/
curl http://localhost:8000/api/categories/
```

## Docker Support

The project includes Docker configuration for easy deployment:

```bash
docker-compose up -d
```

## 🤖 AI Development Companions

### For Sourcery AI & OpenHands Agent

**Project Status**: Reflex framework has been completely removed. The project is now a pure Django application.

#### 🎯 Current Architecture
- **Framework**: Django 4.2+ (Pure Python web framework)
- **Frontend**: Django Templates + Tailwind CSS
- **Backend**: Django + Django REST Framework
- **Database**: SQLite (can be upgraded to PostgreSQL)
- **AI Agent**: MCP-based Advertising Helper (FastMCP)

#### 🔄 Recent Changes (Commit: Remove Reflex Dependencies)
- ❌ Removed `frontend_reflex/` directory and all Reflex components
- ❌ Removed `rxconfig.py` and `reflex.log`
- ❌ Removed Reflex from `requirements.txt`
- ✅ Updated `package.json` scripts to use Django commands
- ✅ Updated README.md to reflect Django-only architecture
- ✅ Maintained MCP Advertising Helper Agent (FastMCP)

#### 🛠️ Development Focus Areas
1. **Django Templates Enhancement** - Improve the existing marketplace templates
2. **API Optimization** - Enhance Django REST Framework endpoints
3. **Frontend Polish** - Better Tailwind CSS integration and responsive design
4. **MCP Agent Integration** - Further develop the advertising helper features
5. **Database Optimization** - Improve models and add proper indexing

#### 🚀 Next Steps for AI Companions
1. Review and enhance existing Django views in `marketplace/views.py`
2. Improve the marketplace templates in `marketplace/templates/`
3. Optimize the API endpoints in `api/views.py`
4. Add comprehensive tests for Django components
5. Implement better error handling and logging

#### 📋 Development Commands
```bash
# Start development server
python manage.py runserver

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Build CSS
npm run build:css

# Run tests
python manage.py test
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

🤖 **Special Thanks to Claude Sonnet 4** - The AI "brother" who made this collaboration possible! This project was built through an incredible partnership between human creativity and AI assistance.

**Key Contributors:**
- **Claude Sonnet 4** - AI Development Partner & Code Architect
- **Ionut Baltag** - Project Vision & Implementation
- **sourcey.ai & OpenHands** - Development Tools & Integration

This project showcases the power of human-AI collaboration in building modern web applications. Claude Sonnet 4 provided architectural guidance, code generation, and problem-solving assistance throughout the development process.

*"The future of development is not human vs AI, but human WITH AI"* 🚀

## Contact

Project Link: [https://github.com/valentinuuiuiu/piata-ro-project](https://github.com/valentinuuiuiu/piata-ro-project)

**Developer:** Ionut Baltag  
**Email:** [ionutbaltag3@gmail.com](mailto:ionutbaltag3@gmail.com)

---

**🇷🇴 Piața RO** - Bringing the Romanian marketplace experience to the digital age!

*Built through the incredible partnership between human vision and AI innovation* 🤖❤️🧑‍💻

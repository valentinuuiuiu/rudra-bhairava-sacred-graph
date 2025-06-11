# 🇷🇴 Piața RO - Modern Romanian Marketplace Platform

<div align="center">

![Django](https://img.shields.io/badge/Django-4.2+-092E20?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-3.0-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)

**A comprehensive, feature-rich marketplace platform built for the Romanian market**

[🚀 Live Demo](#) • [📚 Documentation](#documentation) • [🤝 Contributing](#contributing) • [🐛 Report Bug](https://github.com/valentinuuiuiu/piata-ro-project/issues)

</div>

---

## 📋 Table of Contents

- [🎯 Overview](#-overview)
- [✨ Key Features](#-key-features)
- [🤖 AI-Powered Features](#-ai-powered-features)
- [🛠️ Tech Stack](#️-tech-stack)
- [🏗️ Architecture](#️-architecture)
- [🚀 Quick Start](#-quick-start)
- [📱 Usage](#-usage)
- [🔧 Configuration](#-configuration)
- [🤖 MCP Agents](#-mcp-agents)
- [🧪 Testing](#-testing)
- [📦 Deployment](#-deployment)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)

---

## 🎯 Overview

**Piața RO** is a modern, full-featured marketplace platform specifically designed for the Romanian market. Built with Django and modern web technologies, it provides a seamless experience for buying and selling items across Romania, featuring AI-powered tools and comprehensive marketplace functionality.

### 🌟 Why Piața RO?

- **🇷🇴 Romanian-First**: Built specifically for Romanian users with local market intelligence
- **🤖 AI-Enhanced**: Integrated AI agents for listing optimization and market analysis
- **📱 Mobile-Ready**: Responsive design optimized for all devices
- **🔒 Secure**: Enterprise-grade security with Django's built-in protections
- **⚡ Fast**: Optimized performance with efficient database queries
- **🎨 Modern UI**: Clean, intuitive interface built with Tailwind CSS

---

## ✨ Key Features

### 🛍️ **Marketplace Core**
- **📋 Comprehensive Listings** - Browse thousands of items across multiple categories
- **🔍 Advanced Search & Filters** - Smart filtering with location, price, and category options
- **🏷️ Category Management** - Organized hierarchical categories for easy navigation
- **🖼️ Image Gallery** - Multiple photos per listing with lightbox preview
- **📍 Location Services** - GPS-based location detection and mapping
- **📱 Mobile-First Design** - Optimized responsive experience

### 👥 **User Management**
- **🔐 Secure Authentication** - Registration, login with Django's security
- **👤 User Profiles** - Detailed seller profiles with contact information
- **💬 Messaging System** - Direct communication between buyers and sellers
- **⭐ Rating & Reviews** - Trust building through user feedback
- **📞 Phone Display** - Secure phone number reveal functionality
- **❤️ Favorites** - Save and manage favorite listings

### 💰 **Advanced Features**
- **💳 Credit System** - Internal currency for premium features
- **🔥 Featured Listings** - Boost visibility with promoted posts
- **📊 Analytics Dashboard** - Track listing performance and views
- **🔔 Notifications** - Real-time alerts for messages and updates
- **🗺️ Interactive Maps** - Leaflet-powered location visualization
- **📱 RESTful API** - Complete API for mobile app development

---

## 🤖 AI-Powered Features

### 🚀 **MCP Advertising Helper Agent**

Our advanced **Model Context Protocol (MCP)** agent provides intelligent marketplace optimization:

#### 📝 **Content Optimization**
- **Smart Title Generation** - AI-powered title suggestions with SEO optimization
- **Description Templates** - Professional, category-specific listing descriptions
- **Keyword Integration** - Local Romanian keywords and search terms

#### 💰 **Market Intelligence**
- **Dynamic Pricing Strategy** - Market-based pricing recommendations
- **Competitor Analysis** - Real-time pricing and trend analysis
- **Local Market Data** - City-specific insights (București, Cluj-Napoca, etc.)

#### 📱 **Social Media Integration**
- **Auto-Generated Content** - Ready-to-post content for Facebook, Instagram, WhatsApp
- **Optimal Timing** - Best posting schedules based on Romanian user behavior
- **A/B Testing** - Automated testing for different listing approaches

---

## 🛠️ Tech Stack

<table>
<tr>
<td>

**Backend**
- Python 3.8+
- Django 4.2+
- Django REST Framework
- SQLite/PostgreSQL
- FastMCP (AI Agents)

</td>
<td>

**Frontend**
- Django Templates
- HTML5/CSS3/JavaScript
- Tailwind CSS 3.0
- Leaflet Maps
- Font Awesome Icons

</td>
<td>

**Tools & Infrastructure**
- Git Version Control
- Node.js (Build Tools)
- npm Package Manager
- Docker Support
- VS Code Integration

</td>
</tr>
</table>

---

## 🏗️ Architecture

```
piata-ro-project/
├── 🎨 marketplace/                 # Main Django application
│   ├── 📄 templates/              # HTML templates
│   │   ├── marketplace/
│   │   │   ├── base.html
│   │   │   ├── listing_detail.html
│   │   │   ├── listings.html
│   │   │   └── ...
│   ├── 🎯 static/                 # Static assets
│   ├── 📊 models.py               # Database models
│   ├── 🔧 views.py                # View logic
│   ├── 🛣️ urls.py                 # URL routing
│   ├── ⚙️ admin.py                # Admin interface
│   ├── 📋 forms.py                # Django forms
│   └── 🔗 signals.py              # Database signals
├── 🔌 api/                        # REST API endpoints
│   ├── 📊 models.py               # API models
│   ├── 🔄 serializers.py          # Data serialization
│   ├── 🎯 views.py                # API views
│   └── 🛣️ urls.py                 # API routing
├── ⚙️ piata_ro/                   # Project configuration
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── 🤖 awesome-mcp-servers/        # AI Agents
│   ├── advertising-agent.py       # Marketing optimization
│   ├── django_sql_agent.py        # Database operations
│   └── stock_agent.py             # Inventory management
├── 🗃️ migrations/                 # Database migrations
├── 📦 requirements.txt            # Python dependencies
└── 📄 package.json               # Node.js configuration
```

---

## 🚀 Quick Start

### Prerequisites

Make sure you have the following installed:
- 🐍 **Python 3.8+** - [Download](https://python.org)
- 📦 **Node.js 16+** - [Download](https://nodejs.org)
- 🔧 **Git** - [Download](https://git-scm.com)

### Installation

1. **📥 Clone the repository**
   ```bash
   git clone https://github.com/valentinuuiuiu/piata-ro-project.git
   cd piata-ro-project
   ```

2. **🐍 Set up Python environment**
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment
   source venv/bin/activate  # Linux/Mac
   # venv\Scripts\activate   # Windows
   
   # Install Python dependencies
   pip install -r requirements.txt
   ```

3. **🗃️ Set up the database**
   ```bash
   # Run database migrations
   python manage.py migrate
   
   # Create superuser (optional)
   python manage.py createsuperuser
   
   # Load sample data (optional)
   python add_sample_images.py
   ```

4. **🎨 Build frontend assets**
   ```bash
   # Install Node.js dependencies
   npm install
   
   # Build Tailwind CSS
   npm run build:css
   ```

5. **🚀 Start the development server**
   ```bash
   python manage.py runserver
   ```

6. **🌐 Open your browser**
   
   Navigate to `http://localhost:8000` to see your marketplace!

---

## 📱 Usage

### For Users

1. **🔐 Register/Login** - Create an account or sign in
2. **🏠 Browse Listings** - Explore items by category or search
3. **📍 Set Location** - Enable location services for nearby listings
4. **❤️ Save Favorites** - Add interesting items to your favorites
5. **💬 Contact Sellers** - Use the messaging system to communicate
6. **📞 Get Phone Numbers** - Click "Afișează telefon" to reveal contact info

### For Sellers

1. **➕ Add Listings** - Create detailed product listings
2. **📸 Upload Photos** - Add multiple high-quality images
3. **📍 Set Location** - Add precise location for better visibility
4. **💰 Set Pricing** - Use AI recommendations for competitive pricing
5. **📊 Track Performance** - Monitor views and engagement
6. **🔥 Promote Listings** - Use credits to feature your items

### Admin Features

- **👥 User Management** - Manage users and profiles
- **📋 Content Moderation** - Review and approve listings
- **📊 Analytics** - Monitor platform performance
- **💳 Credit Management** - Manage credit packages and transactions

---

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (optional - SQLite is default)
DATABASE_URL=sqlite:///db.sqlite3

# Stripe (for payments)
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...

# Email (for notifications)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### Django Settings

Key settings can be modified in `piata_ro/settings.py`:

- **ALLOWED_HOSTS** - Add your domain
- **DATABASES** - Switch to PostgreSQL for production
- **STATIC_ROOT** - Configure static files for production
- **MEDIA_ROOT** - Configure media uploads

---

## 🤖 MCP Agents

Our AI agents enhance the marketplace experience:

### 📢 Advertising Agent

Optimize your listings with AI-powered recommendations:

```bash
# Start the advertising agent
cd awesome-mcp-servers
python advertising-agent.py
```

**Features:**
- Title optimization
- Description generation
- Pricing recommendations
- SEO improvements

### 🗄️ Django SQL Agent

Manage database operations efficiently:

```bash
# Start the SQL agent
cd awesome-mcp-servers
python django_sql_agent.py
```

**Features:**
- Database queries
- User management
- Listing operations
- Analytics

### 📊 Stock Agent

Monitor inventory and performance:

```bash
# Start the stock agent
cd awesome-mcp-servers
python stock_agent.py
```

**Features:**
- Inventory tracking
- Performance analytics
- Stock alerts
- Trend analysis

---

## 🧪 Testing

### Run Tests

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test marketplace
python manage.py test api

# Run with coverage
pip install coverage
coverage run --source='.' manage.py test
coverage report
```

### Test Data

```bash
# Load test fixtures
python manage.py loaddata sample-data.json

# Create sample images
python add_sample_images.py

# Create test users
python manage.py shell
# >>> from django.contrib.auth.models import User
# >>> User.objects.create_user('testuser', 'test@example.com', 'password')
```

---

## 📦 Deployment

### Production Setup

1. **🔧 Configure settings**
   ```python
   # piata_ro/settings.py
   DEBUG = False
   ALLOWED_HOSTS = ['yourdomain.com']
   ```

2. **🗃️ Set up database**
   ```bash
   # Use PostgreSQL in production
   pip install psycopg2-binary
   ```

3. **📁 Collect static files**
   ```bash
   python manage.py collectstatic
   ```

4. **🐳 Docker deployment**
   ```bash
   docker-compose up -d
   ```

### Docker

```dockerfile
# Dockerfile included for easy deployment
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

---

## 🤝 Contributing

We welcome contributions! Here's how to get started:

### Development Workflow

1. **🍴 Fork the repository**
2. **🌿 Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **💾 Commit your changes**
   ```bash
   git commit -m 'Add amazing feature'
   ```
4. **📤 Push to the branch**
   ```bash
   git push origin feature/amazing-feature
   ```
5. **📝 Open a Pull Request**

### Code Standards

- Follow PEP 8 for Python code
- Use meaningful commit messages
- Add tests for new features
- Update documentation as needed

### Areas for Contribution

- 🐛 Bug fixes
- ✨ New features
- 📚 Documentation improvements
- 🎨 UI/UX enhancements
- 🧪 Test coverage
- 🌍 Internationalization

---

## 📄 License

This project is licensed under the **Unlicense** - see the [LICENSE](LICENSE) file for details.

**Why Unlicense?** We believe in open knowledge sharing and want this project to be freely usable, modifiable, and distributable by anyone for any purpose.

---

## 🙏 Acknowledgments

### Special Recognition

**🤖 AI Development Partner**: This project was built through an incredible collaboration with **Claude Sonnet 4**, showcasing the power of human-AI partnership in modern software development.

### Key Contributors

- **👨‍💻 Ionut Baltag** - Project Vision & Implementation
- **🤖 Claude Sonnet 4** - AI Development Partner & Code Architect
- **🛠️ Sourcery AI & OpenHands** - Development Tools & Integration

### Technologies & Libraries

- **Django Team** - For the amazing web framework
- **Tailwind CSS** - For the utility-first CSS framework
- **Leaflet** - For interactive maps
- **Font Awesome** - For beautiful icons
- **OpenStreetMap** - For map tiles and data

---

## 📞 Contact & Support

<div align="center">

**🇷🇴 Piața RO Development Team**

📧 **Email**: [ionutbaltag3@gmail.com](mailto:ionutbaltag3@gmail.com)  
🔗 **GitHub**: [valentinuuiuiu/piata-ro-project](https://github.com/valentinuuiuiu/piata-ro-project)  
🐛 **Issues**: [Report a Bug](https://github.com/valentinuuiuiu/piata-ro-project/issues)  
💡 **Discussions**: [Ideas & Feedback](https://github.com/valentinuuiuiu/piata-ro-project/discussions)

---

*"The future of development is not human vs AI, but human WITH AI"* 🚀

**Built with ❤️ in Romania through human-AI collaboration**

</div>
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

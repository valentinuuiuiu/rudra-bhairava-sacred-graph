# 🛒 Piața RO - Romanian Marketplace Platform

**Motto**: Aknolwedging The Limitations of The AI is aknolwedging THe Limitations of Our OLD Ptaherns Stupid Mind,Dare to Dream and The Ai will make it Real


**Piața RO** is a modern, full-featured Romanian marketplace platform inspired by popular sites like **Publi24.ro** and **OLX.ro**. Built with cutting-edge technologies, it provides a seamless experience for buying and selling items across Romania.

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
- **Reflex** - Modern Python-based web framework for reactive UIs
- **HTML/CSS/JavaScript** - Custom responsive components
- **Modern UI Components** - Clean, professional design system

### **Backend**
- **Python 3.8+** - Core application logic
- **Django/FastAPI** - RESTful API development
- **SQL Database** - Robust data storage with migrations
- **Authentication System** - Secure user management

### **Infrastructure**
- **Docker** - Containerized deployment
- **Node.js** - Build tools and package management
- **Migration System** - Database version control
- **RESTful APIs** - Clean API architecture

## 📁 Project Architecture

```
piata-ro-project/
├── 🎨 frontend_reflex/           # Main Reflex frontend application
│   ├── components/               # Reusable UI components
│   ├── pages/                   # Application pages
│   └── state.py                 # State management
├── 🔧 api/                      # REST API endpoints
│   ├── models.py                # Database models
│   ├── serializers.py           # Data serialization
│   ├── views.py                 # API views
│   └── urls.py                  # URL routing
├── 🏪 marketplace/              # Core marketplace logic
│   ├── models.py                # Marketplace models
│   ├── views.py                 # Business logic
│   └── templates/               # HTML templates
├── 📊 migrations/               # Database migrations
├── 🐳 docker-compose.yml        # Docker configuration
├── 📦 requirements.txt          # Python dependencies
└── 🔧 package.json             # Node.js dependencies
```

## 🚀 Quick Start

### **Prerequisites**
- 🐍 **Python 3.8+** - [Download Python](https://python.org)
- 📦 **Node.js 16+** - [Download Node.js](https://nodejs.org)
- 🐳 **Docker** (optional) - [Download Docker](https://docker.com)

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

3. **Install Node.js dependencies:**
```bash
npm install
```

4. **Set up the database:**
```bash
# Create database schema
sqlite3 database.db < create-schema.sql

# Add sample data (optional)
sqlite3 database.db < sample-data.sql

# Run migrations
node run-migrations.js
```

5. **Configure environment:**
```bash
# Copy environment template
cp .env.example .env

# Edit .env with your configuration
nano .env
```
pip install -r requirements.txt
```

3. Set up the database:
```bash
# Run migrations
node run-migrations.js
```

4. Start the development server:
```bash
# Option 1: Using the development script
./run-dev.sh

# Option 2: Using the server script
./run-server.sh

# Option 3: Using Docker
docker-compose up
```

## Development

### Running in Development Mode

```bash
./run-dev.sh
```

### Running the Server

```bash
./run-server.sh
```

### Database Operations

- Create schema: Use `create-schema.sql`
- Sample data: Use `sample-data.sql`
- Migrations: Run `node run-migrations.js`

## API Testing

You can test the API endpoints using the provided `test-api.html` file or by running the test database script:

```bash
node test-db.js
```

## Docker Support

The project includes Docker configuration for easy deployment:

```bash
docker-compose up -d
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

# Piata RO - Romanian Marketplace

A modern marketplace application built with Python and Reflex, featuring a clean and intuitive interface for buying and selling items.

## Features

- 🏪 Browse marketplace listings
- 🔍 Search and filter functionality
- 📱 Responsive design
- 👤 User authentication
- ➕ Add new listings
- 💰 Credit system
- 🏷️ Category-based organization

## Tech Stack

- **Frontend**: Reflex (Python-based web framework)
- **Backend**: Python with API integration
- **Database**: SQL with migrations support
- **Containerization**: Docker support

## Project Structure

```
├── frontend_reflex/          # Main Reflex frontend application
├── api/                      # API endpoints and models
├── marketplace/              # Marketplace core functionality
├── migrations/               # Database migrations
├── client/                   # Static client files
└── docker-compose.yml        # Docker configuration
```

## Getting Started

### Prerequisites

- Python 3.8+
- Node.js (for some dependencies)
- Docker (optional)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/piata-ro-project.git
cd piata-ro-project
```

2. Install Python dependencies:
```bash
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

## Contact

Project Link: [https://github.com/yourusername/piata-ro-project](https://github.com/yourusername/piata-ro-project)

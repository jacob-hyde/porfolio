# Jacob Hyde - Personal Portfolio Website

A modern, containerized portfolio website built with React and Flask. Features a clean, responsive design with smooth animations and a well-organized codebase.

## Tech Stack

### Frontend
- React 18 with TypeScript
- Material-UI (MUI) for components
- Redux Toolkit for state management
- Framer Motion for animations
- Axios for API requests

### Backend
- Flask (Python 3.11)
- SQLAlchemy for database ORM
- JWT for authentication
- MySQL for data storage

### DevOps
- Docker & Docker Compose
- Development Tools: Node.js, npm

## Project Structure

```
.
├── frontend/                # React frontend application
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── store/         # Redux store and slices
│   │   ├── types/         # TypeScript type definitions
│   │   └── utils/         # Utility functions and API client
│   └── Dockerfile         # Frontend Docker configuration
├── backend/               # Flask backend application
│   ├── app/              # Main application package
│   │   ├── models/       # Database models
│   │   ├── routes/       # API routes
│   │   ├── auth/         # Authentication logic
│   │   └── config/       # Configuration
│   ├── main.py          # Application entry point
│   └── Dockerfile       # Backend Docker configuration
└── docker-compose.yml    # Docker compose configuration
```

## Features

- **Modern UI/UX**
  - Responsive Material Design
  - Smooth animations and transitions
  - Dark/Light mode support

- **Portfolio Management**
  - Project showcase with images and details
  - Skills tracking with proficiency levels
  - Dynamic profile information

- **Security**
  - JWT-based authentication
  - Protected admin routes
  - Secure password handling

- **Developer Experience**
  - Docker containerization
  - Hot reloading in development
  - TypeScript for type safety
  - Modular and maintainable codebase

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Node.js 18+ (for local development)
- Python 3.11+ (for local development)

### Running with Docker

1. Clone the repository:
```bash
git clone <repository-url>
cd personal-website
```

2. Create a .env file in the root directory:
```bash
# Backend
MYSQL_USER=portfolio_user
MYSQL_PASSWORD=portfolio_pass
MYSQL_DATABASE=portfolio_db
MYSQL_HOST=db
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret

# Frontend
REACT_APP_API_URL=http://localhost:8092
```

3. Start the application:
```bash
docker compose up --build
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8092

### Local Development

#### Frontend
```bash
cd frontend
npm install
npm start
```

#### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt
flask run
```

## API Documentation

### Authentication
- POST /api/login - Login with username and password
- GET /api/check-auth - Check authentication status

### Projects
- GET /api/projects - List all projects
- POST /api/projects - Create a new project (protected)
- DELETE /api/projects/:id - Delete a project (protected)

### Skills
- GET /api/skills - List all skills
- POST /api/skills - Create a new skill (protected)
- DELETE /api/skills/:id - Delete a skill (protected)

### Profile
- GET /api/profile - Get profile information

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

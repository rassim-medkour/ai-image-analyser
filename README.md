# AI Image Analyser

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

A modern web application for uploading images and analyzing them with AI to generate descriptions and identify key concepts. Built with a Flask backend, React frontend, and Clarifai AI integration.

![Project Screenshot](docs/screenshot.png)

## 🚀 Features

- **Image Upload & Management**: Secure upload, storage, and management of images
- **AI-powered Analysis**: Automatic image content analysis using Clarifai workflows
- **User Authentication**: Secure registration and login system
- **Cloud Storage**: Integration with S3-compatible storage (AWS S3, Cloudflare R2, etc.)
- **Responsive UI**: Modern React frontend with responsive design

## 📋 Prerequisites

- Python 3.10+
- Node.js 16+
- PostgreSQL or other SQL database
- S3-compatible storage (AWS S3, Cloudflare R2, etc.)
- Clarifai account with API key and workflow URL

## 🛠️ Technology Stack

### Backend

- **Framework**: Flask with Flask-SQLAlchemy
- **Authentication**: JWT using Flask-JWT-Extended
- **Database**: PostgreSQL (adaptable to other SQL databases)
- **Cloud Storage**: AWS S3/Cloudflare R2 via boto3
- **AI Integration**: Clarifai API with workflow support

### Frontend

- **Framework**: React with TypeScript
- **Build Tool**: Vite
- **State Management**: React Context API
- **Styling**: CSS modules
- **HTTP Client**: Axios

## 🔧 Installation & Setup

### Backend Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/rassim-medkour/ai-image-analyser.git
   cd ai-image-analyser
   ```

2. **Set up a virtual environment**

   ```bash
   cd backend
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Create a .env file with the following variables**

   ```
   SECRET_KEY=your_secret_key
   DATABASE_URL=postgresql://username:password@localhost:5432/image_analyser
   JWT_SECRET_KEY=your_jwt_secret

   # S3/R2 Configuration
   S3_BUCKET_NAME=your_bucket_name
   S3_ACCESS_KEY=your_access_key
   S3_SECRET_KEY=your_secret_key
   S3_REGION=auto  # 'auto' for R2, or specify region for AWS
   S3_ENDPOINT_URL=https://xxx.r2.cloudflarestorage.com  # For R2, or omit for AWS

   # Clarifai Configuration
   CLARIFAI_PAT=your_personal_access_token
   CLARIFAI_WORKFLOW_URL=https://clarifai.com/username/project/workflows/workflow-name
   ```

5. **Initialize the database**

   ```bash
   flask db upgrade
   ```

6. **Run the development server**
   ```bash
   flask run --debug
   ```

### Frontend Setup

1. **Navigate to frontend directory**

   ```bash
   cd ../frontend
   ```

2. **Install dependencies**

   ```bash
   npm install
   ```

3. **Create a .env file**

   ```
   VITE_API_URL=http://localhost:5000/api/v1
   ```

4. **Run the development server**
   ```bash
   npm run dev
   ```

## 🏗️ Project Structure

```
ai-image-analyser/
├── backend/                  # Flask backend
│   ├── app/                  # Application code
│   │   ├── controllers/      # Handle request processing
│   │   ├── models/           # Database models
│   │   ├── repositories/     # Data access layer
│   │   ├── routes/           # API endpoints
│   │   ├── schemas/          # Data validation schemas
│   │   ├── services/         # Business logic
│   │   └── utils/            # Helper utilities
│   ├── migrations/           # Database migrations
│   └── requirements.txt      # Python dependencies
└── frontend/                 # React frontend
    ├── src/
    │   ├── api/              # API client code
    │   ├── components/       # React components
    │   ├── hooks/            # Custom React hooks
    │   ├── pages/            # Page components
    │   ├── store/            # State management
    │   └── types/            # TypeScript types
    └── package.json          # Node dependencies
```

## 🔄 Architecture

The application follows a clean, layered architecture:

1. **Controllers**: Handle HTTP requests/responses and input validation
2. **Services**: Contain business logic and orchestrate operations
3. **Repositories**: Handle data access and persistence
4. **Models**: Define database structure and relationships

Key design patterns used:

- **Repository Pattern**: Abstracts data access operations
- **Strategy Pattern**: For flexible image analysis approaches
- **Facade Pattern**: Simplifies complex subsystem interactions
- **Adapter Pattern**: For third-party service integration

## 📝 API Documentation

### Authentication Endpoints

- `POST /api/v1/auth/register`: Register a new user
- `POST /api/v1/auth/login`: Login and get access token

### Image Endpoints

- `GET /api/v1/images`: List all user images
- `GET /api/v1/images/{id}`: Get single image details
- `POST /api/v1/images/upload`: Upload a new image
- `DELETE /api/v1/images/{id}`: Delete an image

### User Endpoints

- `GET /api/v1/users/me`: Get current user profile

## 🧪 Testing

Testing infrastructure is planned but not yet implemented. This section will be updated when tests are added.

## 🚀 Deployment

### Backend Deployment

The Flask backend can be deployed using Gunicorn:

```bash
cd backend
gunicorn wsgi:app
```

### Frontend Deployment

Build the production version of the frontend:

```bash
cd frontend
npm run build
```

The output in the `dist` directory can be served by any static file server.

## 🛣️ Roadmap

- Add comprehensive test coverage for both backend and frontend
- Implement OpenAPI/Swagger documentation for API endpoints
- Add containerization for easier deployment
- Implement server-side caching for API responses
- Add user roles and permissions system
- Add error monitoring and structured logging

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature/my-feature`
5. Open a pull request

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Contributors

- [Rassim Medkour](https://github.com/rassim-medkour) - Initial work

## 🙏 Acknowledgments

- [Clarifai](https://www.clarifai.com/) - AI image analysis API
- [Flask](https://flask.palletsprojects.com/) - Web framework for backend
- [React](https://reactjs.org/) - UI library for frontend

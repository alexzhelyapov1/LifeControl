#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Starting LifeControl Application${NC}"

# Check if .env file exists, if not create it
if [ ! -f .env ]; then
    echo -e "${YELLOW}📝 Creating .env file...${NC}"
    cat > .env << EOF
# Database Configuration
POSTGRES_SERVER=db
POSTGRES_USER=financier
POSTGRES_PASSWORD=financier_password
POSTGRES_DB=financier
POSTGRES_PORT=5432

# JWT Settings
SECRET_KEY=your-secret-key-here-change-in-production-123456789
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Frontend Configuration
VITE_API_BASE_URL=http://localhost:8000
EOF
    echo -e "${GREEN}✅ .env file created${NC}"
else
    echo -e "${GREEN}✅ .env file already exists${NC}"
fi

# Check if Docker is running
if ! sudo docker info > /dev/null 2>&1; then
    echo -e "${RED}❌ Docker is not running. Please start Docker and try again.${NC}"
    exit 1
fi

# Stop any existing containers
echo -e "${YELLOW}🛑 Stopping existing containers...${NC}"
sudo docker compose down

# Build and start the application
echo -e "${YELLOW}🔨 Building and starting containers...${NC}"
sudo docker compose up --build -d

# Wait for services to be ready
echo -e "${YELLOW}⏳ Waiting for services to be ready...${NC}"
sleep 10

# Check if services are running
echo -e "${YELLOW}🔍 Checking service status...${NC}"

# Check database
if sudo docker compose ps db | grep -q "Up"; then
    echo -e "${GREEN}✅ Database is running${NC}"
else
    echo -e "${RED}❌ Database failed to start${NC}"
    sudo docker compose logs db
    exit 1
fi

# Check API
if sudo docker compose ps api | grep -q "Up"; then
    echo -e "${GREEN}✅ API is running${NC}"
else
    echo -e "${RED}❌ API failed to start${NC}"
    sudo docker compose logs api
    exit 1
fi

# Check frontend
if sudo docker compose ps frontend | grep -q "Up"; then
    echo -e "${GREEN}✅ Frontend is running${NC}"
else
    echo -e "${RED}❌ Frontend failed to start${NC}"
    sudo docker compose logs frontend
    exit 1
fi

echo -e "${GREEN}🎉 Application is ready!${NC}"
echo -e "${BLUE}📊 Services:${NC}"
echo -e "   🌐 Frontend: ${GREEN}http://localhost:3000${NC}"
echo -e "   🔧 API: ${GREEN}http://localhost:8000${NC}"
echo -e "   📚 API Docs: ${GREEN}http://localhost:8000/docs${NC}"
echo -e "   🗄️  Database: ${GREEN}localhost:5432${NC}"
echo -e ""
echo -e "${BLUE}👤 Admin credentials:${NC}"
echo -e "   Login: ${GREEN}admin${NC}"
echo -e "   Password: ${GREEN}admin${NC}"
echo -e ""
echo -e "${YELLOW}💡 To stop the application, run: docker-compose down${NC}"
echo -e "${YELLOW}💡 To view logs, run: docker-compose logs -f${NC}" 
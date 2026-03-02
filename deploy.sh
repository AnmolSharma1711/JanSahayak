#!/bin/bash

# JanSahayak - Quick Deployment Script

echo "=========================================="
echo "  JanSahayak Deployment Helper"
echo "=========================================="
echo ""

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "❌ Git not initialized. Run: git init"
    exit 1
fi

# Check if changes are committed
if [ -n "$(git status --porcelain)" ]; then
    echo "📝 You have uncommitted changes."
    read -p "Commit and push now? (y/n): " commit_choice
    
    if [ "$commit_choice" = "y" ]; then
        git add .
        read -p "Enter commit message: " commit_msg
        git commit -m "$commit_msg"
        git push origin main
        echo "✅ Changes pushed to GitHub"
    fi
fi

echo ""
echo "Choose deployment platform:"
echo "1) Render (Recommended)"
echo "2) Heroku"
echo "3) Docker (Local)"
echo ""
read -p "Enter choice (1-3): " platform

case $platform in
    1)
        echo ""
        echo "🚀 Deploying to Render..."
        echo ""
        echo "Steps:"
        echo "1. Go to: https://dashboard.render.com/new/web"
        echo "2. Connect your GitHub repository"
        echo "3. Use these settings:"
        echo "   - Build Command: pip install -r requirements.txt"
        echo "   - Start Command: python app.py"
        echo "4. Add environment variables:"
        echo "   - GROQ_API_KEY"
        echo "   - TAVILY_API_KEY"
        echo "   - HF_TOKEN"
        echo ""
        echo "📖 See DEPLOYMENT.md for detailed instructions"
        ;;
    
    2)
        echo ""
        echo "🚀 Deploying to Heroku..."
        
        # Check if heroku CLI is installed
        if ! command -v heroku &> /dev/null; then
            echo "❌ Heroku CLI not installed"
            echo "Install from: https://devcenter.heroku.com/articles/heroku-cli"
            exit 1
        fi
        
        echo ""
        read -p "Enter app name: " app_name
        
        heroku create $app_name
        
        echo ""
        echo "Setting environment variables..."
        read -sp "Enter GROQ_API_KEY: " groq_key
        echo ""
        heroku config:set GROQ_API_KEY="$groq_key"
        
        read -sp "Enter TAVILY_API_KEY: " tavily_key
        echo ""
        heroku config:set TAVILY_API_KEY="$tavily_key"
        
        read -sp "Enter HF_TOKEN: " hf_token
        echo ""
        heroku config:set HF_TOKEN="$hf_token"
        
        echo ""
        echo "Deploying..."
        git push heroku main
        
        echo ""
        echo "✅ Deployed! Opening app..."
        heroku open
        ;;
    
    3)
        echo ""
        echo "🐳 Building Docker container..."
        
        if ! command -v docker &> /dev/null; then
            echo "❌ Docker not installed"
            echo "Install from: https://docs.docker.com/get-docker/"
            exit 1
        fi
        
        # Check for .env file
        if [ ! -f ".env" ]; then
            echo "❌ .env file not found"
            echo "Copy .env.example to .env and add your API keys"
            exit 1
        fi
        
        docker-compose up --build -d
        
        echo ""
        echo "✅ Container started!"
        echo "📱 Access at: http://localhost:5000"
        echo ""
        echo "Useful commands:"
        echo "  - View logs: docker-compose logs -f"
        echo "  - Stop: docker-compose down"
        echo "  - Restart: docker-compose restart"
        ;;
    
    *)
        echo "❌ Invalid choice"
        exit 1
        ;;
esac

echo ""
echo "=========================================="
echo "  Deployment Complete!"
echo "=========================================="

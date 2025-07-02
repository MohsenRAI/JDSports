#!/bin/bash

# Development startup script for Gazman Clone
# This script starts both the backend Flask server and the frontend React app

echo "🚀 Starting Gazman Clone Development Environment"
echo "================================================"

# Function to cleanup background processes on exit
cleanup() {
    echo "🛑 Shutting down servers..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Start Backend (Flask server)
echo "🔧 Starting Backend (Flask) on port 5003..."
cd headswapper
source venv/bin/activate
python3 analyze_user_image.py &
BACKEND_PID=$!
cd ..

# Wait a moment for backend to start
sleep 3

# Start Frontend (React/Vite)
echo "🎨 Starting Frontend (React) on port 5173..."
npm run dev &
FRONTEND_PID=$!

echo ""
echo "✅ Both servers are starting up..."
echo "📱 Frontend: http://localhost:5173"
echo "🔧 Backend:  http://localhost:5003"
echo ""
echo "Press Ctrl+C to stop both servers"
echo ""

# Wait for both processes
wait 
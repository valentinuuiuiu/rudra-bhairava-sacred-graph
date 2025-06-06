#!/bin/bash
# Script to run both the server and client

# Start the server in the background
echo "Starting server on port 5000..."
NODE_ENV=development node server.cjs &
SERVER_PID=$!

# Start the client in the background
echo "Starting Vite client on port 5173..."
cd client && npx vite --port 5173 &
CLIENT_PID=$!

# Function to handle script termination
cleanup() {
  echo "Shutting down server and client..."
  kill $SERVER_PID
  kill $CLIENT_PID
  exit 0
}

# Set up trap to catch termination signals
trap cleanup SIGINT SIGTERM

# Keep the script running
echo "Development environment is running!"
echo "Server: http://localhost:5000"
echo "Client: http://localhost:5173"
echo "Press Ctrl+C to stop both processes"
wait

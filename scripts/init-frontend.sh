#!/bin/bash
mkdir -p frontend
cd frontend

# Initialize package.json if it doesn't exist
if [ ! -f package.json ]; then
    npm init -y
    
    # Install dependencies including Tailwind
    npm install react react-dom @types/react @types/react-dom typescript plotly.js react-plotly.js @types/plotly.js
    npm install -D vite @vitejs/plugin-react tailwindcss postcss autoprefixer
    
    # Initialize Tailwind
    npx tailwindcss init -p
fi 
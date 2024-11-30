#!/bin/bash
mkdir -p frontend
cd frontend

# Initialize package.json if it doesn't exist
if [ ! -f package.json ]; then
    npm init -y
    
    # Add scripts to package.json
    node -e "
        const pkg = require('./package.json');
        pkg.scripts = {
            'dev': 'vite',
            'build': 'tsc && vite build',
            'preview': 'vite preview'
        };
        require('fs').writeFileSync('package.json', JSON.stringify(pkg, null, 2))
    "
    
    # Install dependencies
    npm install react react-dom @types/react @types/react-dom typescript plotly.js react-plotly.js @types/plotly.js
    npm install -D vite @vitejs/plugin-react
    
    # Create tsconfig.json
    echo '{
        "compilerOptions": {
            "target": "ES2020",
            "useDefineForClassFields": true,
            "lib": ["ES2020", "DOM", "DOM.Iterable"],
            "module": "ESNext",
            "skipLibCheck": true,
            "moduleResolution": "bundler",
            "allowImportingTsExtensions": true,
            "resolveJsonModule": true,
            "isolatedModules": true,
            "noEmit": true,
            "jsx": "react-jsx",
            "strict": true,
            "noUnusedLocals": true,
            "noUnusedParameters": true,
            "noFallthroughCasesInSwitch": true
        },
        "include": ["src"],
        "references": [{ "path": "./tsconfig.node.json" }]
    }' > tsconfig.json

    # Create tsconfig.node.json
    echo '{
        "compilerOptions": {
            "composite": true,
            "skipLibCheck": true,
            "module": "ESNext",
            "moduleResolution": "bundler",
            "allowSyntheticDefaultImports": true
        },
        "include": ["vite.config.ts"]
    }' > tsconfig.node.json
fi 
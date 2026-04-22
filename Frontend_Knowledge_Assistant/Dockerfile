# Use a lightweight Node.js 18 image (Alpine = smaller size)
# FROM node:18-alpine 
# local machine may work with v18, but inside Docker, Vite enforces a newer Node version
FROM node:20-alpine

# Set the working directory inside the container to /app
WORKDIR /app

# Copy package.json and lock file first (enables Docker layer caching)
COPY package.json package-lock.json ./

# Install frontend dependencies (React, Vite, etc.)
RUN npm install

# Copy the rest of the frontend source code into the container
COPY . .

# Build the production-ready frontend (Vite build output)
RUN npm run build

# Inform Docker that the app will run on port 5173
EXPOSE 5173

# Start the Vite preview server to serve the built frontend
CMD ["npm", "run", "preview", "--", "--host", "0.0.0.0", "--port", "5173"]
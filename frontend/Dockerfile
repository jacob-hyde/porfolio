# Use Node.js LTS version
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies with legacy peer deps to handle React 18 compatibility
RUN npm install --legacy-peer-deps

# Copy the rest of the application code
COPY . .

# Set environment for development
ENV NODE_ENV=development
ENV FAST_REFRESH=false
ENV WDS_SOCKET_PORT=0

# Expose port 3000
EXPOSE 3000

# Start the application with the development server
CMD ["npm", "start"]

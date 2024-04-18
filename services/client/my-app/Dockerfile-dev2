# Use an official Node runtime as a parent image
FROM node:14

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy package.json and package-lock.json (or yarn.lock)
COPY package.json ./
COPY package-lock.json* yarn.lock* ./

# Install dependencies
RUN npm install --silent

# Copy the rest of your app's source code
COPY . .

# Build your app
RUN npm run build

# Install `serve` to serve your application on port 3000
RUN npm install -g serve

# Command to run the app
CMD ["serve", "-s", "build", "-l", "3000"]

# Expose port 3000 to the outside
EXPOSE 3000

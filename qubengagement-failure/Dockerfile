# Specify a base image
FROM node:16-alpine

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy package.json and package-lock.json
COPY package*.json ./


# Install dependencies, including 'express'
RUN npm install --only=production

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Your app binds to port 80 so you'll use the EXPOSE instruction to have it mapped by the docker daemon
EXPOSE 80

# Define the command to run your app using CMD which defines your runtime
CMD [ "node", "totalRiskApp.js" ]

# Specify a base image
FROM node:16-alpine

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy package.json and package-lock.json
COPY package*.json ./

<<<<<<< HEAD
# Install dependencies, including 'express'
RUN npm install --only=production
=======
# Install dependencies
RUN npm install
>>>>>>> 51f0b1a6579e67541c4ad960fb4f47cbb8dade4f

# Copy the rest of the application code
COPY . .

<<<<<<< HEAD
# Your app binds to port 89 so you'll use the EXPOSE instruction to have it mapped by the docker daemon
EXPOSE 89
=======
# Your app binds to port 80 so you'll use the EXPOSE instruction to have it mapped by the docker daemon
EXPOSE 80
>>>>>>> 51f0b1a6579e67541c4ad960fb4f47cbb8dade4f

# Define the command to run your app using CMD which defines your runtime
CMD [ "node", "totalRiskApp.js" ]

FROM node:18

# Install yt-dlp
RUN apt-get update && apt-get install -y python3 python3-pip && pip3 install yt-dlp

# Set working directory
WORKDIR /app

# Copy files
COPY . .

# Install Node dependencies
RUN npm install

EXPOSE 3000
CMD ["npm", "start"]

FROM node:20-alpine AS builder

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci

COPY . .
RUN npm run build

# Expose port (default for Django)
EXPOSE 3000

CMD ["npm", "run", "preview"]
# Stage 1: Build the application
FROM node:lts-alpine as build-stage

WORKDIR /app

# Copy package files and install dependencies
COPY Frontend/flowerlens/package*.json ./

RUN npm install

# Copy the rest of the application
COPY Frontend/flowerlens/ .

# Build the application
RUN npm run build

# Stage 2: Create the final image with only the compiled app
FROM alpine

# Install serve
RUN apk add --no-cache nodejs npm \
    && npm install -g serve \
    && npm cache clean --force \
    && rm -rf /var/cache/apk/*

WORKDIR /app

# Copy built assets from the build stage
COPY --from=build-stage /app/dist /app

EXPOSE 8080

CMD ["serve", "-s", "/app", "-l", "8080"]

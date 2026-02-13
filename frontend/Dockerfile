# Base Image
FROM node:lts-alpine

# Install pnpm globally
# We verify the installation to ensure it's ready
RUN npm install -g pnpm

# Work Directory
WORKDIR /app

# Install Dependencies
# Copy package.json AND pnpm-lock.yaml
COPY package.json pnpm-lock.yaml ./

# Install using the lockfile for strict reproducibility
RUN pnpm install --frozen-lockfile

# Copy Source Code
COPY . .

# Build the Next.js Application
RUN pnpm run build

# Expose Port
EXPOSE 3000

# Start the Application
CMD ["pnpm", "start"]
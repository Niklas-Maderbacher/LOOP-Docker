# Stage 0, "build-stage", based on Node.js, to build and compile the frontend
FROM node:20 AS build-stage

WORKDIR /app

COPY package*.json /app/

RUN yarn install

COPY ./ /app/

ARG VITE_API_URL=${VITE_API_URL}

RUN yarn run build

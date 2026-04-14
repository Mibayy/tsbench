FROM node:20-alpine
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
RUN npm run build
EXPOSE 3000
EXPOSE 9229
EXPOSE 6666
CMD ["npm", "start"]

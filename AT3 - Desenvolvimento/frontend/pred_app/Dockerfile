FROM node:18-slim

WORKDIR /app

ENV NODE_ENV=development

COPY package*.json ./

RUN npm install 
RUN npm install -g vite@latest

COPY . .

EXPOSE 5173

CMD ["npm", "run", "dev"]

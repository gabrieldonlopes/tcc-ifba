# Etapa 1: build da aplicação
FROM node:20 AS builder
WORKDIR /app
COPY . .
RUN npm install
RUN npm run build

# Etapa 2: Nginx para servir arquivos estáticos
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80

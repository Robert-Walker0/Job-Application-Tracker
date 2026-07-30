FROM node:24.16.0 

WORKDIR /app

RUN useradd --create-home appuser

COPY package*.json ./ 

RUN npm ci

COPY . . 

RUN chown -R appuser:appuser /app

USER appuser

EXPOSE 5173

CMD [ "npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "5173"]

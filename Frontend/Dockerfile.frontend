# Use a lightweight Nginx image
FROM nginx:alpine

# Remove default Nginx HTML files
RUN rm -rf /usr/share/nginx/html/*

# Copy your simple index.html into the Nginx serving directory
COPY index.html /usr/share/nginx/html/

# Nginx listens on port 80 by default
EXPOSE 80
FROM nginx:latest

#COPY frontend/dist/ /usr/share/nginx/html/admin/

COPY nginx.conf /etc/nginx/nginx.conf

CMD ["nginx", "-g", "daemon off;"]
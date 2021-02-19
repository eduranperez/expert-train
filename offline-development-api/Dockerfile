FROM lambci/lambda:nodejs12.x

USER root

RUN npm install -g nodemon

ENV APP_DIR /var/task

WORKDIR $APP_DIR

RUN npm install 

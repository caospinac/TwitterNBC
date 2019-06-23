FROM node:12.2.0-alpine

# set working directory
ADD ./gui /gui
WORKDIR /gui

# add `/gui/node_modules/.bin` to $PATH
ENV PATH /gui/node_modules/.bin:$PATH

# install and cache app dependencies
# COPY gui/gui/package.json /gui/package.json
# RUN npm install --silent
RUN npm -g install yarn
RUN yarn install

FROM php:7-apache

ARG BUILD_PACKAGES="libfreetype6-dev libjpeg62-turbo-dev libmcrypt-dev libpng12-dev libgmp-dev"

RUN apt-get update && \
  apt-get install -y --no-install-recommends $BUILD_PACKAGES && \
  ln -s /usr/include/x86_64-linux-gnu/gmp.h /usr/include/gmp.h && \
  docker-php-ext-configure gmp && \
  docker-php-ext-install pdo pdo_mysql mbstring gd iconv mcrypt gmp && \
  a2enmod rewrite && \
  apt-get remove -y $BUILD_PACKAGES && \
  apt-get autoremove -y && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/*

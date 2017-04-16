#!/bin/bash

NODE_ENV=production node node_modules/webpack/bin/webpack.js --optimize-minimize --define process.env.NODE_ENV="'production'"

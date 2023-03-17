/* logger.js */

var util = require('util');
var winston = require('winston');
var config = require('./config.json');

winston.remove(winston.transports.Console);
winston.add(winston.transports.Console, config.logging);

var logger = exports;

/* logger.*([data], [...]) */

logger.error = function() {
  winston.error(util.format.apply(this, arguments));
}

logger.debug = function() {
  winston.debug(util.format.apply(this, arguments));
}

logger.warn = function() {
  winston.warn(util.format.apply(this, arguments));
}

logger.info = function() {
  winston.info(util.format.apply(this, arguments));
}

logger.verbose = function() {
  winston.verbose(util.format.apply(this, arguments));
}

logger.silly = function() {
  winston.silly(util.format.apply(this, arguments));
}


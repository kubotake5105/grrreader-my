
/*
 * GET home page.
 */

var mysql = require('mysql');
var config = require('../config.json');
var util = require('util');
var logger = require('../logger.js');

function utcToLocal(ts) {
  var t = ts.getTime();
  var dt = ts.getTimezoneOffset() * 60 * 1000;
  var d = new Date();
  d.setTime(t - dt);
  return d;
}

function timestampToDate(ts) {
  var formatString = '%s/%s/%s';
  var year = ts.getFullYear();
  var month = ts.getMonth() + 1;
  var day = ts.getDate();

  year = String(year).slice(2, 4);
  month = (month < 10) ? '0' + month : String(month);
  day = (day < 10) ? '0' + day : String(day);

  return util.format(formatString, year, month, day);
}

function timestampToTime(ts) {
  var formatString = '%s:%s';
  var hours = ts.getHours();
  var minutes = ts.getMinutes();

  hours = (hours < 10) ? '0' + hours : String(hours);
  minutes = (minutes < 10) ? '0' + minutes : String(minutes);

  return util.format(formatString, hours, minutes);
}

function formatTimestamp(ts) {
  var today = timestampToDate(new Date());
  var localTs = utcToLocal(ts);
  var day = timestampToDate(localTs);
  if (day == today) {
    return timestampToTime(localTs);
  } else {
    return day;
  }
}

exports.index = function (req, res) {
  var connection = mysql.createConnection(config.mysql);

  connection.connect();
  connection.query('SELECT feed_id, url, title FROM feed_urls;', function (err, rows, fields) {
    connection.end();
    if (err) {
      logger.debug("query error at index.index: " + util.inspect(err));
      res.send(500);
      return;
    }
    res.render('index', {
      title: 'Express',
      feeds: rows
    });
  });
};

exports.feedContent = function (req, res) {
  var contentId = req.params.cid;
  var connection = mysql.createConnection(config.mysql);

  connection.connect();
  var sql = 'SELECT content_id, feed_id, title, url, body, timestamp'
          + '  FROM feed_contents'
          + '  WHERE content_id = ?;'
  connection.query(sql, contentId, function (err, rows, fields) {
    connection.end();
    if (err) {
      logger.debug("query error at index.feedContent: " + util.inspect(err));
      res.send(500);
      return;
    }
    if (rows.length == 0) {
      res.send(404);
      return;
    }
    for (var i = 0; i < rows.length; i++) {
      rows[i].formatedTimestamp = formatTimestamp(rows[i].timestamp);
    }
    res.json(rows[0]);
  });
};

exports.feedContents = function (req, res) {
/*
  returns json:
  {
    feedId: Number,
    totalCount: Number,
    skip: Number,
    itemCount: Number,
    contents: [
    ]
*/
  var feedId = req.params.fid;
  var connection = mysql.createConnection(config.mysql);
  var skip = Number(req.query.skip) || 0;
  var count = Number(req.query.count) || 20;

  if (feedId === '0') {
    // show all feeds
    // TODO: if use multiple users, need checking subscribing feeds
    var sqlCount = 'SELECT COUNT(content_id) FROM feed_contents;';
    var paramsCount = [];
    var sql = 'SELECT content_id, feed_id, title, url, body, timestamp'
      + '  FROM feed_contents'
      + '  ORDER BY timestamp DESC'
      + '  LIMIT ?, ?'
      + ';';
    var params = [skip, count];
  } else {
    var sqlCount = 'SELECT COUNT(content_id) FROM feed_contents'
      + ' WHERE feed_id = ?;'
    var paramsCount = [feedId];
    var sql = 'SELECT content_id, feed_id, title, url, body, timestamp'
      + '  FROM feed_contents'
      + '  WHERE feed_id = ?'
      + '  ORDER BY timestamp DESC'
      + '  LIMIT ?, ?'
      + ';';
    var params = [feedId, skip, count];
  }

  connection.connect();
  connection.query(sqlCount, paramsCount, function (err, rows, fields) {
    if (err) {
      logger.debug("query error at index.feedContents: " + util.inspect(err));
      res.send(500);
      return;
    }
    if (rows.length == 0) {
      res.send(404);
      return;
    }
    var totalCount = rows[0]['COUNT(content_id)'];
    connection.query(sql, params, function (err, rows, fields) {
      connection.end();
      if (err) {
        logger.debug("query error at index.feedContents: " + util.inspect(err));
        res.send(500);
        return;
      }
      if (rows.length == 0) {
        res.send(404);
        return;
      }
      for (var i = 0; i < rows.length; i++) {
        rows[i].formatedTimestamp = formatTimestamp(rows[i].timestamp);
      }
      var result = {
        "feedId": feedId,
        "total": totalCount,
        "skip": skip,
        "count": count,
        "contents": rows
      }
      res.json(result);
    });
  });
};

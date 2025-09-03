const express = require('express');
const os = require('os');
const app = express();
const port = process.env.PORT || 3000;
const version = process.env.APP_VERSION || 'vX';

app.get('/', (req, res) => {
  res.send(`Hello from ${version} - pod: ${process.env.HOSTNAME || os.hostname()}\n`);
});

app.listen(port, () => {
  console.log(`Listening on ${port}, version ${version}`);
});

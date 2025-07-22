const { exec } = require('child_process');
const path = require('path');
const fs = require('fs');

const dbPath = path.join(__dirname, 'caeser.db');
// Get SQLite path from environment or use system default
const sqlitePath = process.env.SQLITE_PATH || 'sqlite3';

// Remove existing database file if it exists
if (fs.existsSync(dbPath)) {
  fs.unlinkSync(dbPath);
}

// Create database file
fs.writeFileSync(dbPath, '');

// Execute SQL commands to create tables
const commands = [
  `"${sqlitePath}" "${dbPath}" "CREATE TABLE cultural_insights (id INTEGER PRIMARY KEY AUTOINCREMENT, location TEXT NOT NULL, category TEXT NOT NULL, data TEXT NOT NULL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)"`
];

const { CircuitBreaker } = require('../utils/circuitBreaker');
const retry = require('async-retry');

const circuitBreaker = new CircuitBreaker({
  failureThreshold: 3,
  successThreshold: 2,
  timeout: 30000
});

return circuitBreaker.callService(() =>
  retry(async () => {
    return new Promise((resolve, reject) => {
      exec(commands.join(' && '), (error, stdout, stderr) => {
      if (error) {
        console.error(`Error: ${error.message}`);
        return reject(error);
      }
      if (stderr) {
        console.error(`Stderr: ${stderr}`);
        return reject(stderr);
      }
      console.log('Database initialized successfully');
      resolve(stdout);
    });
  if (error) {
    console.error(`Error: ${error.message}`);
    return;
  }
  if (stderr) {
    console.error(`Stderr: ${stderr}`);
    return;
  }
  console.log('Database initialized successfully');
});} ))
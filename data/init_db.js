const { exec } = require('child_process');
const path = require('path');
const fs = require('fs');

const dbPath = path.join(__dirname, 'caeser.db');
const sqlitePath = path.join(__dirname, '../bin/sqlite/sqlite3.exe');

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

exec(commands.join(' && '), (error, stdout, stderr) => {
  if (error) {
    console.error(`Error: ${error.message}`);
    return;
  }
  if (stderr) {
    console.error(`Stderr: ${stderr}`);
    return;
  }
  console.log('Database initialized successfully');
});
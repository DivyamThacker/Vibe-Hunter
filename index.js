const express = require('express');
const app = express();

app.use(express.static('public'));
app.use(express.json());

app.get('/', (req, res) => {
    res.sendFile("./index.html");
});
app.post('/submit', (req, res) => {
    // Run the Python file
    runPythonScript('welcome.py', ["Divyam",23]);
    const playlist_link = req.body.link;
    runPythonScript('scraper.py', [playlist_link]);
});

app.listen(3000, () => {
    console.log(`Server running at http://localhost:3000/`);
});


// Run a Python script and return output
const { spawn } = require('child_process');
// import { spawn } from 'child_process';

function runPythonScript(scriptPath, args) {

  // Use child_process.spawn method from 
  // child_process module and assign it to variable
  const pyProg = spawn('python', [scriptPath].concat(args));

  // Collect data from script and print to console
  let data = '';
  pyProg.stdout.on('data', (stdout) => {
    data += stdout.toString();
  });

  // Print errors to console, if any
  pyProg.stderr.on('data', (stderr) => {
    console.log(`stderr: ${stderr}`);
  });

  // When script is finished, print collected data
  pyProg.on('close', (code) => {
    console.log(`child process exited with code ${code}`);
    console.log(data);
  });
}

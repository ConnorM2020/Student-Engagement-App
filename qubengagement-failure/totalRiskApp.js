const path = require('path');
const express = require('express');
const cors = require('cors');
const app = express();
const port = 80;  // run test on port 80
app.use(cors());
module.exports = app;

app.get('/', (req, res) => {
  const indexPath = path.join('/mnt/c', 'Users', 'Connor Mallon', 
  'Documents', 'MENG CSC', 'Level 3', 'CSC3065 I Cloud', 'A2', 
  'qubengage-frontend', 'src', 'index.html');
  
  res.sendFile(indexPath, (err) => {
    if (err) {
      console.error('Error sending index.html:', err);
      res.status(500).send('Internal Server Error');
    }
  });
});

app.get('/health', (req, res) => {
  res.send('Server is running!');
});

const LectureTotal = 33;
const LabTotal = 22; 
const SupportTotal = 44;
const CanvasTotal = 55;
const LectureWeight = 0.3;
const LabWeight = 0.4;
const SupportWeight = 0.15;
const CanvasWeight = 0.15;

app.get('/EngagementScore', (req, res) => {
  // Check for non-empty and non-zero values before parsing
  const lec = req.query.lec && req.query.lec !== '0' ? parseFloat(req.query.lec) : '';
  const lab = req.query.lab && req.query.lab !== '0' ? parseFloat(req.query.lab) : '';
  const supp = req.query.supp && req.query.supp !== '0' ? parseFloat(req.query.supp) : '';
  const can = req.query.can && req.query.can !== '0' ? parseFloat(req.query.can) : '';

  // Check for empty strings after the conditions above
  if (lec === '' || lab === '' || supp === '' || can === '') {
    return res.status(400).send("Please provide all attendance values. They should not be zero or left blank.\nTry again.");
  }

  // Check for values exceeding total allowed
  if (lec > LectureTotal || lab > LabTotal || supp > SupportTotal || can > CanvasTotal) {
    return res.status(400).send("Attendance values must not exceed total values.\nTry again.");
  }
  
  // All checks pass, calculate the engagement score
  let engagementScore = calculateEngagementScore(lec, lab, supp, can);
  engagementScore = Math.min(engagementScore, 1.0);
  
  // Round the score to two decimal places
  const roundedScore = Number(engagementScore.toFixed(2));
  res.send(roundedScore.toString());
});

// Function to calculate engagement score
function calculateEngagementScore(lec, lab, supp, can) {
  const lecScore = (lec / LectureTotal) * LectureWeight;
  const labScore = (lab / LabTotal) * LabWeight;
  const suppScore = (supp / SupportTotal) * SupportWeight;
  const canScore = (can / CanvasTotal) * CanvasWeight;
  return lecScore + labScore + suppScore + canScore;
}

// Check url for /RiskAssessment
app.get('/RiskAssessment', (req, res) => {
  const engagementScore = req.query.engagementScore && req.query.engagementScore !== '0' ? parseFloat(req.query.engagementScore) : '';
  const cutoff = req.query.cutoff && req.query.cutoff !== '0' ? parseFloat(req.query.cutoff) : '';

  // Check for empty strings or invalid values
  if(engagementScore === '' || cutoff === '' || engagementScore < 0 || engagementScore > 1 || cutoff < 0 || cutoff > 100) {
    return res.status(400).send("Invalid engagement score or cutoff values.");
  }

  const risk = calculateRisk(engagementScore, cutoff);
  res.send(risk);
});

function calculateRisk(engagementScore, cutoff) {
  const normalizedCutoff = cutoff / 100;
  if (engagementScore >= normalizedCutoff) {
    return "Low";
  } else if (engagementScore >= normalizedCutoff * 0.5) {
    return "Moderate";
  } else {
    return "High";
  }
}

if (require.main === module) {
  app.listen(port, () => {
    console.log(`Server running on port ${port}`);
  });
}

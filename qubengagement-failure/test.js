const request = require('supertest');
const express = require('express');
const app = require('./totalRiskApp');

describe('Express Server Tests', () => {
  // Test for the health check endpoint
  it('GET /health - responds with server status', async () => {
    const response = await request(app).get('/health');
    expect(response.statusCode).toBe(200);
    expect(response.text).toContain('Server is running!');
  });

  // Test for the EngagementScore endpoint
  describe('GET /EngagementScore', () => {
    it('responds with calculated engagement score', async () => {
      const response = await request(app)
        .get('/EngagementScore?lec=10&lab=10&supp=10&can=10');
      expect(response.statusCode).toBe(200);
      expect(response.text).toMatch(/^\d+(\.\d{1,2})?$/); // checks if response is a number
    });

    it('responds with error if attendance values exceed total values', async () => {
      const response = await request(app)
        .get('/EngagementScore?lec=34&lab=23&supp=45&can=56');
      expect(response.statusCode).toBe(400);
      expect(response.text).toContain("Attendance values must not exceed total values.");
    });
  });

  // Test for the RiskAssessment endpoint
  describe('GET /RiskAssessment', () => {
    it('responds with risk level based on engagement score and cutoff', async () => {
      const response = await request(app)
        .get('/RiskAssessment?engagementScore=0.6&cutoff=50');
      expect(response.statusCode).toBe(200);
      expect(response.text).toMatch(/Low|Moderate|High/);
    });

    it('responds with error for invalid engagement score or cutoff values', async () => {
      const response = await request(app)
        .get('/RiskAssessment?engagementScore=-1&cutoff=101');
      expect(response.statusCode).toBe(400);
      expect(response.text).toContain("Invalid engagement score or cutoff values.");
    });
  });

});

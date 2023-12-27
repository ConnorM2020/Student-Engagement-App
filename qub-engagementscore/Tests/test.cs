using System;
using NUnit.Framework;
using StudentEngagementApi.Controllers;
using Microsoft.AspNetCore.Mvc;

namespace StudentEngagementApi.Tests
{
    [TestFixture]
    public class EngagementScoreControllerTests
    {
        #pragma warning disable CS8618 // Non-nullable field is uninitialized. Consider declaring as nullable.
        private EngagementScoreController _controller;
        #pragma warning restore CS8618
        [SetUp]
        public void SetUp()
        {
            _controller = new EngagementScoreController(); // This ensures _controller is never null in your tests
        }

       [Test]
    public void GetEngagementScore_WithValidAttendanceValues_ReturnsCorrectScore() {
        // Arrange
        double lectureAttendance = 20;
        double labAttendance = 15;
        double supportAttendance = 30;
        double canvasAttendance = 40;

        // Act
        double expectedScore = CalculateExpectedScore(lectureAttendance, labAttendance, supportAttendance, canvasAttendance);
        ActionResult<double> result = _controller.GetEngagementScore(lectureAttendance, labAttendance, supportAttendance, canvasAttendance);

        // Assert
        Assert.IsNotNull(result.Result, "Expected an ActionResult.");
        var okResult = result.Result as OkObjectResult;
        Assert.IsNotNull(okResult, "Expected an OkObjectResult.");
        var score = okResult.Value as double?;
    
        Assert.IsTrue(score.HasValue, "Expected score value");
        Assert.AreEqual(expectedScore, score.Value, "The calculated score does match the expected score.");

        // Print to console
        TestContext.WriteLine($"Expected Score: {expectedScore}");
        TestContext.WriteLine($"Actual Score: {score.Value}");
}
    [Test]
    public void GetEngagementScoreWithInvalidValues() {
         // Arrange
        double lectureAttendance = 6;
        double labAttendance = 20;
        double supportAttendance = 17;
        double canvasAttendance = 4;
        // wrong input values 
        double wrongLecture =2;
        double wrongLab = 14;
        double wrongSupp = 13;
        double wrongCan = 4;
        // Act
        double expectedScore = CalculateExpectedScore(lectureAttendance, labAttendance, supportAttendance, canvasAttendance);
        ActionResult<double> result = _controller.GetEngagementScore(wrongLecture, wrongLab, wrongSupp, wrongCan);

        // Assert
        Assert.IsNotNull(result.Result, "Expected an ActionResult but was null.");
        var okResult = result.Result as OkObjectResult;
        Assert.IsNotNull(okResult, "Expected an OkObjectResult but was null.");
        var score = okResult.Value as double?;
    
        Assert.IsTrue(score.HasValue, "Expected a score value.");
        Assert.AreNotEqual(expectedScore, score.Value, "The calculated score does not match the expected score.");

        // Print to console
        TestContext.WriteLine($"Expected Score: {expectedScore}");
        TestContext.WriteLine($"Actual Score: {score.Value}");

    }
        private double CalculateExpectedScore(double lec, double lab, double supp, double can)
        {
            // Mock the calculation logic here or provide a static expected score
            double lecScore = (lec / 33) * 0.3;
            double labScore = (lab / 22) * 0.4;
            double suppScore = (supp / 44) * 0.15;
            double canScore = (can / 55) * 0.15;
            double totalScore = lecScore + labScore + suppScore + canScore;
            // Cap the total score at 1.0 as the method does
            return Math.Min(totalScore, 1.0);
        }
    }
}

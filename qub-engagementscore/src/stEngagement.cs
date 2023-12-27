using Microsoft.AspNetCore.Mvc;
using System;
using System.Collections.Generic; // Required for Dictionary

namespace StudentEngagementApi.Controllers
{
    [ApiController]
    [Route("[controller]")]
    public class EngagementScoreController : ControllerBase
    {
        private const double LectureWeight = 0.3;
        private const double LabWeight = 0.4;
        private const double SupportWeight = 0.15;
        private const double CanvasWeight = 0.15;

        [HttpGet]
        public ActionResult<double> GetEngagementScore(
            [FromQuery] double? lec, [FromQuery] double? lecTotal,
            [FromQuery] double? lab, [FromQuery] double? labTotal,
            [FromQuery] double? supp, [FromQuery] double? suppTotal,
            [FromQuery] double? can, [FromQuery] double? canTotal)
        {
            var parameters = new Dictionary<string, double?>
            {
                {"lec", lec},
                {"lecTotal", lecTotal},
                {"lab", lab},
                {"labTotal", labTotal},
                {"supp", supp},
                {"suppTotal", suppTotal},
                {"can", can},
                {"canTotal", canTotal}
            };

            foreach (var param in parameters)
            {
                if (!param.Value.HasValue || double.IsNaN(param.Value.Value))
                {
                    return BadRequest($"The value for {param.Key} is missing or not a number (NaN).");
                }
                if (param.Value <= 0)
                {
                    return BadRequest($"The value for {param.Key} must be greater than zero.");
                }
            }

            // Additional checks to ensure attendance does not exceed total
            if (lec > lecTotal || lab > labTotal || supp > suppTotal || can > canTotal)
            {
                return BadRequest("Attendance values must not exceed total values.");
            }

            // All parameters are valid at this point
            double engagementScore = CalculateEngagementScore(
                lec.Value, lecTotal.Value, lab.Value, labTotal.Value,
                supp.Value, suppTotal.Value, can.Value, canTotal.Value);

            engagementScore = Math.Min(engagementScore, 1.0); // Ensure score does not exceed 1.0
            return Ok(engagementScore);
        }

        private double CalculateEngagementScore(
            double lec, double lecTotal, double lab, double labTotal,
            double supp, double suppTotal, double can, double canTotal)
        {
            // Calculate the weighted score for each category
            double lecScore = (lec / lecTotal) * LectureWeight;
            double labScore = (lab / labTotal) * LabWeight;
            double suppScore = (supp / suppTotal) * SupportWeight;
            double canScore = (can / canTotal) * CanvasWeight;

            // Sum the weighted scores to get the total engagement score
            return lecScore + labScore + suppScore + canScore;
        }
    }
}

import type { DemoClearBoard } from "./types";

export const HERO_DEMO_BOARD: DemoClearBoard = {
  mode: "loaded",
  total_signals: 1240,
  headline: "Surge: many Signals in → few Incidents out",
  subhead: "Every Signal is preserved as a Report; ClearBoard merges pins on dedup and raises Incident Magnitude.",
  incidents: [
    {
      incident_id: "AC-1240",
      title: "Downtown high-rise fire",
      location: "3rd & Pine downtown",
      queue: "Fire / EMS",
      severity: "SEV1",
      report_count: 812,
      sla_minutes: 5,
      dedup_similarity: 0.94,
      status: "escalated",
      summary: "Smoke and visible flames reported from the same downtown tower; callers describe one shared fire scene.",
      sample_signals: [
        "I can see flames from the upper floors at 3rd and Pine.",
        "Smoke pouring out of the high-rise downtown near Pine.",
      ],
    },
    {
      incident_id: "AC-1241",
      title: "Eastside power outage",
      location: "Eastside substation corridor",
      queue: "Utilities",
      severity: "SEV2",
      report_count: 351,
      sla_minutes: 15,
      dedup_similarity: 0.91,
      status: "crews dispatched",
      summary: "Neighborhood reports map to one eastside outage footprint around the same substation corridor.",
      sample_signals: [
        "The whole eastside block lost power ten minutes ago.",
        "Traffic lights are out along the eastside corridor.",
      ],
    },
    {
      incident_id: "AC-1242",
      title: "Gas leak on Oak St",
      location: "Oak St & 7th Ave",
      queue: "Hazmat",
      severity: "SEV1",
      report_count: 77,
      sla_minutes: 5,
      dedup_similarity: 0.89,
      status: "evacuation advised",
      summary: "Reports of gas odor and hissing cluster at Oak Street and 7th Avenue.",
      sample_signals: [
        "Strong gas smell outside the laundromat on Oak Street.",
        "I hear hissing near the Oak and 7th construction trench.",
      ],
    },
  ],
};

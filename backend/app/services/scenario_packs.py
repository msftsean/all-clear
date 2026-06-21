"""Maryland demo scenario packs (019-evolution-loop SPEC-4)."""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Any

from app.core.config import Settings


@dataclass(frozen=True)
class ScenarioPack:
    pack_id: str
    title: str
    domain: str
    description: str
    enabled_setting: str
    mock_seed: int
    same_signal: str
    varied_signals: tuple[str, ...]
    knowledge_seeds: tuple[str, ...]
    clearboard: dict[str, Any]


_PACKS: dict[str, ScenarioPack] = {
    "md-soc-sentinel": ScenarioPack(
        pack_id="md-soc-sentinel",
        title="Maryland SOC / Sentinel Alert Storm",
        domain="cyber-operations",
        description="State SOC receives a storm of Sentinel alerts tied to the same portal incident.",
        enabled_setting="scenario_pack_soc_sentinel_enabled",
        mock_seed=4101,
        same_signal=(
            "Microsoft Sentinel alert storm for the Maryland Workforce portal in Annapolis: "
            "same suspicious sign-ins and account lockouts continue."
        ),
        varied_signals=(
            "Microsoft Sentinel alert storm for the Maryland Workforce portal in Annapolis: suspicious sign-ins are spiking.",
            "SOC reports repeated Sentinel detections on the Maryland Workforce portal in Annapolis with account lockouts.",
            "Another Sentinel burst on the Maryland Workforce portal in Annapolis shows the same suspicious sign-ins.",
            "Maryland SOC is seeing the same Sentinel alerts for the Workforce portal in Annapolis right now.",
        ),
        knowledge_seeds=(
            "SOC runbook: triage Sentinel bursts by preserving indicator evidence and opening one major incident.",
            "Portal incident response: lock impacted identities, keep customer-comms updates batched, preserve forensic chain.",
        ),
        clearboard={
            "mode": "loaded",
            "total_signals": 912,
            "headline": "SOC surge: many alerts, one shared incident graph",
            "subhead": "Sentinel duplicates attach to the same cyber incident; magnitude shows public impact growth.",
            "incidents": [
                {
                    "incident_id": "AC-4101",
                    "title": "Workforce portal suspicious sign-in storm",
                    "location": "Annapolis SOC watch floor",
                    "queue": "compliance-desk",
                    "severity": "SEV1",
                    "report_count": 646,
                    "sla_minutes": 15,
                    "dedup_similarity": 0.95,
                    "status": "escalated",
                    "summary": "Repeated Sentinel detections collapse into one portal incident with statutory reporting pressure.",
                    "sample_signals": [
                        "Sentinel is firing repeated suspicious sign-ins on the Workforce portal.",
                        "Account lockouts are climbing from the same portal campaign.",
                    ],
                },
                {
                    "incident_id": "AC-4102",
                    "title": "Federation gateway intermittent auth failures",
                    "location": "State identity edge",
                    "queue": "engineering",
                    "severity": "SEV2",
                    "report_count": 266,
                    "sla_minutes": 60,
                    "dedup_similarity": 0.9,
                    "status": "investigating",
                    "summary": "Gateway outages are attaching to a single auth edge incident.",
                    "sample_signals": [
                        "Users cannot sign in to the workforce portal from multiple agencies.",
                        "Auth retries are timing out on the same identity edge.",
                    ],
                },
            ],
        },
    ),
    "md-311-911": ScenarioPack(
        pack_id="md-311-911",
        title="Maryland 311 / 911 City Ops",
        domain="city-operations",
        description="311 and 911 calls surge around one active life-safety scene.",
        enabled_setting="scenario_pack_311_911_enabled",
        mock_seed=4102,
        same_signal=(
            "311 and 911 are both reporting smoke and fire at Pratt Street Station in Baltimore; "
            "multiple callers describe the same active scene."
        ),
        varied_signals=(
            "311 and 911 callers report smoke from Pratt Street Station in Baltimore with people evacuating.",
            "Another 911 relay: flames visible at Pratt Street Station in Baltimore and traffic is stopped.",
            "City ops confirms repeated 311 calls about smoke at Pratt Street Station in Baltimore.",
            "Dispatch sees the same Pratt Street Station fire reports from both 311 and 911 lines.",
        ),
        knowledge_seeds=(
            "Joint 311/911 runbook: life-safety reports route to field operations and escalation immediately.",
            "Public comms template: acknowledge one active scene and avoid duplicative dispatches.",
        ),
        clearboard={
            "mode": "loaded",
            "total_signals": 1048,
            "headline": "City-ops surge: duplicate calls collapse to one scene",
            "subhead": "311/911 call bursts attach to existing incidents so responders work the event, not the noise.",
            "incidents": [
                {
                    "incident_id": "AC-4201",
                    "title": "Pratt Street Station fire scene",
                    "location": "Baltimore Pratt Street Station",
                    "queue": "field-operations",
                    "severity": "SEV1",
                    "report_count": 801,
                    "sla_minutes": 15,
                    "dedup_similarity": 0.93,
                    "status": "escalated",
                    "summary": "311 and 911 channels are converging on the same transit fire incident.",
                    "sample_signals": [
                        "Smoke at Pratt Street Station with people exiting.",
                        "911 says flames are visible at Pratt Street Station.",
                    ],
                },
                {
                    "incident_id": "AC-4202",
                    "title": "Harbor tunnel traffic-control outage",
                    "location": "Harbor tunnel approaches",
                    "queue": "engineering",
                    "severity": "SEV2",
                    "report_count": 247,
                    "sla_minutes": 60,
                    "dedup_similarity": 0.88,
                    "status": "crews dispatched",
                    "summary": "Signals about disabled controls attach to one transportation support incident.",
                    "sample_signals": [
                        "Traffic controls are dark near the tunnel approach.",
                        "Dispatch reports repeated outages on the same control segment.",
                    ],
                },
            ],
        },
    ),
    "md-water-utility": ScenarioPack(
        pack_id="md-water-utility",
        title="Maryland Water Utility Leak Surge",
        domain="utility-operations",
        description="Water-main leak reports surge around a single pressure-loss corridor.",
        enabled_setting="scenario_pack_water_utility_enabled",
        mock_seed=4103,
        same_signal=(
            "Major water main break on Frederick Road in Baltimore County is flooding intersections; "
            "multiple reports describe the same leak corridor."
        ),
        varied_signals=(
            "Water utility receives repeated flood reports from the Frederick Road main break in Baltimore County.",
            "Another report on Frederick Road: water main break is flooding lanes and lowering pressure.",
            "Field crews confirm the same Frederick Road leak surge with standing water at intersections.",
            "Residents report identical flooding from the Frederick Road main break corridor.",
        ),
        knowledge_seeds=(
            "Water-main leak playbook: isolate valves by pressure zone and preserve one master incident timeline.",
            "Customer safety guidance: avoid floodwater, report sinkhole signs, and follow boil advisories.",
        ),
        clearboard={
            "mode": "loaded",
            "total_signals": 786,
            "headline": "Utility surge: leak reports attach to one corridor incident",
            "subhead": "Duplicate flood calls merge into one water-main incident and increase magnitude.",
            "incidents": [
                {
                    "incident_id": "AC-4301",
                    "title": "Frederick Road water-main rupture",
                    "location": "Baltimore County Frederick Road corridor",
                    "queue": "field-operations",
                    "severity": "SEV2",
                    "report_count": 612,
                    "sla_minutes": 60,
                    "dedup_similarity": 0.94,
                    "status": "repair underway",
                    "summary": "Leak reports align to one major rupture with expanding local impact.",
                    "sample_signals": [
                        "Frederick Road is flooding from a water-main break.",
                        "Pressure dropped and water is pooling in the same corridor.",
                    ],
                },
                {
                    "incident_id": "AC-4302",
                    "title": "Pump station telemetry degradation",
                    "location": "North county utility zone",
                    "queue": "engineering",
                    "severity": "SEV3",
                    "report_count": 174,
                    "sla_minutes": 240,
                    "dedup_similarity": 0.86,
                    "status": "monitoring",
                    "summary": "Repeated telemetry failures are attached to one contained engineering incident.",
                    "sample_signals": [
                        "Pump telemetry keeps dropping in the same zone.",
                        "SCADA alerts repeat on one station cluster.",
                    ],
                },
            ],
        },
    ),
    "md-traffic-transport": ScenarioPack(
        pack_id="md-traffic-transport",
        title="Maryland Traffic / Transportation",
        domain="transportation-operations",
        description="Transportation hazard reports surge around one blocked corridor incident.",
        enabled_setting="scenario_pack_traffic_transport_enabled",
        mock_seed=4104,
        same_signal=(
            "Traffic operations reports a blocked I-95 ramp near Laurel with debris across lanes; "
            "multiple reports describe the same hazard location."
        ),
        varied_signals=(
            "Another transportation report: debris is blocking the same I-95 ramp near Laurel.",
            "Traffic center confirms repeated calls for the blocked Laurel I-95 ramp with lane hazards.",
            "Drivers report the same I-95 Laurel ramp obstruction and stalled traffic.",
            "State transport hotline says debris still blocks lanes on the Laurel I-95 ramp.",
        ),
        knowledge_seeds=(
            "Traffic hazard SOP: keep one incident per blockage location and attach incoming lane-status reports.",
            "Transportation comms template: lane closure updates every 15 minutes until hazard cleared.",
        ),
        clearboard={
            "mode": "loaded",
            "total_signals": 668,
            "headline": "Transportation surge: lane-hazard duplicates collapse cleanly",
            "subhead": "Ramp blockage reports attach to one incident while magnitude reflects congestion spread.",
            "incidents": [
                {
                    "incident_id": "AC-4401",
                    "title": "I-95 Laurel ramp blockage",
                    "location": "I-95 northbound ramp near Laurel",
                    "queue": "field-operations",
                    "severity": "SEV2",
                    "report_count": 503,
                    "sla_minutes": 60,
                    "dedup_similarity": 0.92,
                    "status": "crews en route",
                    "summary": "Debris and lane block reports are attaching to one transportation hazard incident.",
                    "sample_signals": [
                        "Debris blocks lanes on the Laurel I-95 ramp.",
                        "Traffic is backing up from the same blocked ramp location.",
                    ],
                },
                {
                    "incident_id": "AC-4402",
                    "title": "Signal timing controller outage",
                    "location": "Baltimore beltway corridor",
                    "queue": "engineering",
                    "severity": "SEV3",
                    "report_count": 165,
                    "sla_minutes": 240,
                    "dedup_similarity": 0.85,
                    "status": "diagnosing",
                    "summary": "Controller alerts are grouped into one contained signal-timing incident.",
                    "sample_signals": [
                        "Signal timing controller is offline across one beltway segment.",
                        "Repeated control failures are tied to the same segment controller.",
                    ],
                },
            ],
        },
    ),
}


def _is_enabled(pack: ScenarioPack, settings: Settings) -> bool:
    return bool(getattr(settings, pack.enabled_setting, True))


def list_available_packs(settings: Settings) -> list[dict[str, Any]]:
    packs: list[dict[str, Any]] = []
    for pack in _PACKS.values():
        enabled = _is_enabled(pack, settings)
        packs.append(
            {
                "pack_id": pack.pack_id,
                "title": pack.title,
                "domain": pack.domain,
                "description": pack.description,
                "enabled": enabled,
                "mock_seed": pack.mock_seed,
                "knowledge_seed_count": len(pack.knowledge_seeds),
                "signal_seed_count": len(pack.varied_signals) + 1,
            }
        )
    return packs


def get_scenario_pack(settings: Settings, pack_id: str | None = None) -> ScenarioPack:
    requested = (pack_id or settings.scenario_pack_default).strip().lower()
    pack = _PACKS.get(requested)
    if pack is None:
        raise KeyError(requested)
    if not _is_enabled(pack, settings):
        raise PermissionError(requested)
    return pack


def clearboard_for_pack(settings: Settings, pack_id: str | None = None) -> dict[str, Any]:
    return dict(get_scenario_pack(settings, pack_id).clearboard)


def scenario_signals(
    settings: Settings,
    *,
    pack_id: str | None,
    count: int,
    mode: str,
) -> list[str]:
    pack = get_scenario_pack(settings, pack_id)
    if mode == "same":
        return [pack.same_signal] * count

    rng = random.Random(pack.mock_seed)
    variants = [pack.same_signal, *pack.varied_signals]
    return [rng.choice(variants) for _ in range(count)]


def dedup_probe_signals(settings: Settings, pack_id: str) -> tuple[str, str]:
    pack = get_scenario_pack(settings, pack_id)
    return (pack.same_signal, f"{pack.same_signal} right now")


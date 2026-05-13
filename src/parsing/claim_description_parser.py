from src.schemas.claim_schema import ParsedClaimDescription


def contains_any(text: str, phrases: list[str]) -> bool:
    """
    Helper function to check whether any phrase exists in the claim text.
    """
    return any(phrase in text for phrase in phrases)


def parse_claim_description_basic(description_text: str) -> ParsedClaimDescription:
    """
    Rule-based parser for customer accident descriptions.
    This extracts structured claim fields from natural-language claim narratives.
    Later, this can be upgraded with LLM-based extraction.
    """
    text = description_text.lower()

    incident_type = None
    collision_type = None
    incident_severity = None
    property_damage = False
    police_report_available = None
    claim_state = None
    possible_fraud_signals = []

    # ------------------------------------------------------------
    # Incident Type + Collision Type
    # Specific categories must come before broad categories.
    # ------------------------------------------------------------

    # Theft
    if contains_any(
        text,
        [
            "stolen",
            "was stolen",
            "vehicle was taken",
            "recovered",
            "hot-wired",
            "hot wired",
            "steering column ripped",
            "ignition damaged",
            "catalytic converter",
            "my belongings were missing",
        ],
    ):
        incident_type = "theft"
        collision_type = None

    # Vandalism
    elif contains_any(
        text,
        [
            "vandalized",
            "vandalism",
            "key scratches",
            "keyed",
            "slashed",
            "snapped clean off",
            "paint or permanent marker",
            "scrawled",
            "purely a vandalism claim",
        ],
    ):
        incident_type = "vandalism"
        collision_type = None

    # Fire
    elif contains_any(
        text,
        [
            "fire",
            "flames",
            "smoke",
            "smelling something burning",
            "burning",
            "electrical fault",
            "fire department",
            "engine bay",
            "hood melted",
        ],
    ):
        incident_type = "fire"
        collision_type = None

    # Flood / water damage
    elif contains_any(
        text,
        [
            "flood",
            "flash flood",
            "water damage",
            "water had risen",
            "steering wheel inside the cabin",
            "interior is completely soaked",
            "engine won't even turn over",
        ],
    ):
        incident_type = "weather"
        collision_type = "flood damage"

    # Hail damage
    elif contains_any(
        text,
        [
            "hail",
            "hailstorm",
            "hail storm",
            "golf ball sized hail",
            "pdr",
            "paintless dent",
            "individual dimples",
        ],
    ):
        incident_type = "weather"
        collision_type = "hail damage"

    # Falling object / tree branch
    elif contains_any(
        text,
        [
            "tree branch",
            "falling tree",
            "fallen tree",
            "falling-object",
            "falling object",
            "large branch",
            "oak tree",
            "fell directly on top",
            "tree service",
        ],
    ):
        incident_type = "falling object"
        collision_type = "tree / falling object damage"

    # Animal collision
    elif contains_any(
        text,
        [
            "hit a deer",
            "deer",
            "animal strike",
            "blood and fur",
            "animal control",
        ],
    ):
        incident_type = "animal collision"
        collision_type = "animal impact"

    # Multi-vehicle / pileup
    elif contains_any(
        text,
        [
            "pileup",
            "pile up",
            "chain reaction",
            "5-car",
            "multi vehicle",
            "multi-vehicle",
            "damage front and back",
            "front and back",
        ],
    ):
        incident_type = "collision"
        collision_type = "multi-vehicle collision"

    # Head-on / severe front collision
    elif contains_any(
        text,
        [
            "head-on",
            "head on",
            "front-to-front",
            "center line",
            "crossed the center line",
            "collided pretty much front-to-front",
            "front of my car is folded",
        ],
    ):
        incident_type = "collision"
        collision_type = "front-end collision"

    # Pothole / road hazard
    elif contains_any(
        text,
        [
            "pothole",
            "road impact damage",
            "bent control arm",
            "blown front shock",
            "wheel rim is cracked",
            "front tire had to be replaced",
            "grinding noise from the front end",
        ],
    ):
        incident_type = "road hazard"
        collision_type = "pothole / road impact"

    # Mechanical breakdown with separate physical damage
    elif contains_any(
        text,
        [
            "broke down",
            "transmission gave out",
            "mechanical breakdown",
            "mechanical failure",
            "called for a tow",
            "waiting for a tow",
        ],
    ):
        incident_type = "mechanical / other"
        collision_type = "mechanical breakdown with possible debris damage"

    # Road debris / windshield glass claim
    elif contains_any(
        text,
        [
            "kicked up a big rock",
            "slammed right into my windshield",
            "small chip",
            "14-inch crack",
            "line of sight",
            "full replacement",
            "debris damage",
            "wind blast kicked up some debris",
        ],
    ):
        incident_type = "comprehensive"
        collision_type = "road debris / glass damage"

    # Rear-end collision
    elif contains_any(
        text,
        [
            "rear-ended",
            "rear ended",
            "hit from behind",
            "slammed into the back",
            "crashed into the back",
            "ran into the back",
            "back of my car",
            "rear bumper",
            "car behind me hit me",
        ],
    ):
        incident_type = "collision"
        collision_type = "rear-end collision"

    # Side collision / sideswipe / red-light side impact
    elif contains_any(
        text,
        [
            "sideswiped",
            "side-swiped",
            "side collision",
            "side impact",
            "merged into me",
            "without signaling",
            "t-boned",
            "t boned",
            "t-bone",
            "hit me on the driver side",
            "blew the red light",
            "clipping my front passenger side",
            "driver side from the front wheel",
            "passenger side fender",
            "driver door is caved",
        ],
    ):
        incident_type = "collision"
        collision_type = "side collision"

    # Hit and run / parked hit
    elif contains_any(
        text,
        [
            "hit-and-run",
            "hit and run",
            "no note",
            "parked my car",
            "someone definitely hit my car",
            "just took off",
            "no plate",
            "no info on who hit me",
            "other vehicle was gone",
            "didn't catch the plate",
        ],
    ):
        incident_type = "collision"
        collision_type = "hit and run"

    # General front-end collision
    elif contains_any(
        text,
        [
            "front bumper",
            "front end",
            "front-end",
            "front of my car",
        ],
    ):
        incident_type = "collision"
        collision_type = "front-end collision"

    else:
        incident_type = "unknown"
        collision_type = None

    # ------------------------------------------------------------
    # Severity
    # ------------------------------------------------------------

    if contains_any(
        text,
        [
            "total loss",
            "totaled",
            "completely destroyed",
            "every airbag deployed",
            "airbags deployed",
            "airbag deployed",
            "frame is visibly bent",
            "frame damage",
            "b-pillar",
            "wasn't driveable",
            "not driveable",
            "isn't safe to drive",
            "had to be towed",
            "had to be towed away",
            "ambulance",
            "taken to the er",
            "hospital",
            "broken collarbone",
            "concussion",
            "front half of the car is basically destroyed",
            "engine bay is gutted",
            "water had risen up to the steering wheel",
            "engine won't even turn over",
        ],
    ):
        incident_severity = "high"

    elif contains_any(
        text,
        [
            "minor damage",
            "pretty minor damage",
            "small scratch",
            "light damage",
            "small dent",
            "cosmetic",
            "just the windshield",
            "no other vehicle damage",
            "just the mirror",
        ],
    ):
        incident_severity = "low"

    elif contains_any(
        text,
        [
            "crushed",
            "smashed",
            "cracked",
            "dented",
            "scraped",
            "scratches",
            "shattered",
            "hanging off",
            "buckled",
            "leaking coolant",
            "bent",
            "misaligned",
            "deep dent",
            "doesn't latch",
            "does not latch",
            "damage underneath",
            "sore",
            "bruised",
        ],
    ):
        incident_severity = "medium"

    else:
        incident_severity = "medium"

    # ------------------------------------------------------------
    # Property Damage
    # Only external non-vehicle property.
    # ------------------------------------------------------------

    if contains_any(
        text,
        [
            "fence",
            "garage",
            "mailbox",
            "guardrail",
            "concrete barrier",
            "barrier on the right shoulder",
            "building",
            "wall",
            "utility pole",
            "light pole",
        ],
    ):
        property_damage = True
    else:
        property_damage = False

    # ------------------------------------------------------------
    # Police Report
    # Negative phrases first.
    # ------------------------------------------------------------

    if contains_any(
        text,
        [
            "no police report",
            "no police involved",
            "no police needed",
            "police were not called",
            "did not call police",
            "didn't call police",
            "didn't file a police report",
            "did not file a police report",
            "i don't think a police report is required",
            "police report is required for animal strikes",
        ],
    ):
        police_report_available = False

    elif contains_any(
        text,
        [
            "police report",
            "police were called",
            "called the police",
            "police came",
            "police came out",
            "police closed the road",
            "state troopers",
            "state police",
            "officer",
            "filed a report",
            "made a report",
            "report number",
            "case #",
            "case number",
            "incident #",
            "official report attached",
            "report attached",
            "got cited by the police",
            "cited the other driver",
            "other driver got cited",
            "arrested at the scene",
        ],
    ):
        police_report_available = True

    # ------------------------------------------------------------
    # State Detection
    # ------------------------------------------------------------

    state_keywords = {
        "illinois": "IL",
        "indiana": "IN",
        "ohio": "OH",
        " il ": "IL",
        " in ": "IN",
        " oh ": "OH",
        "i-70": "OH",
        "i-71": "OH",
        "i-80": "OH",
        "dayton": "OH",
        "route 22": "OH",
        "state route 127": "OH",
    }

    padded_text = f" {text} "
    for keyword, state_code in state_keywords.items():
        if keyword in padded_text:
            claim_state = state_code
            break

    # ------------------------------------------------------------
    # Fraud / Risk Signals
    # ------------------------------------------------------------

    if police_report_available is False and collision_type == "hit and run":
        possible_fraud_signals.append("Hit-and-run described without police report")

    if police_report_available is False and incident_type == "theft":
        possible_fraud_signals.append("Theft claim without police report")

    if contains_any(
        text,
        [
            "late report",
            "reported after",
            "weeks later",
            "days later",
            "three days later",
        ],
    ):
        possible_fraud_signals.append("Delayed claim reporting")

    if contains_any(
        text,
        [
            "no witness",
            "no witnesses",
            "nobody saw",
            "nobody saw or heard",
            "no plate",
            "no info",
        ],
    ):
        possible_fraud_signals.append("No witnesses or identifying information")

    if incident_type == "mechanical / other":
        possible_fraud_signals.append(
            "Mechanical breakdown may not be covered unless related physical damage is validated"
        )

    return ParsedClaimDescription(
        incident_type=incident_type,
        collision_type=collision_type,
        incident_severity=incident_severity,
        property_damage=property_damage,
        police_report_available=police_report_available,
        claim_state=claim_state,
        accident_summary=description_text.strip(),
        possible_fraud_signals=possible_fraud_signals,
    )
from collections import OrderedDict

BPRS = OrderedDict((
    (1, "Somatic concern"),
    (2, "Anxiety"),
    (3, "Depression"),
    (4, "Suicidality"),
    (5, "Guilt"),
    (6, "Hostility"),
    (7, "Elated Mood"),
    (8, "Grandiosity"),
    (9, "Suspiciousness"),
    (10, "Hallucinations"),
    (11, "Unusual thought content"),
    (12, "Bizarre behaviour"),
    (13, "Self-neglect"),
    (14, "Disorientation"),
    (15, "Conceptual disorganisation"),
    (16, "Blunted affect"),
    (17, "Emotional withdrawal"),
    (18, "Motor retardation"),
    (19, "Tension"),
    (20, "Uncooperativeness"),
    (21, "Excitement"),
    (22, "Distractibility"),
    (23, "Motor hyperactivity"),
    (24, "Mannerisms and posturing"),
))

PANNS_ITEMS = {
    "positive scale": {
        'P1': 'Delusions',
        'P2': 'Conceptual disorganization',
        'P3': 'Hallucinatory behaviour',
        'P4': 'Excitement',
        'P5': 'Grandiosity',
        'P6': 'Suspiciousness',
        'P7': 'Hostility',
    },
    "negative scale": {
        'N1': 'Blunted affect',
        'N2': 'Emotional withdrawal',
        'N3': 'Poor rapport',
        'N4': 'Passive/apathetic social withdrawal',
        'NS': 'Difficulty in abstract thinking',
        'N6': 'Lack of spontaneity and flow of conversation',
        'N7': 'Stereotyped thinking',
    },
    "general scale": {
        'G1': 'Somatic concern',
        'G2': 'Anxiety',
        'G3': 'Guilt feelings',
        'G4': 'Tension',
        'G5': 'Mannerisms & posturing',
        'G6': 'Depression',
        'G7': 'Motor retardation',
        'G8': 'Uncooperativeness',
        'G9': 'Unusual thought content',
        'G10': 'Disorientation',
        'G11': 'Poor attention',
        'G12': 'Lack of judgment and insight',
        'G13': 'Disturbance of volition',
        'G14': 'Poor impulse control',
        'G15': 'Preoccupation',
        'G16': 'Active social avoidance',
    }
}


def negative_match(keys):
    if not isinstance(keys, (tuple, list)):
        keys = [keys]

    def inner(results):
        return {key: 1 for key in keys} if results == 0 else {}
    return inner


def positive_match(keys):
    if not isinstance(keys, (tuple, list)):
        keys = [keys]

    def inner(results):
        return {key: 1 for key in keys} if results == 1 else {}
    return inner


def existence(keys):
    if not isinstance(keys, (tuple, list)):
        keys = [keys]

    def inner(results):
        return {key: 1 for key in keys} if results > 0 else {}
    return inner

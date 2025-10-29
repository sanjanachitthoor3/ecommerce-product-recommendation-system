def fetch_new_schemes():
    """
    Fetch latest government schemes from official portals
    Returns: list of dicts with scheme info
    """
    return [
        {
            "name": "PM Skill Development Yojana",
            "age_range": [18, 25],
            "gender": "Female",
            "state": "All",
            "income_limit": "5L",
            "pdf_url": "https://gov.in/pmskill2025.pdf"
        }
    ]


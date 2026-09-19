"""
Medical Systems Registry defining the 8 accredited healthcare systems:
1. Modern / Conventional Medicine
2. Ayurveda
3. Homoeopathy
4. Unani
5. Siddha
6. Sowa-Rigpa
7. Yoga & Naturopathy
8. Integrated AYUSH
"""

MEDICAL_SYSTEMS = [
    {
        "code": "modern",
        "name": "Modern / Conventional Medicine",
        "short_description": "Hospitals and clinics providing allopathic clinical care, multi-speciality diagnostics, and surgical interventions.",
        "icon": "stethoscope",
        "svg_path": '<path d="M4.5 3h15M6 3v6a6 6 0 0 0 12 0V3M12 15v4a3 3 0 0 0 3 3h1a2 2 0 0 0 2-2v-1a2 2 0 0 0-2-2h-1"></path>',
        "default_departments": [
            "General Medicine",
            "Cardiology",
            "Dermatology",
            "Orthopedics",
            "Pediatrics",
            "ENT",
            "Neurology",
            "Psychiatry",
            "General Surgery",
            "Radiology"
        ]
    },
    {
        "code": "ayurveda",
        "name": "Ayurveda",
        "short_description": "Ayurvedic healthcare facilities providing dosha assessment, Panchakarma rejuvenation, and herbal therapeutic regimens.",
        "icon": "leaf",
        "svg_path": '<path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z"></path><path d="M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 12 13 13 12"></path>',
        "default_departments": [
            "Kayachikitsa",
            "Panchakarma",
            "Shalya Tantra",
            "Shalakya Tantra",
            "Prasuti & Stri Roga",
            "Kaumarabhritya",
            "Swasthavritta"
        ]
    },
    {
        "code": "homoeopathy",
        "name": "Homoeopathy",
        "short_description": "Homoeopathic clinics offering individualised remedies based on similia similibus curentur and holistic wellness.",
        "icon": "droplet",
        "svg_path": '<path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z"></path>',
        "default_departments": [
            "General Homoeopathy",
            "Pediatrics",
            "Dermatology",
            "Chronic Diseases",
            "Respiratory Medicine",
            "Mental Health"
        ]
    },
    {
        "code": "unani",
        "name": "Unani",
        "short_description": "Unani healthcare centres practising humoral balance, Ilaj-bil-Tadbeer (regimenal therapy), and natural herbal formulations.",
        "icon": "flower",
        "svg_path": '<circle cx="12" cy="12" r="3"></circle><path d="M12 16.5A4.5 4.5 0 1 1 7.5 12 4.5 4.5 0 1 1 12 7.5a4.5 4.5 0 1 1 4.5 4.5 4.5 4.5 0 1 1-4.5 4.5"></path>',
        "default_departments": [
            "Moalijat (General Medicine)",
            "Ilaj-bil-Tadbeer (Regimenal Therapy)",
            "Ilmul Advia (Pharmacology)",
            "Jarahat (Surgery)",
            "Niswan wa Qabalat (Gynecology & Obstetrics)",
            "Amraz-e-Atfal (Pediatrics)"
        ]
    },
    {
        "code": "siddha",
        "name": "Siddha",
        "short_description": "Traditional Siddha facilities applying Mukkuttram diagnostics, Varma therapy, and mineral-herbal preparations.",
        "icon": "sun",
        "svg_path": '<circle cx="12" cy="12" r="4"></circle><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"></path>',
        "default_departments": [
            "General Siddha Medicine",
            "Pothu Maruthuvam",
            "Sirappu Maruthuvam",
            "Kuzhanthai Maruthuvam",
            "Aruvai & Maruthuvam",
            "Varma & Thokkanam"
        ]
    },
    {
        "code": "sowa_rigpa",
        "name": "Sowa-Rigpa",
        "short_description": "Traditional Himalayan healing facilities balancing Nyepa bodily humors, herbal formulations, and dietary lifestyle counsel.",
        "icon": "mountain",
        "svg_path": '<path d="m8 3 4 8 5-5 5 15H2L8 3z"></path>',
        "default_departments": [
            "General Sowa-Rigpa Medicine",
            "Internal Medicine",
            "Traditional Moxibustion & Cupping",
            "Himalayan Pharmacotherapy",
            "Mind-Body Diagnostics"
        ]
    },
    {
        "code": "yoga_naturopathy",
        "name": "Yoga & Naturopathy",
        "short_description": "Drugless healing centres combining yogic therapeutic postures, hydrotherapy, mud therapy, and lifestyle modification.",
        "icon": "activity",
        "svg_path": '<polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline>',
        "default_departments": [
            "Naturopathy Clinical OPD",
            "Therapeutic Yoga",
            "Hydrotherapy & Mud Therapy",
            "Diet & Nutrition Counseling",
            "Stress & Lifestyle Management"
        ]
    },
    {
        "code": "integrated_ayush",
        "name": "Integrated AYUSH",
        "short_description": "Multi-disciplinary healthcare institutions combining multiple AYUSH therapies with modern diagnostic assessment.",
        "icon": "layers",
        "svg_path": '<polygon points="12 2 2 7 12 12 22 7 12 2"></polygon><polyline points="2 17 12 22 22 17"></polyline><polyline points="2 12 12 17 22 12"></polyline>',
        "default_departments": [
            "Integrated Medicine OPD",
            "Ayurveda & Panchakarma",
            "Yoga & Naturopathy",
            "Homoeopathy",
            "Lifestyle & Preventive Medicine"
        ]
    }
]


def get_medical_systems_list(db=None):
    """
    Returns list of medical systems.
    If db is provided, dynamically attaches facility_count from clinics collection.
    """
    systems = []
    for ms in MEDICAL_SYSTEMS:
        item = dict(ms)
        if db is not None:
            # Count matching clinics
            count = db.clinics.count_documents({
                "$or": [
                    {"medical_system": ms["name"]},
                    {"medical_system": ms["code"]},
                    {"medical_system": {"$regex": f"^{ms['name']}$", "$options": "i"}}
                ]
            })
            item["facility_count"] = count
        else:
            item["facility_count"] = 0
        systems.append(item)
    return systems


def get_system_by_code_or_name(identifier):
    """Resolve medical system by code or name."""
    if not identifier:
        return None
    ident = identifier.strip().lower()
    for ms in MEDICAL_SYSTEMS:
        if ms["code"].lower() == ident or ms["name"].lower() == ident:
            return ms
    return None

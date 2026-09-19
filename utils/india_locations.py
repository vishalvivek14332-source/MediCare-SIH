"""
Comprehensive India Location Dataset covering all 28 States and 8 Union Territories
with standard districts and major cities/towns for healthcare facility filtering.
"""

INDIA_LOCATIONS = {
    # 28 States
    "Andhra Pradesh": {
        "districts": {
            "Anantapur": ["Anantapur", "Dharmavaram", "Guntakal", "Hindupur", "Kadiri"],
            "Chittoor": ["Chittoor", "Tirupati", "Madanapalle", "Punganur", "Srikalahasti"],
            "East Godavari": ["Kakinada", "Rajahmundry", "Amalapuram", "Samalkota"],
            "Guntur": ["Guntur", "Tenali", "Narasaraopet", "Bapatla", "Mangalagiri"],
            "Krishna": ["Vijayawada", "Machilipatnam", "Gudivada", "Nuzvid"],
            "Kurnool": ["Kurnool", "Nandyal", "Adoni", "Yemmiganur"],
            "Nellore": ["Nellore", "Kavali", "Gudur", "Venkatagiri"],
            "Prakasam": ["Ongole", "Chirala", "Markapur", "Kandukur"],
            "Srikakulam": ["Srikakulam", "Amadalavalasa", "Palasa", "Rajam"],
            "Visakhapatnam": ["Visakhapatnam", "Anakapalle", "Bheemunipatnam", "Gajuwaka"],
            "Vizianagaram": ["Vizianagaram", "Bobbili", "Parvathipuram", "Salur"],
            "West Godavari": ["Eluru", "Bhimavaram", "Tadepalligudem", "Palakollu"],
            "YSR Kadapa": ["Kadapa", "Proddatur", "Pulivendula", "Rayachoti"]
        }
    },
    "Arunachal Pradesh": {
        "districts": {
            "Papum Pare": ["Itanagar", "Naharlagun", "Doimukh"],
            "Changlang": ["Changlang", "Miao", "Jairampur"],
            "East Siang": ["Pasighat", "Ruksin"],
            "Tawang": ["Tawang", "Lumla", "Jang"],
            "West Kameng": ["Bomdila", "Rupa", "Dirang"]
        }
    },
    "Assam": {
        "districts": {
            "Kamrup Metropolitan": ["Guwahati", "Dispur", "North Guwahati"],
            "Dibrugarh": ["Dibrugarh", "Chabua", "Naharkatia"],
            "Cachar": ["Silchar", "Lakhipur", "Sonai"],
            "Jorhat": ["Jorhat", "Mariani", "Titabor"],
            "Nagaon": ["Nagaon", "Hojai", "Kampur"],
            "Sonitpur": ["Tezpur", "Dhekiajuli", "Rangapara"]
        }
    },
    "Bihar": {
        "districts": {
            "Patna": ["Patna", "Danapur", "Phulwari Sharif", "Barh", "Mokama"],
            "Gaya": ["Gaya", "Bodh Gaya", "Sherghati", "Tekari"],
            "Muzaffarpur": ["Muzaffarpur", "Motipur", "Kanti"],
            "Bhagalpur": ["Bhagalpur", "Kahalgon", "Naugachhia"],
            "Darbhanga": ["Darbhanga", "Benipur", "Baheri"],
            "Purnia": ["Purnia", "Kasba", "Banmankhi"],
            "Rohtas": ["Sasaram", "Dehri", "Bikramganj"]
        }
    },
    "Chhattisgarh": {
        "districts": {
            "Raipur": ["Raipur", "Birgaon", "Arang", "Abhanpur"],
            "Durg": ["Bhilai", "Durg", "Patan", "Kumhari"],
            "Bilaspur": ["Bilaspur", "Kota", "Takhatpur", "Ratanpur"],
            "Bastar": ["Jagdalpur", "Bastanar", "Tokapal"],
            "Rajnandgaon": ["Rajnandgaon", "Dongargarh", "Khairagarh"]
        }
    },
    "Goa": {
        "districts": {
            "North Goa": ["Panaji", "Mapusa", "Ponda", "Bicholim", "Calangute"],
            "South Goa": ["Margao", "Vasco da Gama", "Curchorem", "Cuncolim", "Canacona"]
        }
    },
    "Gujarat": {
        "districts": {
            "Ahmedabad": ["Ahmedabad", "Sanand", "Dholka", "Viramgam", "Dhandhuka"],
            "Surat": ["Surat", "Bardoli", "Mandvi", "Vyara", "Kamrej"],
            "Vadodara": ["Vadodara", "Padra", "Karjan", "Dabhoi", "Savli"],
            "Rajkot": ["Rajkot", "Gondal", "Jetpur", "Dhoraji", "Morbi"],
            "Bhavnagar": ["Bhavnagar", "Palitana", "Mahuva", "Sihor"],
            "Jamnagar": ["Jamnagar", "Dhrol", "Kalavad"],
            "Gandhinagar": ["Gandhinagar", "Kalol", "Mansa", "Dehgam"]
        }
    },
    "Haryana": {
        "districts": {
            "Gurugram": ["Gurugram", "Sohna", "Pataudi", "Manesar"],
            "Faridabad": ["Faridabad", "Ballabgarh", "Badkhal"],
            "Hisar": ["Hisar", "Hansi", "Barwala"],
            "Karnal": ["Karnal", "Gharaunda", "Assandh", "Nilokheri"],
            "Ambala": ["Ambala Cantt", "Ambala City", "Barara", "Naraingarh"],
            "Rohtak": ["Rohtak", "Meham", "Sampla"],
            "Panchkula": ["Panchkula", "Kalka", "Pinjore"]
        }
    },
    "Himachal Pradesh": {
        "districts": {
            "Shimla": ["Shimla", "Rampur", "Theog", "Rohru"],
            "Kangra": ["Dharamshala", "Kangra", "Palampur", "Nurpur", "Dehra"],
            "Mandi": ["Mandi", "Sundernagar", "Sarkaghat", "Jogindernagar"],
            "Kullu": ["Kullu", "Manali", "Banjar", "Anni"],
            "Solan": ["Solan", "Baddi", "Nalagarh", "Parwanoo"]
        }
    },
    "Jharkhand": {
        "districts": {
            "Ranchi": ["Ranchi", "Bundu", "Kanke", "Hatia"],
            "East Singhbhum": ["Jamshedpur", "Ghatshila", "Musabani"],
            "Dhanbad": ["Dhanbad", "Jharia", "Katras", "Sindri"],
            "Bokaro": ["Bokaro Steel City", "Chas", "Bermo"],
            "Hazaribagh": ["Hazaribagh", "Barhi", "Barkagaon"]
        }
    },
    "Karnataka": {
        "districts": {
            "Bengaluru Urban": ["Bengaluru", "Yelahanka", "Kengeri", "Whitefield", "Electronic City"],
            "Bengaluru Rural": ["Doddaballapura", "Devanahalli", "Hosakote", "Nelamangala"],
            "Mysuru": ["Mysuru", "Nanjangud", "Hunsur", "T. Narasipura"],
            "Dakshina Kannada": ["Mangaluru", "Bantwal", "Puttur", "Belthangady", "Sullia"],
            "Dharwad": ["Hubballi", "Dharwad", "Kalghatgi", "Kundgol"],
            "Belagavi": ["Belagavi", "Gokak", "Chikkodi", "Bailhongal"],
            "Kalaburagi": ["Kalaburagi", "Sedam", "Chittapur", "Aland"],
            "Shivamogga": ["Shivamogga", "Bhadravati", "Sagara", "Shikaripura"],
            "Udupi": ["Udupi", "Manipal", "Kundapura", "Karkala"]
        }
    },
    "Kerala": {
        "districts": {
            "Kannur": ["Kannur", "Thalassery", "Payyanur", "Taliparamba", "Mattannur", "Iritty", "Panoor"],
            "Kozhikode": ["Kozhikode", "Vadakara", "Koyilandy", "Feroke", "Ramanattukara"],
            "Ernakulam": ["Kochi", "Aluva", "Angamaly", "Perumbavoor", "Muvattupuzha", "Tripunithura"],
            "Thiruvananthapuram": ["Thiruvananthapuram", "Neyyattinkara", "Attingal", "Nedumangad", "Varkala"],
            "Thrissur": ["Thrissur", "Chalakudy", "Kodungallur", "Guruvayur", "Kunnamkulam"],
            "Malappuram": ["Malappuram", "Manjeri", "Perinthalmanna", "Tirur", "Ponnani"],
            "Palakkad": ["Palakkad", "Ottapalam", "Shoranur", "Chittur", "Mannarkkad"],
            "Kollam": ["Kollam", "Karunagappally", "Punalur", "Paravur", "Kottarakkara"],
            "Alappuzha": ["Alappuzha", "Cherthala", "Kayamkulam", "Mavelikkara", "Chengannur"],
            "Kottayam": ["Kottayam", "Pala", "Changanassery", "Vaikom", "Ettumanoor"],
            "Kasaragod": ["Kasaragod", "Kanhangad", "Nileshwaram", "Uppala"],
            "Wayanad": ["Kalpetta", "Sulthan Bathery", "Mananthavady"],
            "Idukki": ["Thodupuzha", "Munnar", "Adimali", "Kattappana"],
            "Pathanamthitta": ["Pathanamthitta", "Thiruvalla", "Adoor", "Ranni"]
        }
    },
    "Madhya Pradesh": {
        "districts": {
            "Bhopal": ["Bhopal", "Berasia", "Kolar"],
            "Indore": ["Indore", "Mhow", "Sanwer", "Depalpur"],
            "Gwalior": ["Gwalior", "Dabra", "Bhitarwar"],
            "Jabalpur": ["Jabalpur", "Sihora", "Patan"],
            "Ujjain": ["Ujjain", "Nagda", "Khachrod", "Mahidpur"]
        }
    },
    "Maharashtra": {
        "districts": {
            "Mumbai": ["Mumbai", "Colaba", "Dadar", "Bandra", "Andheri", "Borivali"],
            "Pune": ["Pune", "Pimpri-Chinchwad", "Baramati", "Shirur", "Lonavala"],
            "Nagpur": ["Nagpur", "Kamthi", "Umred", "Katol"],
            "Thane": ["Thane", "Kalyan-Dombivli", "Navi Mumbai", "Ulhasnagar", "Bhiwandi"],
            "Nashik": ["Nashik", "Malegaon", "Sinnar", "Deolali"],
            "Aurangabad": ["Chhatrapati Sambhajinagar", "Paithan", "Vaijapur", "Gangapur"],
            "Solapur": ["Solapur", "Pandharpur", "Barshi", "Akkalkot"],
            "Kolhapur": ["Kolhapur", "Ichalkaranji", "Jaysingpur", "Kagal"]
        }
    },
    "Manipur": {
        "districts": {
            "Imphal West": ["Imphal", "Lamphelpat", "Lamsang"],
            "Imphal East": ["Porompat", "Sawombung", "Keirao"],
            "Churachandpur": ["Churachandpur", "Tuibong"],
            "Thoubal": ["Thoubal", "Kakching", "Yairipok"]
        }
    },
    "Meghalaya": {
        "districts": {
            "East Khasi Hills": ["Shillong", "Sohra (Cherrapunji)", "Pynursla"],
            "West Garo Hills": ["Tura", "Phulbari", "Dalu"],
            "Ri-Bhoi": ["Nongpoh", "Umsning", "Byrnihat"]
        }
    },
    "Mizoram": {
        "districts": {
            "Aizawl": ["Aizawl", "Durtlang", "Tanhril"],
            "Lunglei": ["Lunglei", "Tlabung"],
            "Champhai": ["Champhai", "Khawzawl"]
        }
    },
    "Nagaland": {
        "districts": {
            "Kohima": ["Kohima", "Chiephobozou", "Tseminyu"],
            "Dimapur": ["Dimapur", "Chumukedima", "Medziphema"],
            "Mokokchung": ["Mokokchung", "Tuli", "Changtongya"]
        }
    },
    "Odisha": {
        "districts": {
            "Khurda": ["Bhubaneswar", "Jatni", "Khordha"],
            "Cuttack": ["Cuttack", "Choudwar", "Athagarh"],
            "Ganjam": ["Berhampur", "Chhatrapur", "Hinjilicut"],
            "Sundargarh": ["Rourkela", "Sundargarh", "Rajgangpur"],
            "Puri": ["Puri", "Konark", "Pipili"]
        }
    },
    "Punjab": {
        "districts": {
            "Ludhiana": ["Ludhiana", "Jagraon", "Khanna", "Samrala"],
            "Amritsar": ["Amritsar", "Ajnala", "Attari", "Majitha"],
            "Jalandhar": ["Jalandhar", "Nakodar", "Phillaur", "Kartarpur"],
            "Patiala": ["Patiala", "Nabha", "Rajpura", "Samana"],
            "SAS Nagar (Mohali)": ["Mohali", "Kharar", "Dera Bassi", "Zirakpur"],
            "Bathinda": ["Bathinda", "Rampura Phul", "Talwandi Sabo"]
        }
    },
    "Rajasthan": {
        "districts": {
            "Jaipur": ["Jaipur", "Amer", "Sanganer", "Chomu", "Bagru"],
            "Jodhpur": ["Jodhpur", "Bilara", "Phalodi", "Piparcity"],
            "Udaipur": ["Udaipur", "Fatehnagar", "Kherwara"],
            "Kota": ["Kota", "Ramganj Mandi", "Sangod"],
            "Ajmer": ["Ajmer", "Pushkar", "Kishangarh", "Beawar"],
            "Bikaner": ["Bikaner", "Nokha", "Deshnoke"]
        }
    },
    "Sikkim": {
        "districts": {
            "East Sikkim": ["Gangtok", "Singtam", "Rangpo"],
            "South Sikkim": ["Namchi", "Jorethang", "Ravangla"],
            "West Sikkim": ["Geyzing", "Pelling", "Soreng"],
            "North Sikkim": ["Mangan", "Chungthang"]
        }
    },
    "Tamil Nadu": {
        "districts": {
            "Chennai": ["Chennai", "Adayar", "T. Nagar", "Anna Nagar", "Tambaram", "Guindy"],
            "Coimbatore": ["Coimbatore", "Pollachi", "Mettupalayam", "Sulur"],
            "Madurai": ["Madurai", "Melur", "Thirumangalam", "Usilampatti"],
            "Tiruchirappalli": ["Tiruchirappalli", "Srirangam", "Manapparai", "Thuraiyur"],
            "Salem": ["Salem", "Attur", "Mettur", "Omalur"],
            "Tirunelveli": ["Tirunelveli", "Palayamkottai", "Ambasamudram"],
            "Kanyakumari": ["Nagercoil", "Kanyakumari", "Padmanabhapuram", "Colachel"],
            "Vellore": ["Vellore", "Katpadi", "Gudiyatham"],
            "Erode": ["Erode", "Bhavani", "Gobichettipalayam", "Perundurai"]
        }
    },
    "Telangana": {
        "districts": {
            "Hyderabad": ["Hyderabad", "Secunderabad", "Charminar", "Jubilee Hills", "Gachibowli"],
            "Ranga Reddy": ["Shamshabad", "Rajendranagar", "Ibrahimpatnam"],
            "Medchal-Malkajgiri": ["Kukatpally", "Malkajgiri", "Medchal", "Alwal"],
            "Warangal Urban": ["Warangal", "Hanamkonda", "Kazipet"],
            "Karimnagar": ["Karimnagar", "Huzurabad", "Jammikunta"],
            "Nizamabad": ["Nizamabad", "Bodhan", "Armoor"]
        }
    },
    "Tripura": {
        "districts": {
            "West Tripura": ["Agartala", "Ranirbazar", "Mohanpur"],
            "Gomati": ["Udaipur", "Amarpur"],
            "North Tripura": ["Dharmanagar", "Kanchanpur"]
        }
    },
    "Uttar Pradesh": {
        "districts": {
            "Lucknow": ["Lucknow", "Malihabad", "Mohanlalganj"],
            "Kanpur Nagar": ["Kanpur", "Ghatampur", "Bilhaur"],
            "Varanasi": ["Varanasi", "Pindra", "Ramnagar"],
            "Prayagraj": ["Prayagraj", "Phulpur", "Koraon"],
            "Agra": ["Agra", "Fatehabad", "Kheragarh"],
            "Gautam Buddha Nagar": ["Noida", "Greater Noida", "Dadri"],
            "Ghaziabad": ["Ghaziabad", "Modinagar", "Muradnagar"],
            "Meerut": ["Meerut", "Sardhana", "Mawana"],
            "Gorakhpur": ["Gorakhpur", "Sahjanwa", "Campierganj"],
            "Bareilly": ["Bareilly", "Aonla", "Baheri"]
        }
    },
    "Uttarakhand": {
        "districts": {
            "Dehradun": ["Dehradun", "Rishikesh", "Mussoorie", "Vikasnagar"],
            "Haridwar": ["Haridwar", "Roorkee", "Laksar"],
            "Nainital": ["Nainital", "Haldwani", "Ramnagar"],
            "Udham Singh Nagar": ["Rudrapur", "Kashipur", "Kichha"],
            "Almora": ["Almora", "Ranikhet", "Dwarahat"]
        }
    },
    "West Bengal": {
        "districts": {
            "Kolkata": ["Kolkata", "Alipore", "Salt Lake", "Ballygunge", "Dum Dum"],
            "North 24 Parganas": ["Barasat", "Barrackpore", "Bidhannagar", "Bhatpara"],
            "South 24 Parganas": ["Baruipur", "Diamond Harbour", "Alipore"],
            "Howrah": ["Howrah", "Bally", "Uluberia"],
            "Darjeeling": ["Darjeeling", "Siliguri", "Kurseong"],
            "Paschim Bardhaman": ["Asansol", "Durgapur"],
            "Murshidabad": ["Baharampur", "Jangipur", "Kandi"]
        }
    },

    # 8 Union Territories
    "Andaman and Nicobar Islands": {
        "districts": {
            "South Andaman": ["Port Blair", "Ferrargunj"],
            "North and Middle Andaman": ["Mayabunder", "Diglipur", "Rangat"],
            "Nicobar": ["Car Nicobar", "Great Nicobar"]
        }
    },
    "Chandigarh": {
        "districts": {
            "Chandigarh": ["Chandigarh", "Sector 17", "Sector 35", "Manimajra"]
        }
    },
    "Dadra and Nagar Haveli and Daman and Diu": {
        "districts": {
            "Daman": ["Daman", "Nani Daman", "Moti Daman"],
            "Diu": ["Diu", "Ghoghla"],
            "Dadra and Nagar Haveli": ["Silvassa", "Amli"]
        }
    },
    "Delhi": {
        "districts": {
            "New Delhi": ["New Delhi", "Connaught Place", "Chanakyapuri"],
            "Central Delhi": ["Daryaganj", "Karol Bagh", "Pahar Ganj"],
            "South Delhi": ["Saket", "Hauz Khas", "Greater Kailash", "Mehrauli"],
            "South West Delhi": ["Dwarka", "Vasant Kunj", "Najafgarh"],
            "North Delhi": ["Civil Lines", "Model Town", "Narela"],
            "East Delhi": ["Preet Vihar", "Mayur Vihar", "Laxmi Nagar"],
            "West Delhi": ["Rajouri Garden", "Punjabi Bagh", "Janakpuri"]
        }
    },
    "Jammu and Kashmir": {
        "districts": {
            "Srinagar": ["Srinagar", "Hazratbal", "Khanyar"],
            "Jammu": ["Jammu", "Bishnah", "Akhnoor", "R.S. Pura"],
            "Anantnag": ["Anantnag", "Pahalgam", "Bijbehara"],
            "Baramulla": ["Baramulla", "Sopore", "Gulmarg"]
        }
    },
    "Ladakh": {
        "districts": {
            "Leh": ["Leh", "Nubra", "Diskit", "Nyoma", "Khalsi"],
            "Kargil": ["Kargil", "Drass", "Zanskar", "Sankoo"]
        }
    },
    "Lakshadweep": {
        "districts": {
            "Lakshadweep": ["Kavaratti", "Agatti", "Amini", "Andrott", "Minicoy"]
        }
    },
    "Puducherry": {
        "districts": {
            "Puducherry": ["Puducherry", "Oulgaret", "Villianur"],
            "Karaikal": ["Karaikal", "Nedungadu"],
            "Mahe": ["Mahe", "Pandakkal"],
            "Yanam": ["Yanam"]
        }
    }
}


def get_all_states():
    """Return sorted list of all 28 states and 8 Union Territories."""
    return sorted(list(INDIA_LOCATIONS.keys()))


def get_districts_by_state(state):
    """Return sorted list of districts for a given State/UT."""
    if not state:
        return []
    # Case-insensitive match
    for s_name, data in INDIA_LOCATIONS.items():
        if s_name.lower() == state.strip().lower():
            return sorted(list(data["districts"].keys()))
    return []


def get_cities_by_district(state, district):
    """Return sorted list of cities/towns for a given State and District."""
    if not state or not district:
        return []
    state_clean = state.strip().lower()
    district_clean = district.strip().lower()

    for s_name, s_data in INDIA_LOCATIONS.items():
        if s_name.lower() == state_clean:
            for d_name, cities in s_data["districts"].items():
                if d_name.lower() == district_clean:
                    return sorted(cities)
    return []

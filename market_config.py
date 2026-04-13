"""
Market Configuration for Real Estate Dashboard
Defines market-specific parameters for DC, Miami, and other markets
"""

MARKETS = {
    "DC Metro": {
        "name": "Washington DC / Arlington / Alexandria",
        "short": "DC Metro",
        "jurisdictions": ["Washington DC", "Arlington", "Alexandria", "Richmond"],
        "data_source": "data/dc",
        "fmr_file": "data/dc/hud_fmr_2025.csv",
        "geo_file": "data/dc/dc_zcta.geojson",
        "tax_rates": {
            "Washington DC": 0.0085,
            "Arlington": 0.0107,
            "Alexandria": 0.0107,
            "Richmond": 0.0087,
        },
        "tax_type": "homesteaded",  # Note: DC has homestead deduction
        "homestead_deduction": 87500,
        "capital_gains_rate": 0.1075,  # DC rate
        "avg_insurance": 1300,
        "avg_hoa_monthly": 450,
        "vacancy_rate": 0.06,
        "maintenance_pct": 0.01,
        "zip_jurisdiction_func": "zip_jurisdiction_dc",
        "zip_labels": {
            "20001": "Shaw / U St", "20002": "Capitol Hill NE", "20003": "Capitol Hill SE",
            "20004": "Penn Quarter", "20005": "Downtown", "20006": "Foggy Bottom",
            "20007": "Georgetown", "20008": "Cleveland Pk", "20009": "Adams Morgan",
            "20010": "Columbia Heights", "20011": "Petworth", "20012": "Shepherd Park",
            "20015": "Chevy Chase DC", "20016": "Tenleytown", "20017": "Brookland",
            "20018": "Woodridge", "20019": "Deanwood", "20020": "Anacostia",
            "20024": "SW Waterfront", "20032": "Congress Hts", "20036": "Dupont Circle",
            "20037": "West End",
            "22201": "Clarendon", "22202": "Crystal City", "22203": "Ballston",
            "22204": "Columbia Pike", "22205": "Westover", "22206": "Fairlington",
            "22207": "Chain Bridge", "22209": "Rosslyn",
            "22301": "Del Ray", "22302": "Jefferson Park", "22303": "Groveton",
            "22304": "Seminary", "22305": "Arlandria", "22306": "Belle View",
            "22307": "Fort Hunt", "22308": "Waynewood", "22309": "Mt Vernon S",
            "22310": "Franconia", "22311": "Lincolnia", "22312": "Pinecrest",
            "22314": "Old Town", "22315": "Kingstowne",
        },
        "colors": {
            "Washington DC": "#002245",
            "Arlington": "#0071BC",
            "Alexandria": "#EC553A",
            "Richmond": "#795548",
        },
    },
    "Miami-Fort Lauderdale": {
        "name": "Miami-Dade / Broward County",
        "short": "Miami-Fort Lauderdale",
        "jurisdictions": ["Miami-Dade", "Broward"],
        "data_source": "data/miami",
        "fmr_file": "data/national/hud_fmr_new_metros.csv",
        "geo_file": "data/miami/miami_zcta.geojson",
        "tax_rates": {
            "Miami-Dade": 0.0115,  # Non-homesteaded (investment property)
            "Broward": 0.0085,      # Non-homesteaded (investment property)
        },
        "tax_type": "non_homesteaded",  # Rental properties: no homestead exemption
        "homestead_deduction": 0,  # Does not apply to rental properties
        "capital_gains_rate": 0.06,  # Florida (no income tax, cap gains vary)
        "avg_insurance": 2750,  # 0.55% of $500K property - much higher due to hurricane risk
        "avg_hoa_monthly": 300,
        "vacancy_rate": 0.08,  # Slightly higher coastal vacancy
        "maintenance_pct": 0.01,
        "zip_jurisdiction_func": "zip_jurisdiction_miami",
        "zip_labels": {
            "33010": "Palmetto", "33011": "Kendale", "33012": "Westchester",
            "33013": "Kendall", "33014": "Kendall", "33015": "Kendall Heights",
            "33016": "Kendall", "33017": "Westchester", "33018": "Kendall",
            "33030": "Palmetto", "33031": "Homestead", "33032": "Homestead",
            "33033": "Palmetto", "33034": "Palmetto", "33035": "Homestead",
            "33039": "Homestead", "33054": "Palmetto", "33055": "Kendall",
            "33056": "Westchester", "33101": "Miami Downtown", "33109": "Miami Beach",
            "33122": "Westchester", "33125": "Wynwood", "33126": "Allapattah",
            "33127": "Buena Vista", "33128": "Wynwood", "33129": "Buena Vista",
            "33130": "Wynwood", "33131": "Midtown", "33132": "Wynwood",
            "33133": "Wynwood", "33134": "Wynwood", "33135": "Wynwood",
            "33136": "Wynwood", "33137": "Wynwood", "33138": "Model City",
            "33139": "Wynwood", "33140": "Buena Vista", "33141": "Wynwood",
            "33142": "Wynwood", "33143": "Wynwood", "33144": "Wynwood",
            "33145": "Wynwood", "33146": "Wynwood", "33147": "Wynwood",
            "33149": "Wynwood", "33150": "Wynwood", "33154": "Palmetto",
            "33155": "Palmetto", "33156": "Palmetto", "33157": "Kendall",
            "33158": "Kendall", "33160": "Palmetto", "33161": "Kendall",
            "33162": "Kendall", "33163": "Kendall", "33165": "Kendall",
            "33166": "Palmetto", "33167": "Wynwood", "33168": "Model City",
            "33169": "Model City", "33170": "Wynwood", "33172": "Kendall",
            "33173": "Palmetto", "33174": "Palmetto", "33175": "Palmetto",
            "33176": "Kendall", "33177": "Kendall", "33178": "Palmetto",
            "33179": "Broward", "33180": "Wynwood", "33181": "Model City",
            "33182": "Wynwood", "33183": "Wynwood", "33184": "Wynwood",
            "33185": "Palmetto", "33186": "Wynwood", "33187": "Model City",
            "33189": "Wynwood", "33190": "Palmetto", "33193": "Palmetto",
            "33194": "Palmetto", "33196": "Palmetto",
        },
        "colors": {
            "Miami-Dade": "#FF6F00",
            "Broward": "#FF8A50",
        },
    },
}

def get_market_config(market_name):
    """Get configuration for a market."""
    return MARKETS.get(market_name)

def list_markets():
    """List available markets."""
    return list(MARKETS.keys())

def zip_jurisdiction_dc(zc):
    """Determine DC-area jurisdiction from zip code."""
    if zc.startswith("200"):
        return "Washington DC"
    elif zc.startswith("222"):
        return "Arlington"
    elif zc.startswith("223"):
        return "Alexandria"
    elif zc.startswith("231") or zc.startswith("232"):
        return "Richmond"
    return "Other"

def zip_jurisdiction_miami(zc):
    """Determine Miami-area jurisdiction from zip code."""
    if zc.startswith("330") or zc.startswith("331") or zc.startswith("332"):
        # Miami-Dade County zips
        if 33179 <= int(zc) <= 33182:  # Broward spillover
            return "Broward"
        return "Miami-Dade"
    elif 33001 <= int(zc) <= 33499:
        # Broward County
        return "Broward"
    return "Other"

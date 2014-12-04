import string,nltk,re,csv,os

def read_file(filename):
    r"""Assume the file is the format
    word \t tag
    word \t tag
    [[blank line separates sentences]]
    
    This function reads the file and returns a list of sentences.  each
    sentence is a pair (tokens, tags), each of which is a list of strings of
    the same length.
    """
    sentences = open(filename).read().strip().split("\n\n")
    ret = []
    for sent in sentences:
        lines = sent.split("\n")
        pairs = [L.split("\t") for L in lines]
        tokens = [tok for tok,tag in pairs]
        tags = [tag for tok,tag in pairs]
        ret.append( (tokens,tags) )
    return ret

def clean_str(s):
    """Clean a word string so it doesn't contain special crfsuite characters"""
    return s.replace(":","_COLON_").replace("\\", "_BACKSLASH_")

def extract_features_for_sentence1(tokens):
    N = len(tokens)
    feats_per_position = [set() for i in range(N)]
    for t in range(N):
        w = clean_str(tokens[t])
        feats_per_position[t].add("word=%s" % w)
    return feats_per_position

def extract_features_for_sentence2(tokens):
    N = len(tokens)
    feats_per_position = [set() for i in range(N)]
    PoS=nltk.pos_tag(tokens)
    for t in range(N):
        w = clean_str(tokens[t])
        feats_per_position[t].add("word=%s" %w)
        feats_per_position[t].add("wordLowerCase=%s" %w.lower())
        feats_per_position[t].add("wordUpperCase=%s" %w.upper())
        for i in range(3):
            if len(w)>i:
                feats_per_position[t].add("%iChar=%s"%(i+1,w[i]))
                feats_per_position[t].add("%iFromLastChar=%s"%(i,w[-(i+1)]))
            else:
                feats_per_position[t].add("%iChar=%s"%(i+1,""))
                feats_per_position[t].add("%iFromLastChar=%s"%(i,""))
        if "NNP" in PoS[t] or "NNPS" in PoS[t]:
            feats_per_position[t].add("NLTKIsName=%s"%True)
        else:
            feats_per_position[t].add("NLTKIsName=%s"%False)
        temp=handleSymbol(w)
        feats_per_position[t].add("hasSymbol=%s"%temp[0])
        feats_per_position[t].add("isHash=%s"%temp[1])
        feats_per_position[t].add("isMention=%s"%temp[2])
        feats_per_position[t].add("isMonth=%s"%isMonth(w))
        feats_per_position[t].add("isDay=%s"%isDay(w))
        feats_per_position[t].add("isCountry=%s"%isCountry(w))
        feats_per_position[t].add("isName=%s"%isName(w,firstNames))
        feats_per_position[t].add("isSurname=%s"%isName(w,surnames))
        feats_per_position[t].add("isBasketballTeam=%s"%isName(w,basketballTeams))
        feats_per_position[t].add("isBaseballTeam=%s"%isName(w,baseballTeams))
        feats_per_position[t].add("isFootballTeam=%s"%isName(w,footballTeams))
        feats_per_position[t].add("isHockeyTeam=%s"%isName(w,hockeyTeams))
        feats_per_position[t].add("isCity=%s"%isName(w,cityNames))
        feats_per_position[t].add("isState=%s"%isState(w))
        feats_per_position[t].add("allCaps=%s"%(w==w.upper()))
        feats_per_position[t].add("noCaps=%s"%(w==w.lower()))
        feats_per_position[t].add("capitalized=%s"%(w[0] in string.uppercase and w[1:len(w)-1]==w[1:len(w)-1].lower()))
    return feats_per_position
def readNames(file):
    readNames=csv.reader(open(file).read())
    names=[]
    holder=""
    for n in readNames:
        if n==[]:
            names.append(holder)
            holder=""
        else:
            holder+=n[0].lower()
    return names
def isName(word, names):
    if word.lower() is not "firstname" and word.lower() in names:
        if word is not "in" and word is not "an" and word is not "ward" and word is not "mark" and word is not "my":
            return True
    return False
def isCountry(word):
    countries={
        "AD",
        "ANDORRA",
        "AE",
        "UNITED ARAB EMIRATES",
        "AF",
        "AFGHANISTAN",
        "AG",
        "ANTIGUA AND BARBUDA",
        "AI",
        "ANGUILLA",
        "AL",
        "ALBANIA",
        "AM",
        "ARMENIA",
        "AN",
        "NETHERLANDS ANTILLES",
        "AO",
        "ANGOLA",
        "AQ",
        "ANTARCTICA",
        "AR",
        "ARGENTINA",
        "AS",
        "AMERICAN SAMOA",
        "AT",
        "AUSTRIA",
        "AU",
        "AUSTRALIA"
        "AW",
        "ARUBA",
        "AZ",
        "AZERBAIJAN",
        "BA",
        "BOSNIA AND HERZEGOVINA",
        "BB",
        "BARBADOS",
        "BD",
        "BANGLADESH",
        "BE",
        "BELGIUM",
        "BF",
        "BURKINA FASO"
        "BG",
        "BULGARIA",
        "BH",
        "BAHRAIN",
        "BI",
        "BURUNDI",
        "BJ",
        "BENIN",
        "BM",
        "BERMUDA",
        "BN",
        "BRUNEI DARUSSALAM",
        "BO",
        "BOLIVIA",
        "BR",
        "BRAZIL",
        "BS",
        "BAHAMAS",
        "BT",
        "BHUTAN",
        "BV",
        "BOUVET ISLAND",
        "BW",
        "BOTSWANA",
        "BY",
        "BELARUS",
        "BZ",
        "BELIZE",
        "CA",
        "CANADA",
        "CC",
        "COCOS (KEELING) ISLANDS",
        "CD",
        "CONGO, THE DEMOCRATIC REPUBLIC OF THE",
        "CF",
        "CENTRAL AFRICAN REPUBLIC",
        "CG",
        "CONGO"
        "CH",
        "SWITZERLAND"
        "CI",
        "COTE D'IVOIRE",
        "CK",
        "COOK ISLANDS",
        "CL",
        "CHILE",
        "CM",
        "CAMEROON",
        "CN",
        "CHINA",
        "CO",
        "COLOMBIA",
        "CR",
        "COSTA RICA"
        "CU",
        "CUBA",
        "CV",
        "CAPE VERDE",
        "CX",
        "CHRISTMAS ISLAND",
        "CY",
        "CYPRUS",
        "CZ",
        "CZECH REPUBLIC",
        "DE",
        "GERMANY",
        "DJ",
        "DJIBOUTI",
        "DK",
        "DENMARK",
        "DM",
        "DOMINICA",
        "DO",
        "DOMINICAN REPUBLIC",
        "DZ",
        "ALGERIA",
        "EC",
        "ECUADOR",
        "EE",
        "ESTONIA",
        "EG",
        "EGYPT",
        "EH",
        "WESTERN SARARA",
        "ER",
        "ERITREA",
        "ES",
        "SPAIN",
        "ET",
        "ETHIOPIA",
        "FI",
        "FINLAND",
        "FJ",
        "FIJI",
        "FK",
        "FALKLAND ISLANDS (MALVINAS)",
        "FM",
        "MICRONESIA, FEDERATED STATES OF",
        "FO",
        "FAROE ISLANDS",
        "FR",
        "FRANCE",
        "GA",
        "GABON",
        "GB",
        "UNITED KINGDOM",
        "GD",
        "GRENADA",
        "GE",
        "GEORGIA",
        "GF",
        "FRENCH GUIANA",
        "GH",
        "GHANA",
        "GI",
        "GIBRALTAR",
        "GL",
        "GREENLAND",
        "GM",
        "GAMBIA",
        "GN",
        "GUINEA",
        "GP",
        "GUADELOUPE",
        "GQ",
        "EQUATORIAL GUINEA",
        "GR",
        "GREECE",
        "GS",
        "SOUTH GEORGIA AND THE SOUTH SANDWICH ISLANDS",
        "GT",
        "GUATEMALA",
        "GU",
        "GUAM",
        "GW",
        "GUINEA-BISSAU",
        "GY",
        "GUYANA",
        "HK",
        "HONG KONG",
        "HM",
        "HEARD ISLAND AND MCDONALD ISLANDS",
        "HN",
        "HONDURAS",
        "HR",
        "CROATIA",
        "HT",
        "HAITI",
        "HU",
        "HUNGARY",
        "ID",
        "INDONESIA",
        "IE",
        "IRELAND",
        "IL",
        "ISRAEL",
        "IN",
        "INDIA",
        "IO",
        "BRITISH INDIAN OCEAN TERRITORY",
        "IQ",
        "IRAQ",
        "IR",
        "IRAN, ISLAMIC REPUBLIC OF",
        "IS",
        "ICELAND",
        "IT",
        "ITALY",
        "JM",
        "JAMAICA",
        "JO",
        "JORDAN",
        "JP",
        "JAPAN",
        "KE",
        "KENYA",
        "KG",
        "KYRGYZSTAN",
        "KH",
        "CAMBODIA",
        "KI",
        "KIRIBATI",
        "KM",
        "COMOROS",
        "KN",
        "SAINT KITTS AND NEVIS",
        "KP",
        "KOREA, DEMOCRATIC PEOPLE'S REPUBLIC OF",
        "KR",
        "KOREA, REPUBLIC OF",
        "KW",
        "KUWAIT",
        "KY",
        "CAYMAN ISLANDS",
        "KZ",
        "KAZAKHSTAN",
        "LA",
        "LAO PEOPLE'S DEMOCRATIC REPUBLIC",
        "LB",
        "LEBANON",
        "LC",
        "SAINT LUCIA",
        "LI",
        "LIECHTENSTEIN",
        "LK",
        "SRI LANKA",
        "LR",
        "LIBERIA",
        "LS",
        "LESOTHO",
        "LT",
        "LITHUANIA",
        "LU",
        "LUXEMBOURG",
        "LV",
        "LATVIA",
        "LY",
        "LIBYAN ARAB JAMABIRIYA",
        "MA",
        "MOROCCO",
        "MC",
        "MONACO",
        "MD",
        "MOLDOVA, REPUBLIC OF",
        "MG",
        "MADAGASCAR",
        "MH",
        "MARSHALL ISLANDS",
        "MK",
        "MACEDONIA, THE FORMER YUGOSLAV REPU8LIC OF",
        "ML",
        "MALI",
        "MM",
        "MYANMAR",
        "MN",
        "MONGOLIA",
        "MO",
        "MACAU",
        "MP",
        "NORTHERN MARIANA ISLANDS",
        "MQ",
        "MARTINIQUE",
        "MR",
        "MAURITANIA",
        "MS",
        "MONTSERRAT",
        "MT",
        "MALTA",
        "MU",
        "MAURITIUS",
        "MV",
        "MALDIVES",
        "MW",
        "MALAWI",
        "MX",
        "MEXICO",
        "MY",
        "MALAYSIA",
        "MZ",
        "MOZAMBIQUE",
        "NA",
        "NAMIBIA",
        "NC",
        "NEW CALEDONIA",
        "NE",
        "NIGER",
        "NF",
        "NORFOLK ISLAND",
        "NG",
        "NIGERIA",
        "NI",
        "NICARAGUA",
        "NL",
        "NETHERLANDS",
        "NO",
        "NORWAY",
        "NP",
        "NEPAL",
        "NU",
        "NIUE",
        "NZ",
        "NEW ZEALAND",
        "OM",
        "OMAN",
        "PA",
        "PANAMA",
        "PE",
        "PERU",
        "PF",
        "FRENCH POLYNESIA",
        "PG",
        "PAPUA NEW GUINEA",
        "PH",
        "PHILIPPINES",
        "PK",
        "PAKISTAN",
        "PL",
        "POLAND",
        "PM",
        "SAINT PIERRE AND MIQUELON",
        "PN",
        "PITCAIRN",
        "PR",
        "PUERTO RICO",
        "PT",
        "PORTUGAL",
        "PW",
        "PALAU",
        "PY",
        "PARAGUAY",
        "QA",
        "QATAR",
        "RE",
        "REUNION",
        "RO",
        "ROMANIA",
        "RU",
        "RUSSIAN FEDERATION",
        "RW",
        "RWANDA",
        "SA",
        "SAUDI ARABIA",
        "SB",
        "SOLOMON ISLANDS",
        "SC",
        "SEYCHELLES",
        "SD",
        "SUDAN",
        "SE",
        "SWEDEN",
        "SG",
        "SINGAPORE",
        "SH",
        "SAINT HELENA",
        "SI",
        "SLOVENIA",
        "SJ",
        "SVALBARD AND JAN MAYEN",
        "SK",
        "SLOVAKIA",
        "SL",
        "SIERRA LEONE",
        "SM",
        "SAN MARINO",
        "SN",
        "SENEGAL",
        "SO",
        "SOMALIA",
        "SR",
        "SURINAME",
        "ST",
        "SAO TOME AND PRINCIPE",
        "SV",
        "EL SALVADOR",
        "SY",
        "SYRIAN ARAB REPUBLIC",
        "SZ",
        "SWAZILAND",
        "TC",
        "TURKS AND CAICOS ISLANDS",
        "TD",
        "CHAD",
        "TF",
        "FRENCH SOUTHERN TERRITORIES",
        "TG",
        "TOGO",
        "TH",
        "THAILAND",
        "TJ",
        "TAJIKISTAN",
        "TK",
        "TOKELAU",
        "TM",
        "TURKMENISTAN",
        "TN",
        "TUNISIA",
        "TO",
        "TONGA",
        "TP",
        "EAST TIMOR",
        "TR",
        "TURKEY",
        "TT",
        "TRINIDAD AND TOBAGO",
        "TV",
        "TUVALU",
        "TW",
        "TAIWAN, PROVINCE OF CHINA",
        "TZ",
        "TANZANIA, UNITED REPUBLIC OF",
        "UA",
        "UKRAINE",
        "UG",
        "UGANDA",
        "UM",
        "UNITED STATES MINOR OUTLYING ISLANDS",
        "US",
        "UNITED STATES",
        "UY",
        "URUGUAY",
        "UZ",
        "UZBEKISTAN",
        "VE",
        "VENEZUELA",
        "VG",
        "VIRGIN ISLANDS, BRITISH",
        "VI",
        "VIRGIN ISLANDS, U.S.",
        "VN",
        "VIET NAM",
        "VU",
        "VANUATU",
        "WF",
        "WALLIS AND FUTUNA",
        "WS",
        "SAMOA",
        "YE",
        "YEMEN",
        "YT",
        "MAYOTTE",
        "YU",
        "YUGOSLAVIA",
        "ZA",
        "SOUTH AFRICA",
        "ZM",
        "ZAMBIA",
        "ZW",
        "ZIMBABWE",
    }
    if word.upper() in countries:
        return True
    return False
def handleSymbol(word):
    values=[False,False,False]
    if re.match("^[\w]+$",word) is None:
        values[0]=True
        if "#" in word:
            if string.find(word,"#")==0:
                values[1]=True
        if "@" in word:
            if string.find(word,"@")==0:
                values[2]=True
        if "-" in word or "_" in word:
            PoS=nltk.pos_tag(string.replace(string.replace(word,"_",""),"-",""))
            if "NNP" in PoS or "NNPS" in PoS:
                i=i
                #return "B"
    return values
def isMonth(word):
    months={
        #"jan":True,
        "january":True,
        "feb":True,
        "february":True,
        "mar":True,
        "march":True,
        "apr":True,
        #"april":True,
        "jun":True,
        #"june":True,
        "jul":True,
        "july":True,
        "aug":True,
        "august":True,
        "sep":True,
        "september":True,
        "oct":True,
        "october":True,
        "nov":True,
        "november":True,
        "dec":True,
        "december":True
    }
    if word.lower() in months:
        return True
    return False
def isState(word):
    states={
        "AK",
        "Alaska",
        "AL",
        "Alabama",
        "AR",
        "Arkansas",
        "AZ",
        "Arizona",
        "CA",
        "California",
        "CO",
        "Colorado",
        "CT",
        "Connecticut",
        "DC",
        "District Of Columbia",
        "DE",
        "Delaware",
        "FL",
        "Florida",
        "GA",
        "Georgia",
        "HI",
        "Hawaii",
        "IA",
        "Iowa",
        "ID",
        "Idaho",
        "IL",
        "Illinois",
        "IN",
        "Indiana",
        "KS",
        "Kansas",
        "KY",
        "Kentucky",
        "LA",
        "Louisiana",
        "MA",
        "Massachusetts",
        "MD",
        "Maryland",
        "ME",
        "Maine",
        "MI",
        "Michigan",
        "MN",
        "Minnesota",
        "MO",
        "Missouri",
        "MS",
        "Mississippi",
        "MT",
        "Montana",
        "NC",
        "North Carolina",
        "ND",
        "North Dakota",
        "NE",
        "Nebraska",
        "NH",
        "New Hampshire",
        "NJ",
        "New Jersey",
        "NM",
        "New Mexico",
        "NV",
        "Nevada",
        "NY",
        "New York",
        "OH",
        "Ohio",
        "OK",
        "Oklahoma",
        "OR",
        "Oregon",
        "PA",
        "Pennsylvania",
        "RI",
        "Rhode Island",
        "SC",
        "South Carolina",
        "SD",
        "South Dakota",
        "TN",
        "Tennessee",
        "TX",
        "Texas",
        "UT",
        "Utah",
        "VA",
        "Virginia",
        "VT",
        "Vermont",
        "WA",
        "Washington",
        "WI",
        "Wisconsin",
        "WV",
        "West Virginia",
        "WY",
        "Wyoming",
    }
    if word is not "ma" and word is not"ok" and word is not "or" and word is not "pa" and word is not "me" and word is not "in" and word is not "oh":
        for s in states:
            if word.lower()==s.lower():
                return True
    return False
def isDay(word):
    days={
        #"sun",
        "sunday",
        "mon",
        "monday"
        "tue",
        "tuesday",
        #"wed",
        "wednesday",
        "thu",
        "thursday",
        "fri",
        "friday",
        #"sat",
        "saturday"
    }
    if word in days:
        return True
    return False

extract_features_for_sentence = extract_features_for_sentence2

def extract_features_for_file(input_file, output_file):
    """This runs the feature extractor on input_file, and saves the output to
    output_file."""
    sents = read_file(input_file)
    with open(output_file,'w') as output_fileobj:
        for tokens,goldtags in sents:
            feats = extract_features_for_sentence(tokens)
            for t in range(len(tokens)):
                feats_tabsep = "\t".join(feats[t])
                print>>output_fileobj, "%s\t%s" % (goldtags[t],feats_tabsep)
            print>>output_fileobj, ""

#get the list of names
firstNames=readNames("CSV_Database_of_First_Names.csv")
surnames=readNames("CSV_Database_of_Last_Names.csv")
basketballTeams=readNames("basketballTeams.csv")
baseballTeams=readNames("baseballTeams.csv")
cityNames=readNames("cities.csv")
footballTeams=readNames("footballTeams.csv")
hockeyTeams=readNames("hockeyTeams.csv")
#the learned patterns
learn={}
#retrive prior learning
#if os.path.isFile("ml.csv"):
#    learn=csv.DictReader(open("ml.csv"))
extract_features_for_file("train.txt", "train.feats")
extract_features_for_file("dev.txt", "dev.feats")
#save most recent learning
#csv.DictWriter("ml.csv",learn)
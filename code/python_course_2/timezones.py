import pytz
import locale

locale.setlocale(locale.LC_ALL, "ru_RU.utf8")

_short_tz_names = {
    "Europe/Kaliningrad": "KALT",
    "Europe/Moscow":      "MSK",
    "Europe/Simferopol":  "MSK",
    "Europe/Kirov":       "MSK",
    "Europe/Astrakhan":   "SAMT",
    "Europe/Volgograd":   "SAMT",
    "Europe/Saratov":     "SAMT",
    "Europe/Ulyanovsk":   "SAMT",
    "Europe/Samara":      "SAMT",
    "Asia/Yekaterinburg": "YEKT",
    "Asia/Omsk":          "OMST",
    "Asia/Novosibirsk":   "NOVT",
    "Asia/Barnaul":       "KRAT",
    "Asia/Tomsk":         "KRAT",
    "Asia/Novokuznetsk":  "KRAT",
    "Asia/Krasnoyarsk":   "KRAT",
    "Asia/Irkutsk":       "IRKT",
    "Asia/Chita":         "YAKT",
    "Asia/Yakutsk":       "YAKT",
    "Asia/Khandyga":      "VLAT",
    "Asia/Vladivostok":   "VLAT",
    "Asia/Ust-Nera":      "VLAT",
    "Asia/Magadan":       "MAGT",
    "Asia/Sakhalin":      "MAGT",
    "Asia/Srednekolymsk": "MAGT",
    "Asia/Kamchatka":     "PETT",
    "Asia/Anadyr":        "PETT",
    "Europe/Kiev":        "EET",
    "Europe/Uzhgorod":    "EET",
    "Europe/Zaporozhye":  "EET",
    "Europe/Minsk":       "FET",
    "Asia/Almaty":        "ALMT",
    "Asia/Qyzylorda":     "QYZT",
    "Asia/Qostanay":      "ALMT",
    "Asia/Aqtobe":        "AQTT",
    "Asia/Aqtau":         "AQTT",
    "Asia/Atyrau":        "AQTT",
    "Asia/Oral":          "AQTT",
    "Asia/Samarkand":     "UZT",
    "Asia/Tashkent":      "UZT",
    "Asia/Baku":          "AZT",
    "Asia/Yerevan":       "AMT",
    "Asia/Bishkek":       "KGT",
    "Europe/Chisinau":    "EET",
    "Asia/Dushanbe":      "TJT",
    "Asia/Ashgabat":      "TMT",
    "Asia/Tbilisi":       "GET",
}
_short_tz_descriptions = {
    "KALT": "Калининградское время, Москва -1 час, UTC+2",
    "MSK": "Московское время, UTC+3",
    "SAMT": "Самарское время, Москва +1 час, UTC+4",
    "YEKT": "Екатеринбургское время, Москва +2 часа, UTC+5",
    "OMST": "Омское время, Москва +3 часа, UTC+6",
    "NOVT": "Новосибирское время, Москва +4 часа, UTC+7",
    "KRAT": "Красноярское время, Москва +4 часа, UTC+7",
    "IRKT": "Иркутское время, Москва +5 часов, UTC+8",
    "YAKT": "Якутское время, Москва +6 часов, UTC+9",
    "VLAT": "Владивостокское время, Москва +7 часов, UTC+10",
    "MAGT": "Магаданское время, Москва +8 часов, UTC+11",
    "PETT": "Камчатское время, Москва +9 часов, UTC+12",
    "EET": "Восточноевропейское время (летнее UTC+3, зимнее UTC+2)",
    "FET": "Дальневосточноевропейское время, UTC+3",
    "ALMT": "Время Алматы, UTC+6",
    "AQTT": "Время Актобе, UTC+5",
    "QYZT": "Время Кызылорды, UTC+5",
    "UZT": "Время Узбекистана, UTC+5",
    "AZT": "Время Азербайджана (летнее UTC+5, зимнее UTC+4)",
    "AMT": "Время Армении, UTC+4",
    "KGT": "Время Кыргыстана, UTC+6",
    "TJT": "Время Таджикистана, UTC+5",
    "TMT": "Время Туркменистана, UTC+5",
    "GET": "Время Грузии, UTC+4"
}
_translations_countries = [
    ("RU", "Россия"),
    ("BY", "Белоруссия"),
    ("UA", "Украина"),
    ("KZ", "Казахстан"),
    ("AZ", "Азербайджан"),
    ("AM", "Армения"),
    ("GE", "Грузия"),
    ("KG", "Кыргызстан"),
    ("MD", "Молдавия"),
    ("TJ", "Таджикистан"),
    ("TM", "Туркменистан"),
    ("UZ", "Узбекистан"),
]
_translations_tz = {
    "Europe/Kaliningrad": "Калининград",
    "Europe/Moscow":      "Москва",
    "Europe/Simferopol":  "Симферополь",
    "Europe/Kirov":       "Киров",
    "Europe/Astrakhan":   "Астрахань",
    "Europe/Volgograd":   "Волгоград",
    "Europe/Saratov":     "Саратов",
    "Europe/Ulyanovsk":   "Ульяновск",
    "Europe/Samara":      "Самара",
    "Asia/Yekaterinburg": "Екатеринбург",
    "Asia/Omsk":          "Омск",
    "Asia/Novosibirsk":   "Новосибирск",
    "Asia/Barnaul":       "Барнаул",
    "Asia/Tomsk":         "Томск",
    "Asia/Novokuznetsk":  "Новокузнецк",
    "Asia/Krasnoyarsk":   "Красноярск",
    "Asia/Irkutsk":       "Иркутск",
    "Asia/Chita":         "Чита",
    "Asia/Yakutsk":       "Якутск",
    "Asia/Khandyga":      "Хандыга",
    "Asia/Vladivostok":   "Владивосток",
    "Asia/Ust-Nera":      "Усть-Нера",
    "Asia/Magadan":       "Магадан",
    "Asia/Sakhalin":      "Сахалин",
    "Asia/Srednekolymsk": "Среднеколымск",
    "Asia/Kamchatka":     "Камчатка",
    "Asia/Anadyr":        "Анадырь",
    "Europe/Kiev":        "Киев",
    "Europe/Uzhgorod":    "Ужгород",
    "Europe/Zaporozhye":  "Запорожье",
    "Europe/Minsk":       "Минск",
    "Asia/Almaty":        "Алматы",
    "Asia/Qyzylorda":     "Кызылорда",
    "Asia/Qostanay":      "Костанай",
    "Asia/Aqtobe":        "Актобе",
    "Asia/Aqtau":         "Актау",
    "Asia/Atyrau":        "Атырау",
    "Asia/Oral":          "Уральск",
    "Asia/Samarkand":     "Самарканд",
    "Asia/Tashkent":      "Ташкент",
    "Asia/Baku":          "Баку",
    "Asia/Yerevan":       "Ереван",
    "Asia/Bishkek":       "Бишкек",
    "Europe/Chisinau":    "Кишинёв",
    "Asia/Dushanbe":      "Душанбе",
    "Asia/Ashgabat":      "Ашхабад",
    "Asia/Tbilisi":       "Тбилиси",
}

def make_readable_utc_offset(dt):
    utcshift = dt.strftime("%z")
    if not utcshift:
        return ""
    if utcshift.endswith("00"):
        utcshift = utcshift[:-2]
    else:
        utcshift = "{}:{}".format(utcshift[:-2], utcshift[-2:])
    if utcshift[1] == "0":
        utcshift = utcshift[0] + utcshift[2:]
    return "UTC{}".format(utcshift)

def make_tz_shortname_for(datetime):
    name = datetime.tzinfo.zone
    if name in _short_tz_names:
        shortname = _short_tz_names[name]
        description = _short_tz_descriptions.get(shortname, "")
    else:
        shortname = datetime.strftime("%Z")
        description = make_readable_utc_offset(datetime)
    return (shortname, description)

def _make_readable_tzname(tzname):
    tokens = tzname.split("/")
    if len(tokens) == 1:
        return tzname.replace("_", " ")
    elif len(tokens) == 2:
        return tokens[1].replace("_", " ")
    elif len(tokens) == 3:
        state_name = tokens[1].replace("_", " ")
        city = tokens[2].replace("_", " ")
        return "{}, {}".format(city, state_name)
    else:
        return "/".join(tokens[1:])

def translate_tz_name(tzname):
    if tzname in _translations_tz:
        return _translations_tz[tzname]
    else:
        return _make_readable_tzname(tzname)

def build_countries_and_timezones_list(now):
    countries = _translations_countries[:]
    base_country_codes = set([c[0] for c in _translations_countries])
    for code in pytz.country_names:
        try:
            timezones = pytz.country_timezones(code)
        except KeyError:
            timezones = ()
        if code not in base_country_codes and len(timezones) > 0:
            countries.append((code, pytz.country_names[code]))
    country_tz = {}
    for code, _ in countries:
        timezones = pytz.country_timezones(code)
        loc_timezones = []
        for tzname in timezones:
            tz = pytz.timezone(tzname)
            time_str = now.astimezone(tz).strftime("%H:%M")
            loc_timezones.append((tzname, translate_tz_name(tzname), time_str))
        country_tz[code] = loc_timezones
    return (countries, country_tz)

def find_country_for_timezone(tzname):
    for code in pytz.country_names.keys():
        try:
            timezones = pytz.country_timezones(code)
        except KeyError:
            continue
        if tzname in timezones:
            return code
    return None
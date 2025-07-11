from enum import Enum
from collections import defaultdict

class Line(str, Enum):
    AEL = 'AEL'  # Airport Express
    DRL = 'DRL'  # Disneyland Resort Line
    EAL = 'EAL'  # East Rail Line
    ISL = 'ISL'  # Island Line
    KTL = 'KTL'  # Kwun Tong Line
    SIL = 'SIL'  # South Island Line
    TCL = 'TCL'  # Tung Chung Line
    TKL = 'TKL'  # Tseung Kwan O Line
    TML = 'TML'  # Tuen Ma Line
    TWL = 'TWL'  # Tsuen Wan Line


class Station(str, Enum):
    ADM = 'ADM'  # Admiralty
    AIR = 'AIR'  # Airport
    AUS = 'AUS'  # Austin
    AWE = 'AWE'  # AsiaWorld Expo
    CAB = 'CAB'  # Causeway Bay
    CEN = 'CEN'  # Central
    CHH = 'CHH'  # Choi Hung
    CHW = 'CHW'  # Chai Wan
    CIO = 'CIO'  # City One
    CKT = 'CKT'  # Che Kung Temple
    CSW = 'CSW'  # Cheung Sha Wan
    DIH = 'DIH'  # Diamond Hill
    DIS = 'DIS'  # Disneyland Resort
    ETS = 'ETS'  # East Tsim Sha Tsui
    EXC = 'EXC'  # Exhibition Centre
    FAN = 'FAN'  # Fanling
    FOH = 'FOH'  # Fortress Hill
    FOT = 'FOT'  # Fo Tan
    HAH = 'HAH'  # Hang Hau
    HEO = 'HEO'  # Heng On
    HFC = 'HFC'  # Heng Fa Chuen
    HIK = 'HIK'  # Hin Keng
    HKU = 'HKU'  # HKU
    HOK = 'HOK'  # Hong Kong
    HOM = 'HOM'  # Ho Man Tin
    HUH = 'HUH'  # Hung Hom
    JOR = 'JOR'  # Jordan
    KAT = 'KAT'  # Kai Tak
    KET = 'KET'  # Kennedy Town
    KOB = 'KOB'  # Kowloon Bay
    KOT = 'KOT'  # Kowloon Tong
    KOW = 'KOW'  # Kowloon
    KSR = 'KSR'  # Kam Sheung Road
    KWF = 'KWF'  # Kwai Fong
    KWH = 'KWH'  # Kwai Hing
    KWT = 'KWT'  # Kwun Tong
    LAK = 'LAK'  # Lai King
    LAT = 'LAT'  # Lam Tin
    LCK = 'LCK'  # Lai Chi Kok
    LET = 'LET'  # Lei Tung
    LHP = 'LHP'  # LOHAS Park
    LMC = 'LMC'  # Lok Ma Chau
    LOF = 'LOF'  # Lok Fu
    LOP = 'LOP'  # Long Ping
    LOW = 'LOW'  # Lo Wu
    MEF = 'MEF'  # Mei Foo
    MKK = 'MKK'  # Mong Kok East
    MOK = 'MOK'  # Mong Kok
    MOS = 'MOS'  # Ma On Shan
    NAC = 'NAC'  # Nam Cheong
    NOP = 'NOP'  # North Point
    NTK = 'NTK'  # Ngau Tau Kok
    OCP = 'OCP'  # Ocean Park
    OLY = 'OLY'  # Olympic
    POA = 'POA'  # Po Lam
    PRE = 'PRE'  # Prince Edward
    QUB = 'QUB'  # Quarry Bay
    RAC = 'RAC'  # Racecourse
    SHM = 'SHM'  # Shek Mun
    SHS = 'SHS'  # Sheung Shui
    SHT = 'SHT'  # Sha Tin
    SHW = 'SHW'  # Sheung Wan
    SIH = 'SIH'  # Siu Hong
    SKM = 'SKM'  # Shek Kip Mei
    SKW = 'SKW'  # Shau Kei Wan
    SOH = 'SOH'  # South Horizons
    SSP = 'SSP'  # Sham Shui Po
    STW = 'STW'  # Sha Tin Wai
    SUN = 'SUN'  # Sunny Bay
    SUW = 'SUW'  # Sung Wong Toi
    SWH = 'SWH'  # Sai Wan Ho
    SYP = 'SYP'  # Sai Ying Pun
    TAK = 'TAK'  # Tai Koo
    TAP = 'TAP'  # Tai Po Market
    TAW = 'TAW'  # Tai Wai
    TIH = 'TIH'  # Tin Hau
    TIK = 'TIK'  # Tiu Keng Leng
    TIS = 'TIS'  # Tin Shui Wai
    TKO = 'TKO'  # Tseung Kwan O
    TKW = 'TKW'  # To Kwa Wan
    TSH = 'TSH'  # Tai Shui Hang
    TST = 'TST'  # Tsim Sha Tsui
    TSW = 'TSW'  # Tsuen Wan
    TSY = 'TSY'  # Tsing Yi
    TUC = 'TUC'  # Tung Chung
    TUM = 'TUM'  # Tuen Mun
    TWH = 'TWH'  # Tai Wo Hau
    TWO = 'TWO'  # Tai Wo
    TWW = 'TWW'  # Tsuen Wan West
    UNI = 'UNI'  # University
    WAC = 'WAC'  # Wan Chai
    WCH = 'WCH'  # Wong Chuk Hang
    WHA = 'WHA'  # Whampoa
    WKS = 'WKS'  # Wu Kai Sha
    WTS = 'WTS'  # Wong Tai Sin
    YAT = 'YAT'  # Yau Tong
    YMT = 'YMT'  # Yau Ma Tei
    YUL = 'YUL'  # Yuen Long


# Dictionary mapping lines to their stations
line_stations = defaultdict(set)

# Airport Express
line_stations[Line.AEL] = {
    Station.HOK,
    Station.KOW,
    Station.TSY,
    Station.AIR,
    Station.AWE
}

# Tung Chung Line
line_stations[Line.TCL] = {
    Station.HOK,
    Station.KOW,
    Station.OLY,
    Station.NAC,
    Station.LAK,
    Station.TSY,
    Station.SUN,
    Station.TUC
}

# Tuen Ma Line
line_stations[Line.TML] = {
    Station.WKS,
    Station.MOS,
    Station.HEO,
    Station.TSH,
    Station.SHM,
    Station.CIO,
    Station.STW,
    Station.CKT,
    Station.TAW,
    Station.HIK,
    Station.DIH,
    Station.KAT,
    Station.SUW,
    Station.TKW,
    Station.HOM,
    Station.HUH,
    Station.ETS,
    Station.AUS,
    Station.NAC,
    Station.MEF,
    Station.TWW,
    Station.KSR,
    Station.YUL,
    Station.LOP,
    Station.TIS,
    Station.SIH,
    Station.TUM
}

# Tseung Kwan O Line
line_stations[Line.TKL] = {
    Station.NOP,
    Station.QUB,
    Station.YAT,
    Station.TIK,
    Station.TKO,
    Station.LHP,
    Station.HAH,
    Station.POA
}

# East Rail Line
line_stations[Line.EAL] = {
    Station.ADM,
    Station.EXC,
    Station.HUH,
    Station.MKK,
    Station.KOT,
    Station.TAW,
    Station.SHT,
    Station.FOT,
    Station.RAC,
    Station.UNI,
    Station.TAP,
    Station.TWO,
    Station.FAN,
    Station.SHS,
    Station.LOW,
    Station.LMC
}

# South Island Line
line_stations[Line.SIL] = {
    Station.ADM,
    Station.OCP,
    Station.WCH,
    Station.LET,
    Station.SOH
}

# Tsuen Wan Line
line_stations[Line.TWL] = {
    Station.CEN,
    Station.ADM,
    Station.TST,
    Station.JOR,
    Station.YMT,
    Station.MOK,
    Station.PRE,
    Station.SSP,
    Station.CSW,
    Station.LCK,
    Station.MEF,
    Station.LAK,
    Station.KWF,
    Station.KWH,
    Station.TWH,
    Station.TSW
}

# Island Line
line_stations[Line.ISL] = {
    Station.KET,
    Station.HKU,
    Station.SYP,
    Station.SHW,
    Station.CEN,
    Station.ADM,
    Station.WAC,
    Station.CAB,
    Station.TIH,
    Station.FOH,
    Station.NOP,
    Station.QUB,
    Station.TAK,
    Station.SWH,
    Station.SKW,
    Station.HFC,
    Station.CHW
}

# Kwun Tong Line
line_stations[Line.KTL] = {
    Station.WHA,
    Station.HOM,
    Station.YMT,
    Station.MOK,
    Station.PRE,
    Station.SKM,
    Station.KOT,
    Station.LOF,
    Station.WTS,
    Station.DIH,
    Station.CHH,
    Station.KOB,
    Station.NTK,
    Station.KWT,
    Station.LAT,
    Station.YAT,
    Station.TIK
}

# Disneyland Resort Line
line_stations[Line.DRL] = {
    Station.SUN,
    Station.DIS
}
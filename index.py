import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import json

# Set page config for mobile
st.set_page_config(
    layout="wide",
    initial_sidebar_state="collapsed"  # Auto-collapse sidebar on mobile
)

# Constants
CO2_SAVED_PER_KWH = 0.4    # kg CO2 per kWh
PANEL_EFFICIENCY = 0.18     # 18% efficient panels
ELECTRICITY_RATE = 0.15     # $ per kWh (national average)

def load_solar_data():
    """Load solar data from the provided JSON file"""
    # [Your full JSON data here]
    json_data = """
    [
      {
        "Date": "2023-04-19 12:03:17.301846",
        "Solar_Irradiance_W/m2": 224.83570765056163,
        "Panel_Temperature_C": 35.97922627548841,
        "Ambient_Temperature_C": 29.030808112113583,
        "Cloud_Cover_%": 96.06269755131997,
        "Energy_Generated_kWh": 75.88281138239319,
        "CO2_Saved_kg": 61.806409124521444,
        "Money_Saved_INR": 455.2968682943591
      },
      {
        "Date": "2023-04-20 12:03:17.301846",
        "Solar_Irradiance_W/m2": 193.08678494144075,
        "Panel_Temperature_C": 30.10813611192484,
        "Ambient_Temperature_C": 21.42991234597444,
        "Cloud_Cover_%": 19.692570445342838,
        "Energy_Generated_kWh": 65.06843306919522,
        "CO2_Saved_kg": 43.72686554048697,
        "Money_Saved_INR": 390.4105984151713
      },
      {
    "Date": "2023-04-21 12:03:17.301846",
    "Solar_Irradiance_W/m2": 232.38442690503462,
    "Panel_Temperature_C": 37.04126377857236,
    "Ambient_Temperature_C": 28.536837198997823,
    "Cloud_Cover_%": 95.14298103618323,
    "Energy_Generated_kWh": 76.46451673768436,
    "CO2_Saved_kg": 50.45222708999982,
    "Money_Saved_INR": 458.7871004261062
  },
  {
    "Date": "2023-04-22 12:03:17.301846",
    "Solar_Irradiance_W/m2": 276.15149282040124,
    "Panel_Temperature_C": 26.4870819788108,
    "Ambient_Temperature_C": 24.0463568205349,
    "Cloud_Cover_%": 99.4819293965951,
    "Energy_Generated_kWh": 49.02763402272507,
    "CO2_Saved_kg": 50.511979018810855,
    "Money_Saved_INR": 294.1658041363504
  },
  {
    "Date": "2023-04-23 12:03:17.301846",
    "Solar_Irradiance_W/m2": 188.2923312638332,
    "Panel_Temperature_C": 40.14577818662822,
    "Ambient_Temperature_C": 25.93633585136694,
    "Cloud_Cover_%": 71.17228057460487,
    "Energy_Generated_kWh": 70.1769250571579,
    "CO2_Saved_kg": 44.98215807188468,
    "Money_Saved_INR": 421.0615503429474
  },
  {
    "Date": "2023-04-24 12:03:17.301846",
    "Solar_Irradiance_W/m2": 188.29315215254098,
    "Panel_Temperature_C": 37.362987412065216,
    "Ambient_Temperature_C": 34.12004883094427,
    "Cloud_Cover_%": 98.1143731791822,
    "Energy_Generated_kWh": 74.30249013260658,
    "CO2_Saved_kg": 36.27534452115899,
    "Money_Saved_INR": 445.8149407956395
  },
  {
    "Date": "2023-04-25 12:03:17.301846",
    "Solar_Irradiance_W/m2": 278.9606407753696,
    "Panel_Temperature_C": 36.28014867156938,
    "Ambient_Temperature_C": 41.689331530459846,
    "Cloud_Cover_%": 56.95397795671037,
    "Energy_Generated_kWh": 74.8764049500924,
    "CO2_Saved_kg": 53.22974503617668,
    "Money_Saved_INR": 449.25842970055436
  },
  {
    "Date": "2023-04-26 12:03:17.301846",
    "Solar_Irradiance_W/m2": 238.37173645764545,
    "Panel_Temperature_C": 39.91345491972757,
    "Ambient_Temperature_C": 32.76270070876087,
    "Cloud_Cover_%": 25.954178317609035,
    "Energy_Generated_kWh": 75.17005108258442,
    "CO2_Saved_kg": 49.389960281446164,
    "Money_Saved_INR": 451.02030649550653
  },
  {
    "Date": "2023-04-27 12:03:17.301846",
    "Solar_Irradiance_W/m2": 176.52628070325238,
    "Panel_Temperature_C": 43.32737222231288,
    "Ambient_Temperature_C": 21.62881856575371,
    "Cloud_Cover_%": 43.699588566562085,
    "Energy_Generated_kWh": 78.76471600279743,
    "CO2_Saved_kg": 55.0024046943657,
    "Money_Saved_INR": 472.58829601678457
  },
  {
    "Date": "2023-04-28 12:03:17.301846",
    "Solar_Irradiance_W/m2": 227.12800217929822,
    "Panel_Temperature_C": 40.07185032509065,
    "Ambient_Temperature_C": 33.11221867754099,
    "Cloud_Cover_%": 59.35609353787859,
    "Energy_Generated_kWh": 89.58883036172128,
    "CO2_Saved_kg": 44.66399693560833,
    "Money_Saved_INR": 537.5329821703276
  },
  {
    "Date": "2023-04-29 12:03:17.301846",
    "Solar_Irradiance_W/m2": 176.82911535937689,
    "Panel_Temperature_C": 25.795628843341774,
    "Ambient_Temperature_C": 38.37642040651956,
    "Cloud_Cover_%": 7.308156202701499,
    "Energy_Generated_kWh": 97.49034148265045,
    "CO2_Saved_kg": 62.20821298813048,
    "Money_Saved_INR": 584.9420488959026
  },
  {
    "Date": "2023-04-30 12:03:17.301846",
    "Solar_Irradiance_W/m2": 176.71351232148714,
    "Panel_Temperature_C": 28.602115166321493,
    "Ambient_Temperature_C": 25.731519669764324,
    "Cloud_Cover_%": 62.234326461724606,
    "Energy_Generated_kWh": 67.00469546303466,
    "CO2_Saved_kg": 41.23226218788155,
    "Money_Saved_INR": 402.028172778208
  },
  {
    "Date": "2023-05-01 12:03:17.301846",
    "Solar_Irradiance_W/m2": 212.0981135783017,
    "Panel_Temperature_C": 31.875907111521606,
    "Ambient_Temperature_C": 29.061879833289577,
    "Cloud_Cover_%": 98.11778367622945,
    "Energy_Generated_kWh": 55.93598289221711,
    "CO2_Saved_kg": 67.12040284017893,
    "Money_Saved_INR": 335.61589735330267
  },
  {
    "Date": "2023-05-02 12:03:17.301846",
    "Solar_Irradiance_W/m2": 104.33598776711011,
    "Panel_Temperature_C": 35.130455251054165,
    "Ambient_Temperature_C": 30.10281736310438,
    "Cloud_Cover_%": 19.010764978372762,
    "Energy_Generated_kWh": 59.15911175513794,
    "CO2_Saved_kg": 32.52363490171739,
    "Money_Saved_INR": 354.9546705308277
  },
  {
    "Date": "2023-05-03 12:03:17.301846",
    "Solar_Irradiance_W/m2": 113.75410837434836,
    "Panel_Temperature_C": 37.58829510234561,
    "Ambient_Temperature_C": 24.50571180842432,
    "Cloud_Cover_%": 79.25951162883833,
    "Energy_Generated_kWh": 70.25594157610146,
    "CO2_Saved_kg": 54.347700645568914,
    "Money_Saved_INR": 421.5356494566088
  },
  {
    "Date": "2023-05-04 12:03:17.301846",
    "Solar_Irradiance_W/m2": 171.88562353795137,
    "Panel_Temperature_C": 31.371280934232672,
    "Ambient_Temperature_C": 34.537963036907016,
    "Cloud_Cover_%": 90.78987937796194,
    "Energy_Generated_kWh": 72.96157364366982,
    "CO2_Saved_kg": 54.754306825266234,
    "Money_Saved_INR": 437.76944186201894
  },
  {
    "Date": "2023-05-05 12:03:17.301846",
    "Solar_Irradiance_W/m2": 149.35844398327882,
    "Panel_Temperature_C": 35.93383382238539,
    "Ambient_Temperature_C": 29.15336295974553,
    "Cloud_Cover_%": 94.37015928202209,
    "Energy_Generated_kWh": 64.60007867605086,
    "CO2_Saved_kg": 42.04442932059118,
    "Money_Saved_INR": 387.60047205630514
  },
  {
    "Date": "2023-05-06 12:03:17.301846",
    "Solar_Irradiance_W/m2": 215.7123666297637,
    "Panel_Temperature_C": 31.22308533823339,
    "Ambient_Temperature_C": 32.93672710734919,
    "Cloud_Cover_%": 96.01356044054472,
    "Energy_Generated_kWh": 54.07766671500211,
    "CO2_Saved_kg": 54.24393937861012,
    "Money_Saved_INR": 324.46600029001263
  },
  {
    "Date": "2023-05-07 12:03:17.301846",
    "Solar_Irradiance_W/m2": 154.59879622393944,
    "Panel_Temperature_C": 31.942410985040258,
    "Ambient_Temperature_C": 23.7875547553853,
    "Cloud_Cover_%": 52.14596387214719,
    "Energy_Generated_kWh": 70.87758345051624,
    "CO2_Saved_kg": 62.795186697601586,
    "Money_Saved_INR": 425.2655007030975
  },
  {
    "Date": "2023-05-08 12:03:17.301846",
    "Solar_Irradiance_W/m2": 129.38481493323542,
    "Panel_Temperature_C": 27.96669451575889,
    "Ambient_Temperature_C": 26.937791897736126,
    "Cloud_Cover_%": 97.73079079915037,
    "Energy_Generated_kWh": 83.62853240227943,
    "CO2_Saved_kg": 27.831811606459354,
    "Money_Saved_INR": 501.7711944136766
  },
  {
    "Date": "2023-05-09 12:03:17.301846",
    "Solar_Irradiance_W/m2": 273.2824384460777,
    "Panel_Temperature_C": 30.38383376944548,
    "Ambient_Temperature_C": 35.0566695047944,
    "Cloud_Cover_%": 75.73102071344388,
    "Energy_Generated_kWh": 91.90058931671129,
    "CO2_Saved_kg": 55.02744807490814,
    "Money_Saved_INR": 551.4035359002678
  },
  {
    "Date": "2023-05-10 12:03:17.301846",
    "Solar_Irradiance_W/m2": 188.7111849756732,
    "Panel_Temperature_C": 28.24157697191833,
    "Ambient_Temperature_C": 27.39016793535763,
    "Cloud_Cover_%": 16.16714362369619,
    "Energy_Generated_kWh": 68.85153893783358,
    "CO2_Saved_kg": 25.067291796699223,
    "Money_Saved_INR": 413.10923362700146
  },
  {
    "Date": "2023-05-11 12:03:17.301846",
    "Solar_Irradiance_W/m2": 203.3764102343962,
    "Panel_Temperature_C": 30.120633735113337,
    "Ambient_Temperature_C": 42.088746958633834,
    "Cloud_Cover_%": 47.690010646797,
    "Energy_Generated_kWh": 71.74004355713132,
    "CO2_Saved_kg": 40.34335196476792,
    "Money_Saved_INR": 430.4402613427879
  },
  {
    "Date": "2023-05-12 12:03:17.301846",
    "Solar_Irradiance_W/m2": 128.76259068932717,
    "Panel_Temperature_C": 40.2682089830392,
    "Ambient_Temperature_C": 27.202546700697784,
    "Cloud_Cover_%": 71.8331175372004,
    "Energy_Generated_kWh": 61.466033823053785,
    "CO2_Saved_kg": 66.29166364900945,
    "Money_Saved_INR": 368.7962029383227
  },
  {
    "Date": "2023-05-13 12:03:17.301846",
    "Solar_Irradiance_W/m2": 172.78086377374086,
    "Panel_Temperature_C": 30.253005555840286,
    "Ambient_Temperature_C": 31.572793080263203,
    "Cloud_Cover_%": 24.734031581908333,
    "Energy_Generated_kWh": 79.37121659250447,
    "CO2_Saved_kg": 44.18217966607946,
    "Money_Saved_INR": 476.2272995550268
  },
  {
    "Date": "2023-05-14 12:03:17.301846",
    "Solar_Irradiance_W/m2": 205.5461294854933,
    "Panel_Temperature_C": 48.161910324186955,
    "Ambient_Temperature_C": 36.528135823111626,
    "Cloud_Cover_%": 64.06151835488873,
    "Energy_Generated_kWh": 63.03142731618371,
    "CO2_Saved_kg": 38.261200355910276,
    "Money_Saved_INR": 378.18856389710226
  },
  {
    "Date": "2023-05-15 12:03:17.301846",
    "Solar_Irradiance_W/m2": 142.45032112888487,
    "Panel_Temperature_C": 37.466589504404446,
    "Ambient_Temperature_C": 20.071439869468776,
    "Cloud_Cover_%": 66.66004790466192,
    "Energy_Generated_kWh": 91.462556264824,
    "CO2_Saved_kg": 48.020622710153184,
    "Money_Saved_INR": 548.775337588944
  },
  {
    "Date": "2023-05-16 12:03:17.301846",
    "Solar_Irradiance_W/m2": 218.7849009172836,
    "Panel_Temperature_C": 35.92418061847437,
    "Ambient_Temperature_C": 17.67433831613457,
    "Cloud_Cover_%": 16.26997438085659,
    "Energy_Generated_kWh": 44.282670161317775,
    "CO2_Saved_kg": 70.67906338163553,
    "Money_Saved_INR": 265.69602096790663
  },
  {
    "Date": "2023-05-17 12:03:17.301846",
    "Solar_Irradiance_W/m2": 169.96806550405975,
    "Panel_Temperature_C": 30.708211099093933,
    "Ambient_Temperature_C": 19.320405798009336,
    "Cloud_Cover_%": 56.50853124527563,
    "Energy_Generated_kWh": 72.80740655095076,
    "CO2_Saved_kg": 31.68317752793974,
    "Money_Saved_INR": 436.84443930570455
  },
  {
    "Date": "2023-05-18 12:03:17.301846",
    "Solar_Irradiance_W/m2": 185.41531251033615,
    "Panel_Temperature_C": 38.501549397044954,
    "Ambient_Temperature_C": 38.838088723990275,
    "Cloud_Cover_%": 77.16269109786077,
    "Energy_Generated_kWh": 86.02214678383484,
    "CO2_Saved_kg": 39.48690088360655,
    "Money_Saved_INR": 516.132880703009
  },
  {
    "Date": "2023-05-19 12:03:17.301846",
    "Solar_Irradiance_W/m2": 169.91466938853014,
    "Panel_Temperature_C": 32.12181086881113,
    "Ambient_Temperature_C": 26.136992978752872,
    "Cloud_Cover_%": 49.88956645359419,
    "Energy_Generated_kWh": 83.67669032645009,
    "CO2_Saved_kg": 64.97431683179626,
    "Money_Saved_INR": 502.0601419587005
  },
  {
    "Date": "2023-05-20 12:03:17.301846",
    "Solar_Irradiance_W/m2": 292.6139092254469,
    "Panel_Temperature_C": 35.610049073226804,
    "Ambient_Temperature_C": 47.90739499967776,
    "Cloud_Cover_%": 1.2103116776107425,
    "Energy_Generated_kWh": 133.86067327960993,
    "CO2_Saved_kg": 68.57702343537733,
    "Money_Saved_INR": 803.1640396776595
  },
  {
    "Date": "2023-05-21 12:03:17.301846",
    "Solar_Irradiance_W/m2": 199.3251387631033,
    "Panel_Temperature_C": 47.800422691343975,
    "Ambient_Temperature_C": 26.05026680939828,
    "Cloud_Cover_%": 0.9038469079292177,
    "Energy_Generated_kWh": 86.99600049135815,
    "CO2_Saved_kg": 48.96568775709716,
    "Money_Saved_INR": 521.9760029481489
  },
  {
    "Date": "2023-05-22 12:03:17.301846",
    "Solar_Irradiance_W/m2": 147.114453552205,
    "Panel_Temperature_C": 34.519700501376754,
    "Ambient_Temperature_C": 31.291859122379257,
    "Cloud_Cover_%": 35.702934397001215,
    "Energy_Generated_kWh": 59.91890806315979,
    "CO2_Saved_kg": 37.60947297473358,
    "Money_Saved_INR": 359.51344837895874
  },
  {
    "Date": "2023-05-23 12:03:17.301846",
    "Solar_Irradiance_W/m2": 241.12724560515946,
    "Panel_Temperature_C": 40.74636663142838,
    "Ambient_Temperature_C": 40.79476966797513,
    "Cloud_Cover_%": 92.6194068431782,
    "Energy_Generated_kWh": 78.09071505821854,
    "CO2_Saved_kg": 70.95843501809159,
    "Money_Saved_INR": 468.5442903493112
  },
  {
    "Date": "2023-05-24 12:03:17.301846",
    "Solar_Irradiance_W/m2": 138.9578175014489,
    "Panel_Temperature_C": 31.48411787437056,
    "Ambient_Temperature_C": 44.04265021711386,
    "Cloud_Cover_%": 22.867677960360876,
    "Energy_Generated_kWh": 44.475073330670966,
    "CO2_Saved_kg": 65.94442391749197,
    "Money_Saved_INR": 266.8504399840258
  },
  {
    "Date": "2023-05-25 12:03:17.301846",
    "Solar_Irradiance_W/m2": 210.44317975023776,
    "Panel_Temperature_C": 34.82505754751519,
    "Ambient_Temperature_C": 44.43052503645478,
    "Cloud_Cover_%": 63.43636888716871,
    "Energy_Generated_kWh": 78.38800501406479,
    "CO2_Saved_kg": 56.78946987762233,
    "Money_Saved_INR": 470.32803008438873
  },
  {
    "Date": "2023-05-26 12:03:17.301846",
    "Solar_Irradiance_W/m2": 102.01649380601123,
    "Panel_Temperature_C": 43.85400317817755,
    "Ambient_Temperature_C": 38.458563614152,
    "Cloud_Cover_%": 22.207587069332057,
    "Energy_Generated_kWh": 63.33887885998483,
    "CO2_Saved_kg": 41.8759765106258,
    "Money_Saved_INR": 380.03327315990896
  },
  {
    "Date": "2023-05-27 12:03:17.301846",
    "Solar_Irradiance_W/m2": 133.59069755507846,
    "Panel_Temperature_C": 31.865164711061162,
    "Ambient_Temperature_C": 37.168437680680235,
    "Cloud_Cover_%": 32.16699896595486,
    "Energy_Generated_kWh": 98.30780551120324,
    "CO2_Saved_kg": 49.50970659161963,
    "Money_Saved_INR": 589.8468330672194
  },
  {
    "Date": "2023-05-28 12:03:17.301846",
    "Solar_Irradiance_W/m2": 209.84306179345617,
    "Panel_Temperature_C": 44.062242789984644,
    "Ambient_Temperature_C": 34.147688644408284,
    "Cloud_Cover_%": 84.8042089601484,
    "Energy_Generated_kWh": 69.00919450808931,
    "CO2_Saved_kg": 48.396399189551694,
    "Money_Saved_INR": 414.05516704853585
  },
  {
    "Date": "2023-05-29 12:03:17.301846",
    "Solar_Irradiance_W/m2": 236.92332899977052,
    "Panel_Temperature_C": 38.538759677277376,
    "Ambient_Temperature_C": 35.44852753316646,
    "Cloud_Cover_%": 72.88614422699469,
    "Energy_Generated_kWh": 77.66468168409507,
    "CO2_Saved_kg": 53.30851304615578,
    "Money_Saved_INR": 465.98809010457046
  },
  {
    "Date": "2023-05-30 12:03:17.301846",
    "Solar_Irradiance_W/m2": 208.56841405949854,
    "Panel_Temperature_C": 32.18766612052866,
    "Ambient_Temperature_C": 26.141699985700267,
    "Cloud_Cover_%": 9.539927731321063,
    "Energy_Generated_kWh": 67.28884317191194,
    "CO2_Saved_kg": 64.51001438131337,
    "Money_Saved_INR": 403.7330590314716
  },
  {
    "Date": "2023-05-31 12:03:17.301846",
    "Solar_Irradiance_W/m2": 194.21758588058796,
    "Panel_Temperature_C": 38.1620386952776,
    "Ambient_Temperature_C": 24.272607816043852,
    "Cloud_Cover_%": 42.87020209864336,
    "Energy_Generated_kWh": 114.77702703706663,
    "CO2_Saved_kg": 58.79417041137403,
    "Money_Saved_INR": 688.6621622223997
  },
  {
    "Date": "2023-06-01 12:03:17.301846",
    "Solar_Irradiance_W/m2": 184.94481522053556,
    "Panel_Temperature_C": 39.86277224813365,
    "Ambient_Temperature_C": 29.976378798123335,
    "Cloud_Cover_%": 2.916976364526447,
    "Energy_Generated_kWh": 73.57514467764176,
    "CO2_Saved_kg": 39.226239230152416,
    "Money_Saved_INR": 441.45086806585056
  },
  {
    "Date": "2023-06-02 12:03:17.301846",
    "Solar_Irradiance_W/m2": 126.07390048162863,
    "Panel_Temperature_C": 38.10904981108598,
    "Ambient_Temperature_C": 28.8087076423255,
    "Cloud_Cover_%": 48.0890146603009,
    "Energy_Generated_kWh": 116.65114086958403,
    "CO2_Saved_kg": 63.764964500195376,
    "Money_Saved_INR": 699.9068452175042
  },
  {
    "Date": "2023-06-03 12:03:17.301846",
    "Solar_Irradiance_W/m2": 164.00778958026456,
    "Panel_Temperature_C": 27.148876400547717,
    "Ambient_Temperature_C": 26.827403654709073,
    "Cloud_Cover_%": 66.24340117010681,
    "Energy_Generated_kWh": 96.28303524236533,
    "CO2_Saved_kg": 53.131321400131554,
    "Money_Saved_INR": 577.698211454192
  },
  {
    "Date": "2023-06-04 12:03:17.301846",
    "Solar_Irradiance_W/m2": 176.96806145201063,
    "Panel_Temperature_C": 31.364314120875658,
    "Ambient_Temperature_C": 34.874712132197004,
    "Cloud_Cover_%": 11.850262359815156,
    "Energy_Generated_kWh": 89.64133454670772,
    "CO2_Saved_kg": 56.87065795858916,
    "Money_Saved_INR": 537.8480072802463
  },
  {
    "Date": "2023-06-05 12:03:17.301846",
    "Solar_Irradiance_W/m2": 252.85611131094578,
    "Panel_Temperature_C": 33.762406822242475,
    "Ambient_Temperature_C": 36.687136459993575,
    "Cloud_Cover_%": 28.888493890916568,
    "Energy_Generated_kWh": 87.3746629463504,
    "CO2_Saved_kg": 64.66540859278604,
    "Money_Saved_INR": 524.2479776781024
  },
  {
    "Date": "2023-06-06 12:03:17.301846",
    "Solar_Irradiance_W/m2": 217.18091447842306,
    "Panel_Temperature_C": 34.62783285449977,
    "Ambient_Temperature_C": 30.61884820404293,
    "Cloud_Cover_%": 39.783662550215695,
    "Energy_Generated_kWh": 87.87594596432503,
    "CO2_Saved_kg": 38.88419750486449,
    "Money_Saved_INR": 527.2556757859502
  },
  {
    "Date": "2023-06-07 12:03:17.301846",
    "Solar_Irradiance_W/m2": 111.8479922318633,
    "Panel_Temperature_C": 38.10336048775339,
    "Ambient_Temperature_C": 40.34271056738683,
    "Cloud_Cover_%": 91.95310246560497,
    "Energy_Generated_kWh": 41.4465484130878,
    "CO2_Saved_kg": 49.64174421293537,
    "Money_Saved_INR": 248.67929047852678
  },
  {
    "Date": "2023-06-08 12:03:17.301846",
    "Solar_Irradiance_W/m2": 216.20419846973977,
    "Panel_Temperature_C": 35.88850500466627,
    "Ambient_Temperature_C": 22.008176201065464,
    "Cloud_Cover_%": 99.32550154229641,
    "Energy_Generated_kWh": 74.42233211698488,
    "CO2_Saved_kg": 44.68545448640785,
    "Money_Saved_INR": 446.53399270190926
  },
  {
    "Date": "2023-06-09 12:03:17.301846",
    "Solar_Irradiance_W/m2": 180.74588597918418,
    "Panel_Temperature_C": 28.323278206449494,
    "Ambient_Temperature_C": 28.644383785041974,
    "Cloud_Cover_%": 4.491129899561585,
    "Energy_Generated_kWh": 96.90315942368643,
    "CO2_Saved_kg": 34.32140574634544,
    "Money_Saved_INR": 581.4189565421186
  },
  {
    "Date": "2023-06-10 12:03:17.301846",
    "Solar_Irradiance_W/m2": 166.15389998470206,
    "Panel_Temperature_C": 36.90098925502981,
    "Ambient_Temperature_C": 24.982243755780367,
    "Cloud_Cover_%": 76.1007923495392,
    "Energy_Generated_kWh": 79.02205633051788,
    "CO2_Saved_kg": 53.467099776049196,
    "Money_Saved_INR": 474.1323379831073
  },
  {
    "Date": "2023-06-11 12:03:17.301846",
    "Solar_Irradiance_W/m2": 230.5838144420434,
    "Panel_Temperature_C": 38.05292872641912,
    "Ambient_Temperature_C": 16.934243680488578,
    "Cloud_Cover_%": 37.17240664023432,
    "Energy_Generated_kWh": 51.896203063928496,
    "CO2_Saved_kg": 75.11556551584424,
    "Money_Saved_INR": 311.37721838357095
  },
  {
    "Date": "2023-06-12 12:03:17.301846",
    "Solar_Irradiance_W/m2": 251.54997612479755,
    "Panel_Temperature_C": 37.7989522396552,
    "Ambient_Temperature_C": 29.421235199101105,
    "Cloud_Cover_%": 39.245818622948,
    "Energy_Generated_kWh": 78.9519109884506,
    "CO2_Saved_kg": 31.59922255494247,
    "Money_Saved_INR": 473.71146593070364
  },
  {
    "Date": "2023-06-13 12:03:17.301846",
    "Solar_Irradiance_W/m2": 246.56400595580993,
    "Panel_Temperature_C": 40.40390362777311,
    "Ambient_Temperature_C": 29.147767441317015,
    "Cloud_Cover_%": 75.42649733470228,
    "Energy_Generated_kWh": 114.08211032510982,
    "CO2_Saved_kg": 49.6771938895053,
    "Money_Saved_INR": 684.4926619506589
  },
  {
    "Date": "2023-06-14 12:03:17.301846",
    "Solar_Irradiance_W/m2": 158.03912383886808,
    "Panel_Temperature_C": 39.16961077274452,
    "Ambient_Temperature_C": 40.59414820269492,
    "Cloud_Cover_%": 91.84264321454087,
    "Energy_Generated_kWh": 104.93783431069438,
    "CO2_Saved_kg": 56.40542935074774,
    "Money_Saved_INR": 629.6270058641663
  },
  {
    "Date": "2023-06-15 12:03:17.301846",
    "Solar_Irradiance_W/m2": 184.53938120743928,
    "Panel_Temperature_C": 37.29590039614219,
    "Ambient_Temperature_C": 34.41568179188344,
    "Cloud_Cover_%": 95.09285945025483,
    "Energy_Generated_kWh": 78.75991981267937,
    "CO2_Saved_kg": 51.23078201656181,
    "Money_Saved_INR": 472.55951887607625
  },
  {
    "Date": "2023-06-16 12:03:17.301846",
    "Solar_Irradiance_W/m2": 216.5631715701782,
    "Panel_Temperature_C": 34.649171442706766,
    "Ambient_Temperature_C": 22.830692229695565,
    "Cloud_Cover_%": 57.712258603832076,
    "Energy_Generated_kWh": 99.02898554116173,
    "CO2_Saved_kg": 48.86871947484259,
    "Money_Saved_INR": 594.1739132469704
  },
  {
    "Date": "2023-06-17 12:03:17.301846",
    "Solar_Irradiance_W/m2": 248.77725635611796,
    "Panel_Temperature_C": 26.69519533242004,
    "Ambient_Temperature_C": 42.978647964339316,
    "Cloud_Cover_%": 35.71211593005028,
    "Energy_Generated_kWh": 72.66985959263896,
    "CO2_Saved_kg": 37.007836365541756,
    "Money_Saved_INR": 436.0191575558338
  },
  {
    "Date": "2023-06-18 12:03:17.301846",
    "Solar_Irradiance_W/m2": 176.0412881077355,
    "Panel_Temperature_C": 37.14809109566293,
    "Ambient_Temperature_C": 38.54723586867747,
    "Cloud_Cover_%": 78.75490858587793,
    "Energy_Generated_kWh": 45.92256826346562,
    "CO2_Saved_kg": 52.327867429401635,
    "Money_Saved_INR": 275.5354095807937
  },
  {
    "Date": "2023-06-19 12:03:17.301846",
    "Solar_Irradiance_W/m2": 190.71705116680914,
    "Panel_Temperature_C": 36.03843843581556,
    "Ambient_Temperature_C": 34.07468392428031,
    "Cloud_Cover_%": 25.100138326230027,
    "Energy_Generated_kWh": 61.51068023740891,
    "CO2_Saved_kg": 42.43236022984074,
    "Money_Saved_INR": 369.0640814244535
  },
  {
    "Date": "2023-06-20 12:03:17.301846",
    "Solar_Irradiance_W/m2": 144.68325129969858,
    "Panel_Temperature_C": 36.35789418597687,
    "Ambient_Temperature_C": 28.414611308051178,
    "Cloud_Cover_%": 56.40740288335178,
    "Energy_Generated_kWh": 111.25777537016396,
    "CO2_Saved_kg": 28.100782950214466,
    "Money_Saved_INR": 667.5466522209838
  },
  {
    "Date": "2023-06-21 12:03:17.301846",
    "Solar_Irradiance_W/m2": 140.18966879596647,
    "Panel_Temperature_C": 28.616257120898453,
    "Ambient_Temperature_C": 23.283925342935643,
    "Cloud_Cover_%": 35.85784615248732,
    "Energy_Generated_kWh": 74.52013836341392,
    "CO2_Saved_kg": 61.94592220513731,
    "Money_Saved_INR": 447.1208301804835
  },
  {
    "Date": "2023-06-22 12:03:17.301846",
    "Solar_Irradiance_W/m2": 240.6262911197099,
    "Panel_Temperature_C": 29.594717297958688,
    "Ambient_Temperature_C": 27.39455256750263,
    "Cloud_Cover_%": 65.66310737078761,
    "Energy_Generated_kWh": 75.13232041249964,
    "CO2_Saved_kg": 59.58385819842042,
    "Money_Saved_INR": 450.7939224749978
  },
  {
    "Date": "2023-06-23 12:03:17.301846",
    "Solar_Irradiance_W/m2": 267.8120014285412,
    "Panel_Temperature_C": 40.26576426666452,
    "Ambient_Temperature_C": 37.6212403379293,
    "Cloud_Cover_%": 24.03989128935069,
    "Energy_Generated_kWh": 74.00323607450238,
    "CO2_Saved_kg": 50.5166097685108,
    "Money_Saved_INR": 444.0194164470143
  },
  {
    "Date": "2023-06-24 12:03:17.301846",
    "Solar_Irradiance_W/m2": 196.3994939209833,
    "Panel_Temperature_C": 34.802224230716725,
    "Ambient_Temperature_C": 43.19210414154226,
    "Cloud_Cover_%": 19.159294573482576,
    "Energy_Generated_kWh": 118.08273179146013,
    "CO2_Saved_kg": 52.29074688205703,
    "Money_Saved_INR": 708.4963907487609
  },
  {
    "Date": "2023-06-25 12:03:17.301846",
    "Solar_Irradiance_W/m2": 250.17664489460122,
    "Panel_Temperature_C": 38.40750348686312,
    "Ambient_Temperature_C": 40.80270469790533,
    "Cloud_Cover_%": 91.8239086675437,
    "Energy_Generated_kWh": 112.51917830724126,
    "CO2_Saved_kg": 60.74318012715561,
    "Money_Saved_INR": 675.1150698434476
  },
  {
    "Date": "2023-06-26 12:03:17.301846",
    "Solar_Irradiance_W/m2": 218.0818012523817,
    "Panel_Temperature_C": 35.14159188065231,
    "Ambient_Temperature_C": 26.57805404749608,
    "Cloud_Cover_%": 10.18036829495369,
    "Energy_Generated_kWh": 124.37560466896268,
    "CO2_Saved_kg": 52.24339656778083,
    "Money_Saved_INR": 746.253628013776
  },
  {
    "Date": "2023-06-27 12:03:17.301846",
    "Solar_Irradiance_W/m2": 167.7440122697438,
    "Panel_Temperature_C": 35.14878069747873,
    "Ambient_Temperature_C": 22.162677966976922,
    "Cloud_Cover_%": 50.595790773493164,
    "Energy_Generated_kWh": 76.81909579199898,
    "CO2_Saved_kg": 59.040175547613146,
    "Money_Saved_INR": 460.9145747519939
  },
  {
    "Date": "2023-06-28 12:03:17.301846",
    "Solar_Irradiance_W/m2": 218.0697802754207,
    "Panel_Temperature_C": 39.69141902987999,
    "Ambient_Temperature_C": 30.986203728378428,
    "Cloud_Cover_%": 22.085278296300892,
    "Energy_Generated_kWh": 85.9124897749419,
    "CO2_Saved_kg": 47.0251779912615,
    "Money_Saved_INR": 515.4749386496514
  },
  {
    "Date": "2023-06-29 12:03:17.301846",
    "Solar_Irradiance_W/m2": 276.90182832329845,
    "Panel_Temperature_C": 32.41977635891313,
    "Ambient_Temperature_C": 17.62092444106004,
    "Cloud_Cover_%": 3.892996332566745,
    "Energy_Generated_kWh": 49.66714901158418,
    "CO2_Saved_kg": 63.119837385739466,
    "Money_Saved_INR": 298.0028940695051
  },
  {
    "Date": "2023-06-30 12:03:17.301846",
    "Solar_Irradiance_W/m2": 198.20869804450243,
    "Panel_Temperature_C": 35.48060388470492,
    "Ambient_Temperature_C": 32.26217399929347,
    "Cloud_Cover_%": 3.601881829142639,
    "Energy_Generated_kWh": 109.53868852236549,
    "CO2_Saved_kg": 53.207857259326836,
    "Money_Saved_INR": 657.232131134193
  },
  {
    "Date": "2023-07-01 12:03:17.301846",
    "Solar_Irradiance_W/m2": 278.23218279070034,
    "Panel_Temperature_C": 32.68862355647479,
    "Ambient_Temperature_C": 28.96678189590932,
    "Cloud_Cover_%": 17.522177210582733,
    "Energy_Generated_kWh": 56.6444089746413,
    "CO2_Saved_kg": 51.94051943605874,
    "Money_Saved_INR": 339.8664538478478
  },
  {
    "Date": "2023-07-02 12:03:17.301846",
    "Solar_Irradiance_W/m2": 69.01274479551279,
    "Panel_Temperature_C": 32.827518862838424,
    "Ambient_Temperature_C": 26.737744486922303,
    "Cloud_Cover_%": 86.67703545060003,
    "Energy_Generated_kWh": 84.33551127525259,
    "CO2_Saved_kg": 37.29938911287968,
    "Money_Saved_INR": 506.0130676515155
  },
  {
    "Date": "2023-07-03 12:03:17.301846",
    "Solar_Irradiance_W/m2": 241.09512521876118,
    "Panel_Temperature_C": 33.454139382656805,
    "Ambient_Temperature_C": 18.837078529132434,
    "Cloud_Cover_%": 28.247874397702667,
    "Energy_Generated_kWh": 58.053949447343115,
    "CO2_Saved_kg": 52.869558543017085,
    "Money_Saved_INR": 348.3236966840587
  },
  {
    "Date": "2023-07-04 12:03:17.301846",
    "Solar_Irradiance_W/m2": 204.35235341190855,
    "Panel_Temperature_C": 36.110668858168566,
    "Ambient_Temperature_C": 33.595200745988016,
    "Cloud_Cover_%": 95.04591705752958,
    "Energy_Generated_kWh": 68.22266346522608,
    "CO2_Saved_kg": 41.68045082505549,
    "Money_Saved_INR": 409.33598079135646
  },
  {
    "Date": "2023-07-05 12:03:17.301846",
    "Solar_Irradiance_W/m2": 185.04963247670662,
    "Panel_Temperature_C": 32.60625689168261,
    "Ambient_Temperature_C": 26.27109412236662,
    "Cloud_Cover_%": 58.16222929891936,
    "Energy_Generated_kWh": 63.254751379005995,
    "CO2_Saved_kg": 43.617172734715055,
    "Money_Saved_INR": 379.52850827403597
  },
  {
    "Date": "2023-07-06 12:03:17.301846",
    "Solar_Irradiance_W/m2": 204.58803882677512,
    "Panel_Temperature_C": 41.278780627867604,
    "Ambient_Temperature_C": 21.810582150027983,
    "Cloud_Cover_%": 43.66141897687661,
    "Energy_Generated_kWh": 67.84249478648364,
    "CO2_Saved_kg": 41.846243716838785,
    "Money_Saved_INR": 407.0549687189018
  },
  {
    "Date": "2023-07-07 12:03:17.301846",
    "Solar_Irradiance_W/m2": 100.62155426995535,
    "Panel_Temperature_C": 30.52696348890248,
    "Ambient_Temperature_C": 9.894164507028457,
    "Cloud_Cover_%": 58.00888346694546,
    "Energy_Generated_kWh": 69.21754593702043,
    "CO2_Saved_kg": 39.33765068100775,
    "Money_Saved_INR": 415.3052756221226
  },
  {
    "Date": "2023-07-08 12:03:17.301846",
    "Solar_Irradiance_W/m2": 189.01640560812442,
    "Panel_Temperature_C": 34.06564177919321,
    "Ambient_Temperature_C": 29.807395664645547,
    "Cloud_Cover_%": 51.669838522626776,
    "Energy_Generated_kWh": 69.03462410149845,
    "CO2_Saved_kg": 71.24771403016962,
    "Money_Saved_INR": 414.2077446089907
  },
  {
    "Date": "2023-07-09 12:03:17.301846",
    "Solar_Irradiance_W/m2": 217.85562857558733,
    "Panel_Temperature_C": 32.801344708629124,
    "Ambient_Temperature_C": 42.40576117668821,
    "Cloud_Cover_%": 75.87762537573252,
    "Energy_Generated_kWh": 96.66667823560614,
    "CO2_Saved_kg": 63.31339061988403,
    "Money_Saved_INR": 580.0000694136369
  },
  {
    "Date": "2023-07-10 12:03:17.301846",
    "Solar_Irradiance_W/m2": 273.8947022370758,
    "Panel_Temperature_C": 42.23488942176866,
    "Ambient_Temperature_C": 41.62881450183509,
    "Cloud_Cover_%": 28.249606597285226,
    "Energy_Generated_kWh": 57.9027441387496,
    "CO2_Saved_kg": 69.20367502144262,
    "Money_Saved_INR": 347.4164648324976
  },
  {
    "Date": "2023-07-11 12:03:17.301846",
    "Solar_Irradiance_W/m2": 174.08648908631764,
    "Panel_Temperature_C": 35.98277388255787,
    "Ambient_Temperature_C": 26.8003262038961,
    "Cloud_Cover_%": 35.30503916003024,
    "Energy_Generated_kWh": 84.41082854027734,
    "CO2_Saved_kg": 37.77104980444436,
    "Money_Saved_INR": 506.464971241664
  },
  {
    "Date": "2023-07-12 12:03:17.301846",
    "Solar_Irradiance_W/m2": 159.5753198553406,
    "Panel_Temperature_C": 40.159222697343175,
    "Ambient_Temperature_C": 25.784515577467538,
    "Cloud_Cover_%": 89.40943025332507,
    "Energy_Generated_kWh": 104.35918304611117,
    "CO2_Saved_kg": 50.712537499108926,
    "Money_Saved_INR": 626.155098276667
  },
  {
    "Date": "2023-07-13 12:03:17.301846",
    "Solar_Irradiance_W/m2": 174.91214782077316,
    "Panel_Temperature_C": 27.57219813481514,
    "Ambient_Temperature_C": 33.28141979252516,
    "Cloud_Cover_%": 94.64565131504055,
    "Energy_Generated_kWh": 69.73607270973208,
    "CO2_Saved_kg": 37.06492374795904,
    "Money_Saved_INR": 418.41643625839254
  },
  {
    "Date": "2023-07-14 12:03:17.301846",
    "Solar_Irradiance_W/m2": 245.7701058851037,
    "Panel_Temperature_C": 36.33525132934629,
    "Ambient_Temperature_C": 23.01130192568196,
    "Cloud_Cover_%": 89.25582274864745,
    "Energy_Generated_kWh": 65.64162218504796,
    "CO2_Saved_kg": 43.04305122802936,
    "Money_Saved_INR": 393.8497331102878
  },
  {
    "Date": "2023-07-15 12:03:17.301846",
    "Solar_Irradiance_W/m2": 216.43755548298424,
    "Panel_Temperature_C": 39.44815397811718,
    "Ambient_Temperature_C": 32.11254329873626,
    "Cloud_Cover_%": 41.94479939573136,
    "Energy_Generated_kWh": 75.38950749639498,
    "CO2_Saved_kg": 40.81873016583425,
    "Money_Saved_INR": 452.33704497836993
  },
  {
    "Date": "2023-07-16 12:03:17.301846",
    "Solar_Irradiance_W/m2": 173.51198981164805,
    "Panel_Temperature_C": 35.41141994637712,
    "Ambient_Temperature_C": 35.36256194869283,
    "Cloud_Cover_%": 78.03655030068816,
    "Energy_Generated_kWh": 103.59450416721421,
    "CO2_Saved_kg": 62.395840064415616,
    "Money_Saved_INR": 621.5670250032853
  },
  {
    "Date": "2023-07-17 12:03:17.301846",
    "Solar_Irradiance_W/m2": 225.66337165566782,
    "Panel_Temperature_C": 40.32740187532676,
    "Ambient_Temperature_C": 38.58853256719016,
    "Cloud_Cover_%": 47.63357333010988,
    "Energy_Generated_kWh": 83.88215261906716,
    "CO2_Saved_kg": 46.0377032189824,
    "Money_Saved_INR": 503.29291571440297
  },
  {
    "Date": "2023-07-18 12:03:17.301846",
    "Solar_Irradiance_W/m2": 204.85387746740201,
    "Panel_Temperature_C": 32.41355774949814,
    "Ambient_Temperature_C": 29.29892146464033,
    "Cloud_Cover_%": 49.75398521461022,
    "Energy_Generated_kWh": 69.37571410784803,
    "CO2_Saved_kg": 60.68379333694016,
    "Money_Saved_INR": 416.2542846470882
  },
  {
    "Date": "2023-07-19 12:03:17.301846",
    "Solar_Irradiance_W/m2": 248.43224952664445,
    "Panel_Temperature_C": 42.0467372009279,
    "Ambient_Temperature_C": 28.57428374876124,
    "Cloud_Cover_%": 20.468010905728395,
    "Energy_Generated_kWh": 89.67753302376079,
    "CO2_Saved_kg": 56.04120889588518,
    "Money_Saved_INR": 538.0651981425647
  },
  {
    "Date": "2023-07-20 12:03:17.301846",
    "Solar_Irradiance_W/m2": 164.89734530613237,
    "Panel_Temperature_C": 46.49449061809625,
    "Ambient_Temperature_C": 23.85412189270407,
    "Cloud_Cover_%": 59.113030325851646,
    "Energy_Generated_kWh": 57.95415700327153,
    "CO2_Saved_kg": 73.03638752104789,
    "Money_Saved_INR": 347.7249420196292
  },
  {
    "Date": "2023-07-21 12:03:17.301846",
    "Solar_Irradiance_W/m2": 183.61689267011158,
    "Panel_Temperature_C": 33.18580719780171,
    "Ambient_Temperature_C": 24.21183752172098,
    "Cloud_Cover_%": 18.613589775334795,
    "Energy_Generated_kWh": 93.62719020885896,
    "CO2_Saved_kg": 35.20555776860276,
    "Money_Saved_INR": 561.7631412531538
  },
  {
    "Date": "2023-07-22 12:03:17.301846",
    "Solar_Irradiance_W/m2": 180.3945923433921,
    "Panel_Temperature_C": 32.77248739299614,
    "Ambient_Temperature_C": 28.414647756689313,
    "Cloud_Cover_%": 33.15646990671938,
    "Energy_Generated_kWh": 88.17214615403535,
    "CO2_Saved_kg": 62.59233239786799,
    "Money_Saved_INR": 529.0328769242121
  },
  {
    "Date": "2023-07-23 12:03:17.301846",
    "Solar_Irradiance_W/m2": 126.82425259339408,
    "Panel_Temperature_C": 42.2669223855885,
    "Ambient_Temperature_C": 32.571558547713245,
    "Cloud_Cover_%": 85.50302016199352,
    "Energy_Generated_kWh": 73.84383057722232,
    "CO2_Saved_kg": 61.464408704007276,
    "Money_Saved_INR": 443.0629834633339
  },
  {
    "Date": "2023-07-24 12:03:17.301846",
    "Solar_Irradiance_W/m2": 214.8060138532288,
    "Panel_Temperature_C": 42.89786072865356,
    "Ambient_Temperature_C": 36.39509238363274,
    "Cloud_Cover_%": 20.707580921085523,
    "Energy_Generated_kWh": 63.22828403105538,
    "CO2_Saved_kg": 40.26621161972965,
    "Money_Saved_INR": 379.3697041863323
  },
  {
    "Date": "2023-07-25 12:03:17.301846",
    "Solar_Irradiance_W/m2": 213.05276360899447,
    "Panel_Temperature_C": 32.38569986423366,
    "Ambient_Temperature_C": 24.377747345237587,
    "Cloud_Cover_%": 7.115828517343282,
    "Energy_Generated_kWh": 62.266381554330856,
    "CO2_Saved_kg": 60.0713333647316,
    "Money_Saved_INR": 373.59828932598515
  },
  {
    "Date": "2023-07-26 12:03:17.301846",
    "Solar_Irradiance_W/m2": 200.25567283212305,
    "Panel_Temperature_C": 32.89906591452071,
    "Ambient_Temperature_C": 40.44881998271665,
    "Cloud_Cover_%": 6.90075926128163,
    "Energy_Generated_kWh": 90.69634672691821,
    "CO2_Saved_kg": 53.361449630262285,
    "Money_Saved_INR": 544.1780803615093
  },
  {
    "Date": "2023-07-27 12:03:17.301846",
    "Solar_Irradiance_W/m2": 188.27064333124267,
    "Panel_Temperature_C": 33.59107695569747,
    "Ambient_Temperature_C": 28.102134792702017,
    "Cloud_Cover_%": 94.07845205031079,
    "Energy_Generated_kWh": 104.57961004978124,
    "CO2_Saved_kg": 47.72523740046592,
    "Money_Saved_INR": 627.4776602986874
  },
  {
    "Date": "2023-07-28 12:03:17.301846",
    "Solar_Irradiance_W/m2": 129.23146289747928,
    "Panel_Temperature_C": 28.277747444828613,
    "Ambient_Temperature_C": 29.850428939560945,
    "Cloud_Cover_%": 50.69204379618346,
    "Energy_Generated_kWh": 67.25384505942411,
    "CO2_Saved_kg": 41.760645130280004,
    "Money_Saved_INR": 403.5230703565446
  },
  {
    "Date": "2023-07-29 12:03:17.301846",
    "Solar_Irradiance_W/m2": 178.96773386173206,
    "Panel_Temperature_C": 30.40674026757901,
    "Ambient_Temperature_C": 24.769518245965237,
    "Cloud_Cover_%": 40.941207181701834,
    "Energy_Generated_kWh": 89.16773407102968,
    "CO2_Saved_kg": 42.80890548550814,
    "Money_Saved_INR": 535.006404426178
  },
  {
    "Date": "2023-07-30 12:03:17.301846",
    "Solar_Irradiance_W/m2": 182.86427417366153,
    "Panel_Temperature_C": 29.97929616623966,
    "Ambient_Temperature_C": 13.03031817808941,
    "Cloud_Cover_%": 81.08785810079185,
    "Energy_Generated_kWh": 38.25945962795863,
    "CO2_Saved_kg": 70.49812095785926,
    "Money_Saved_INR": 229.55675776775178
  },
  {
    "Date": "2023-07-31 12:03:17.301846",
    "Solar_Irradiance_W/m2": 159.88613653891906,
    "Panel_Temperature_C": 31.161012174479357,
    "Ambient_Temperature_C": 36.18831777452735,
    "Cloud_Cover_%": 83.5825927910516,
    "Energy_Generated_kWh": 68.30764538685601,
    "CO2_Saved_kg": 50.006828189574826,
    "Money_Saved_INR": 409.8458723211361
  },
  {
    "Date": "2023-08-01 12:03:17.301846",
    "Solar_Irradiance_W/m2": 191.93571441669954,
    "Panel_Temperature_C": 34.82657556306609,
    "Ambient_Temperature_C": 35.157907279647034,
    "Cloud_Cover_%": 33.21910331156046,
    "Energy_Generated_kWh": 79.37882134258196,
    "CO2_Saved_kg": 57.82130001531459,
    "Money_Saved_INR": 476.2729280554918
  },
  {
    "Date": "2023-08-02 12:03:17.301846",
    "Solar_Irradiance_W/m2": 220.20254284072692,
    "Panel_Temperature_C": 36.1710736626826,
    "Ambient_Temperature_C": 28.030707100172506,
    "Cloud_Cover_%": 69.36180574737952,
    "Energy_Generated_kWh": 61.80633166036333,
    "CO2_Saved_kg": 42.09100618332447,
    "Money_Saved_INR": 370.83798996217996
  },
  {
    "Date": "2023-08-03 12:03:17.301846",
    "Solar_Irradiance_W/m2": 294.3092950605265,
    "Panel_Temperature_C": 42.75250246407038,
    "Ambient_Temperature_C": 30.468935020574104,
    "Cloud_Cover_%": 77.11228158518865,
    "Energy_Generated_kWh": 61.26987250420808,
    "CO2_Saved_kg": 42.201470537783614,
    "Money_Saved_INR": 367.6192350252485
  },
  {
    "Date": "2023-08-04 12:03:17.301846",
    "Solar_Irradiance_W/m2": 208.72889064159196,
    "Panel_Temperature_C": 30.008229796306047,
    "Ambient_Temperature_C": 33.611574523928695,
    "Cloud_Cover_%": 65.46506868659546,
    "Energy_Generated_kWh": 66.64440887062227,
    "CO2_Saved_kg": 60.81984809249942,
    "Money_Saved_INR": 399.86645322373363
  },
  {
    "Date": "2023-08-05 12:03:17.301846",
    "Solar_Irradiance_W/m2": 212.8775195361382,
    "Panel_Temperature_C": 39.92161199238292,
    "Ambient_Temperature_C": 19.0621790017942,
    "Cloud_Cover_%": 15.159507480009937,
    "Energy_Generated_kWh": 85.84385456652747,
    "CO2_Saved_kg": 36.50423788448468,
    "Money_Saved_INR": 515.0631273991648
  },
  {
    "Date": "2023-08-06 12:03:17.301846",
    "Solar_Irradiance_W/m2": 196.27770421169163,
    "Panel_Temperature_C": 33.93005577887246,
    "Ambient_Temperature_C": 26.296631258575935,
    "Cloud_Cover_%": 87.5883083517057,
    "Energy_Generated_kWh": 76.2534196318725,
    "CO2_Saved_kg": 45.847862320947286,
    "Money_Saved_INR": 457.520517791235
  },
  {
    "Date": "2023-08-07 12:03:17.301846",
    "Solar_Irradiance_W/m2": 104.06143923504793,
    "Panel_Temperature_C": 34.752681451737836,
    "Ambient_Temperature_C": 35.559852757352786,
    "Cloud_Cover_%": 53.90945527360087,
    "Energy_Generated_kWh": 35.235375333500556,
    "CO2_Saved_kg": 50.34027411072232,
    "Money_Saved_INR": 211.41225200100334
  },
  {
    "Date": "2023-08-08 12:03:17.301846",
    "Solar_Irradiance_W/m2": 198.67430622753915,
    "Panel_Temperature_C": 38.37409746083302,
    "Ambient_Temperature_C": 21.219974037815255,
    "Cloud_Cover_%": 28.24724263700037,
    "Energy_Generated_kWh": 37.585996947298675,
    "CO2_Saved_kg": 51.11372601840053,
    "Money_Saved_INR": 225.51598168379206
  },
  {
    "Date": "2023-08-09 12:03:17.301846",
    "Solar_Irradiance_W/m2": 203.01151049705132,
    "Panel_Temperature_C": 29.386389892188507,
    "Ambient_Temperature_C": 32.054905525166404,
    "Cloud_Cover_%": 42.52281854376939,
    "Energy_Generated_kWh": 67.86269644285649,
    "CO2_Saved_kg": 48.20906714983844,
    "Money_Saved_INR": 407.17617865713896
  },
  {
    "Date": "2023-08-10 12:03:17.301846",
    "Solar_Irradiance_W/m2": 323.1621056242643,
    "Panel_Temperature_C": 36.912048730920255,
    "Ambient_Temperature_C": 20.503927367636166,
    "Cloud_Cover_%": 3.757109039890738,
    "Energy_Generated_kWh": 89.15373172107104,
    "CO2_Saved_kg": 53.958197810959234,
    "Money_Saved_INR": 534.9223903264262
  },
  {
    "Date": "2023-08-11 12:03:17.301846",
    "Solar_Irradiance_W/m2": 190.38195176094388,
    "Panel_Temperature_C": 35.83226104106528,
    "Ambient_Temperature_C": 33.265009877034686,
    "Cloud_Cover_%": 12.786680122241755,
    "Energy_Generated_kWh": 25.049903145495307,
    "CO2_Saved_kg": 56.92855755817811,
    "Money_Saved_INR": 150.29941887297184
  },
  {
    "Date": "2023-08-12 12:03:17.301846",
    "Solar_Irradiance_W/m2": 215.07736711668062,
    "Panel_Temperature_C": 37.462256320040744,
    "Ambient_Temperature_C": 29.750509623917615,
    "Cloud_Cover_%": 76.55467505158609,
    "Energy_Generated_kWh": 70.00539647696739,
    "CO2_Saved_kg": 57.3463754545933,
    "Money_Saved_INR": 420.0323788618043
  },
  {
    "Date": "2023-08-13 12:03:17.301846",
    "Solar_Irradiance_W/m2": 198.26441151473784,
    "Panel_Temperature_C": 36.44584321953909,
    "Ambient_Temperature_C": 18.694077288661433,
    "Cloud_Cover_%": 0.0011634755366141114,
    "Energy_Generated_kWh": 69.47504286965157,
    "CO2_Saved_kg": 40.14196191332174,
    "Money_Saved_INR": 416.8502572179094
  },
  {
    "Date": "2023-08-14 12:03:17.301846",
    "Solar_Irradiance_W/m2": 141.5660981190234,
    "Panel_Temperature_C": 47.276500699554475,
    "Ambient_Temperature_C": 38.1531754812002,
    "Cloud_Cover_%": 41.65658284822922,
    "Energy_Generated_kWh": 107.76675556416896,
    "CO2_Saved_kg": 47.15844902071203,
    "Money_Saved_INR": 646.6005333850137
  },
  {
    "Date": "2023-08-15 12:03:17.301846",
    "Solar_Irradiance_W/m2": 257.14114072575103,
    "Panel_Temperature_C": 31.81130007874342,
    "Ambient_Temperature_C": 24.857858962413655,
    "Cloud_Cover_%": 52.251018108558846,
    "Energy_Generated_kWh": 72.29956376574273,
    "CO2_Saved_kg": 61.94762861876938,
    "Money_Saved_INR": 433.7973825944564
  },
  {
    "Date": "2023-08-16 12:03:17.301846",
    "Solar_Irradiance_W/m2": 237.5966516343387,
    "Panel_Temperature_C": 32.34501522499091,
    "Ambient_Temperature_C": 24.328232940899333,
    "Cloud_Cover_%": 5.4634420000972295,
    "Energy_Generated_kWh": 87.65977969481857,
    "CO2_Saved_kg": 58.94647187573872,
    "Money_Saved_INR": 525.9586781689114
  },
  {
    "Date": "2023-08-17 12:03:17.301846",
    "Solar_Irradiance_W/m2": 239.55159735215233,
    "Panel_Temperature_C": 31.88429736787618,
    "Ambient_Temperature_C": 31.4039843806166,
    "Cloud_Cover_%": 97.30781629723329,
    "Energy_Generated_kWh": 82.82514280174927,
    "CO2_Saved_kg": 36.27140548518936,
    "Money_Saved_INR": 496.95085681049557
  },
  {
    "Date": "2023-08-18 12:03:17.301846",
    "Solar_Irradiance_W/m2": 154.53062726026306,
    "Panel_Temperature_C": 32.22261440419873,
    "Ambient_Temperature_C": 38.040461446001004,
    "Cloud_Cover_%": 22.612533124967193,
    "Energy_Generated_kWh": 37.38867040385599,
    "CO2_Saved_kg": 53.514799003522015,
    "Money_Saved_INR": 224.33202242313592
  },
  {
    "Date": "2023-08-19 12:03:17.301846",
    "Solar_Irradiance_W/m2": 270.13971554680495,
    "Panel_Temperature_C": 31.81306436346741,
    "Ambient_Temperature_C": 22.88924726715122,
    "Cloud_Cover_%": 30.419871963628086,
    "Energy_Generated_kWh": 95.36414433263475,
    "CO2_Saved_kg": 30.217747506251897,
    "Money_Saved_INR": 572.1848659958085
  },
  {
    "Date": "2023-08-20 12:03:17.301846",
    "Solar_Irradiance_W/m2": 129.90744686038596,
    "Panel_Temperature_C": 40.94508265553776,
    "Ambient_Temperature_C": 30.4317589489358,
    "Cloud_Cover_%": 30.39425122550273,
    "Energy_Generated_kWh": 84.30793010912576,
    "CO2_Saved_kg": 50.469349020603694,
    "Money_Saved_INR": 505.84758065475455
  },
  {
    "Date": "2023-08-21 12:03:17.301846",
    "Solar_Irradiance_W/m2": 229.34285469001352,
    "Panel_Temperature_C": 42.102521239949276,
    "Ambient_Temperature_C": 33.00171550231401,
    "Cloud_Cover_%": 23.04166621173499,
    "Energy_Generated_kWh": 90.1653727934918,
    "CO2_Saved_kg": 68.97767016745976,
    "Money_Saved_INR": 540.9922367609508
  },
  {
    "Date": "2023-08-22 12:03:17.301846",
    "Solar_Irradiance_W/m2": 309.5227812904989,
    "Panel_Temperature_C": 32.146268531252616,
    "Ambient_Temperature_C": 34.85173925084201,
    "Cloud_Cover_%": 0.1473822086311416,
    "Energy_Generated_kWh": 158.52475412872653,
    "CO2_Saved_kg": 40.521072827310135,
    "Money_Saved_INR": 951.1485247723592
  },
  {
    "Date": "2023-08-23 12:03:17.301846",
    "Solar_Irradiance_W/m2": 150.4731837434656,
    "Panel_Temperature_C": 30.838222134478855,
    "Ambient_Temperature_C": 31.235090886940576,
    "Cloud_Cover_%": 72.93447940879963,
    "Energy_Generated_kWh": 38.31774121002823,
    "CO2_Saved_kg": 41.65676954508418,
    "Money_Saved_INR": 229.9064472601694
  },
  {
    "Date": "2023-08-24 12:03:17.301846",
    "Solar_Irradiance_W/m2": 171.6851135198614,
    "Panel_Temperature_C": 37.35707778193202,
    "Ambient_Temperature_C": 27.430805126416743,
    "Cloud_Cover_%": 96.68454997992853,
    "Energy_Generated_kWh": 114.49393299522217,
    "CO2_Saved_kg": 57.640297815728594,
    "Money_Saved_INR": 686.963597971333
  },
  {
    "Date": "2023-08-25 12:03:17.301846",
    "Solar_Irradiance_W/m2": 204.98256825438207,
    "Panel_Temperature_C": 32.23888477859514,
    "Ambient_Temperature_C": 24.206868455458963,
    "Cloud_Cover_%": 22.429348328504506,
    "Energy_Generated_kWh": 74.25104961199288,
    "CO2_Saved_kg": 34.571984847903536,
    "Money_Saved_INR": 445.5062976719573
  },
  {
    "Date": "2023-08-26 12:03:17.301846",
    "Solar_Irradiance_W/m2": 174.82621729419003,
    "Panel_Temperature_C": 38.164659088777555,
    "Ambient_Temperature_C": 30.603007181324624,
    "Cloud_Cover_%": 66.30471918034225,
    "Energy_Generated_kWh": 85.74657808806019,
    "CO2_Saved_kg": 43.67244970114961,
    "Money_Saved_INR": 514.4794685283612
  },
  {
    "Date": "2023-08-27 12:03:17.301846",
    "Solar_Irradiance_W/m2": 122.46682844669337,
    "Panel_Temperature_C": 36.0146151042565,
    "Ambient_Temperature_C": 22.495026916100752,
    "Cloud_Cover_%": 74.18963269587151,
    "Energy_Generated_kWh": 79.08975509397516,
    "CO2_Saved_kg": 55.96441137581753,
    "Money_Saved_INR": 474.53853056385094
  },
  {
    "Date": "2023-08-28 12:03:17.301846",
    "Solar_Irradiance_W/m2": 203.42814874030137,
    "Panel_Temperature_C": 27.42127942501384,
    "Ambient_Temperature_C": 9.550546615537748,
    "Cloud_Cover_%": 84.84253790905247,
    "Energy_Generated_kWh": 71.51527333203913,
    "CO2_Saved_kg": 43.65714152310597,
    "Money_Saved_INR": 429.0916399922348
  },
  {
    "Date": "2023-08-29 12:03:17.301846",
    "Solar_Irradiance_W/m2": 146.88481431369476,
    "Panel_Temperature_C": 42.737526006650306,
    "Ambient_Temperature_C": 33.05591862910367,
    "Cloud_Cover_%": 42.262919701360914,
    "Energy_Generated_kWh": 68.60334143522482,
    "CO2_Saved_kg": 47.640300127890285,
    "Money_Saved_INR": 411.6200486113489
  },
  {
    "Date": "2023-08-30 12:03:17.301846",
    "Solar_Irradiance_W/m2": 223.67962153175907,
    "Panel_Temperature_C": 43.97938836547761,
    "Ambient_Temperature_C": 36.32754388760337,
    "Cloud_Cover_%": 30.293090564042924,
    "Energy_Generated_kWh": 86.59017471146018,
    "CO2_Saved_kg": 57.44185710315035,
    "Money_Saved_INR": 519.5410482687611
  },
  {
    "Date": "2023-08-31 12:03:17.301846",
    "Solar_Irradiance_W/m2": 154.02878828830984,
    "Panel_Temperature_C": 31.93605654757807,
    "Ambient_Temperature_C": 13.459472951207132,
    "Cloud_Cover_%": 32.52951340230311,
    "Energy_Generated_kWh": 49.656526066566414,
    "CO2_Saved_kg": 54.21546083536561,
    "Money_Saved_INR": 297.9391563993985
  },
  {
    "Date": "2023-09-01 12:03:17.301846",
    "Solar_Irradiance_W/m2": 277.496720250877,
    "Panel_Temperature_C": 33.06149220032008,
    "Ambient_Temperature_C": 22.931885067030436,
    "Cloud_Cover_%": 71.26213330985128,
    "Energy_Generated_kWh": 95.01158335043532,
    "CO2_Saved_kg": 52.66818396295402,
    "Money_Saved_INR": 570.0695001026119
  },
  {
    "Date": "2023-09-02 12:03:17.301846",
    "Solar_Irradiance_W/m2": 160.83733538318813,
    "Panel_Temperature_C": 36.429326953624525,
    "Ambient_Temperature_C": 34.33407982703638,
    "Cloud_Cover_%": 81.6779466505636,
    "Energy_Generated_kWh": 71.67611190229492,
    "CO2_Saved_kg": 46.60877720729961,
    "Money_Saved_INR": 430.05667141376955
  },
  {
    "Date": "2023-09-03 12:03:17.301846",
    "Solar_Irradiance_W/m2": 183.89692418971623,
    "Panel_Temperature_C": 36.67228394993513,
    "Ambient_Temperature_C": 44.40246828798189,
    "Cloud_Cover_%": 18.161396775660265,
    "Energy_Generated_kWh": 57.398613219192846,
    "CO2_Saved_kg": 53.700611152689554,
    "Money_Saved_INR": 344.3916793151571
  },
  {
    "Date": "2023-09-04 12:03:17.301846",
    "Solar_Irradiance_W/m2": 240.67586086848348,
    "Panel_Temperature_C": 38.29272136336415,
    "Ambient_Temperature_C": 30.145555953727854,
    "Cloud_Cover_%": 37.09410081577652,
    "Energy_Generated_kWh": 70.99974284008373,
    "CO2_Saved_kg": 48.762673199002435,
    "Money_Saved_INR": 425.99845704050233
  },
  {
    "Date": "2023-09-05 12:03:17.301846",
    "Solar_Irradiance_W/m2": 138.45678417830223,
    "Panel_Temperature_C": 45.05102269383175,
    "Ambient_Temperature_C": 24.903979411396058,
    "Cloud_Cover_%": 90.19401967491501,
    "Energy_Generated_kWh": 105.14298433725145,
    "CO2_Saved_kg": 54.57805609925785,
    "Money_Saved_INR": 630.8579060235087
  },
  {
    "Date": "2023-09-06 12:03:17.301846",
    "Solar_Irradiance_W/m2": 211.37299673020647,
    "Panel_Temperature_C": 34.11526386252975,
    "Ambient_Temperature_C": 28.71972491226612,
    "Cloud_Cover_%": 80.66935196947392,
    "Energy_Generated_kWh": 69.29329825967554,
    "CO2_Saved_kg": 45.03067974882022,
    "Money_Saved_INR": 415.7597895580532
  },
  {
    "Date": "2023-09-07 12:03:17.301846",
    "Solar_Irradiance_W/m2": 265.3571377141214,
    "Panel_Temperature_C": 31.00851377730773,
    "Ambient_Temperature_C": 39.62413493403729,
    "Cloud_Cover_%": 98.48584027624759,
    "Energy_Generated_kWh": 87.1690723641924,
    "CO2_Saved_kg": 48.17431025620459,
    "Money_Saved_INR": 523.0144341851544
  },
  {
    "Date": "2023-09-08 12:03:17.301846",
    "Solar_Irradiance_W/m2": 119.62583827193862,
    "Panel_Temperature_C": 28.103403859927365,
    "Ambient_Temperature_C": 25.478250746128253,
    "Cloud_Cover_%": 75.42482596820807,
    "Energy_Generated_kWh": 65.38087448569053,
    "CO2_Saved_kg": 40.10042207447986,
    "Money_Saved_INR": 392.28524691414316
  },
  {
    "Date": "2023-09-09 12:03:17.301846",
    "Solar_Irradiance_W/m2": 209.2316929266152,
    "Panel_Temperature_C": 31.345349800290403,
    "Ambient_Temperature_C": 24.405655953448225,
    "Cloud_Cover_%": 39.319520102792225,
    "Energy_Generated_kWh": 95.1584369984724,
    "CO2_Saved_kg": 49.64992389993764,
    "Money_Saved_INR": 570.9506219908344
  },
  {
    "Date": "2023-09-10 12:03:17.301846",
    "Solar_Irradiance_W/m2": 212.99413971242117,
    "Panel_Temperature_C": 34.83436513563102,
    "Ambient_Temperature_C": 26.620795344725774,
    "Cloud_Cover_%": 59.06378339946377,
    "Energy_Generated_kWh": 93.71015477580409,
    "CO2_Saved_kg": 41.88999136371155,
    "Money_Saved_INR": 562.2609286548245
  },
  {
    "Date": "2023-09-11 12:03:17.301846",
    "Solar_Irradiance_W/m2": 239.09114358886552,
    "Panel_Temperature_C": 43.97278931758894,
    "Ambient_Temperature_C": 23.326699742189014,
    "Cloud_Cover_%": 66.10142542473203,
    "Energy_Generated_kWh": 116.97217666592823,
    "CO2_Saved_kg": 38.85953549838007,
    "Money_Saved_INR": 701.8330599955693
  },
  {
    "Date": "2023-09-12 12:03:17.301846",
    "Solar_Irradiance_W/m2": 138.1524644560959,
    "Panel_Temperature_C": 32.41194350481914,
    "Ambient_Temperature_C": 30.858692211963568,
    "Cloud_Cover_%": 7.845581631712395,
    "Energy_Generated_kWh": 76.48872109001569,
    "CO2_Saved_kg": 52.586611478553884,
    "Money_Saved_INR": 458.9323265400941
  },
  {
    "Date": "2023-09-13 12:03:17.301846",
    "Solar_Irradiance_W/m2": 133.9771693457862,
    "Panel_Temperature_C": 36.11893975819449,
    "Ambient_Temperature_C": 41.37274920928692,
    "Cloud_Cover_%": 54.44969591038651,
    "Energy_Generated_kWh": 93.37309609515813,
    "CO2_Saved_kg": 52.127397758576606,
    "Money_Saved_INR": 560.2385765709488
  },
  {
    "Date": "2023-09-14 12:03:17.301846",
    "Solar_Irradiance_W/m2": 226.09707828084487,
    "Panel_Temperature_C": 34.917885519636236,
    "Ambient_Temperature_C": 32.261554911812205,
    "Cloud_Cover_%": 70.93208284726096,
    "Energy_Generated_kWh": 81.9613507907789,
    "CO2_Saved_kg": 57.82873734948573,
    "Money_Saved_INR": 491.76810474467334
  },
  {
    "Date": "2023-09-15 12:03:17.301846",
    "Solar_Irradiance_W/m2": 214.8492336616593,
    "Panel_Temperature_C": 40.94196636724042,
    "Ambient_Temperature_C": 28.233525485115987,
    "Cloud_Cover_%": 16.732130400106037,
    "Energy_Generated_kWh": 105.91743563726028,
    "CO2_Saved_kg": 45.68874430424901,
    "Money_Saved_INR": 635.5046138235617
  },
  {
    "Date": "2023-09-16 12:03:17.301846",
    "Solar_Irradiance_W/m2": 212.52464251729384,
    "Panel_Temperature_C": 47.63466212936811,
    "Ambient_Temperature_C": 27.957321117591192,
    "Cloud_Cover_%": 78.06317174255571,
    "Energy_Generated_kWh": 65.6233522478254,
    "CO2_Saved_kg": 54.08052846836756,
    "Money_Saved_INR": 393.7401134869524
  },
  {
    "Date": "2023-09-17 12:03:17.301846",
    "Solar_Irradiance_W/m2": 217.3224104748488,
    "Panel_Temperature_C": 32.3456561353984,
    "Ambient_Temperature_C": 19.0576643391234,
    "Cloud_Cover_%": 58.37727805141116,
    "Energy_Generated_kWh": 94.90010625754562,
    "CO2_Saved_kg": 55.50797572273663,
    "Money_Saved_INR": 569.4006375452736
  },
  {
    "Date": "2023-09-18 12:03:17.301846",
    "Solar_Irradiance_W/m2": 165.99876392107547,
    "Panel_Temperature_C": 32.552802787408886,
    "Ambient_Temperature_C": 36.18176844003011,
    "Cloud_Cover_%": 95.22217856975946,
    "Energy_Generated_kWh": 76.10605407766637,
    "CO2_Saved_kg": 54.44773807831595,
    "Money_Saved_INR": 456.6363244659982
  },
  {
    "Date": "2023-09-19 12:03:17.301846",
    "Solar_Irradiance_W/m2": 211.6126848580502,
    "Panel_Temperature_C": 40.22080438534536,
    "Ambient_Temperature_C": 29.455139620910387,
    "Cloud_Cover_%": 4.24222982068917,
    "Energy_Generated_kWh": 78.71623645783005,
    "CO2_Saved_kg": 41.743463171978576,
    "Money_Saved_INR": 472.29741874698027
  },
  {
    "Date": "2023-09-20 12:03:17.301846",
    "Solar_Irradiance_W/m2": 214.65362366493406,
    "Panel_Temperature_C": 38.409457448131555,
    "Ambient_Temperature_C": 28.73664060486562,
    "Cloud_Cover_%": 26.5326137555467,
    "Energy_Generated_kWh": 81.83504968896746,
    "CO2_Saved_kg": 51.49363482271189,
    "Money_Saved_INR": 491.0102981338048
  },
  {
    "Date": "2023-09-21 12:03:17.301846",
    "Solar_Irradiance_W/m2": 164.2824290986816,
    "Panel_Temperature_C": 44.23353662868017,
    "Ambient_Temperature_C": 52.35175297491402,
    "Cloud_Cover_%": 60.15538792998241,
    "Energy_Generated_kWh": 85.04480792853354,
    "CO2_Saved_kg": 53.641402960546614,
    "Money_Saved_INR": 510.26884757120126
  },
  {
    "Date": "2023-09-22 12:03:17.301846",
    "Solar_Irradiance_W/m2": 293.28872555723785,
    "Panel_Temperature_C": 37.91964092662982,
    "Ambient_Temperature_C": 32.091270358559804,
    "Cloud_Cover_%": 29.65599122059307,
    "Energy_Generated_kWh": 77.67541913756084,
    "CO2_Saved_kg": 50.07178466907942,
    "Money_Saved_INR": 466.05251482536505
  },
  {
    "Date": "2023-09-23 12:03:17.301846",
    "Solar_Irradiance_W/m2": 223.69164604558938,
    "Panel_Temperature_C": 33.203539546064704,
    "Ambient_Temperature_C": 24.737462649333708,
    "Cloud_Cover_%": 71.44241640712423,
    "Energy_Generated_kWh": 84.29426366341053,
    "CO2_Saved_kg": 29.135223416289154,
    "Money_Saved_INR": 505.7655819804632
  },
  {
    "Date": "2023-09-24 12:03:17.301846",
    "Solar_Irradiance_W/m2": 140.43482513986757,
    "Panel_Temperature_C": 37.95327415346155,
    "Ambient_Temperature_C": 27.015496826561197,
    "Cloud_Cover_%": 75.9005282521931,
    "Energy_Generated_kWh": 111.56236115124369,
    "CO2_Saved_kg": 51.6048962397348,
    "Money_Saved_INR": 669.3741669074622
  },
  {
    "Date": "2023-09-25 12:03:17.301846",
    "Solar_Irradiance_W/m2": 232.82768043169148,
    "Panel_Temperature_C": 40.54351790291454,
    "Ambient_Temperature_C": 38.039119964377285,
    "Cloud_Cover_%": 10.251596406647446,
    "Energy_Generated_kWh": 99.70899371230436,
    "CO2_Saved_kg": 72.12531039397243,
    "Money_Saved_INR": 598.2539622738261
  },
  {
    "Date": "2023-09-26 12:03:17.301846",
    "Solar_Irradiance_W/m2": 151.26591648863393,
    "Panel_Temperature_C": 39.10241090598682,
    "Ambient_Temperature_C": 30.79289287376435,
    "Cloud_Cover_%": 51.38544642067677,
    "Energy_Generated_kWh": 97.38309184993793,
    "CO2_Saved_kg": 46.39960731243017,
    "Money_Saved_INR": 584.2985510996275
  },
  {
    "Date": "2023-09-27 12:03:17.301846",
    "Solar_Irradiance_W/m2": 239.3542301871226,
    "Panel_Temperature_C": 37.53637015553649,
    "Ambient_Temperature_C": 19.93205415177843,
    "Cloud_Cover_%": 50.889055559105586,
    "Energy_Generated_kWh": 70.88920947952259,
    "CO2_Saved_kg": 42.719229021446786,
    "Money_Saved_INR": 425.3352568771355
  },
  {
    "Date": "2023-09-28 12:03:17.301846",
    "Solar_Irradiance_W/m2": 257.9297789503702,
    "Panel_Temperature_C": 40.33337344794577,
    "Ambient_Temperature_C": 36.434602542026425,
    "Cloud_Cover_%": 36.92807702155411,
    "Energy_Generated_kWh": 62.21518343543352,
    "CO2_Saved_kg": 53.73348559711398,
    "Money_Saved_INR": 373.2911006126011
  },
  {
    "Date": "2023-09-29 12:03:17.301846",
    "Solar_Irradiance_W/m2": 158.96588408241448,
    "Panel_Temperature_C": 40.84647795222836,
    "Ambient_Temperature_C": 25.322991401227043,
    "Cloud_Cover_%": 93.29248625696721,
    "Energy_Generated_kWh": 99.10601116475506,
    "CO2_Saved_kg": 53.123782104665715,
    "Money_Saved_INR": 594.6360669885304
  },
  {
    "Date": "2023-09-30 12:03:17.301846",
    "Solar_Irradiance_W/m2": 248.16880646221608,
    "Panel_Temperature_C": 41.91079495518763,
    "Ambient_Temperature_C": 43.113084433522815,
    "Cloud_Cover_%": 82.75063198732212,
    "Energy_Generated_kWh": 97.52093585059589,
    "CO2_Saved_kg": 61.92735165416414,
    "Money_Saved_INR": 585.1256151035753
  },
  {
    "Date": "2023-10-01 12:03:17.301846",
    "Solar_Irradiance_W/m2": 220.63904634682493,
    "Panel_Temperature_C": 38.24354943794821,
    "Ambient_Temperature_C": 37.56033646000254,
    "Cloud_Cover_%": 69.72093819096368,
    "Energy_Generated_kWh": 109.45341351501963,
    "CO2_Saved_kg": 37.42131844091112,
    "Money_Saved_INR": 656.7204810901178
  },
  {
    "Date": "2023-10-02 12:03:17.301846",
    "Solar_Irradiance_W/m2": 241.1030079997245,
    "Panel_Temperature_C": 34.16440959841573,
    "Ambient_Temperature_C": 26.868746730388743,
    "Cloud_Cover_%": 71.43266357349975,
    "Energy_Generated_kWh": 67.9203874806154,
    "CO2_Saved_kg": 57.31380252574992,
    "Money_Saved_INR": 407.5223248836924
  },
  {
    "Date": "2023-10-03 12:03:17.301846",
    "Solar_Irradiance_W/m2": 294.8396491326974,
    "Panel_Temperature_C": 35.733568432166614,
    "Ambient_Temperature_C": 38.96711453214579,
    "Cloud_Cover_%": 46.17161438131191,
    "Energy_Generated_kWh": 75.40902689279307,
    "CO2_Saved_kg": 55.904220612514635,
    "Money_Saved_INR": 452.4541613567584
  },
  {
    "Date": "2023-10-04 12:03:17.301846",
    "Solar_Irradiance_W/m2": 187.73059419985648,
    "Panel_Temperature_C": 41.03254483254179,
    "Ambient_Temperature_C": 30.474988573691824,
    "Cloud_Cover_%": 92.09945210965759,
    "Energy_Generated_kWh": 47.21031674949132,
    "CO2_Saved_kg": 48.57853463059454,
    "Money_Saved_INR": 283.26190049694793
  },
  {
    "Date": "2023-10-05 12:03:17.301846",
    "Solar_Irradiance_W/m2": 162.31319178212553,
    "Panel_Temperature_C": 30.91532164506382,
    "Ambient_Temperature_C": 35.969415725855534,
    "Cloud_Cover_%": 69.45954272532853,
    "Energy_Generated_kWh": 72.15057787878254,
    "CO2_Saved_kg": 53.3868731792169,
    "Money_Saved_INR": 432.90346727269525
  },
  {
    "Date": "2023-10-06 12:03:17.301846",
    "Solar_Irradiance_W/m2": 155.52427851872383,
    "Panel_Temperature_C": 36.84336654436451,
    "Ambient_Temperature_C": 33.39312972106132,
    "Cloud_Cover_%": 72.89810616558164,
    "Energy_Generated_kWh": 99.93141021158894,
    "CO2_Saved_kg": 60.29457481598357,
    "Money_Saved_INR": 599.5884612695336
  },
  {
    "Date": "2023-10-07 12:03:17.301846",
    "Solar_Irradiance_W/m2": 159.2094857517281,
    "Panel_Temperature_C": 33.0333059383632,
    "Ambient_Temperature_C": 24.075503415063885,
    "Cloud_Cover_%": 86.16909037873452,
    "Energy_Generated_kWh": 70.67009241543605,
    "CO2_Saved_kg": 58.72315380028451,
    "Money_Saved_INR": 424.02055449261627
  },
  {
    "Date": "2023-10-08 12:03:17.301846",
    "Solar_Irradiance_W/m2": 196.1449145292948,
    "Panel_Temperature_C": 35.143724114674086,
    "Ambient_Temperature_C": 25.495151173777767,
    "Cloud_Cover_%": 27.4071589342191,
    "Energy_Generated_kWh": 92.80959590401648,
    "CO2_Saved_kg": 38.569806879262714,
    "Money_Saved_INR": 556.8575754240989
  },
  {
    "Date": "2023-10-09 12:03:17.301846",
    "Solar_Irradiance_W/m2": 217.0575987408322,
    "Panel_Temperature_C": 41.39225931303649,
    "Ambient_Temperature_C": 37.20972572306813,
    "Cloud_Cover_%": 80.7070903866703,
    "Energy_Generated_kWh": 76.18993788004377,
    "CO2_Saved_kg": 58.20158186755484,
    "Money_Saved_INR": 457.13962728026263
  },
  {
    "Date": "2023-10-10 12:03:17.301846",
    "Solar_Irradiance_W/m2": 213.83453996650096,
    "Panel_Temperature_C": 35.95549534009952,
    "Ambient_Temperature_C": 27.656572675254214,
    "Cloud_Cover_%": 19.524060295649203,
    "Energy_Generated_kWh": 86.48114056443121,
    "CO2_Saved_kg": 49.353113949674814,
    "Money_Saved_INR": 518.8868433865873
  },
  {
    "Date": "2023-10-11 12:03:17.301846",
    "Solar_Irradiance_W/m2": 241.35916245180118,
    "Panel_Temperature_C": 35.23218274078074,
    "Ambient_Temperature_C": 27.174460757306022,
    "Cloud_Cover_%": 34.53419522448878,
    "Energy_Generated_kWh": 57.04617220368665,
    "CO2_Saved_kg": 50.72874098015515,
    "Money_Saved_INR": 342.27703322211994
  },
  {
    "Date": "2023-10-12 12:03:17.301846",
    "Solar_Irradiance_W/m2": 200.65009459389535,
    "Panel_Temperature_C": 28.200719295100406,
    "Ambient_Temperature_C": 23.314141944554528,
    "Cloud_Cover_%": 33.56104542698427,
    "Energy_Generated_kWh": 81.70418899267803,
    "CO2_Saved_kg": 50.73196991001694,
    "Money_Saved_INR": 490.22513395606813
  },
  {
    "Date": "2023-10-13 12:03:17.301846",
    "Solar_Irradiance_W/m2": 272.67670385786585,
    "Panel_Temperature_C": 38.731267830136105,
    "Ambient_Temperature_C": 32.96519345915423,
    "Cloud_Cover_%": 97.85254683891405,
    "Energy_Generated_kWh": 20.177280581985535,
    "CO2_Saved_kg": 48.4975701120174,
    "Money_Saved_INR": 121.06368349191321
  },
  {
    "Date": "2023-10-14 12:03:17.301846",
    "Solar_Irradiance_W/m2": 186.7671583381022,
    "Panel_Temperature_C": 38.22742090570538,
    "Ambient_Temperature_C": 44.43767443470202,
    "Cloud_Cover_%": 85.65372237479268,
    "Energy_Generated_kWh": 76.2620768367603,
    "CO2_Saved_kg": 61.91707497107065,
    "Money_Saved_INR": 457.57246102056183
  },
  {
    "Date": "2023-10-15 12:03:17.301846",
    "Solar_Irradiance_W/m2": 336.00845832948096,
    "Panel_Temperature_C": 45.8162736165273,
    "Ambient_Temperature_C": 22.52726960022009,
    "Cloud_Cover_%": 70.11698615902597,
    "Energy_Generated_kWh": 47.3905351256972,
    "CO2_Saved_kg": 49.16282040150788,
    "Money_Saved_INR": 284.3432107541832
  },
  {
    "Date": "2023-10-16 12:03:17.301846",
    "Solar_Irradiance_W/m2": 231.28336738825033,
    "Panel_Temperature_C": 33.461108825234994,
    "Ambient_Temperature_C": 30.169536196709306,
    "Cloud_Cover_%": 72.70567616153902,
    "Energy_Generated_kWh": 104.11989033093633,
    "CO2_Saved_kg": 38.80453871616831,
    "Money_Saved_INR": 624.719341985618
  },
  {
    "Date": "2023-10-17 12:03:17.301846",
    "Solar_Irradiance_W/m2": 157.1421221791859,
    "Panel_Temperature_C": 36.0957516383197,
    "Ambient_Temperature_C": 39.88554388790801,
    "Cloud_Cover_%": 56.20727944025711,
    "Energy_Generated_kWh": 95.54814705529023,
    "CO2_Saved_kg": 46.06470144030271,
    "Money_Saved_INR": 573.2888823317414
  },
  {
    "Date": "2023-10-18 12:03:17.301846",
    "Solar_Irradiance_W/m2": 146.45537509694438,
    "Panel_Temperature_C": 36.246918418553776,
    "Ambient_Temperature_C": 29.442510261279995,
    "Cloud_Cover_%": 94.70906671085191,
    "Energy_Generated_kWh": 89.33341963932162,
    "CO2_Saved_kg": 51.78694716810475,
    "Money_Saved_INR": 536.0005178359297
  },
  {
    "Date": "2023-10-19 12:03:17.301846",
    "Solar_Irradiance_W/m2": 224.12362076215928,
    "Panel_Temperature_C": 42.887266398817374,
    "Ambient_Temperature_C": 33.166602573748136,
    "Cloud_Cover_%": 49.62587528823615,
    "Energy_Generated_kWh": 110.4201245431876,
    "CO2_Saved_kg": 62.29214784297051,
    "Money_Saved_INR": 662.5207472591255
  },
  {
    "Date": "2023-10-20 12:03:17.301846",
    "Solar_Irradiance_W/m2": 188.82686073370746,
    "Panel_Temperature_C": 34.52352233806524,
    "Ambient_Temperature_C": 22.563245302971843,
    "Cloud_Cover_%": 38.05177098698945,
    "Energy_Generated_kWh": 61.021669583503254,
    "CO2_Saved_kg": 56.03094684948834,
    "Money_Saved_INR": 366.13001750101955
  },
  {
    "Date": "2023-10-21 12:03:17.301846",
    "Solar_Irradiance_W/m2": 235.7000247046046,
    "Panel_Temperature_C": 36.3951076288517,
    "Ambient_Temperature_C": 32.99814968045354,
    "Cloud_Cover_%": 16.3035336931591,
    "Energy_Generated_kWh": 114.94726395831117,
    "CO2_Saved_kg": 41.49464721252956,
    "Money_Saved_INR": 689.683583749867
  },
  {
    "Date": "2023-10-22 12:03:17.301846",
    "Solar_Irradiance_W/m2": 223.66188122867723,
    "Panel_Temperature_C": 38.0394825485827,
    "Ambient_Temperature_C": 28.68999014496816,
    "Cloud_Cover_%": 78.6205652261058,
    "Energy_Generated_kWh": 98.6438312852077,
    "CO2_Saved_kg": 74.85189916678891,
    "Money_Saved_INR": 591.8629877112462
  },
  {
    "Date": "2023-10-23 12:03:17.301846",
    "Solar_Irradiance_W/m2": 196.35855436715636,
    "Panel_Temperature_C": 35.93304561578179,
    "Ambient_Temperature_C": 36.90010996975904,
    "Cloud_Cover_%": 73.44439320755914,
    "Energy_Generated_kWh": 75.26889425562108,
    "CO2_Saved_kg": 52.6477531097798,
    "Money_Saved_INR": 451.61336553372644
  },
  {
    "Date": "2023-10-24 12:03:17.301846",
    "Solar_Irradiance_W/m2": 157.66031409657975,
    "Panel_Temperature_C": 32.76783192724736,
    "Ambient_Temperature_C": 38.31170236095326,
    "Cloud_Cover_%": 38.43550385241349,
    "Energy_Generated_kWh": 102.71240294365889,
    "CO2_Saved_kg": 62.753907379990146,
    "Money_Saved_INR": 616.2744176619533
  },
  {
    "Date": "2023-10-25 12:03:17.301846",
    "Solar_Irradiance_W/m2": 124.25763876570677,
    "Panel_Temperature_C": 35.970449964491536,
    "Ambient_Temperature_C": 48.1269454941303,
    "Cloud_Cover_%": 2.519341395922936,
    "Energy_Generated_kWh": 57.87412975176731,
    "CO2_Saved_kg": 48.482855664227706,
    "Money_Saved_INR": 347.24477851060385
  },
  {
    "Date": "2023-10-26 12:03:17.301846",
    "Solar_Irradiance_W/m2": 177.67425239664894,
    "Panel_Temperature_C": 40.36815874929886,
    "Ambient_Temperature_C": 34.05743221249503,
    "Cloud_Cover_%": 83.89973277180107,
    "Energy_Generated_kWh": 63.50971676944653,
    "CO2_Saved_kg": 55.33359244705449,
    "Money_Saved_INR": 381.05830061667916
  },
  {
    "Date": "2023-10-27 12:03:17.301846",
    "Solar_Irradiance_W/m2": 242.81993971617362,
    "Panel_Temperature_C": 29.8674235029447,
    "Ambient_Temperature_C": 32.280574216075166,
    "Cloud_Cover_%": 1.1417983454073632,
    "Energy_Generated_kWh": 67.828205535206,
    "CO2_Saved_kg": 58.39468504518405,
    "Money_Saved_INR": 406.969233211236
  },
  {
    "Date": "2023-10-28 12:03:17.301846",
    "Solar_Irradiance_W/m2": 210.7046872065102,
    "Panel_Temperature_C": 35.66484837073438,
    "Ambient_Temperature_C": 31.36069011104135,
    "Cloud_Cover_%": 70.3699779629051,
    "Energy_Generated_kWh": 69.4204458387197,
    "CO2_Saved_kg": 62.18194711754256,
    "Money_Saved_INR": 416.5226750323182
  },
  {
    "Date": "2023-10-29 12:03:17.301846",
    "Solar_Irradiance_W/m2": 137.7130610644006,
    "Panel_Temperature_C": 31.499395925304135,
    "Ambient_Temperature_C": 27.527835950325183,
    "Cloud_Cover_%": 97.02571097260571,
    "Energy_Generated_kWh": 58.86884714479494,
    "CO2_Saved_kg": 60.57368305378225,
    "Money_Saved_INR": 353.2130828687697
  },
  {
    "Date": "2023-10-30 12:03:17.301846",
    "Solar_Irradiance_W/m2": 208.6590462925591,
    "Panel_Temperature_C": 40.97523314462421,
    "Ambient_Temperature_C": 32.36938690423184,
    "Cloud_Cover_%": 43.766132814820345,
    "Energy_Generated_kWh": 104.4616613419065,
    "CO2_Saved_kg": 58.721970000729776,
    "Money_Saved_INR": 626.769968051439
  },
  {
    "Date": "2023-10-31 12:03:17.301846",
    "Solar_Irradiance_W/m2": 219.26586898644183,
    "Panel_Temperature_C": 27.384065476081126,
    "Ambient_Temperature_C": 27.932190129026793,
    "Cloud_Cover_%": 23.497340499595275,
    "Energy_Generated_kWh": 74.82291199260337,
    "CO2_Saved_kg": 46.849132688058916,
    "Money_Saved_INR": 448.9374719556202
  },
  {
    "Date": "2023-11-01 12:03:17.301846",
    "Solar_Irradiance_W/m2": 155.80712818994334,
    "Panel_Temperature_C": 32.20539076364206,
    "Ambient_Temperature_C": 31.1792268338873,
    "Cloud_Cover_%": 70.48710100433817,
    "Energy_Generated_kWh": 87.05009936713759,
    "CO2_Saved_kg": 44.28253958043938,
    "Money_Saved_INR": 522.3005962028255
  },
  {
    "Date": "2023-11-02 12:03:17.301846",
    "Solar_Irradiance_W/m2": 207.6862552972764,
    "Panel_Temperature_C": 36.8860593753226,
    "Ambient_Temperature_C": 39.22318274925572,
    "Cloud_Cover_%": 81.71281420155852,
    "Energy_Generated_kWh": 68.59297267172639,
    "CO2_Saved_kg": 53.326075103241976,
    "Money_Saved_INR": 411.5578360303583
  },
  {
    "Date": "2023-11-03 12:03:17.301846",
    "Solar_Irradiance_W/m2": 202.9104359223,
    "Panel_Temperature_C": 42.827620146171704,
    "Ambient_Temperature_C": 22.954202043042514,
    "Cloud_Cover_%": 54.64303160778473,
    "Energy_Generated_kWh": 43.58793398902966,
    "CO2_Saved_kg": 59.33128072341069,
    "Money_Saved_INR": 261.52760393417793
  },
  {
    "Date": "2023-11-04 12:03:17.301846",
    "Solar_Irradiance_W/m2": 142.85148510846884,
    "Panel_Temperature_C": 34.67124869463506,
    "Ambient_Temperature_C": 37.97914992790332,
    "Cloud_Cover_%": 96.70352752561462,
    "Energy_Generated_kWh": 85.40114716782844,
    "CO2_Saved_kg": 47.77279299223393,
    "Money_Saved_INR": 512.4068830069707
  },
  {
    "Date": "2023-11-05 12:03:17.301846",
    "Solar_Irradiance_W/m2": 217.88936801741417,
    "Panel_Temperature_C": 32.22400236653401,
    "Ambient_Temperature_C": 39.21980547137906,
    "Cloud_Cover_%": 5.166872165796111,
    "Energy_Generated_kWh": 41.75490049160446,
    "CO2_Saved_kg": 60.651719657143865,
    "Money_Saved_INR": 250.52940294962676
  },
  {
    "Date": "2023-11-06 12:03:17.301846",
    "Solar_Irradiance_W/m2": 228.03922631841172,
    "Panel_Temperature_C": 44.40578534720295,
    "Ambient_Temperature_C": 29.17352031106245,
    "Cloud_Cover_%": 50.479559830452814,
    "Energy_Generated_kWh": 78.62731907829063,
    "CO2_Saved_kg": 64.52616745486179,
    "Money_Saved_INR": 471.7639144697438
  },
  {
    "Date": "2023-11-07 12:03:17.301846",
    "Solar_Irradiance_W/m2": 254.15256215876386,
    "Panel_Temperature_C": 27.75993049791878,
    "Ambient_Temperature_C": 15.147015706939838,
    "Cloud_Cover_%": 71.845394732255,
    "Energy_Generated_kWh": 52.63369922334379,
    "CO2_Saved_kg": 40.83679080926581,
    "Money_Saved_INR": 315.8021953400627
  },
  {
    "Date": "2023-11-08 12:03:17.301846",
    "Solar_Irradiance_W/m2": 252.69010260174514,
    "Panel_Temperature_C": 24.00597021689959,
    "Ambient_Temperature_C": 25.745246090338973,
    "Cloud_Cover_%": 86.2640471149179,
    "Energy_Generated_kWh": 119.74551998461615,
    "CO2_Saved_kg": 41.630792962037205,
    "Money_Saved_INR": 718.4731199076969
  },
  {
    "Date": "2023-11-09 12:03:17.301846",
    "Solar_Irradiance_W/m2": 131.11653160214544,
    "Panel_Temperature_C": 37.200072250266665,
    "Ambient_Temperature_C": 39.07896182592776,
    "Cloud_Cover_%": 17.925561190779003,
    "Energy_Generated_kWh": 98.22725444349443,
    "CO2_Saved_kg": 48.59624941094663,
    "Money_Saved_INR": 589.3635266609666
  },
  {
    "Date": "2023-11-10 12:03:17.301846",
    "Solar_Irradiance_W/m2": 153.10874800424386,
    "Panel_Temperature_C": 32.489728878236946,
    "Ambient_Temperature_C": 29.839923563907824,
    "Cloud_Cover_%": 80.00034817636814,
    "Energy_Generated_kWh": 82.11507582542961,
    "CO2_Saved_kg": 53.076126681891964,
    "Money_Saved_INR": 492.6904549525777
  },
  {
    "Date": "2023-11-11 12:03:17.301846",
    "Solar_Irradiance_W/m2": 225.751763360433,
    "Panel_Temperature_C": 29.893835914346433,
    "Ambient_Temperature_C": 23.004884373935624,
    "Cloud_Cover_%": 55.27070757185453,
    "Energy_Generated_kWh": 105.27413355309338,
    "CO2_Saved_kg": 44.75432986232949,
    "Money_Saved_INR": 631.6448013185602
  },
  {
    "Date": "2023-11-12 12:03:17.301846",
    "Solar_Irradiance_W/m2": 225.68929754561043,
    "Panel_Temperature_C": 38.541782236496765,
    "Ambient_Temperature_C": 26.466575551402478,
    "Cloud_Cover_%": 39.65536819899632,
    "Energy_Generated_kWh": 63.07368045068529,
    "CO2_Saved_kg": 63.52202678867144,
    "Money_Saved_INR": 378.4420827041117
  },
  {
    "Date": "2023-11-13 12:03:17.301846",
    "Solar_Irradiance_W/m2": 225.7523843153024,
    "Panel_Temperature_C": 36.219003568855996,
    "Ambient_Temperature_C": 35.88434018553187,
    "Cloud_Cover_%": 13.171502857909356,
    "Energy_Generated_kWh": 90.86958757340186,
    "CO2_Saved_kg": 54.24066861518451,
    "Money_Saved_INR": 545.2175254404111
  },
  {
    "Date": "2023-11-14 12:03:17.301846",
    "Solar_Irradiance_W/m2": 392.63657453273606,
    "Panel_Temperature_C": 32.17960684631636,
    "Ambient_Temperature_C": 33.827134977409656,
    "Cloud_Cover_%": 86.52957589089124,
    "Energy_Generated_kWh": 83.99620867437427,
    "CO2_Saved_kg": 50.39447048240739,
    "Money_Saved_INR": 503.97725204624567
  },
  {
    "Date": "2023-11-15 12:03:17.301846",
    "Solar_Irradiance_W/m2": 228.54452553465836,
    "Panel_Temperature_C": 28.59847800664553,
    "Ambient_Temperature_C": 28.32747530581214,
    "Cloud_Cover_%": 15.727320817971535,
    "Energy_Generated_kWh": 85.2804016266734,
    "CO2_Saved_kg": 35.64090476131472,
    "Money_Saved_INR": 511.6824097600404
  },
  {
    "Date": "2023-11-16 12:03:17.301846",
    "Solar_Irradiance_W/m2": 256.77828200902997,
    "Panel_Temperature_C": 39.36228664140072,
    "Ambient_Temperature_C": 27.432229117297187,
    "Cloud_Cover_%": 30.978785920909925,
    "Energy_Generated_kWh": 105.44707000213535,
    "CO2_Saved_kg": 36.84184183572493,
    "Money_Saved_INR": 632.6824200128121
  },
  {
    "Date": "2023-11-17 12:03:17.301846",
    "Solar_Irradiance_W/m2": 247.70008817466012,
    "Panel_Temperature_C": 38.251005889793305,
    "Ambient_Temperature_C": 27.257692956693248,
    "Cloud_Cover_%": 29.004553196243688,
    "Energy_Generated_kWh": 94.64984205559604,
    "CO2_Saved_kg": 52.810092502818065,
    "Money_Saved_INR": 567.8990523335763
  },
  {
    "Date": "2023-11-18 12:03:17.301846",
    "Solar_Irradiance_W/m2": 232.5695625652899,
    "Panel_Temperature_C": 34.50412068110309,
    "Ambient_Temperature_C": 23.543128708510483,
    "Cloud_Cover_%": 87.14140341908544,
    "Energy_Generated_kWh": 85.77447325650047,
    "CO2_Saved_kg": 28.674043738451637,
    "Money_Saved_INR": 514.6468395390028
  },
  {
    "Date": "2023-11-19 12:03:17.301846",
    "Solar_Irradiance_W/m2": 184.23653776798272,
    "Panel_Temperature_C": 44.23318498023833,
    "Ambient_Temperature_C": 41.30762982628609,
    "Cloud_Cover_%": 67.2702994208898,
    "Energy_Generated_kWh": 46.902251275434075,
    "CO2_Saved_kg": 60.12637409644071,
    "Money_Saved_INR": 281.41350765260444
  },
  {
    "Date": "2023-11-20 12:03:17.301846",
    "Solar_Irradiance_W/m2": 237.94846102466337,
    "Panel_Temperature_C": 29.649576168369236,
    "Ambient_Temperature_C": 27.74375671552062,
    "Cloud_Cover_%": 79.66813971913723,
    "Energy_Generated_kWh": 60.79907409441073,
    "CO2_Saved_kg": 48.418461556276796,
    "Money_Saved_INR": 364.79444456646434
  },
  {
    "Date": "2023-11-21 12:03:17.301846",
    "Solar_Irradiance_W/m2": 161.35873927312142,
    "Panel_Temperature_C": 27.372374145376305,
    "Ambient_Temperature_C": 38.520109645778476,
    "Cloud_Cover_%": 25.046789879249896,
    "Energy_Generated_kWh": 77.54582132808552,
    "CO2_Saved_kg": 82.43092969594733,
    "Money_Saved_INR": 465.2749279685131
  },
  {
    "Date": "2023-11-22 12:03:17.301846",
    "Solar_Irradiance_W/m2": 188.15906966299957,
    "Panel_Temperature_C": 31.540459650593778,
    "Ambient_Temperature_C": 40.64921236345716,
    "Cloud_Cover_%": 62.48740996069989,
    "Energy_Generated_kWh": 81.86744748553302,
    "CO2_Saved_kg": 73.07916250616111,
    "Money_Saved_INR": 491.2046849131981
  },
  {
    "Date": "2023-11-23 12:03:17.301846",
    "Solar_Irradiance_W/m2": 175.73182260854483,
    "Panel_Temperature_C": 34.77206991822251,
    "Ambient_Temperature_C": 36.98817628703572,
    "Cloud_Cover_%": 57.17459831437487,
    "Energy_Generated_kWh": 57.39592550652152,
    "CO2_Saved_kg": 48.18550930752483,
    "Money_Saved_INR": 344.37555303912916
  },
  {
    "Date": "2023-11-24 12:03:17.301846",
    "Solar_Irradiance_W/m2": 204.09370696931612,
    "Panel_Temperature_C": 36.21669724661346,
    "Ambient_Temperature_C": 26.97865781097366,
    "Cloud_Cover_%": 83.28303767882711,
    "Energy_Generated_kWh": 128.23353351156842,
    "CO2_Saved_kg": 48.93662997468685,
    "Money_Saved_INR": 769.4012010694105
  },
  {
    "Date": "2023-11-25 12:03:17.301846",
    "Solar_Irradiance_W/m2": 315.73292833367543,
    "Panel_Temperature_C": 33.79381971071835,
    "Ambient_Temperature_C": 32.82611063235627,
    "Cloud_Cover_%": 90.60870604812605,
    "Energy_Generated_kWh": 110.32788110507146,
    "CO2_Saved_kg": 59.9558151400203,
    "Money_Saved_INR": 661.9672866304287
  },
  {
    "Date": "2023-11-26 12:03:17.301846",
    "Solar_Irradiance_W/m2": 106.6367403704126,
    "Panel_Temperature_C": 36.76027698257148,
    "Ambient_Temperature_C": 29.830630755263588,
    "Cloud_Cover_%": 1.2156771477386807,
    "Energy_Generated_kWh": 92.04236640784967,
    "CO2_Saved_kg": 67.03172609918037,
    "Money_Saved_INR": 552.254198447098
  },
  {
    "Date": "2023-11-27 12:03:17.301846",
    "Solar_Irradiance_W/m2": 234.31300951872566,
    "Panel_Temperature_C": 28.74230287904778,
    "Ambient_Temperature_C": 23.674086974889104,
    "Cloud_Cover_%": 67.40199190587927,
    "Energy_Generated_kWh": 81.4407372256749,
    "CO2_Saved_kg": 33.61970942563983,
    "Money_Saved_INR": 488.64442335404937
  },
  {
    "Date": "2023-11-28 12:03:17.301846",
    "Solar_Irradiance_W/m2": 119.36420644051742,
    "Panel_Temperature_C": 42.2188230203663,
    "Ambient_Temperature_C": 32.270514972051224,
    "Cloud_Cover_%": 5.1835799119729025,
    "Energy_Generated_kWh": 75.75582060197696,
    "CO2_Saved_kg": 32.13624534645314,
    "Money_Saved_INR": 454.5349236118618
  },
  {
    "Date": "2023-11-29 12:03:17.301846",
    "Solar_Irradiance_W/m2": 176.40340671052832,
    "Panel_Temperature_C": 34.58924410803716,
    "Ambient_Temperature_C": 21.746721461881382,
    "Cloud_Cover_%": 54.88586650773559,
    "Energy_Generated_kWh": 60.96163079955529,
    "CO2_Saved_kg": 43.779651944456184,
    "Money_Saved_INR": 365.76978479733174
  },
  {
    "Date": "2023-11-30 12:03:17.301846",
    "Solar_Irradiance_W/m2": 254.4475298483683,
    "Panel_Temperature_C": 40.58647915794064,
    "Ambient_Temperature_C": 38.31375571923095,
    "Cloud_Cover_%": 28.76327290436782,
    "Energy_Generated_kWh": 81.54961037037725,
    "CO2_Saved_kg": 55.82737583173864,
    "Money_Saved_INR": 489.2976622222635
  },
  {
    "Date": "2023-12-01 12:03:17.301846",
    "Solar_Irradiance_W/m2": 203.21400095477313,
    "Panel_Temperature_C": 36.71362673188852,
    "Ambient_Temperature_C": 26.747678918911248,
    "Cloud_Cover_%": 30.67765995221412,
    "Energy_Generated_kWh": 85.15505080285502,
    "CO2_Saved_kg": 54.968735905075974,
    "Money_Saved_INR": 510.9303048171301
  },
  {
    "Date": "2023-12-02 12:03:17.301846",
    "Solar_Irradiance_W/m2": 146.1127611035347,
    "Panel_Temperature_C": 37.28376609576892,
    "Ambient_Temperature_C": 31.408117591109875,
    "Cloud_Cover_%": 35.29585034523566,
    "Energy_Generated_kWh": 55.16478849036751,
    "CO2_Saved_kg": 60.6977145498385,
    "Money_Saved_INR": 330.98873094220505
  },
  {
    "Date": "2023-12-03 12:03:17.301846",
    "Solar_Irradiance_W/m2": 164.2348145370016,
    "Panel_Temperature_C": 37.84883640116102,
    "Ambient_Temperature_C": 31.983015100822996,
    "Cloud_Cover_%": 62.12924490496101,
    "Energy_Generated_kWh": 86.68352834489795,
    "CO2_Saved_kg": 38.003024716346914,
    "Money_Saved_INR": 520.1011700693878
  },
  {
    "Date": "2023-12-04 12:03:17.301846",
    "Solar_Irradiance_W/m2": 233.97988744673378,
    "Panel_Temperature_C": 37.23854280008658,
    "Ambient_Temperature_C": 28.18766518407146,
    "Cloud_Cover_%": 33.40499656687692,
    "Energy_Generated_kWh": 76.89481902350502,
    "CO2_Saved_kg": 26.838561370311233,
    "Money_Saved_INR": 461.36891414103013
  },
  {
    "Date": "2023-12-05 12:03:17.301846",
    "Solar_Irradiance_W/m2": 163.48166841414317,
    "Panel_Temperature_C": 38.21361379933772,
    "Ambient_Temperature_C": 34.10685661032692,
    "Cloud_Cover_%": 73.26990505902803,
    "Energy_Generated_kWh": 41.84384884245218,
    "CO2_Saved_kg": 58.58014195302145,
    "Money_Saved_INR": 251.06309305471308
  },
  {
    "Date": "2023-12-06 12:03:17.301846",
    "Solar_Irradiance_W/m2": 210.82292947909875,
    "Panel_Temperature_C": 41.64576265066216,
    "Ambient_Temperature_C": 26.67567440364233,
    "Cloud_Cover_%": 40.45273855738697,
    "Energy_Generated_kWh": 62.79229978440996,
    "CO2_Saved_kg": 41.71803727034765,
    "Money_Saved_INR": 376.75379870645975
  },
  {
    "Date": "2023-12-07 12:03:17.301846",
    "Solar_Irradiance_W/m2": 202.27859199519068,
    "Panel_Temperature_C": 35.98260584850735,
    "Ambient_Temperature_C": 36.09908108220071,
    "Cloud_Cover_%": 6.835320030995861,
    "Energy_Generated_kWh": 71.72788933156711,
    "CO2_Saved_kg": 29.81512135611362,
    "Money_Saved_INR": 430.3673359894027
  },
  {
    "Date": "2023-12-08 12:03:17.301846",
    "Solar_Irradiance_W/m2": 167.41998261970915,
    "Panel_Temperature_C": 38.54501878794256,
    "Ambient_Temperature_C": 20.57814223827276,
    "Cloud_Cover_%": 78.37598424841073,
    "Energy_Generated_kWh": 117.7537531468038,
    "CO2_Saved_kg": 51.450637459593814,
    "Money_Saved_INR": 706.5225188808229
  },
  {
    "Date": "2023-12-09 12:03:17.301846",
    "Solar_Irradiance_W/m2": 307.19720446626627,
    "Panel_Temperature_C": 34.55132152856387,
    "Ambient_Temperature_C": 30.88465705682488,
    "Cloud_Cover_%": 28.5758324592706,
    "Energy_Generated_kWh": 91.13106249067516,
    "CO2_Saved_kg": 57.931756882186775,
    "Money_Saved_INR": 546.786374944051
  },
  {
    "Date": "2023-12-10 12:03:17.301846",
    "Solar_Irradiance_W/m2": 231.69595111590056,
    "Panel_Temperature_C": 42.200586077247365,
    "Ambient_Temperature_C": 43.572502993407994,
    "Cloud_Cover_%": 43.276687959926264,
    "Energy_Generated_kWh": 53.29036861800218,
    "CO2_Saved_kg": 48.77942867878723,
    "Money_Saved_INR": 319.7422117080131
  },
  {
    "Date": "2023-12-11 12:03:17.301846",
    "Solar_Irradiance_W/m2": 98.74287066711965,
    "Panel_Temperature_C": 31.61803848970365,
    "Ambient_Temperature_C": 22.997680727760976,
    "Cloud_Cover_%": 68.54438832219016,
    "Energy_Generated_kWh": 89.72072578835274,
    "CO2_Saved_kg": 45.42151613817511,
    "Money_Saved_INR": 538.3243547301164
  },
  {
    "Date": "2023-12-12 12:03:17.301846",
    "Solar_Irradiance_W/m2": 209.32271573847137,
    "Panel_Temperature_C": 44.004702164554075,
    "Ambient_Temperature_C": 25.25578520632604,
    "Cloud_Cover_%": 33.2456157148712,
    "Energy_Generated_kWh": 49.05392022123269,
    "CO2_Saved_kg": 48.406377678540935,
    "Money_Saved_INR": 294.3235213273961
  },
  {
    "Date": "2023-12-13 12:03:17.301846",
    "Solar_Irradiance_W/m2": 166.9106767615806,
    "Panel_Temperature_C": 34.79921024677828,
    "Ambient_Temperature_C": 33.5973549476124,
    "Cloud_Cover_%": 5.658565614671563,
    "Energy_Generated_kWh": 101.65382107774147,
    "CO2_Saved_kg": 46.29417237599217,
    "Money_Saved_INR": 609.9229264664489
  },
  {
    "Date": "2023-12-14 12:03:17.301846",
    "Solar_Irradiance_W/m2": 242.6216667398112,
    "Panel_Temperature_C": 27.84612448940976,
    "Ambient_Temperature_C": 31.257072473577185,
    "Cloud_Cover_%": 37.39210470128136,
    "Energy_Generated_kWh": 70.57750696364243,
    "CO2_Saved_kg": 36.51952888059833,
    "Money_Saved_INR": 423.4650417818546
  },
  {
    "Date": "2023-12-15 12:03:17.301846",
    "Solar_Irradiance_W/m2": 160.37396307836497,
    "Panel_Temperature_C": 35.64052207455395,
    "Ambient_Temperature_C": 32.45441069491491,
    "Cloud_Cover_%": 94.44485826943034,
    "Energy_Generated_kWh": 78.12727622521658,
    "CO2_Saved_kg": 42.853193230095684,
    "Money_Saved_INR": 468.76365735129946
  },
  {
    "Date": "2023-12-16 12:03:17.301846",
    "Solar_Irradiance_W/m2": 194.26317792665506,
    "Panel_Temperature_C": 31.594741712625595,
    "Ambient_Temperature_C": 33.424309911033646,
    "Cloud_Cover_%": 64.17343972985582,
    "Energy_Generated_kWh": 106.5159329508438,
    "CO2_Saved_kg": 55.212799050138145,
    "Money_Saved_INR": 639.0955977050628
  },
  {
    "Date": "2023-12-17 12:03:17.301846",
    "Solar_Irradiance_W/m2": 225.24936394902286,
    "Panel_Temperature_C": 39.20321774494362,
    "Ambient_Temperature_C": 34.44305027993239,
    "Cloud_Cover_%": 67.1479148667207,
    "Energy_Generated_kWh": 54.256728628315,
    "CO2_Saved_kg": 53.216785413765,
    "Money_Saved_INR": 325.54037176989004
  },
  {
    "Date": "2023-12-18 12:03:17.301846",
    "Solar_Irradiance_W/m2": 243.2877597085061,
    "Panel_Temperature_C": 31.736880103488044,
    "Ambient_Temperature_C": 37.76789889369356,
    "Cloud_Cover_%": 63.22821536376399,
    "Energy_Generated_kWh": 52.057636297740174,
    "CO2_Saved_kg": 51.6805980596682,
    "Money_Saved_INR": 312.34581778644105
  },
  {
    "Date": "2023-12-19 12:03:17.301846",
    "Solar_Irradiance_W/m2": 139.9851796472112,
    "Panel_Temperature_C": 32.7690828339261,
    "Ambient_Temperature_C": 32.86873059849959,
    "Cloud_Cover_%": 19.899213895943678,
    "Energy_Generated_kWh": 68.3280134730799,
    "CO2_Saved_kg": 40.04851518146621,
    "Money_Saved_INR": 409.9680808384794
  },
  {
    "Date": "2023-12-20 12:03:17.301846",
    "Solar_Irradiance_W/m2": 183.27493820795257,
    "Panel_Temperature_C": 25.552296345272346,
    "Ambient_Temperature_C": 28.311196417670203,
    "Cloud_Cover_%": 41.833386410228016,
    "Energy_Generated_kWh": 100.76757702038634,
    "CO2_Saved_kg": 48.184968378643326,
    "Money_Saved_INR": 604.605462122318
  },
  {
    "Date": "2023-12-21 12:03:17.301846",
    "Solar_Irradiance_W/m2": 176.25273444195219,
    "Panel_Temperature_C": 32.73846840375462,
    "Ambient_Temperature_C": 34.70801590841912,
    "Cloud_Cover_%": 75.09397983633183,
    "Energy_Generated_kWh": 49.61307849046315,
    "CO2_Saved_kg": 28.22934953557145,
    "Money_Saved_INR": 297.6784709427789
  },
  {
    "Date": "2023-12-22 12:03:17.301846",
    "Solar_Irradiance_W/m2": 167.3335383713144,
    "Panel_Temperature_C": 22.88060336685522,
    "Ambient_Temperature_C": 43.29917354426651,
    "Cloud_Cover_%": 10.137289755315916,
    "Energy_Generated_kWh": 23.35688803778862,
    "CO2_Saved_kg": 51.784766638853895,
    "Money_Saved_INR": 140.14132822673173
  },
  {
    "Date": "2023-12-23 12:03:17.301846",
    "Solar_Irradiance_W/m2": 288.27271201405483,
    "Panel_Temperature_C": 27.080485882571384,
    "Ambient_Temperature_C": 29.071563775321984,
    "Cloud_Cover_%": 27.785277608971228,
    "Energy_Generated_kWh": 70.97682283182003,
    "CO2_Saved_kg": 64.28857707813567,
    "Money_Saved_INR": 425.8609369909202
  },
  {
    "Date": "2023-12-24 12:03:17.301846",
    "Solar_Irradiance_W/m2": 220.2490855480478,
    "Panel_Temperature_C": 38.80207328072149,
    "Ambient_Temperature_C": 23.17829486730551,
    "Cloud_Cover_%": 27.631910846585363,
    "Energy_Generated_kWh": 91.0348159982184,
    "CO2_Saved_kg": 35.25867867957894,
    "Money_Saved_INR": 546.2088959893105
  },
  {
    "Date": "2023-12-25 12:03:17.301846",
    "Solar_Irradiance_W/m2": 136.95580228324775,
    "Panel_Temperature_C": 38.92900079325416,
    "Ambient_Temperature_C": 37.74956468500881,
    "Cloud_Cover_%": 43.2018927594506,
    "Energy_Generated_kWh": 104.00523499477659,
    "CO2_Saved_kg": 44.14072326682245,
    "Money_Saved_INR": 624.0314099686595
  },
  {
    "Date": "2023-12-26 12:03:17.301846",
    "Solar_Irradiance_W/m2": 245.8930973527388,
    "Panel_Temperature_C": 37.12728780892483,
    "Ambient_Temperature_C": 29.157331852324813,
    "Cloud_Cover_%": 98.0368740942185,
    "Energy_Generated_kWh": 70.73677275829202,
    "CO2_Saved_kg": 53.2910677871013,
    "Money_Saved_INR": 424.4206365497521
  },
  {
    "Date": "2023-12-27 12:03:17.301846",
    "Solar_Irradiance_W/m2": 306.10780985063167,
    "Panel_Temperature_C": 30.165119284353935,
    "Ambient_Temperature_C": 14.791313177901747,
    "Cloud_Cover_%": 6.750254668382194,
    "Energy_Generated_kWh": 71.77146785767995,
    "CO2_Saved_kg": 62.528426344274834,
    "Money_Saved_INR": 430.6288071460797
  },
  {
    "Date": "2023-12-28 12:03:17.301846",
    "Solar_Irradiance_W/m2": 251.62326302755736,
    "Panel_Temperature_C": 34.7614432192901,
    "Ambient_Temperature_C": 35.93195174005295,
    "Cloud_Cover_%": 51.870099438059505,
    "Energy_Generated_kWh": 103.07801468511494,
    "CO2_Saved_kg": 45.51775383699851,
    "Money_Saved_INR": 618.4680881106897
  },
  {
    "Date": "2023-12-29 12:03:17.301846",
    "Solar_Irradiance_W/m2": 124.03150170229932,
    "Panel_Temperature_C": 34.98198730454716,
    "Ambient_Temperature_C": 26.25270269832254,
    "Cloud_Cover_%": 17.936468201221047,
    "Energy_Generated_kWh": 42.605166006091586,
    "CO2_Saved_kg": 43.077496707341034,
    "Money_Saved_INR": 255.6309960365495
  },
  {
    "Date": "2023-12-30 12:03:17.301846",
    "Solar_Irradiance_W/m2": 175.78829635668743,
    "Panel_Temperature_C": 29.208176554037287,
    "Ambient_Temperature_C": 29.366267023870876,
    "Cloud_Cover_%": 97.06765454097442,
    "Energy_Generated_kWh": 72.22958449633981,
    "CO2_Saved_kg": 30.31076857583917,
    "Money_Saved_INR": 433.37750697803887
  },
  {
    "Date": "2023-12-31 12:03:17.301846",
    "Solar_Irradiance_W/m2": 263.34555745933113,
    "Panel_Temperature_C": 42.51699150883575,
    "Ambient_Temperature_C": 32.3238623139831,
    "Cloud_Cover_%": 11.33035047274642,
    "Energy_Generated_kWh": 83.80847779850116,
    "CO2_Saved_kg": 51.03438129308106,
    "Money_Saved_INR": 502.850866791007
  },
  {
    "Date": "2024-01-01 12:03:17.301846",
    "Solar_Irradiance_W/m2": 164.61652671906097,
    "Panel_Temperature_C": 39.386811452878355,
    "Ambient_Temperature_C": 31.333497758453465,
    "Cloud_Cover_%": 40.36010023615913,
    "Energy_Generated_kWh": 88.98437442570068,
    "CO2_Saved_kg": 70.42076040143743,
    "Money_Saved_INR": 533.906246554204
  },
  {
    "Date": "2024-01-02 12:03:17.301846",
    "Solar_Irradiance_W/m2": 222.19097140731142,
    "Panel_Temperature_C": 33.89517913085168,
    "Ambient_Temperature_C": 34.966162719973276,
    "Cloud_Cover_%": 73.78849848346061,
    "Energy_Generated_kWh": 69.80386613618235,
    "CO2_Saved_kg": 52.77358461964676,
    "Money_Saved_INR": 418.8231968170941
  },
  {
    "Date": "2024-01-03 12:03:17.301846",
    "Solar_Irradiance_W/m2": 238.73170267146685,
    "Panel_Temperature_C": 35.134429194972654,
    "Ambient_Temperature_C": 26.951595406011098,
    "Cloud_Cover_%": 70.45544280274453,
    "Energy_Generated_kWh": 80.68882023411683,
    "CO2_Saved_kg": 49.77721020816287,
    "Money_Saved_INR": 484.132921404701
  },
  {
    "Date": "2024-01-04 12:03:17.301846",
    "Solar_Irradiance_W/m2": 153.65347642109586,
    "Panel_Temperature_C": 36.04191403973776,
    "Ambient_Temperature_C": 33.59174058723258,
    "Cloud_Cover_%": 42.272863689393226,
    "Energy_Generated_kWh": 30.23345293174021,
    "CO2_Saved_kg": 53.22082310766986,
    "Money_Saved_INR": 181.40071759044127
  },
  {
    "Date": "2024-01-05 12:03:17.301846",
    "Solar_Irradiance_W/m2": 197.02373219691,
    "Panel_Temperature_C": 24.791325657878545,
    "Ambient_Temperature_C": 28.18317325691258,
    "Cloud_Cover_%": 34.652416795271826,
    "Energy_Generated_kWh": 66.83503175332304,
    "CO2_Saved_kg": 49.88907996051398,
    "Money_Saved_INR": 401.0101905199382
  },
  {
    "Date": "2024-01-06 12:03:17.301846",
    "Solar_Irradiance_W/m2": 37.936632996546365,
    "Panel_Temperature_C": 33.764113087397014,
    "Ambient_Temperature_C": 35.171673366212524,
    "Cloud_Cover_%": 39.76123785528706,
    "Energy_Generated_kWh": 89.07017425108936,
    "CO2_Saved_kg": 41.8698562773987,
    "Money_Saved_INR": 534.4210455065361
  },
  {
    "Date": "2024-01-07 12:03:17.301846",
    "Solar_Irradiance_W/m2": 148.7806179332855,
    "Panel_Temperature_C": 31.590078760011007,
    "Ambient_Temperature_C": 34.30757238809137,
    "Cloud_Cover_%": 26.42762631586393,
    "Energy_Generated_kWh": 60.35411931490641,
    "CO2_Saved_kg": 58.232799156777055,
    "Money_Saved_INR": 362.12471588943845
  },
  {
    "Date": "2024-01-08 12:03:17.301846",
    "Solar_Irradiance_W/m2": 187.371592430342,
    "Panel_Temperature_C": 29.991899950525422,
    "Ambient_Temperature_C": 23.451929085687834,
    "Cloud_Cover_%": 20.53329387067998,
    "Energy_Generated_kWh": 81.17968443179194,
    "CO2_Saved_kg": 52.25761523111754,
    "Money_Saved_INR": 487.07810659075164
  },
  {
    "Date": "2024-01-09 12:03:17.301846",
    "Solar_Irradiance_W/m2": 137.6108409017575,
    "Panel_Temperature_C": 33.594498535570224,
    "Ambient_Temperature_C": 37.60187481322522,
    "Cloud_Cover_%": 48.303969755889,
    "Energy_Generated_kWh": 88.93745001605396,
    "CO2_Saved_kg": 50.176132519336576,
    "Money_Saved_INR": 533.6247000963237
  },
  {
    "Date": "2024-01-10 12:03:17.301846",
    "Solar_Irradiance_W/m2": 281.62056519658177,
    "Panel_Temperature_C": 43.988432634247616,
    "Ambient_Temperature_C": 26.248255884201665,
    "Cloud_Cover_%": 26.853375606760732,
    "Energy_Generated_kWh": 73.1490159828447,
    "CO2_Saved_kg": 40.2463397272175,
    "Money_Saved_INR": 438.8940958970682
  },
  {
    "Date": "2024-01-11 12:03:17.301846",
    "Solar_Irradiance_W/m2": 128.49293110196837,
    "Panel_Temperature_C": 38.20421430633505,
    "Ambient_Temperature_C": 35.65640458796801,
    "Cloud_Cover_%": 28.746166489725013,
    "Energy_Generated_kWh": 83.40927541993142,
    "CO2_Saved_kg": 63.03507931934759,
    "Money_Saved_INR": 500.4556525195885
  },
  {
    "Date": "2024-01-12 12:03:17.301846",
    "Solar_Irradiance_W/m2": 177.9977756651508,
    "Panel_Temperature_C": 32.144105051086015,
    "Ambient_Temperature_C": 32.57101119380938,
    "Cloud_Cover_%": 65.67560634745571,
    "Energy_Generated_kWh": 60.74534869430775,
    "CO2_Saved_kg": 56.6470274533311,
    "Money_Saved_INR": 364.4720921658465
  },
  {
    "Date": "2024-01-13 12:03:17.301846",
    "Solar_Irradiance_W/m2": 206.53702886430457,
    "Panel_Temperature_C": 37.86291390678079,
    "Ambient_Temperature_C": 42.86728573756586,
    "Cloud_Cover_%": 96.85373316998923,
    "Energy_Generated_kWh": 75.86777440607906,
    "CO2_Saved_kg": 44.47079162632698,
    "Money_Saved_INR": 455.2066464364744
  },
  {
    "Date": "2024-01-14 12:03:17.301846",
    "Solar_Irradiance_W/m2": 272.06366445330576,
    "Panel_Temperature_C": 41.99677718293001,
    "Ambient_Temperature_C": 28.435738123397034,
    "Cloud_Cover_%": 60.363720055937506,
    "Energy_Generated_kWh": 92.20432339178446,
    "CO2_Saved_kg": 60.01824853681937,
    "Money_Saved_INR": 553.2259403507068
  },
  {
    "Date": "2024-01-15 12:03:17.301846",
    "Solar_Irradiance_W/m2": 128.20689244102803,
    "Panel_Temperature_C": 39.62316841456384,
    "Ambient_Temperature_C": 27.55478242717262,
    "Cloud_Cover_%": 7.697946706496628,
    "Energy_Generated_kWh": 83.13945921936869,
    "CO2_Saved_kg": 45.02429161614793,
    "Money_Saved_INR": 498.83675531621213
  },
  {
    "Date": "2024-01-16 12:03:17.301846",
    "Solar_Irradiance_W/m2": 258.158187607748,
    "Panel_Temperature_C": 35.29815184960087,
    "Ambient_Temperature_C": 29.86406275878587,
    "Cloud_Cover_%": 7.558361385406698,
    "Energy_Generated_kWh": 68.2693746087213,
    "CO2_Saved_kg": 42.17996507488963,
    "Money_Saved_INR": 409.61624765232773
  },
  {
    "Date": "2024-01-17 12:03:17.301846",
    "Solar_Irradiance_W/m2": 200.51165305097936,
    "Panel_Temperature_C": 31.76531611147213,
    "Ambient_Temperature_C": 27.877741520160072,
    "Cloud_Cover_%": 95.1423220845566,
    "Energy_Generated_kWh": 84.48432808581586,
    "CO2_Saved_kg": 42.40296882519713,
    "Money_Saved_INR": 506.90596851489516
  },
  {
    "Date": "2024-01-18 12:03:17.301846",
    "Solar_Irradiance_W/m2": 150.92456744760244,
    "Panel_Temperature_C": 38.49111656806795,
    "Ambient_Temperature_C": 35.59959331359435,
    "Cloud_Cover_%": 29.729079030733363,
    "Energy_Generated_kWh": 94.29219581273236,
    "CO2_Saved_kg": 32.28931446911909,
    "Money_Saved_INR": 565.7531748763942
  },
  {
    "Date": "2024-01-19 12:03:17.301846",
    "Solar_Irradiance_W/m2": 223.10517371316354,
    "Panel_Temperature_C": 36.96742692710875,
    "Ambient_Temperature_C": 18.685825740943883,
    "Cloud_Cover_%": 9.206698608247542,
    "Energy_Generated_kWh": 39.00117442845044,
    "CO2_Saved_kg": 54.71542380418206,
    "Money_Saved_INR": 234.00704657070264
  },
  {
    "Date": "2024-01-20 12:03:17.301846",
    "Solar_Irradiance_W/m2": 209.9529847786735,
    "Panel_Temperature_C": 39.47596610013866,
    "Ambient_Temperature_C": 22.62422306597552,
    "Cloud_Cover_%": 59.90445871503815,
    "Energy_Generated_kWh": 103.18148129911796,
    "CO2_Saved_kg": 31.6885512166165,
    "Money_Saved_INR": 619.0888877947077
  },
  {
    "Date": "2024-01-21 12:03:17.301846",
    "Solar_Irradiance_W/m2": 169.98915614206027,
    "Panel_Temperature_C": 38.175859008409844,
    "Ambient_Temperature_C": 22.525379548945647,
    "Cloud_Cover_%": 62.36487782902661,
    "Energy_Generated_kWh": 73.27490522637856,
    "CO2_Saved_kg": 37.71556168734237,
    "Money_Saved_INR": 439.6494313582714
  },
  {
    "Date": "2024-01-22 12:03:17.301846",
    "Solar_Irradiance_W/m2": 203.49010424950094,
    "Panel_Temperature_C": 40.247763576596675,
    "Ambient_Temperature_C": 36.65215314381503,
    "Cloud_Cover_%": 64.85048201186882,
    "Energy_Generated_kWh": 88.5097986648046,
    "CO2_Saved_kg": 29.244119909214668,
    "Money_Saved_INR": 531.0587919888276
  },
  {
    "Date": "2024-01-23 12:03:17.301846",
    "Solar_Irradiance_W/m2": 180.734320156912,
    "Panel_Temperature_C": 32.32382394219716,
    "Ambient_Temperature_C": 41.97429360807348,
    "Cloud_Cover_%": 26.74020278575413,
    "Energy_Generated_kWh": 103.94493847290455,
    "CO2_Saved_kg": 49.13930307209107,
    "Money_Saved_INR": 623.6696308374273
  },
  {
    "Date": "2024-01-24 12:03:17.301846",
    "Solar_Irradiance_W/m2": 205.6758672625624,
    "Panel_Temperature_C": 41.58697032817163,
    "Ambient_Temperature_C": 29.2688554702377,
    "Cloud_Cover_%": 1.5110684214475034,
    "Energy_Generated_kWh": 52.56652605539068,
    "CO2_Saved_kg": 48.49679539728128,
    "Money_Saved_INR": 315.3991563323441
  },
  {
    "Date": "2024-01-25 12:03:17.301846",
    "Solar_Irradiance_W/m2": 233.10653372605233,
    "Panel_Temperature_C": 35.987998023462,
    "Ambient_Temperature_C": 28.818247937669927,
    "Cloud_Cover_%": 96.50153694544719,
    "Energy_Generated_kWh": 65.81117995144906,
    "CO2_Saved_kg": 46.73303786813636,
    "Money_Saved_INR": 394.8670797086944
  },
  {
    "Date": "2024-01-26 12:03:17.301846",
    "Solar_Irradiance_W/m2": 279.3008408072676,
    "Panel_Temperature_C": 45.37630436312632,
    "Ambient_Temperature_C": 30.49036514179227,
    "Cloud_Cover_%": 25.089304569110247,
    "Energy_Generated_kWh": 74.2290260824859,
    "CO2_Saved_kg": 39.57422305329423,
    "Money_Saved_INR": 445.3741564949154
  },
  {
    "Date": "2024-01-27 12:03:17.301846",
    "Solar_Irradiance_W/m2": 138.10922505865756,
    "Panel_Temperature_C": 31.55406090955216,
    "Ambient_Temperature_C": 38.13314811825733,
    "Cloud_Cover_%": 67.60262880525475,
    "Energy_Generated_kWh": 64.32492957751143,
    "CO2_Saved_kg": 38.2776624656336,
    "Money_Saved_INR": 385.94957746506856
  },
  {
    "Date": "2024-01-28 12:03:17.301846",
    "Solar_Irradiance_W/m2": 306.65166873281333,
    "Panel_Temperature_C": 43.67981901582625,
    "Ambient_Temperature_C": 23.50852806066598,
    "Cloud_Cover_%": 70.66298698787095,
    "Energy_Generated_kWh": 114.69873151673616,
    "CO2_Saved_kg": 54.64369863546574,
    "Money_Saved_INR": 688.1923891004169
  },
  {
    "Date": "2024-01-29 12:03:17.301846",
    "Solar_Irradiance_W/m2": 102.39561002387491,
    "Panel_Temperature_C": 35.98955391731324,
    "Ambient_Temperature_C": 31.668582879143496,
    "Cloud_Cover_%": 61.00074170794857,
    "Energy_Generated_kWh": 62.86455812346415,
    "CO2_Saved_kg": 44.494480682915125,
    "Money_Saved_INR": 377.1873487407849
  },
  {
    "Date": "2024-01-30 12:03:17.301846",
    "Solar_Irradiance_W/m2": 192.41074524822082,
    "Panel_Temperature_C": 31.74290998192776,
    "Ambient_Temperature_C": 36.82638340847701,
    "Cloud_Cover_%": 31.290739421364822,
    "Energy_Generated_kWh": 68.88906441026266,
    "CO2_Saved_kg": 53.16358321536145,
    "Money_Saved_INR": 413.33438646157595
  },
  {
    "Date": "2024-01-31 12:03:17.301846",
    "Solar_Irradiance_W/m2": 229.41586032422882,
    "Panel_Temperature_C": 32.580570829728394,
    "Ambient_Temperature_C": 33.507659189578916,
    "Cloud_Cover_%": 27.109625376406576,
    "Energy_Generated_kWh": 84.08778063205953,
    "CO2_Saved_kg": 41.14751313875777,
    "Money_Saved_INR": 504.5266837923572
  },
  {
    "Date": "2024-02-01 12:03:17.301846",
    "Solar_Irradiance_W/m2": 214.04959338675164,
    "Panel_Temperature_C": 33.3982634590284,
    "Ambient_Temperature_C": 31.327071316191205,
    "Cloud_Cover_%": 59.76682827027031,
    "Energy_Generated_kWh": 55.95700947847823,
    "CO2_Saved_kg": 51.81062742771083,
    "Money_Saved_INR": 335.74205687086936
  },
  {
    "Date": "2024-02-02 12:03:17.301846",
    "Solar_Irradiance_W/m2": 168.8650240089703,
    "Panel_Temperature_C": 37.12082973200958,
    "Ambient_Temperature_C": 37.007322647969985,
    "Cloud_Cover_%": 86.60956336116915,
    "Energy_Generated_kWh": 72.08638576487472,
    "CO2_Saved_kg": 63.032780373160634,
    "Money_Saved_INR": 432.51831458924835
  },
  {
    "Date": "2024-02-03 12:03:17.301846",
    "Solar_Irradiance_W/m2": 189.59388748213624,
    "Panel_Temperature_C": 37.6141774401775,
    "Ambient_Temperature_C": 11.077373949005342,
    "Cloud_Cover_%": 94.67337289233956,
    "Energy_Generated_kWh": 86.3490652250035,
    "CO2_Saved_kg": 55.861658003927836,
    "Money_Saved_INR": 518.0943913500209
  },
  {
    "Date": "2024-02-04 12:03:17.301846",
    "Solar_Irradiance_W/m2": 175.34995326705837,
    "Panel_Temperature_C": 32.131499980307105,
    "Ambient_Temperature_C": 34.74512723671636,
    "Cloud_Cover_%": 10.590580440375764,
    "Energy_Generated_kWh": 73.34279191234978,
    "CO2_Saved_kg": 45.875861817835194,
    "Money_Saved_INR": 440.0567514740987
  },
  {
    "Date": "2024-02-05 12:03:17.301846",
    "Solar_Irradiance_W/m2": 170.5317621527894,
    "Panel_Temperature_C": 34.87822703869509,
    "Ambient_Temperature_C": 25.421470218108034,
    "Cloud_Cover_%": 15.482861259771985,
    "Energy_Generated_kWh": 78.13226282200104,
    "CO2_Saved_kg": 52.571989703559275,
    "Money_Saved_INR": 468.7935769320062
  },
  {
    "Date": "2024-02-06 12:03:17.301846",
    "Solar_Irradiance_W/m2": 242.48010485105124,
    "Panel_Temperature_C": 45.71135179305932,
    "Ambient_Temperature_C": 17.1855697220048,
    "Cloud_Cover_%": 94.47362587830797,
    "Energy_Generated_kWh": 69.41335775103258,
    "CO2_Saved_kg": 47.59334825469787,
    "Money_Saved_INR": 416.48014650619547
  },
  {
    "Date": "2024-02-07 12:03:17.301846",
    "Solar_Irradiance_W/m2": 217.85077429825236,
    "Panel_Temperature_C": 43.637715850503554,
    "Ambient_Temperature_C": 33.57841819667487,
    "Cloud_Cover_%": 73.65352283347926,
    "Energy_Generated_kWh": 49.71059381638466,
    "CO2_Saved_kg": 50.07880184694728,
    "Money_Saved_INR": 298.26356289830795
  },
  {
    "Date": "2024-02-08 12:03:17.301846",
    "Solar_Irradiance_W/m2": 165.3545202369673,
    "Panel_Temperature_C": 37.18161834837016,
    "Ambient_Temperature_C": 39.615609816140704,
    "Cloud_Cover_%": 88.29938248297731,
    "Energy_Generated_kWh": 86.43186422678477,
    "CO2_Saved_kg": 46.743889478514966,
    "Money_Saved_INR": 518.5911853607086
  },
  {
    "Date": "2024-02-09 12:03:17.301846",
    "Solar_Irradiance_W/m2": 244.97999377166252,
    "Panel_Temperature_C": 35.190017390841,
    "Ambient_Temperature_C": 29.037860397606156,
    "Cloud_Cover_%": 20.263263413534315,
    "Energy_Generated_kWh": 115.09866143294482,
    "CO2_Saved_kg": 48.356647941146086,
    "Money_Saved_INR": 690.5919685976689
  },
  {
    "Date": "2024-02-10 12:03:17.301846",
    "Solar_Irradiance_W/m2": 215.36497604383047,
    "Panel_Temperature_C": 35.600156633591304,
    "Ambient_Temperature_C": 36.67012183042057,
    "Cloud_Cover_%": 58.758587110940184,
    "Energy_Generated_kWh": 80.36803261566877,
    "CO2_Saved_kg": 52.12093353074175,
    "Money_Saved_INR": 482.2081956940126
  },
  {
    "Date": "2024-02-11 12:03:17.301846",
    "Solar_Irradiance_W/m2": 240.64310594194802,
    "Panel_Temperature_C": 38.06758986365208,
    "Ambient_Temperature_C": 41.285947805920514,
    "Cloud_Cover_%": 70.11395944174737,
    "Energy_Generated_kWh": 84.50528234495098,
    "CO2_Saved_kg": 40.06641300418049,
    "Money_Saved_INR": 507.0316940697059
  },
  {
    "Date": "2024-02-12 12:03:17.301846",
    "Solar_Irradiance_W/m2": 231.48144209618061,
    "Panel_Temperature_C": 29.886037174007974,
    "Ambient_Temperature_C": 39.204401175088336,
    "Cloud_Cover_%": 68.01118854469726,
    "Energy_Generated_kWh": 93.85445510233718,
    "CO2_Saved_kg": 39.84121173010021,
    "Money_Saved_INR": 563.1267306140231
  },
  {
    "Date": "2024-02-13 12:03:17.301846",
    "Solar_Irradiance_W/m2": 158.55024945389638,
    "Panel_Temperature_C": 33.71311731288328,
    "Ambient_Temperature_C": 41.47975170559975,
    "Cloud_Cover_%": 40.81516908666981,
    "Energy_Generated_kWh": 54.613390069066014,
    "CO2_Saved_kg": 36.11457446168789,
    "Money_Saved_INR": 327.6803404143961
  },
  {
    "Date": "2024-02-14 12:03:17.301846",
    "Solar_Irradiance_W/m2": 171.9909479901515,
    "Panel_Temperature_C": 26.657079630612053,
    "Ambient_Temperature_C": 35.19489243750324,
    "Cloud_Cover_%": 1.5394891691308477,
    "Energy_Generated_kWh": 114.05029316259211,
    "CO2_Saved_kg": 33.9972889549629,
    "Money_Saved_INR": 684.3017589755527
  },
  {
    "Date": "2024-02-15 12:03:17.301846",
    "Solar_Irradiance_W/m2": 237.3646802561631,
    "Panel_Temperature_C": 36.9961156130264,
    "Ambient_Temperature_C": 30.52803547231115,
    "Cloud_Cover_%": 58.29260568042631,
    "Energy_Generated_kWh": 84.04657592845604,
    "CO2_Saved_kg": 37.82717307779521,
    "Money_Saved_INR": 504.2794555707362
  },
  {
    "Date": "2024-02-16 12:03:17.301846",
    "Solar_Irradiance_W/m2": 230.51851327167324,
    "Panel_Temperature_C": 38.2359796985137,
    "Ambient_Temperature_C": 18.786239316719822,
    "Cloud_Cover_%": 25.310153917960875,
    "Energy_Generated_kWh": 112.63713798178217,
    "CO2_Saved_kg": 51.59462506804129,
    "Money_Saved_INR": 675.822827890693
  },
  {
    "Date": "2024-02-17 12:03:17.301846",
    "Solar_Irradiance_W/m2": 198.95492030179258,
    "Panel_Temperature_C": 32.58406768850313,
    "Ambient_Temperature_C": 28.27756258309036,
    "Cloud_Cover_%": 45.02542461428904,
    "Energy_Generated_kWh": 65.33934008952022,
    "CO2_Saved_kg": 41.07212484508116,
    "Money_Saved_INR": 392.0360405371213
  },
  {
    "Date": "2024-02-18 12:03:17.301846",
    "Solar_Irradiance_W/m2": 205.8663691654391,
    "Panel_Temperature_C": 42.869933816450164,
    "Ambient_Temperature_C": 24.09727383278666,
    "Cloud_Cover_%": 95.75810150838173,
    "Energy_Generated_kWh": 116.3612384511565,
    "CO2_Saved_kg": 55.13614464231096,
    "Money_Saved_INR": 698.167430706939
  },
  {
    "Date": "2024-02-19 12:03:17.301846",
    "Solar_Irradiance_W/m2": 263.88324478942127,
    "Panel_Temperature_C": 28.871171684988294,
    "Ambient_Temperature_C": 45.1965990224847,
    "Cloud_Cover_%": 39.903531764243475,
    "Energy_Generated_kWh": 95.50310988069566,
    "CO2_Saved_kg": 50.34713748752562,
    "Money_Saved_INR": 573.018659284174
  },
  {
    "Date": "2024-02-20 12:03:17.301846",
    "Solar_Irradiance_W/m2": 170.4214305582085,
    "Panel_Temperature_C": 27.6781255989509,
    "Ambient_Temperature_C": 28.768799312973645,
    "Cloud_Cover_%": 83.98016066644267,
    "Energy_Generated_kWh": 91.06080171704717,
    "CO2_Saved_kg": 30.314957865619462,
    "Money_Saved_INR": 546.364810302283
  },
  {
    "Date": "2024-02-21 12:03:17.301846",
    "Solar_Irradiance_W/m2": 227.3548690585019,
    "Panel_Temperature_C": 36.12225909279986,
    "Ambient_Temperature_C": 30.8624336474914,
    "Cloud_Cover_%": 18.854060574925114,
    "Energy_Generated_kWh": 84.68048908706297,
    "CO2_Saved_kg": 56.549755842216896,
    "Money_Saved_INR": 508.0829345223778
  },
  {
    "Date": "2024-02-22 12:03:17.301846",
    "Solar_Irradiance_W/m2": 189.89036737830529,
    "Panel_Temperature_C": 40.23549151306077,
    "Ambient_Temperature_C": 33.860397632283274,
    "Cloud_Cover_%": 67.24604980250288,
    "Energy_Generated_kWh": 75.02942763851101,
    "CO2_Saved_kg": 58.1079864559171,
    "Money_Saved_INR": 450.17656583106606
  },
  {
    "Date": "2024-02-23 12:03:17.301846",
    "Solar_Irradiance_W/m2": 189.11593983863898,
    "Panel_Temperature_C": 43.419638457289345,
    "Ambient_Temperature_C": 30.305217124607175,
    "Cloud_Cover_%": 97.70069544389435,
    "Energy_Generated_kWh": 104.01063316947744,
    "CO2_Saved_kg": 40.06137325165147,
    "Money_Saved_INR": 624.0637990168647
  },
  {
    "Date": "2024-02-24 12:03:17.301846",
    "Solar_Irradiance_W/m2": 254.9388425993595,
    "Panel_Temperature_C": 32.7055786856553,
    "Ambient_Temperature_C": 41.86535728301527,
    "Cloud_Cover_%": 10.189310087293679,
    "Energy_Generated_kWh": 82.80719739696094,
    "CO2_Saved_kg": 54.20191542894992,
    "Money_Saved_INR": 496.8431843817657
  },
  {
    "Date": "2024-02-25 12:03:17.301846",
    "Solar_Irradiance_W/m2": 241.27081744940148,
    "Panel_Temperature_C": 40.393404167156476,
    "Ambient_Temperature_C": 25.641454467858836,
    "Cloud_Cover_%": 0.8319942227192012,
    "Energy_Generated_kWh": 40.658605928256954,
    "CO2_Saved_kg": 41.43501762590801,
    "Money_Saved_INR": 243.95163556954174
  },
  {
    "Date": "2024-02-26 12:03:17.301846",
    "Solar_Irradiance_W/m2": 240.67548180003192,
    "Panel_Temperature_C": 34.80745765249647,
    "Ambient_Temperature_C": 31.362252186660697,
    "Cloud_Cover_%": 43.35827926326144,
    "Energy_Generated_kWh": 57.65627076585995,
    "CO2_Saved_kg": 50.97670376748336,
    "Money_Saved_INR": 345.9376245951597
  },
  {
    "Date": "2024-02-27 12:03:17.301846",
    "Solar_Irradiance_W/m2": 265.27394035771647,
    "Panel_Temperature_C": 34.1368635002959,
    "Ambient_Temperature_C": 24.80270590011366,
    "Cloud_Cover_%": 9.26254830513672,
    "Energy_Generated_kWh": 76.28308495614506,
    "CO2_Saved_kg": 37.35501593045034,
    "Money_Saved_INR": 457.6985097368704
  },
  {
    "Date": "2024-02-28 12:03:17.301846",
    "Solar_Irradiance_W/m2": 201.05019208163796,
    "Panel_Temperature_C": 39.41829968743336,
    "Ambient_Temperature_C": 20.759842421455062,
    "Cloud_Cover_%": 74.83843496762313,
    "Energy_Generated_kWh": 86.1999796633111,
    "CO2_Saved_kg": 32.06893547465423,
    "Money_Saved_INR": 517.1998779798666
  },
  {
    "Date": "2024-02-29 12:03:17.301846",
    "Solar_Irradiance_W/m2": 234.0976485647482,
    "Panel_Temperature_C": 38.261614392067095,
    "Ambient_Temperature_C": 25.717616363663,
    "Cloud_Cover_%": 91.45486638485589,
    "Energy_Generated_kWh": 78.86823022200208,
    "CO2_Saved_kg": 46.17182810387031,
    "Money_Saved_INR": 473.2093813320125
  },
  {
    "Date": "2024-03-01 12:03:17.301846",
    "Solar_Irradiance_W/m2": 184.4866621703272,
    "Panel_Temperature_C": 27.118039215078753,
    "Ambient_Temperature_C": 29.740742420661118,
    "Cloud_Cover_%": 43.402097270875885,
    "Energy_Generated_kWh": 104.37941579587326,
    "CO2_Saved_kg": 48.762710537251635,
    "Money_Saved_INR": 626.2764947752396
  },
  {
    "Date": "2024-03-02 12:03:17.301846",
    "Solar_Irradiance_W/m2": 216.2083176244221,
    "Panel_Temperature_C": 42.38270174862948,
    "Ambient_Temperature_C": 26.99488442837918,
    "Cloud_Cover_%": 25.871164215544095,
    "Energy_Generated_kWh": 40.977962719227506,
    "CO2_Saved_kg": 46.02320306385396,
    "Money_Saved_INR": 245.86777631536503
  },
  {
    "Date": "2024-03-03 12:03:17.301846",
    "Solar_Irradiance_W/m2": 193.49284728161578,
    "Panel_Temperature_C": 41.90045677073726,
    "Ambient_Temperature_C": 25.15305314088301,
    "Cloud_Cover_%": 43.44033190066098,
    "Energy_Generated_kWh": 82.87175873010321,
    "CO2_Saved_kg": 38.1596944177744,
    "Money_Saved_INR": 497.23055238061926
  },
  {
    "Date": "2024-03-04 12:03:17.301846",
    "Solar_Irradiance_W/m2": 204.8497982496359,
    "Panel_Temperature_C": 31.872186492452354,
    "Ambient_Temperature_C": 20.155777754297162,
    "Cloud_Cover_%": 72.3447817850001,
    "Energy_Generated_kWh": 43.640415492256906,
    "CO2_Saved_kg": 46.00100937868863,
    "Money_Saved_INR": 261.8424929535414
  },
  {
    "Date": "2024-03-05 12:03:17.301846",
    "Solar_Irradiance_W/m2": 229.75785127184568,
    "Panel_Temperature_C": 36.979017667187044,
    "Ambient_Temperature_C": 29.418260991599137,
    "Cloud_Cover_%": 0.9054161580370979,
    "Energy_Generated_kWh": 95.19424590968336,
    "CO2_Saved_kg": 52.69294752580734,
    "Money_Saved_INR": 571.1654754581002
  },
  {
    "Date": "2024-03-06 12:03:17.301846",
    "Solar_Irradiance_W/m2": 159.08896583832637,
    "Panel_Temperature_C": 37.47015093141369,
    "Ambient_Temperature_C": 19.466957381782983,
    "Cloud_Cover_%": 58.945398948469716,
    "Energy_Generated_kWh": 78.11082571115995,
    "CO2_Saved_kg": 49.55106969877463,
    "Money_Saved_INR": 468.6649542669597
  },
  {
    "Date": "2024-03-07 12:03:17.301846",
    "Solar_Irradiance_W/m2": 304.619363784273,
    "Panel_Temperature_C": 36.303368829119535,
    "Ambient_Temperature_C": 35.320391745827216,
    "Cloud_Cover_%": 61.329168488737906,
    "Energy_Generated_kWh": 88.39219944048236,
    "CO2_Saved_kg": 51.82501030599214,
    "Money_Saved_INR": 530.3531966428941
  },
  {
    "Date": "2024-03-08 12:03:17.301846",
    "Solar_Irradiance_W/m2": 149.6991309250149,
    "Panel_Temperature_C": 32.2484742307729,
    "Ambient_Temperature_C": 30.577078270541524,
    "Cloud_Cover_%": 63.76882468959355,
    "Energy_Generated_kWh": 62.722340788204676,
    "CO2_Saved_kg": 43.29884799545767,
    "Money_Saved_INR": 376.334044729228
  },
  {
    "Date": "2024-03-09 12:03:17.301846",
    "Solar_Irradiance_W/m2": 139.2905693606134,
    "Panel_Temperature_C": 31.641883160309742,
    "Ambient_Temperature_C": 19.797139503745484,
    "Cloud_Cover_%": 24.202207998087722,
    "Energy_Generated_kWh": 105.58929863315502,
    "CO2_Saved_kg": 61.717179147161595,
    "Money_Saved_INR": 633.5357917989302
  },
  {
    "Date": "2024-03-10 12:03:17.301846",
    "Solar_Irradiance_W/m2": 257.9055436750034,
    "Panel_Temperature_C": 34.87222964504277,
    "Ambient_Temperature_C": 27.835536460650957,
    "Cloud_Cover_%": 71.40527233781268,
    "Energy_Generated_kWh": 100.83449328117703,
    "CO2_Saved_kg": 38.238266634452195,
    "Money_Saved_INR": 605.0069596870621
  },
  {
    "Date": "2024-03-11 12:03:17.301846",
    "Solar_Irradiance_W/m2": 239.5831346981468,
    "Panel_Temperature_C": 40.86364509629682,
    "Ambient_Temperature_C": 24.734905160865917,
    "Cloud_Cover_%": 9.13914863317764,
    "Energy_Generated_kWh": 91.67088606023775,
    "CO2_Saved_kg": 54.875602970867185,
    "Money_Saved_INR": 550.0253163614265
  },
  {
    "Date": "2024-03-12 12:03:17.301846",
    "Solar_Irradiance_W/m2": 231.20599085260775,
    "Panel_Temperature_C": 37.71800077297216,
    "Ambient_Temperature_C": 32.23422157293426,
    "Cloud_Cover_%": 19.92703364668008,
    "Energy_Generated_kWh": 77.40965506273119,
    "CO2_Saved_kg": 61.81891092959962,
    "Money_Saved_INR": 464.45793037638714
  },
  {
    "Date": "2024-03-13 12:03:17.301846",
    "Solar_Irradiance_W/m2": 231.417275463214,
    "Panel_Temperature_C": 33.14692833956947,
    "Ambient_Temperature_C": 39.383153122162014,
    "Cloud_Cover_%": 87.74700466544819,
    "Energy_Generated_kWh": 91.59714570590265,
    "CO2_Saved_kg": 54.80908092748896,
    "Money_Saved_INR": 549.5828742354158
  },
  {
    "Date": "2024-03-14 12:03:17.301846",
    "Solar_Irradiance_W/m2": 199.38766135765428,
    "Panel_Temperature_C": 38.85849355324172,
    "Ambient_Temperature_C": 16.873792712479787,
    "Cloud_Cover_%": 73.87231507265663,
    "Energy_Generated_kWh": 65.86214864025303,
    "CO2_Saved_kg": 47.9747577293517,
    "Money_Saved_INR": 395.17289184151815
  },
  {
    "Date": "2024-03-15 12:03:17.301846",
    "Solar_Irradiance_W/m2": 155.1372814257084,
    "Panel_Temperature_C": 20.75728689684962,
    "Ambient_Temperature_C": 30.80518255403192,
    "Cloud_Cover_%": 1.3745554011345251,
    "Energy_Generated_kWh": 97.11111318041424,
    "CO2_Saved_kg": 44.71702953337021,
    "Money_Saved_INR": 582.6666790824854
  },
  {
    "Date": "2024-03-16 12:03:17.301846",
    "Solar_Irradiance_W/m2": 203.7902279096863,
    "Panel_Temperature_C": 40.74382850186052,
    "Ambient_Temperature_C": 28.87907043103352,
    "Cloud_Cover_%": 24.83762603698002,
    "Energy_Generated_kWh": 112.98961788647841,
    "CO2_Saved_kg": 60.36087651046256,
    "Money_Saved_INR": 677.9377073188705
  },
  {
    "Date": "2024-03-17 12:03:17.301846",
    "Solar_Irradiance_W/m2": 166.14191442439443,
    "Panel_Temperature_C": 26.301431106109504,
    "Ambient_Temperature_C": 34.69938053515326,
    "Cloud_Cover_%": 21.440648299316457,
    "Energy_Generated_kWh": 101.41221119958372,
    "CO2_Saved_kg": 35.77025074738327,
    "Money_Saved_INR": 608.4732671975023
  },
  {
    "Date": "2024-03-18 12:03:17.301846",
    "Solar_Irradiance_W/m2": 248.75598667088755,
    "Panel_Temperature_C": 33.18779529298434,
    "Ambient_Temperature_C": 31.492376397663826,
    "Cloud_Cover_%": 27.080632803697256,
    "Energy_Generated_kWh": 65.40795060385182,
    "CO2_Saved_kg": 40.29875739620356,
    "Money_Saved_INR": 392.4477036231109
  },
  {
    "Date": "2024-03-19 12:03:17.301846",
    "Solar_Irradiance_W/m2": 192.64713092489308,
    "Panel_Temperature_C": 29.401650526869282,
    "Ambient_Temperature_C": 24.736214677828265,
    "Cloud_Cover_%": 24.755977027988642,
    "Energy_Generated_kWh": 87.22834634546206,
    "CO2_Saved_kg": 46.02442234508278,
    "Money_Saved_INR": 523.3700780727723
  },
  {
    "Date": "2024-03-20 12:03:17.301846",
    "Solar_Irradiance_W/m2": 158.72514016037442,
    "Panel_Temperature_C": 28.526592621395473,
    "Ambient_Temperature_C": 27.766622450333674,
    "Cloud_Cover_%": 6.252629574284574,
    "Energy_Generated_kWh": 54.13716912482705,
    "CO2_Saved_kg": 62.37653757511998,
    "Money_Saved_INR": 324.8230147489623
  },
  {
    "Date": "2024-03-21 12:03:17.301846",
    "Solar_Irradiance_W/m2": 183.93070791735033,
    "Panel_Temperature_C": 40.8041339368926,
    "Ambient_Temperature_C": 24.42781900237558,
    "Cloud_Cover_%": 45.894051659682034,
    "Energy_Generated_kWh": 91.44780622351351,
    "CO2_Saved_kg": 53.79767636040896,
    "Money_Saved_INR": 548.6868373410811
  },
  {
    "Date": "2024-03-22 12:03:17.301846",
    "Solar_Irradiance_W/m2": 220.6465727137812,
    "Panel_Temperature_C": 32.661493993440544,
    "Ambient_Temperature_C": 37.53204997019019,
    "Cloud_Cover_%": 73.27334747861651,
    "Energy_Generated_kWh": 89.01206825725077,
    "CO2_Saved_kg": 40.31954241489755,
    "Money_Saved_INR": 534.0724095435046
  },
  {
    "Date": "2024-03-23 12:03:17.301846",
    "Solar_Irradiance_W/m2": 171.81377235980125,
    "Panel_Temperature_C": 36.73251940865358,
    "Ambient_Temperature_C": 30.149181540703594,
    "Cloud_Cover_%": 60.67317247174364,
    "Energy_Generated_kWh": 42.60367320935672,
    "CO2_Saved_kg": 46.896922946150966,
    "Money_Saved_INR": 255.62203925614034
  },
  {
    "Date": "2024-03-24 12:03:17.301846",
    "Solar_Irradiance_W/m2": 158.88898022167842,
    "Panel_Temperature_C": 34.76539710560408,
    "Ambient_Temperature_C": 43.308334800271055,
    "Cloud_Cover_%": 67.28716685980798,
    "Energy_Generated_kWh": 56.764323121752724,
    "CO2_Saved_kg": 43.85676855903706,
    "Money_Saved_INR": 340.5859387305163
  },
  {
    "Date": "2024-03-25 12:03:17.301846",
    "Solar_Irradiance_W/m2": 212.18436057459562,
    "Panel_Temperature_C": 37.385204136115604,
    "Ambient_Temperature_C": 29.575374303297654,
    "Cloud_Cover_%": 8.114917853623915,
    "Energy_Generated_kWh": 74.33722206512466,
    "CO2_Saved_kg": 42.90211007766465,
    "Money_Saved_INR": 446.023332390748
  },
  {
    "Date": "2024-03-26 12:03:17.301846",
    "Solar_Irradiance_W/m2": 212.24832855543613,
    "Panel_Temperature_C": 35.38410945530128,
    "Ambient_Temperature_C": 25.04115263162676,
    "Cloud_Cover_%": 95.14907101767872,
    "Energy_Generated_kWh": 73.98280505718347,
    "CO2_Saved_kg": 59.78889558556779,
    "Money_Saved_INR": 443.8968303431008
  },
  {
    "Date": "2024-03-27 12:03:17.301846",
    "Solar_Irradiance_W/m2": 174.65284123144352,
    "Panel_Temperature_C": 28.58503887905715,
    "Ambient_Temperature_C": 19.40399925171021,
    "Cloud_Cover_%": 83.84918338430248,
    "Energy_Generated_kWh": 55.810461291623895,
    "CO2_Saved_kg": 36.282568707364945,
    "Money_Saved_INR": 334.8627677497434
  },
  {
    "Date": "2024-03-28 12:03:17.301846",
    "Solar_Irradiance_W/m2": 176.44808471908385,
    "Panel_Temperature_C": 39.9813340972357,
    "Ambient_Temperature_C": 17.378022266208383,
    "Cloud_Cover_%": 80.50903184956627,
    "Energy_Generated_kWh": 87.77957458704367,
    "CO2_Saved_kg": 66.08780855734373,
    "Money_Saved_INR": 526.677447522262
  },
  {
    "Date": "2024-03-29 12:03:17.301846",
    "Solar_Irradiance_W/m2": 211.60249686788183,
    "Panel_Temperature_C": 32.531217084193436,
    "Ambient_Temperature_C": 18.911048398961572,
    "Cloud_Cover_%": 82.29838050417675,
    "Energy_Generated_kWh": 85.02947217881024,
    "CO2_Saved_kg": 58.28229690184623,
    "Money_Saved_INR": 510.1768330728614
  },
  {
    "Date": "2024-03-30 12:03:17.301846",
    "Solar_Irradiance_W/m2": 127.59578292513379,
    "Panel_Temperature_C": 27.217090506701247,
    "Ambient_Temperature_C": 31.869886557080385,
    "Cloud_Cover_%": 93.27105081327613,
    "Energy_Generated_kWh": 76.11461736042962,
    "CO2_Saved_kg": 60.90861670603698,
    "Money_Saved_INR": 456.6877041625777
  },
  {
    "Date": "2024-03-31 12:03:17.301846",
    "Solar_Irradiance_W/m2": 129.62681128117225,
    "Panel_Temperature_C": 32.85942419517044,
    "Ambient_Temperature_C": 33.56107516260954,
    "Cloud_Cover_%": 54.42539661136977,
    "Energy_Generated_kWh": 64.88416999683274,
    "CO2_Saved_kg": 45.37060487974742,
    "Money_Saved_INR": 389.30501998099646
  },
  {
    "Date": "2024-04-01 12:03:17.301846",
    "Solar_Irradiance_W/m2": 164.07778893737822,
    "Panel_Temperature_C": 42.503798953171554,
    "Ambient_Temperature_C": 18.931665085775066,
    "Cloud_Cover_%": 20.02820178676259,
    "Energy_Generated_kWh": 100.97414252833127,
    "CO2_Saved_kg": 48.500592809208904,
    "Money_Saved_INR": 605.8448551699876
  },
  {
    "Date": "2024-04-02 12:03:17.301846",
    "Solar_Irradiance_W/m2": 189.32764241440765,
    "Panel_Temperature_C": 39.251108710567465,
    "Ambient_Temperature_C": 36.26526819853281,
    "Cloud_Cover_%": 61.678360785254114,
    "Energy_Generated_kWh": 113.1081422617659,
    "CO2_Saved_kg": 35.66848185475288,
    "Money_Saved_INR": 678.6488535705954
  },
  {
    "Date": "2024-04-03 12:03:17.301846",
    "Solar_Irradiance_W/m2": 215.54537827990023,
    "Panel_Temperature_C": 33.2567393279607,
    "Ambient_Temperature_C": 26.618572638215923,
    "Cloud_Cover_%": 74.2881493667939,
    "Energy_Generated_kWh": 70.32877032306926,
    "CO2_Saved_kg": 44.753375929331966,
    "Money_Saved_INR": 421.9726219384156
  },
  {
    "Date": "2024-04-04 12:03:17.301846",
    "Solar_Irradiance_W/m2": 273.7678108474776,
    "Panel_Temperature_C": 33.25371147840786,
    "Ambient_Temperature_C": 31.027551083898846,
    "Cloud_Cover_%": 73.79173933540254,
    "Energy_Generated_kWh": 67.75666165690359,
    "CO2_Saved_kg": 54.93654847643151,
    "Money_Saved_INR": 406.53996994142153
  },
  {
    "Date": "2024-04-05 12:03:17.301846",
    "Solar_Irradiance_W/m2": 242.88298116010097,
    "Panel_Temperature_C": 33.391824743913084,
    "Ambient_Temperature_C": 41.28554439778797,
    "Cloud_Cover_%": 52.14490241668801,
    "Energy_Generated_kWh": 89.82415330823993,
    "CO2_Saved_kg": 62.96063061781396,
    "Money_Saved_INR": 538.9449198494395
  },
  {
    "Date": "2024-04-06 12:03:17.301846",
    "Solar_Irradiance_W/m2": 192.00307350182865,
    "Panel_Temperature_C": 45.383739917804206,
    "Ambient_Temperature_C": 36.27787521105872,
    "Cloud_Cover_%": 6.845871933357806,
    "Energy_Generated_kWh": 72.83941240506027,
    "CO2_Saved_kg": 38.92843183197549,
    "Money_Saved_INR": 437.03647443036164
  },
  {
    "Date": "2024-04-07 12:03:17.301846",
    "Solar_Irradiance_W/m2": 199.04918960486555,
    "Panel_Temperature_C": 36.90967726115777,
    "Ambient_Temperature_C": 28.120285464659172,
    "Cloud_Cover_%": 37.11129384301278,
    "Energy_Generated_kWh": 77.21205598673532,
    "CO2_Saved_kg": 46.34494063014734,
    "Money_Saved_INR": 463.27233592041193
  },
  {
    "Date": "2024-04-08 12:03:17.301846",
    "Solar_Irradiance_W/m2": 149.87353176810956,
    "Panel_Temperature_C": 37.15020823595535,
    "Ambient_Temperature_C": 23.761654422092988,
    "Cloud_Cover_%": 92.07666084633573,
    "Energy_Generated_kWh": 94.79306303449343,
    "CO2_Saved_kg": 48.48700779767478,
    "Money_Saved_INR": 568.7583782069605
  },
  {
    "Date": "2024-04-09 12:03:17.301846",
    "Solar_Irradiance_W/m2": 199.0743432003805,
    "Panel_Temperature_C": 40.151417270159214,
    "Ambient_Temperature_C": 14.937292190694865,
    "Cloud_Cover_%": 58.4448909757426,
    "Energy_Generated_kWh": 41.812878249854144,
    "CO2_Saved_kg": 36.04210797807515,
    "Money_Saved_INR": 250.87726949912485
  },
  {
    "Date": "2024-04-10 12:03:17.301846",
    "Solar_Irradiance_W/m2": 185.5670680539931,
    "Panel_Temperature_C": 36.19394579513257,
    "Ambient_Temperature_C": 24.96592676530306,
    "Cloud_Cover_%": 53.83319432557134,
    "Energy_Generated_kWh": 106.36604649705339,
    "CO2_Saved_kg": 55.913492417584,
    "Money_Saved_INR": 638.1962789823203
  },
  {
    "Date": "2024-04-11 12:03:17.301846",
    "Solar_Irradiance_W/m2": 216.13592801690447,
    "Panel_Temperature_C": 33.704789270896484,
    "Ambient_Temperature_C": 28.522088328206138,
    "Cloud_Cover_%": 26.885351438219352,
    "Energy_Generated_kWh": 81.45361048658683,
    "CO2_Saved_kg": 42.76009668257391,
    "Money_Saved_INR": 488.72166291952095
  },
  {
    "Date": "2024-04-12 12:03:17.301846",
    "Solar_Irradiance_W/m2": 158.63845282238384,
    "Panel_Temperature_C": 34.01825075457511,
    "Ambient_Temperature_C": 23.089743309941714,
    "Cloud_Cover_%": 36.84489199165789,
    "Energy_Generated_kWh": 71.7701371087564,
    "CO2_Saved_kg": 48.04609648822976,
    "Money_Saved_INR": 430.62082265253844
  },
  {
    "Date": "2024-04-13 12:03:17.301846",
    "Solar_Irradiance_W/m2": 225.96732571205862,
    "Panel_Temperature_C": 34.64199370292968,
    "Ambient_Temperature_C": 29.081201230353866,
    "Cloud_Cover_%": 89.53460891531692,
    "Energy_Generated_kWh": 78.21531691557102,
    "CO2_Saved_kg": 45.48050628088122,
    "Money_Saved_INR": 469.29190149342617
  },
  {
    "Date": "2024-04-14 12:03:17.301846",
    "Solar_Irradiance_W/m2": 276.6369456501289,
    "Panel_Temperature_C": 34.813888817450795,
    "Ambient_Temperature_C": 30.537963180711376,
    "Cloud_Cover_%": 66.64630475268358,
    "Energy_Generated_kWh": 79.24858710041038,
    "CO2_Saved_kg": 42.106614942803255,
    "Money_Saved_INR": 475.4915226024623
  },
  {
    "Date": "2024-04-15 12:03:17.301846",
    "Solar_Irradiance_W/m2": 194.56199257715713,
    "Panel_Temperature_C": 38.6381477181849,
    "Ambient_Temperature_C": 28.42600812734345,
    "Cloud_Cover_%": 78.73870267523328,
    "Energy_Generated_kWh": 45.37597393110149,
    "CO2_Saved_kg": 49.929550145194455,
    "Money_Saved_INR": 272.25584358660893
  },
  {
    "Date": "2024-04-16 12:03:17.301846",
    "Solar_Irradiance_W/m2": 220.08558610494708,
    "Panel_Temperature_C": 35.2597294290365,
    "Ambient_Temperature_C": 25.44998193423578,
    "Cloud_Cover_%": 45.434542306765515,
    "Energy_Generated_kWh": 109.89876454906472,
    "CO2_Saved_kg": 47.84390421431978,
    "Money_Saved_INR": 659.3925872943884
  },
  {
    "Date": "2024-04-17 12:03:17.301846",
    "Solar_Irradiance_W/m2": 234.5071995855556,
    "Panel_Temperature_C": 38.6632003860779,
    "Ambient_Temperature_C": 31.180582703767094,
    "Cloud_Cover_%": 63.024721945615795,
    "Energy_Generated_kWh": 80.82651264541236,
    "CO2_Saved_kg": 46.281421177213346,
    "Money_Saved_INR": 484.95907587247416
  },
  {
    "Date": "2024-04-18 12:03:17.301846",
    "Solar_Irradiance_W/m2": 179.9389764057082,
    "Panel_Temperature_C": 34.596417099457085,
    "Ambient_Temperature_C": 33.093584546985866,
    "Cloud_Cover_%": 24.838360874320752,
    "Energy_Generated_kWh": 88.86004260894751,
    "CO2_Saved_kg": 42.71538378319657,
    "Money_Saved_INR": 533.160255653685
  },
  {
    "Date": "2024-04-19 12:03:17.301846",
    "Solar_Irradiance_W/m2": 211.20462409052084,
    "Panel_Temperature_C": 35.39317595158045,
    "Ambient_Temperature_C": 22.367206457900078,
    "Cloud_Cover_%": 70.54608302834863,
    "Energy_Generated_kWh": 99.03099541148086,
    "CO2_Saved_kg": 53.195246707829554,
    "Money_Saved_INR": 594.1859724688852
  },
  {
    "Date": "2024-04-20 12:03:17.301846",
    "Solar_Irradiance_W/m2": 200.62962003908973,
    "Panel_Temperature_C": 25.00899657733946,
    "Ambient_Temperature_C": 39.87652665822389,
    "Cloud_Cover_%": 42.76013337033373,
    "Energy_Generated_kWh": 59.57675084879399,
    "CO2_Saved_kg": 66.53617268492285,
    "Money_Saved_INR": 357.4605050927639
  },
  {
    "Date": "2024-04-21 12:03:17.301846",
    "Solar_Irradiance_W/m2": 204.8838049274416,
    "Panel_Temperature_C": 39.581638373512405,
    "Ambient_Temperature_C": 29.309883074010166,
    "Cloud_Cover_%": 44.25455148147456,
    "Energy_Generated_kWh": 89.46943798070457,
    "CO2_Saved_kg": 51.39887232839127,
    "Money_Saved_INR": 536.8166278842274
  },
  {
    "Date": "2024-04-22 12:03:17.301846",
    "Solar_Irradiance_W/m2": 161.3495108072267,
    "Panel_Temperature_C": 36.73244237948996,
    "Ambient_Temperature_C": 30.131947360613935,
    "Cloud_Cover_%": 64.93223245768817,
    "Energy_Generated_kWh": 74.64717818202413,
    "CO2_Saved_kg": 59.96118214911129,
    "Money_Saved_INR": 447.8830690921448
  },
  {
    "Date": "2024-04-23 12:03:17.301846",
    "Solar_Irradiance_W/m2": 201.22550871294715,
    "Panel_Temperature_C": 39.99005054929826,
    "Ambient_Temperature_C": 34.9575009627959,
    "Cloud_Cover_%": 93.62806214689266,
    "Energy_Generated_kWh": 96.93541550432988,
    "CO2_Saved_kg": 36.097780748465375,
    "Money_Saved_INR": 581.6124930259793
  },
  {
    "Date": "2024-04-24 12:03:17.301846",
    "Solar_Irradiance_W/m2": 224.8999145622725,
    "Panel_Temperature_C": 20.518723109031555,
    "Ambient_Temperature_C": 31.63251291884451,
    "Cloud_Cover_%": 6.400634660862092,
    "Energy_Generated_kWh": 37.45545159297009,
    "CO2_Saved_kg": 51.5776143929377,
    "Money_Saved_INR": 224.73270955782056
  },
  {
    "Date": "2024-04-25 12:03:17.301846",
    "Solar_Irradiance_W/m2": 272.5571803897521,
    "Panel_Temperature_C": 45.44187352390364,
    "Ambient_Temperature_C": 36.671956437392716,
    "Cloud_Cover_%": 82.47432373470076,
    "Energy_Generated_kWh": 78.01811399517462,
    "CO2_Saved_kg": 39.02631681028933,
    "Money_Saved_INR": 468.1086839710477
  },
  {
    "Date": "2024-04-26 12:03:17.301846",
    "Solar_Irradiance_W/m2": 247.96354130426033,
    "Panel_Temperature_C": 34.30205185922413,
    "Ambient_Temperature_C": 32.00986915641277,
    "Cloud_Cover_%": 29.238311041219312,
    "Energy_Generated_kWh": 67.94358688432077,
    "CO2_Saved_kg": 35.23075072468099,
    "Money_Saved_INR": 407.66152130592457
  },
  {
    "Date": "2024-04-27 12:03:17.301846",
    "Solar_Irradiance_W/m2": 307.65912287557785,
    "Panel_Temperature_C": 40.54091408368758,
    "Ambient_Temperature_C": 25.712938377516934,
    "Cloud_Cover_%": 44.391945450637785,
    "Energy_Generated_kWh": 88.64525901268311,
    "CO2_Saved_kg": 42.60628592540964,
    "Money_Saved_INR": 531.8715540760986
  },
  {
    "Date": "2024-04-28 12:03:17.301846",
    "Solar_Irradiance_W/m2": 161.63262185559753,
    "Panel_Temperature_C": 29.800470364372345,
    "Ambient_Temperature_C": 32.53052467644271,
    "Cloud_Cover_%": 2.1913328775008956,
    "Energy_Generated_kWh": 89.40088374736405,
    "CO2_Saved_kg": 61.91899334413573,
    "Money_Saved_INR": 536.4053024841843
  },
  {
    "Date": "2024-04-29 12:03:17.301846",
    "Solar_Irradiance_W/m2": 243.61603183603393,
    "Panel_Temperature_C": 38.063869525312846,
    "Ambient_Temperature_C": 21.993916548755365,
    "Cloud_Cover_%": 30.1046077834313,
    "Energy_Generated_kWh": 65.84748210355949,
    "CO2_Saved_kg": 59.500158286696454,
    "Money_Saved_INR": 395.0848926213569
  },
  {
    "Date": "2024-04-30 12:03:17.301846",
    "Solar_Irradiance_W/m2": 209.1671002869176,
    "Panel_Temperature_C": 29.73292218413172,
    "Ambient_Temperature_C": 30.759917940435663,
    "Cloud_Cover_%": 50.26312426301305,
    "Energy_Generated_kWh": 65.75652271647913,
    "CO2_Saved_kg": 52.430047220544,
    "Money_Saved_INR": 394.5391362988747
  },
  {
    "Date": "2024-05-01 12:03:17.301846",
    "Solar_Irradiance_W/m2": 309.4901466608836,
    "Panel_Temperature_C": 31.881155196520975,
    "Ambient_Temperature_C": 29.767390065488776,
    "Cloud_Cover_%": 5.617607734743901,
    "Energy_Generated_kWh": 77.78669262885342,
    "CO2_Saved_kg": 34.672994401100695,
    "Money_Saved_INR": 466.7201557731205
  },
  {
    "Date": "2024-05-02 12:03:17.301846",
    "Solar_Irradiance_W/m2": 159.58508573224242,
    "Panel_Temperature_C": 44.570156769333934,
    "Ambient_Temperature_C": 28.543181999092223,
    "Cloud_Cover_%": 49.10957293831652,
    "Energy_Generated_kWh": 62.06715545369583,
    "CO2_Saved_kg": 48.03719348612063,
    "Money_Saved_INR": 372.402932722175
  },
  {
    "Date": "2024-05-03 12:03:17.301846",
    "Solar_Irradiance_W/m2": 158.0139078909612,
    "Panel_Temperature_C": 34.04658799618327,
    "Ambient_Temperature_C": 29.100237419927485,
    "Cloud_Cover_%": 92.71106288584274,
    "Energy_Generated_kWh": 96.83967390904255,
    "CO2_Saved_kg": 53.01700008901736,
    "Money_Saved_INR": 581.0380434542553
  },
  {
    "Date": "2024-05-04 12:03:17.301846",
    "Solar_Irradiance_W/m2": 170.0303677277989,
    "Panel_Temperature_C": 36.087164365898616,
    "Ambient_Temperature_C": 16.827056681516524,
    "Cloud_Cover_%": 10.539321810780521,
    "Energy_Generated_kWh": 72.61585599105108,
    "CO2_Saved_kg": 51.75536229578598,
    "Money_Saved_INR": 435.69513594630644
  },
  {
    "Date": "2024-05-05 12:03:17.301846",
    "Solar_Irradiance_W/m2": 93.80521378450966,
    "Panel_Temperature_C": 39.35033865344377,
    "Ambient_Temperature_C": 26.15892564581327,
    "Cloud_Cover_%": 76.44407280755044,
    "Energy_Generated_kWh": 21.86023561356717,
    "CO2_Saved_kg": 31.56206416519254,
    "Money_Saved_INR": 131.16141368140302
  },
  {
    "Date": "2024-05-06 12:03:17.301846",
    "Solar_Irradiance_W/m2": 173.71224891596194,
    "Panel_Temperature_C": 37.47840943986302,
    "Ambient_Temperature_C": 30.649914307987803,
    "Cloud_Cover_%": 40.967105337599264,
    "Energy_Generated_kWh": 72.50355886756388,
    "CO2_Saved_kg": 41.09682151980128,
    "Money_Saved_INR": 435.0213532053833
  },
  {
    "Date": "2024-05-07 12:03:17.301846",
    "Solar_Irradiance_W/m2": 162.0433669223151,
    "Panel_Temperature_C": 35.75209452571788,
    "Ambient_Temperature_C": 31.1189947439818,
    "Cloud_Cover_%": 65.5173714524338,
    "Energy_Generated_kWh": 59.229123583120554,
    "CO2_Saved_kg": 49.35922235851283,
    "Money_Saved_INR": 355.3747414987233
  },
  {
    "Date": "2024-05-08 12:03:17.301846",
    "Solar_Irradiance_W/m2": 207.51968932381038,
    "Panel_Temperature_C": 36.824805012331126,
    "Ambient_Temperature_C": 22.806274013518294,
    "Cloud_Cover_%": 26.023659798522935,
    "Energy_Generated_kWh": 47.37448369078109,
    "CO2_Saved_kg": 55.3629090951719,
    "Money_Saved_INR": 284.24690214468654
  },
  {
    "Date": "2024-05-09 12:03:17.301846",
    "Solar_Irradiance_W/m2": 217.08779878885798,
    "Panel_Temperature_C": 47.01707792619138,
    "Ambient_Temperature_C": 38.859954886052904,
    "Cloud_Cover_%": 15.949226254135828,
    "Energy_Generated_kWh": 55.251467235548546,
    "CO2_Saved_kg": 28.038721789000537,
    "Money_Saved_INR": 331.5088034132913
  },
  {
    "Date": "2024-05-10 12:03:17.301846",
    "Solar_Irradiance_W/m2": 293.8085419607943,
    "Panel_Temperature_C": 34.711906014832074,
    "Ambient_Temperature_C": 23.936776062498495,
    "Cloud_Cover_%": 16.046261427122644,
    "Energy_Generated_kWh": 82.18816943665941,
    "CO2_Saved_kg": 48.37876024520141,
    "Money_Saved_INR": 493.1290166199565
  },
  {
    "Date": "2024-05-11 12:03:17.301846",
    "Solar_Irradiance_W/m2": 247.5211919093025,
    "Panel_Temperature_C": 36.005495233574834,
    "Ambient_Temperature_C": 36.78620040368716,
    "Cloud_Cover_%": 7.049194564314465,
    "Energy_Generated_kWh": 106.57281656496463,
    "CO2_Saved_kg": 51.43048769878952,
    "Money_Saved_INR": 639.4368993897878
  },
  {
    "Date": "2024-05-12 12:03:17.301846",
    "Solar_Irradiance_W/m2": 171.15481721687985,
    "Panel_Temperature_C": 40.25327198003806,
    "Ambient_Temperature_C": 32.99036053310179,
    "Cloud_Cover_%": 18.564670490124303,
    "Energy_Generated_kWh": 86.26368947729961,
    "CO2_Saved_kg": 58.49611988516213,
    "Money_Saved_INR": 517.5821368637976
  },
  {
    "Date": "2024-05-13 12:03:17.301846",
    "Solar_Irradiance_W/m2": 155.0792664325821,
    "Panel_Temperature_C": 40.52762966478992,
    "Ambient_Temperature_C": 25.47640883109338,
    "Cloud_Cover_%": 66.42193849889682,
    "Energy_Generated_kWh": 67.86993223568521,
    "CO2_Saved_kg": 56.928575842374364,
    "Money_Saved_INR": 407.2195934141113
  },
  {
    "Date": "2024-05-14 12:03:17.301846",
    "Solar_Irradiance_W/m2": 224.59595857532528,
    "Panel_Temperature_C": 40.9351515278019,
    "Ambient_Temperature_C": 42.42717624826658,
    "Cloud_Cover_%": 88.16906118435081,
    "Energy_Generated_kWh": 89.11808390341406,
    "CO2_Saved_kg": 55.82571318808805,
    "Money_Saved_INR": 534.7085034204844
  },
  {
    "Date": "2024-05-15 12:03:17.301846",
    "Solar_Irradiance_W/m2": 133.9883396489679,
    "Panel_Temperature_C": 38.19365111014592,
    "Ambient_Temperature_C": 21.64454217770464,
    "Cloud_Cover_%": 81.41256855911618,
    "Energy_Generated_kWh": 70.81819379562016,
    "CO2_Saved_kg": 42.00059493298066,
    "Money_Saved_INR": 424.90916277372094
  },
  {
    "Date": "2024-05-16 12:03:17.301846",
    "Solar_Irradiance_W/m2": 291.5729382927177,
    "Panel_Temperature_C": 29.284975436347583,
    "Ambient_Temperature_C": 36.43407921527001,
    "Cloud_Cover_%": 68.51343098744842,
    "Energy_Generated_kWh": 66.1079926167371,
    "CO2_Saved_kg": 30.919978628766923,
    "Money_Saved_INR": 396.64795570042264
  },
  {
    "Date": "2024-05-17 12:03:17.301846",
    "Solar_Irradiance_W/m2": 258.97200603606433,
    "Panel_Temperature_C": 43.16715766150548,
    "Ambient_Temperature_C": 37.004076226300846,
    "Cloud_Cover_%": 11.043186341110268,
    "Energy_Generated_kWh": 56.91274663534031,
    "CO2_Saved_kg": 46.06947242938599,
    "Money_Saved_INR": 341.4764798120419
  },
  {
    "Date": "2024-05-18 12:03:17.301846",
    "Solar_Irradiance_W/m2": 176.54121739476477,
    "Panel_Temperature_C": 29.26827303490656,
    "Ambient_Temperature_C": 25.305658536463486,
    "Cloud_Cover_%": 28.918744629594983,
    "Energy_Generated_kWh": 44.96342386496562,
    "CO2_Saved_kg": 60.0163182520856,
    "Money_Saved_INR": 269.7805431897937
  },
  {
    "Date": "2024-05-19 12:03:17.301846",
    "Solar_Irradiance_W/m2": 114.34327354545613,
    "Panel_Temperature_C": 36.51317732619517,
    "Ambient_Temperature_C": 39.7472571004503,
    "Cloud_Cover_%": 30.980687532246897,
    "Energy_Generated_kWh": 72.20152586881109,
    "CO2_Saved_kg": 63.93454527524432,
    "Money_Saved_INR": 433.20915521286656
  },
  {
    "Date": "2024-05-20 12:03:17.301846",
    "Solar_Irradiance_W/m2": 267.69361870827066,
    "Panel_Temperature_C": 31.22862074990321,
    "Ambient_Temperature_C": 28.24967439780733,
    "Cloud_Cover_%": 24.99569463976212,
    "Energy_Generated_kWh": 83.16106979840264,
    "CO2_Saved_kg": 57.10549102297785,
    "Money_Saved_INR": 498.9664187904158
  },
  {
    "Date": "2024-05-21 12:03:17.301846",
    "Solar_Irradiance_W/m2": 194.2730077373691,
    "Panel_Temperature_C": 34.67930826703504,
    "Ambient_Temperature_C": 32.020855404959,
    "Cloud_Cover_%": 51.50056597097231,
    "Energy_Generated_kWh": 78.0675265997022,
    "CO2_Saved_kg": 54.29340822801734,
    "Money_Saved_INR": 468.40515959821323
  },
  {
    "Date": "2024-05-22 12:03:17.301846",
    "Solar_Irradiance_W/m2": 261.8908155986731,
    "Panel_Temperature_C": 36.6438120515174,
    "Ambient_Temperature_C": 31.822252871398547,
    "Cloud_Cover_%": 53.55538148796726,
    "Energy_Generated_kWh": 71.68066144105282,
    "CO2_Saved_kg": 53.79639648385965,
    "Money_Saved_INR": 430.0839686463169
  },
  {
    "Date": "2024-05-23 12:03:17.301846",
    "Solar_Irradiance_W/m2": 120.27861706028165,
    "Panel_Temperature_C": 36.606786077251364,
    "Ambient_Temperature_C": 29.059838809706164,
    "Cloud_Cover_%": 35.68859751711102,
    "Energy_Generated_kWh": 61.08507878606438,
    "CO2_Saved_kg": 44.43881253239219,
    "Money_Saved_INR": 366.5104727163863
  },
  {
    "Date": "2024-05-24 12:03:17.301846",
    "Solar_Irradiance_W/m2": 170.03124885231136,
    "Panel_Temperature_C": 37.109603771176424,
    "Ambient_Temperature_C": 35.675657912118474,
    "Cloud_Cover_%": 35.3789158736436,
    "Energy_Generated_kWh": 92.16492383369938,
    "CO2_Saved_kg": 48.6993970644638,
    "Money_Saved_INR": 552.9895430021962
  },
  {
    "Date": "2024-05-25 12:03:17.301846",
    "Solar_Irradiance_W/m2": 200.26218498590916,
    "Panel_Temperature_C": 43.06855634529323,
    "Ambient_Temperature_C": 35.55442104386549,
    "Cloud_Cover_%": 82.85555979060814,
    "Energy_Generated_kWh": 53.6573616010683,
    "CO2_Saved_kg": 66.6906952582633,
    "Money_Saved_INR": 321.9441696064098
  },
  {
    "Date": "2024-05-26 12:03:17.301846",
    "Solar_Irradiance_W/m2": 202.3490296882371,
    "Panel_Temperature_C": 37.2676715075699,
    "Ambient_Temperature_C": 17.760276187332735,
    "Cloud_Cover_%": 78.92928483196856,
    "Energy_Generated_kWh": 95.52055827686951,
    "CO2_Saved_kg": 40.574419942081235,
    "Money_Saved_INR": 573.123349661217
  },
  {
    "Date": "2024-05-27 12:03:17.301846",
    "Solar_Irradiance_W/m2": 177.4967264260378,
    "Panel_Temperature_C": 33.779216823546754,
    "Ambient_Temperature_C": 39.13038170014707,
    "Cloud_Cover_%": 30.779583168074566,
    "Energy_Generated_kWh": 59.9556596214655,
    "CO2_Saved_kg": 66.14778790709852,
    "Money_Saved_INR": 359.73395772879303
  },
  {
    "Date": "2024-05-28 12:03:17.301846",
    "Solar_Irradiance_W/m2": 231.14249661737495,
    "Panel_Temperature_C": 39.820435841441785,
    "Ambient_Temperature_C": 18.362556083750277,
    "Cloud_Cover_%": 91.37884438732593,
    "Energy_Generated_kWh": 64.9512952529393,
    "CO2_Saved_kg": 46.77971845507942,
    "Money_Saved_INR": 389.7077715176358
  },
  {
    "Date": "2024-05-29 12:03:17.301846",
    "Solar_Irradiance_W/m2": 146.61897853087027,
    "Panel_Temperature_C": 40.947352444623206,
    "Ambient_Temperature_C": 37.2278234303916,
    "Cloud_Cover_%": 95.2815017002506,
    "Energy_Generated_kWh": 50.66429618768646,
    "CO2_Saved_kg": 63.25432109095078,
    "Money_Saved_INR": 303.98577712611876
  },
  {
    "Date": "2024-05-30 12:03:17.301846",
    "Solar_Irradiance_W/m2": 192.88102574893531,
    "Panel_Temperature_C": 28.86196092431504,
    "Ambient_Temperature_C": 37.886935957793085,
    "Cloud_Cover_%": 32.67425420300408,
    "Energy_Generated_kWh": 69.97195706228726,
    "CO2_Saved_kg": 35.93184990502462,
    "Money_Saved_INR": 419.83174237372356
  },
  {
    "Date": "2024-05-31 12:03:17.301846",
    "Solar_Irradiance_W/m2": 206.01478158559493,
    "Panel_Temperature_C": 37.98700034924929,
    "Ambient_Temperature_C": 22.363234988493613,
    "Cloud_Cover_%": 35.442494879305485,
    "Energy_Generated_kWh": 99.50624916955958,
    "CO2_Saved_kg": 55.859042011646494,
    "Money_Saved_INR": 597.0374950173575
  },
  {
    "Date": "2024-06-01 12:03:17.301846",
    "Solar_Irradiance_W/m2": 225.72194170293744,
    "Panel_Temperature_C": 38.50586371155449,
    "Ambient_Temperature_C": 27.124299984317908,
    "Cloud_Cover_%": 50.56341534219588,
    "Energy_Generated_kWh": 90.31256176887914,
    "CO2_Saved_kg": 42.63229864052378,
    "Money_Saved_INR": 541.8753706132748
  },
  {
    "Date": "2024-06-02 12:03:17.301846",
    "Solar_Irradiance_W/m2": 235.5807439044445,
    "Panel_Temperature_C": 33.51218248320004,
    "Ambient_Temperature_C": 22.260067320598452,
    "Cloud_Cover_%": 94.11208125336735,
    "Energy_Generated_kWh": 99.5684422405607,
    "CO2_Saved_kg": 35.847328080758125,
    "Money_Saved_INR": 597.4106534433643
  },
  {
    "Date": "2024-06-03 12:03:17.301846",
    "Solar_Irradiance_W/m2": 143.76789540810654,
    "Panel_Temperature_C": 41.878534066558096,
    "Ambient_Temperature_C": 28.495552787978852,
    "Cloud_Cover_%": 87.63194331423115,
    "Energy_Generated_kWh": 90.44285091867872,
    "CO2_Saved_kg": 52.185340424109455,
    "Money_Saved_INR": 542.6571055120723
  },
  {
    "Date": "2024-06-04 12:03:17.301846",
    "Solar_Irradiance_W/m2": 123.29429146321888,
    "Panel_Temperature_C": 34.249722064837364,
    "Ambient_Temperature_C": 27.84376001069981,
    "Cloud_Cover_%": 10.25679625835898,
    "Energy_Generated_kWh": 57.926603429392614,
    "CO2_Saved_kg": 60.09471788595969,
    "Money_Saved_INR": 347.55962057635566
  },
  {
    "Date": "2024-06-05 12:03:17.301846",
    "Solar_Irradiance_W/m2": 263.88384109492546,
    "Panel_Temperature_C": 35.62788226735771,
    "Ambient_Temperature_C": 35.45762372588538,
    "Cloud_Cover_%": 39.27307432714162,
    "Energy_Generated_kWh": 73.38421551344885,
    "CO2_Saved_kg": 41.550585614065035,
    "Money_Saved_INR": 440.3052930806931
  },
  {
    "Date": "2024-06-06 12:03:17.301846",
    "Solar_Irradiance_W/m2": 216.61570059897957,
    "Panel_Temperature_C": 34.134640878580655,
    "Ambient_Temperature_C": 39.17216122283726,
    "Cloud_Cover_%": 55.33711897497719,
    "Energy_Generated_kWh": 64.39601741765074,
    "CO2_Saved_kg": 35.00984039541599,
    "Money_Saved_INR": 386.37610450590444
  },
  {
    "Date": "2024-06-07 12:03:17.301846",
    "Solar_Irradiance_W/m2": 162.57567317217232,
    "Panel_Temperature_C": 35.077895237907335,
    "Ambient_Temperature_C": 39.769786675529694,
    "Cloud_Cover_%": 50.313247255154,
    "Energy_Generated_kWh": 106.6114980807808,
    "CO2_Saved_kg": 49.08155235665045,
    "Money_Saved_INR": 639.6689884846849
  },
  {
    "Date": "2024-06-08 12:03:17.301846",
    "Solar_Irradiance_W/m2": 277.55759877612616,
    "Panel_Temperature_C": 29.518624565523993,
    "Ambient_Temperature_C": 26.064823813951886,
    "Cloud_Cover_%": 19.38630679368927,
    "Energy_Generated_kWh": 56.064227071473766,
    "CO2_Saved_kg": 49.12564671222819,
    "Money_Saved_INR": 336.3853624288426
  },
  {
    "Date": "2024-06-09 12:03:17.301846",
    "Solar_Irradiance_W/m2": 205.78373171464293,
    "Panel_Temperature_C": 27.79974558702853,
    "Ambient_Temperature_C": 28.535446883788307,
    "Cloud_Cover_%": 85.88167711681547,
    "Energy_Generated_kWh": 97.87395378778221,
    "CO2_Saved_kg": 55.483196275544984,
    "Money_Saved_INR": 587.2437227266932
  },
  {
    "Date": "2024-06-10 12:03:17.301846",
    "Solar_Irradiance_W/m2": 258.96485920319134,
    "Panel_Temperature_C": 42.97252531612486,
    "Ambient_Temperature_C": 18.215932654453347,
    "Cloud_Cover_%": 67.69407829968374,
    "Energy_Generated_kWh": 97.85907740217539,
    "CO2_Saved_kg": 59.495945713644886,
    "Money_Saved_INR": 587.1544644130523
  },
  {
    "Date": "2024-06-11 12:03:17.301846",
    "Solar_Irradiance_W/m2": 203.37592407050545,
    "Panel_Temperature_C": 30.76519325840836,
    "Ambient_Temperature_C": 24.358909534526678,
    "Cloud_Cover_%": 83.79083748518036,
    "Energy_Generated_kWh": 116.59240403432175,
    "CO2_Saved_kg": 49.40584818727506,
    "Money_Saved_INR": 699.5544242059304
  },
  {
    "Date": "2024-06-12 12:03:17.301846",
    "Solar_Irradiance_W/m2": 303.03739624409934,
    "Panel_Temperature_C": 30.043038252718464,
    "Ambient_Temperature_C": 36.7539614316822,
    "Cloud_Cover_%": 85.87642793494722,
    "Energy_Generated_kWh": 71.80626814741005,
    "CO2_Saved_kg": 68.55503314794262,
    "Money_Saved_INR": 430.83760888446034
  },
  {
    "Date": "2024-06-13 12:03:17.301846",
    "Solar_Irradiance_W/m2": 287.7670421221602,
    "Panel_Temperature_C": 24.233049431981428,
    "Ambient_Temperature_C": 41.30907976483762,
    "Cloud_Cover_%": 74.83558536657398,
    "Energy_Generated_kWh": 94.24644319160325,
    "CO2_Saved_kg": 52.24234744535292,
    "Money_Saved_INR": 565.4786591496195
  },
  {
    "Date": "2024-06-14 12:03:17.301846",
    "Solar_Irradiance_W/m2": 187.55179257604632,
    "Panel_Temperature_C": 31.805191261552487,
    "Ambient_Temperature_C": 21.359557896840546,
    "Cloud_Cover_%": 43.92106012497173,
    "Energy_Generated_kWh": 125.63303673077685,
    "CO2_Saved_kg": 46.535734939931004,
    "Money_Saved_INR": 753.7982203846611
  },
  {
    "Date": "2024-06-15 12:03:17.301846",
    "Solar_Irradiance_W/m2": 248.57854754771776,
    "Panel_Temperature_C": 28.38455103296251,
    "Ambient_Temperature_C": 25.85275018592974,
    "Cloud_Cover_%": 61.054675501542455,
    "Energy_Generated_kWh": 67.64716646132607,
    "CO2_Saved_kg": 33.88432640897172,
    "Money_Saved_INR": 405.8829987679564
  },
  {
    "Date": "2024-06-16 12:03:17.301846",
    "Solar_Irradiance_W/m2": 232.2687974792574,
    "Panel_Temperature_C": 43.21007580068185,
    "Ambient_Temperature_C": 29.81515970128751,
    "Cloud_Cover_%": 16.036540611974313,
    "Energy_Generated_kWh": 49.299195049352804,
    "CO2_Saved_kg": 47.37340479683832,
    "Money_Saved_INR": 295.7951702961168
  },
  {
    "Date": "2024-06-17 12:03:17.301846",
    "Solar_Irradiance_W/m2": 268.43157787661744,
    "Panel_Temperature_C": 40.04908544671317,
    "Ambient_Temperature_C": 31.961128111737246,
    "Cloud_Cover_%": 67.36454174749078,
    "Energy_Generated_kWh": 42.399799321844725,
    "CO2_Saved_kg": 46.63613054588864,
    "Money_Saved_INR": 254.39879593106835
  },
  {
    "Date": "2024-06-18 12:03:17.301846",
    "Solar_Irradiance_W/m2": 151.7538269709948,
    "Panel_Temperature_C": 31.559248274111383,
    "Ambient_Temperature_C": 24.332775360548478,
    "Cloud_Cover_%": 17.925325573928074,
    "Energy_Generated_kWh": 94.25424057722662,
    "CO2_Saved_kg": 59.6030479628147,
    "Money_Saved_INR": 565.5254434633598
  },
  {
    "Date": "2024-06-19 12:03:17.301846",
    "Solar_Irradiance_W/m2": 234.30257299992195,
    "Panel_Temperature_C": 46.26217902672154,
    "Ambient_Temperature_C": 32.968427311248625,
    "Cloud_Cover_%": 69.39495905101568,
    "Energy_Generated_kWh": 42.33699583882832,
    "CO2_Saved_kg": 54.62483624066854,
    "Money_Saved_INR": 254.02197503296992
  },
  {
    "Date": "2024-06-20 12:03:17.301846",
    "Solar_Irradiance_W/m2": 252.92122434247938,
    "Panel_Temperature_C": 39.90882743495797,
    "Ambient_Temperature_C": 26.683124570503587,
    "Cloud_Cover_%": 22.959816075396866,
    "Energy_Generated_kWh": 72.55361894124154,
    "CO2_Saved_kg": 38.206308783673826,
    "Money_Saved_INR": 435.3217136474492
  },
  {
    "Date": "2024-06-21 12:03:17.301846",
    "Solar_Irradiance_W/m2": 112.06302567884428,
    "Panel_Temperature_C": 33.37584308245689,
    "Ambient_Temperature_C": 29.898834103852046,
    "Cloud_Cover_%": 11.755130015021997,
    "Energy_Generated_kWh": 88.74626374077921,
    "CO2_Saved_kg": 51.72254386411038,
    "Money_Saved_INR": 532.4775824446752
  },
  {
    "Date": "2024-06-22 12:03:17.301846",
    "Solar_Irradiance_W/m2": 140.83707436671125,
    "Panel_Temperature_C": 22.502971425632133,
    "Ambient_Temperature_C": 33.823989736025894,
    "Cloud_Cover_%": 16.52844901429574,
    "Energy_Generated_kWh": 83.70351073659828,
    "CO2_Saved_kg": 56.71531171729053,
    "Money_Saved_INR": 502.22106441958965
  },
  {
    "Date": "2024-06-23 12:03:17.301846",
    "Solar_Irradiance_W/m2": 98.03839111199497,
    "Panel_Temperature_C": 46.45471286295371,
    "Ambient_Temperature_C": 30.044955888676565,
    "Cloud_Cover_%": 0.1992135219070268,
    "Energy_Generated_kWh": 88.50889728368344,
    "CO2_Saved_kg": 65.28031359387833,
    "Money_Saved_INR": 531.0533837021006
  },
  {
    "Date": "2024-06-24 12:03:17.301846",
    "Solar_Irradiance_W/m2": 186.5296582777721,
    "Panel_Temperature_C": 28.05213766618202,
    "Ambient_Temperature_C": 26.945298766314018,
    "Cloud_Cover_%": 71.87396178535302,
    "Energy_Generated_kWh": 84.44579711601708,
    "CO2_Saved_kg": 58.875039674140595,
    "Money_Saved_INR": 506.67478269610245
  },
  {
    "Date": "2024-06-25 12:03:17.301846",
    "Solar_Irradiance_W/m2": 235.8771127897981,
    "Panel_Temperature_C": 26.773006265215542,
    "Ambient_Temperature_C": 29.232731372519183,
    "Cloud_Cover_%": 73.24010490583791,
    "Energy_Generated_kWh": 105.57731626626787,
    "CO2_Saved_kg": 57.60846654311478,
    "Money_Saved_INR": 633.4638975976072
  },
  {
    "Date": "2024-06-26 12:03:17.301846",
    "Solar_Irradiance_W/m2": 275.1178526048014,
    "Panel_Temperature_C": 40.1128521600482,
    "Ambient_Temperature_C": 29.381459285562652,
    "Cloud_Cover_%": 51.493334991325945,
    "Energy_Generated_kWh": 60.95367238522406,
    "CO2_Saved_kg": 50.60085994615164,
    "Money_Saved_INR": 365.7220343113444
  },
  {
    "Date": "2024-06-27 12:03:17.301846",
    "Solar_Irradiance_W/m2": 203.70473902098877,
    "Panel_Temperature_C": 47.19876203169636,
    "Ambient_Temperature_C": 27.409922790825107,
    "Cloud_Cover_%": 16.13628010553837,
    "Energy_Generated_kWh": 66.46009723082938,
    "CO2_Saved_kg": 53.883120054234496,
    "Money_Saved_INR": 398.76058338497626
  },
  {
    "Date": "2024-06-28 12:03:17.301846",
    "Solar_Irradiance_W/m2": 281.4307772785646,
    "Panel_Temperature_C": 41.921364092552594,
    "Ambient_Temperature_C": 28.188427561330283,
    "Cloud_Cover_%": 8.355433751068976,
    "Energy_Generated_kWh": 64.54681109458352,
    "CO2_Saved_kg": 62.49504900706159,
    "Money_Saved_INR": 387.2808665675011
  },
  {
    "Date": "2024-06-29 12:03:17.301846",
    "Solar_Irradiance_W/m2": 130.99492708925544,
    "Panel_Temperature_C": 37.8195456002618,
    "Ambient_Temperature_C": 41.19053019353302,
    "Cloud_Cover_%": 1.912896643728701,
    "Energy_Generated_kWh": 96.60383623725221,
    "CO2_Saved_kg": 36.6722260252035,
    "Money_Saved_INR": 579.6230174235133
  },
  {
    "Date": "2024-06-30 12:03:17.301846",
    "Solar_Irradiance_W/m2": 114.83087803224227,
    "Panel_Temperature_C": 37.97377170832643,
    "Ambient_Temperature_C": 33.92643613558867,
    "Cloud_Cover_%": 16.57481769652207,
    "Energy_Generated_kWh": 98.00797176790127,
    "CO2_Saved_kg": 46.50560672783044,
    "Money_Saved_INR": 588.0478306074076
  },
  {
    "Date": "2024-07-01 12:03:17.301846",
    "Solar_Irradiance_W/m2": 197.22261505516906,
    "Panel_Temperature_C": 39.267077793901535,
    "Ambient_Temperature_C": 27.931637773795877,
    "Cloud_Cover_%": 89.08555349831467,
    "Energy_Generated_kWh": 89.02450638637016,
    "CO2_Saved_kg": 42.27431251243759,
    "Money_Saved_INR": 534.147038318221
  },
  {
    "Date": "2024-07-02 12:03:17.301846",
    "Solar_Irradiance_W/m2": 219.20327244696537,
    "Panel_Temperature_C": 38.79464294893383,
    "Ambient_Temperature_C": 34.87868083157515,
    "Cloud_Cover_%": 24.153684170168177,
    "Energy_Generated_kWh": 103.66987333779855,
    "CO2_Saved_kg": 53.79153118726124,
    "Money_Saved_INR": 622.0192400267913
  },
  {
    "Date": "2024-07-03 12:03:17.301846",
    "Solar_Irradiance_W/m2": 198.36526259529535,
    "Panel_Temperature_C": 36.40595711984688,
    "Ambient_Temperature_C": 27.66326357170793,
    "Cloud_Cover_%": 35.42713272172156,
    "Energy_Generated_kWh": 56.43918265247238,
    "CO2_Saved_kg": 62.302221756507876,
    "Money_Saved_INR": 338.6350959148343
  },
  {
    "Date": "2024-07-04 12:03:17.301846",
    "Solar_Irradiance_W/m2": 96.62789499800617,
    "Panel_Temperature_C": 35.52100551975938,
    "Ambient_Temperature_C": 38.21187246310649,
    "Cloud_Cover_%": 10.534548448133318,
    "Energy_Generated_kWh": 113.34448223102274,
    "CO2_Saved_kg": 44.03025713278926,
    "Money_Saved_INR": 680.0668933861364
  },
  {
    "Date": "2024-07-05 12:03:17.301846",
    "Solar_Irradiance_W/m2": 195.54399802436058,
    "Panel_Temperature_C": 34.68703436050239,
    "Ambient_Temperature_C": 32.58749534538666,
    "Cloud_Cover_%": 22.236130474817028,
    "Energy_Generated_kWh": 110.46477243424516,
    "CO2_Saved_kg": 26.09695632530562,
    "Money_Saved_INR": 662.788634605471
  },
  {
    "Date": "2024-07-06 12:03:17.301846",
    "Solar_Irradiance_W/m2": 134.77652497475734,
    "Panel_Temperature_C": 31.23017705566662,
    "Ambient_Temperature_C": 29.2488849919704,
    "Cloud_Cover_%": 51.922457078020514,
    "Energy_Generated_kWh": 94.71243994491493,
    "CO2_Saved_kg": 45.8777925497553,
    "Money_Saved_INR": 568.2746396694896
  },
  {
    "Date": "2024-07-07 12:03:17.301846",
    "Solar_Irradiance_W/m2": 233.48362744150194,
    "Panel_Temperature_C": 33.59662461566613,
    "Ambient_Temperature_C": 33.13401848067194,
    "Cloud_Cover_%": 60.775268309565256,
    "Energy_Generated_kWh": 115.6359781754212,
    "CO2_Saved_kg": 59.13473732017407,
    "Money_Saved_INR": 693.8158690525272
  },
  {
    "Date": "2024-07-08 12:03:17.301846",
    "Solar_Irradiance_W/m2": 218.32991230484242,
    "Panel_Temperature_C": 26.535215929023074,
    "Ambient_Temperature_C": 19.003866935520506,
    "Cloud_Cover_%": 24.535231416621105,
    "Energy_Generated_kWh": 46.867535846444525,
    "CO2_Saved_kg": 55.376299029498796,
    "Money_Saved_INR": 281.20521507866715
  },
  {
    "Date": "2024-07-09 12:03:17.301846",
    "Solar_Irradiance_W/m2": 153.00601068363224,
    "Panel_Temperature_C": 34.50830186602625,
    "Ambient_Temperature_C": 22.112627717631362,
    "Cloud_Cover_%": 5.773215922511721,
    "Energy_Generated_kWh": 69.51103727474697,
    "CO2_Saved_kg": 54.281862478105765,
    "Money_Saved_INR": 417.0662236484818
  },
  {
    "Date": "2024-07-10 12:03:17.301846",
    "Solar_Irradiance_W/m2": 174.30665413316532,
    "Panel_Temperature_C": 30.057044464245415,
    "Ambient_Temperature_C": 21.64252495520661,
    "Cloud_Cover_%": 39.10328691273987,
    "Energy_Generated_kWh": 65.29393078636096,
    "CO2_Saved_kg": 47.200066981255205,
    "Money_Saved_INR": 391.76358471816576
  },
  {
    "Date": "2024-07-11 12:03:17.301846",
    "Solar_Irradiance_W/m2": 147.0393239055524,
    "Panel_Temperature_C": 29.482053413921143,
    "Ambient_Temperature_C": 31.000601663345947,
    "Cloud_Cover_%": 23.420337092633414,
    "Energy_Generated_kWh": 94.42958647514686,
    "CO2_Saved_kg": 37.209692637802135,
    "Money_Saved_INR": 566.5775188508812
  },
  {
    "Date": "2024-07-12 12:03:17.301846",
    "Solar_Irradiance_W/m2": 196.8660451363414,
    "Panel_Temperature_C": 35.89947075576739,
    "Ambient_Temperature_C": 42.12760499639565,
    "Cloud_Cover_%": 21.955392322980195,
    "Energy_Generated_kWh": 58.99718520795709,
    "CO2_Saved_kg": 55.15294321624467,
    "Money_Saved_INR": 353.9831112477425
  },
  {
    "Date": "2024-07-13 12:03:17.301846",
    "Solar_Irradiance_W/m2": 247.75711602506192,
    "Panel_Temperature_C": 41.960011431723,
    "Ambient_Temperature_C": 45.61910102334843,
    "Cloud_Cover_%": 95.98628027134552,
    "Energy_Generated_kWh": 95.14990298674971,
    "CO2_Saved_kg": 41.65718189965375,
    "Money_Saved_INR": 570.8994179204983
  },
  {
    "Date": "2024-07-14 12:03:17.301846",
    "Solar_Irradiance_W/m2": 150.71369768322282,
    "Panel_Temperature_C": 39.59158303001156,
    "Ambient_Temperature_C": 34.4663577100853,
    "Cloud_Cover_%": 61.63004859257241,
    "Energy_Generated_kWh": 107.41072287993427,
    "CO2_Saved_kg": 71.84096733380457,
    "Money_Saved_INR": 644.4643372796056
  },
  {
    "Date": "2024-07-15 12:03:17.301846",
    "Solar_Irradiance_W/m2": 225.20232577589223,
    "Panel_Temperature_C": 27.147496981884114,
    "Ambient_Temperature_C": 33.5059113246112,
    "Cloud_Cover_%": 55.68784431720959,
    "Energy_Generated_kWh": 93.90405800167999,
    "CO2_Saved_kg": 55.70507208354516,
    "Money_Saved_INR": 563.4243480100799
  },
  {
    "Date": "2024-07-16 12:03:17.301846",
    "Solar_Irradiance_W/m2": 173.48711908137795,
    "Panel_Temperature_C": 30.051859317148313,
    "Ambient_Temperature_C": 17.392595860930825,
    "Cloud_Cover_%": 41.57751035233219,
    "Energy_Generated_kWh": 85.67502047323002,
    "CO2_Saved_kg": 44.19351697446049,
    "Money_Saved_INR": 514.0501228393802
  },
  {
    "Date": "2024-07-17 12:03:17.301846",
    "Solar_Irradiance_W/m2": 160.3563583868828,
    "Panel_Temperature_C": 39.70385593994108,
    "Ambient_Temperature_C": 26.201283401861847,
    "Cloud_Cover_%": 42.89443334301443,
    "Energy_Generated_kWh": 60.24253318198502,
    "CO2_Saved_kg": 43.88614752611372,
    "Money_Saved_INR": 361.4551990919101
  },
  {
    "Date": "2024-07-18 12:03:17.301846",
    "Solar_Irradiance_W/m2": 194.64848200227212,
    "Panel_Temperature_C": 30.087563032308452,
    "Ambient_Temperature_C": 24.48551373664233,
    "Cloud_Cover_%": 54.090500383808084,
    "Energy_Generated_kWh": 63.0629806774927,
    "CO2_Saved_kg": 49.070557933864116,
    "Money_Saved_INR": 378.3778840649562
  },
  {
    "Date": "2024-07-19 12:03:17.301846",
    "Solar_Irradiance_W/m2": 148.2378838790313,
    "Panel_Temperature_C": 33.87683425001488,
    "Ambient_Temperature_C": 25.65406681224219,
    "Cloud_Cover_%": 69.64298070361072,
    "Energy_Generated_kWh": 104.99237810593334,
    "CO2_Saved_kg": 47.6049807797825,
    "Money_Saved_INR": 629.9542686356001
  },
  {
    "Date": "2024-07-20 12:03:17.301846",
    "Solar_Irradiance_W/m2": 172.3175347326409,
    "Panel_Temperature_C": 37.75026049512276,
    "Ambient_Temperature_C": 28.822993269906473,
    "Cloud_Cover_%": 70.21460961818295,
    "Energy_Generated_kWh": 95.58698007810665,
    "CO2_Saved_kg": 61.16833775529955,
    "Money_Saved_INR": 573.5218804686399
  },
  {
    "Date": "2024-07-21 12:03:17.301846",
    "Solar_Irradiance_W/m2": 140.10610537055757,
    "Panel_Temperature_C": 30.158277725681824,
    "Ambient_Temperature_C": 26.695365956120106,
    "Cloud_Cover_%": 17.169390770544958,
    "Energy_Generated_kWh": 79.21960961244912,
    "CO2_Saved_kg": 51.864161697440466,
    "Money_Saved_INR": 475.3176576746947
  },
  {
    "Date": "2024-07-22 12:03:17.301846",
    "Solar_Irradiance_W/m2": 298.2362566458195,
    "Panel_Temperature_C": 35.5268775307298,
    "Ambient_Temperature_C": 16.144901327369485,
    "Cloud_Cover_%": 50.0112752076627,
    "Energy_Generated_kWh": 71.6418090846822,
    "CO2_Saved_kg": 42.683682610914715,
    "Money_Saved_INR": 429.85085450809316
  },
  {
    "Date": "2024-07-23 12:03:17.301846",
    "Solar_Irradiance_W/m2": 201.76317759858642,
    "Panel_Temperature_C": 28.329872525408977,
    "Ambient_Temperature_C": 35.23537179282274,
    "Cloud_Cover_%": 41.195809503410196,
    "Energy_Generated_kWh": 39.48384253777246,
    "CO2_Saved_kg": 68.90440685155782,
    "Money_Saved_INR": 236.90305522663476
  },
  {
    "Date": "2024-07-24 12:03:17.301846",
    "Solar_Irradiance_W/m2": 165.01372460037072,
    "Panel_Temperature_C": 31.99316178024393,
    "Ambient_Temperature_C": 22.490798819821354,
    "Cloud_Cover_%": 87.05269662693841,
    "Energy_Generated_kWh": 58.58295162631123,
    "CO2_Saved_kg": 50.49308331520223,
    "Money_Saved_INR": 351.49770975786737
  },
  {
    "Date": "2024-07-25 12:03:17.301846",
    "Solar_Irradiance_W/m2": 210.6989955367111,
    "Panel_Temperature_C": 36.598909670712686,
    "Ambient_Temperature_C": 31.674728048778046,
    "Cloud_Cover_%": 63.14189212183764,
    "Energy_Generated_kWh": 118.22838174279447,
    "CO2_Saved_kg": 57.68839675968897,
    "Money_Saved_INR": 709.3702904567668
  },
  {
    "Date": "2024-07-26 12:03:17.301846",
    "Solar_Irradiance_W/m2": 194.38359751545852,
    "Panel_Temperature_C": 27.035031332341653,
    "Ambient_Temperature_C": 44.51857868824982,
    "Cloud_Cover_%": 53.25040664159818,
    "Energy_Generated_kWh": 54.39088857995067,
    "CO2_Saved_kg": 43.91773492555241,
    "Money_Saved_INR": 326.345331479704
  },
  {
    "Date": "2024-07-27 12:03:17.301846",
    "Solar_Irradiance_W/m2": 188.95152002333884,
    "Panel_Temperature_C": 37.202373689801995,
    "Ambient_Temperature_C": 23.564307858895035,
    "Cloud_Cover_%": 11.539464217891737,
    "Energy_Generated_kWh": 83.78959642442162,
    "CO2_Saved_kg": 53.631156277445236,
    "Money_Saved_INR": 502.7375785465297
  },
  {
    "Date": "2024-07-28 12:03:17.301846",
    "Solar_Irradiance_W/m2": 230.70833500217125,
    "Panel_Temperature_C": 34.901811005366596,
    "Ambient_Temperature_C": 12.287987340775693,
    "Cloud_Cover_%": 60.56378893234115,
    "Energy_Generated_kWh": 100.14887946390397,
    "CO2_Saved_kg": 53.11109991143195,
    "Money_Saved_INR": 600.8932767834237
  },
  {
    "Date": "2024-07-29 12:03:17.301846",
    "Solar_Irradiance_W/m2": 237.87538550236525,
    "Panel_Temperature_C": 37.76244977208574,
    "Ambient_Temperature_C": 27.997970446839226,
    "Cloud_Cover_%": 11.720390568023342,
    "Energy_Generated_kWh": 54.90154663995415,
    "CO2_Saved_kg": 31.103507079038472,
    "Money_Saved_INR": 329.4092798397249
  },
  {
    "Date": "2024-07-30 12:03:17.301846",
    "Solar_Irradiance_W/m2": 173.47494261947364,
    "Panel_Temperature_C": 36.119570670323306,
    "Ambient_Temperature_C": 37.70671744499,
    "Cloud_Cover_%": 33.720657556575205,
    "Energy_Generated_kWh": 83.69420949562166,
    "CO2_Saved_kg": 70.15275110460641,
    "Money_Saved_INR": 502.16525697373
  },
  {
    "Date": "2024-07-31 12:03:17.301846",
    "Solar_Irradiance_W/m2": 171.209087967766,
    "Panel_Temperature_C": 41.82070214986922,
    "Ambient_Temperature_C": 43.70843217954416,
    "Cloud_Cover_%": 14.284196481433186,
    "Energy_Generated_kWh": 98.7583107502131,
    "CO2_Saved_kg": 62.906444609225474,
    "Money_Saved_INR": 592.5498645012785
  },
  {
    "Date": "2024-08-01 12:03:17.301846",
    "Solar_Irradiance_W/m2": 186.2474151424178,
    "Panel_Temperature_C": 35.62612251323954,
    "Ambient_Temperature_C": 21.393152838833082,
    "Cloud_Cover_%": 69.20736470243689,
    "Energy_Generated_kWh": 80.249986438145,
    "CO2_Saved_kg": 46.02804683854012,
    "Money_Saved_INR": 481.49991862887
  },
  {
    "Date": "2024-08-02 12:03:17.301846",
    "Solar_Irradiance_W/m2": 84.90394176322076,
    "Panel_Temperature_C": 32.852972294373735,
    "Ambient_Temperature_C": 33.47689456265565,
    "Cloud_Cover_%": 20.62521138361526,
    "Energy_Generated_kWh": 137.36806111333536,
    "CO2_Saved_kg": 38.977302595441444,
    "Money_Saved_INR": 824.2083666800122
  },
  {
    "Date": "2024-08-03 12:03:17.301846",
    "Solar_Irradiance_W/m2": 124.24044689007239,
    "Panel_Temperature_C": 35.61148751516142,
    "Ambient_Temperature_C": 26.742826802539625,
    "Cloud_Cover_%": 39.1859373188026,
    "Energy_Generated_kWh": 46.62801482243609,
    "CO2_Saved_kg": 53.47561613803552,
    "Money_Saved_INR": 279.76808893461657
  },
  {
    "Date": "2024-08-04 12:03:17.301846",
    "Solar_Irradiance_W/m2": 268.34371337222626,
    "Panel_Temperature_C": 37.716490145181936,
    "Ambient_Temperature_C": 29.258361519871052,
    "Cloud_Cover_%": 89.56747776187787,
    "Energy_Generated_kWh": 101.17457059767759,
    "CO2_Saved_kg": 50.86697699414397,
    "Money_Saved_INR": 607.0474235860655
  },
  {
    "Date": "2024-08-05 12:03:17.301846",
    "Solar_Irradiance_W/m2": 282.2483856750642,
    "Panel_Temperature_C": 35.244300351628524,
    "Ambient_Temperature_C": 48.51040342911924,
    "Cloud_Cover_%": 20.431638339897027,
    "Energy_Generated_kWh": 76.5439652520707,
    "CO2_Saved_kg": 53.55668948563229,
    "Money_Saved_INR": 459.26379151242423
  },
  {
    "Date": "2024-08-06 12:03:17.301846",
    "Solar_Irradiance_W/m2": 187.54819802218108,
    "Panel_Temperature_C": 35.20295845601941,
    "Ambient_Temperature_C": 19.47920770123393,
    "Cloud_Cover_%": 50.780506395877914,
    "Energy_Generated_kWh": 95.43840309673351,
    "CO2_Saved_kg": 51.91577396194089,
    "Money_Saved_INR": 572.630418580401
  },
  {
    "Date": "2024-08-07 12:03:17.301846",
    "Solar_Irradiance_W/m2": 228.8278481527883,
    "Panel_Temperature_C": 31.490041560966223,
    "Ambient_Temperature_C": 31.776177630462016,
    "Cloud_Cover_%": 41.9271661166022,
    "Energy_Generated_kWh": 88.82614303398492,
    "CO2_Saved_kg": 55.06240989305926,
    "Money_Saved_INR": 532.9568582039095
  },
  {
    "Date": "2024-08-08 12:03:17.301846",
    "Solar_Irradiance_W/m2": 215.5625077271768,
    "Panel_Temperature_C": 31.68549541224526,
    "Ambient_Temperature_C": 33.27385220235803,
    "Cloud_Cover_%": 1.8124041045729733,
    "Energy_Generated_kWh": 65.33687605780007,
    "CO2_Saved_kg": 64.47305699391806,
    "Money_Saved_INR": 392.02125634680044
  },
  {
    "Date": "2024-08-09 12:03:17.301846",
    "Solar_Irradiance_W/m2": 353.9440404227619,
    "Panel_Temperature_C": 27.986973641001534,
    "Ambient_Temperature_C": 37.60050427457543,
    "Cloud_Cover_%": 79.27581135728128,
    "Energy_Generated_kWh": 84.5799278491868,
    "CO2_Saved_kg": 55.681032051286465,
    "Money_Saved_INR": 507.47956709512084
  },
  {
    "Date": "2024-08-10 12:03:17.301846",
    "Solar_Irradiance_W/m2": 255.97874557172884,
    "Panel_Temperature_C": 43.7478837159347,
    "Ambient_Temperature_C": 30.685882074296266,
    "Cloud_Cover_%": 6.904590631459973,
    "Energy_Generated_kWh": 42.841970972034254,
    "CO2_Saved_kg": 39.50344501090059,
    "Money_Saved_INR": 257.0518258322055
  },
  {
    "Date": "2024-08-11 12:03:17.301846",
    "Solar_Irradiance_W/m2": 193.60412042596167,
    "Panel_Temperature_C": 28.780683823043574,
    "Ambient_Temperature_C": 32.15635377652872,
    "Cloud_Cover_%": 47.42550209769536,
    "Energy_Generated_kWh": 92.06495001142787,
    "CO2_Saved_kg": 63.62562852712452,
    "Money_Saved_INR": 552.3897000685672
  },
  {
    "Date": "2024-08-12 12:03:17.301846",
    "Solar_Irradiance_W/m2": 152.22297796997873,
    "Panel_Temperature_C": 31.53547401102046,
    "Ambient_Temperature_C": 27.258460028047462,
    "Cloud_Cover_%": 56.06782949389499,
    "Energy_Generated_kWh": 85.96316931981052,
    "CO2_Saved_kg": 66.40614563488288,
    "Money_Saved_INR": 515.7790159188631
  },
  {
    "Date": "2024-08-13 12:03:17.301846",
    "Solar_Irradiance_W/m2": 119.67768398712137,
    "Panel_Temperature_C": 31.40796367215401,
    "Ambient_Temperature_C": 31.883888588715752,
    "Cloud_Cover_%": 62.842645661458704,
    "Energy_Generated_kWh": 92.77320337286204,
    "CO2_Saved_kg": 81.52056734512085,
    "Money_Saved_INR": 556.6392202371723
  },
  {
    "Date": "2024-08-14 12:03:17.301846",
    "Solar_Irradiance_W/m2": 210.17318179336115,
    "Panel_Temperature_C": 39.474621884722204,
    "Ambient_Temperature_C": 27.597654071518125,
    "Cloud_Cover_%": 68.86316293078755,
    "Energy_Generated_kWh": 101.16236650174301,
    "CO2_Saved_kg": 38.76505966760402,
    "Money_Saved_INR": 606.974199010458
  },
  {
    "Date": "2024-08-15 12:03:17.301846",
    "Solar_Irradiance_W/m2": 162.18246273578484,
    "Panel_Temperature_C": 33.52525160853986,
    "Ambient_Temperature_C": 34.351003228992354,
    "Cloud_Cover_%": 25.327238352271507,
    "Energy_Generated_kWh": 87.35239680419421,
    "CO2_Saved_kg": 52.42882013150275,
    "Money_Saved_INR": 524.1143808251653
  },
  {
    "Date": "2024-08-16 12:03:17.301846",
    "Solar_Irradiance_W/m2": 128.8873145201163,
    "Panel_Temperature_C": 41.23871036336867,
    "Ambient_Temperature_C": 27.412727647694563,
    "Cloud_Cover_%": 0.9978776658449373,
    "Energy_Generated_kWh": 82.96178839596553,
    "CO2_Saved_kg": 29.17901296811013,
    "Money_Saved_INR": 497.77073037579316
  },
  {
    "Date": "2024-08-17 12:03:17.301846",
    "Solar_Irradiance_W/m2": 167.67135578787367,
    "Panel_Temperature_C": 31.63254687878066,
    "Ambient_Temperature_C": 32.639702757315305,
    "Cloud_Cover_%": 72.3443662354912,
    "Energy_Generated_kWh": 62.37863326677416,
    "CO2_Saved_kg": 55.53149156379209,
    "Money_Saved_INR": 374.27179960064495
  },
  {
    "Date": "2024-08-18 12:03:17.301846",
    "Solar_Irradiance_W/m2": 145.92259981928026,
    "Panel_Temperature_C": 36.39497081111901,
    "Ambient_Temperature_C": 29.79516030420515,
    "Cloud_Cover_%": 53.56565993475786,
    "Energy_Generated_kWh": 65.75558472701898,
    "CO2_Saved_kg": 44.517997018332274,
    "Money_Saved_INR": 394.53350836211393
  },
  {
    "Date": "2024-08-19 12:03:17.301846",
    "Solar_Irradiance_W/m2": 284.3570817536282,
    "Panel_Temperature_C": 30.823264733701215,
    "Ambient_Temperature_C": 37.882351755405175,
    "Cloud_Cover_%": 83.61177032072487,
    "Energy_Generated_kWh": 103.73469240354662,
    "CO2_Saved_kg": 69.23445794824953,
    "Money_Saved_INR": 622.4081544212797
  },
  {
    "Date": "2024-08-20 12:03:17.301846",
    "Solar_Irradiance_W/m2": 244.08198784747253,
    "Panel_Temperature_C": 45.72574563886694,
    "Ambient_Temperature_C": 29.640243934880598,
    "Cloud_Cover_%": 82.13883629006943,
    "Energy_Generated_kWh": 108.72670811411957,
    "CO2_Saved_kg": 42.25385029981418,
    "Money_Saved_INR": 652.3602486847175
  },
  {
    "Date": "2024-08-21 12:03:17.301846",
    "Solar_Irradiance_W/m2": 199.60136793416913,
    "Panel_Temperature_C": 29.062007904852436,
    "Ambient_Temperature_C": 17.58877272255183,
    "Cloud_Cover_%": 84.33261677878832,
    "Energy_Generated_kWh": 75.23779127375892,
    "CO2_Saved_kg": 33.10816962032739,
    "Money_Saved_INR": 451.4267476425535
  },
  {
    "Date": "2024-08-22 12:03:17.301846",
    "Solar_Irradiance_W/m2": 273.9972069445013,
    "Panel_Temperature_C": 36.54910355113514,
    "Ambient_Temperature_C": 38.83345050499794,
    "Cloud_Cover_%": 48.50946599795402,
    "Energy_Generated_kWh": 80.92005494506549,
    "CO2_Saved_kg": 45.2873625929748,
    "Money_Saved_INR": 485.5203296703929
  },
  {
    "Date": "2024-08-23 12:03:17.301846",
    "Solar_Irradiance_W/m2": 203.8684153823809,
    "Panel_Temperature_C": 38.168884404660496,
    "Ambient_Temperature_C": 23.659873893961667,
    "Cloud_Cover_%": 33.362839583686565,
    "Energy_Generated_kWh": 61.907712500124674,
    "CO2_Saved_kg": 30.245122287828625,
    "Money_Saved_INR": 371.4462750007481
  },
  {
    "Date": "2024-08-24 12:03:17.301846",
    "Solar_Irradiance_W/m2": 156.93578993358682,
    "Panel_Temperature_C": 37.06899548725749,
    "Ambient_Temperature_C": 25.42363562945826,
    "Cloud_Cover_%": 79.155820259137,
    "Energy_Generated_kWh": 103.4551369053489,
    "CO2_Saved_kg": 57.5109945450731,
    "Money_Saved_INR": 620.7308214320933
  },
  {
    "Date": "2024-08-25 12:03:17.301846",
    "Solar_Irradiance_W/m2": 276.15620386348286,
    "Panel_Temperature_C": 34.07356170561146,
    "Ambient_Temperature_C": 25.830370941695556,
    "Cloud_Cover_%": 45.12941130292549,
    "Energy_Generated_kWh": 93.30833647383557,
    "CO2_Saved_kg": 29.349169537436794,
    "Money_Saved_INR": 559.8500188430135
  },
  {
    "Date": "2024-08-26 12:03:17.301846",
    "Solar_Irradiance_W/m2": 226.94550218423294,
    "Panel_Temperature_C": 34.35089650133287,
    "Ambient_Temperature_C": 39.62106665219572,
    "Cloud_Cover_%": 18.34421964034345,
    "Energy_Generated_kWh": 118.82434872927499,
    "CO2_Saved_kg": 50.28457581183159,
    "Money_Saved_INR": 712.9460923756499
  },
  {
    "Date": "2024-08-27 12:03:17.301846",
    "Solar_Irradiance_W/m2": 148.13769228367718,
    "Panel_Temperature_C": 35.21905735989555,
    "Ambient_Temperature_C": 15.050280502149132,
    "Cloud_Cover_%": 85.49740195614743,
    "Energy_Generated_kWh": 62.43353845640522,
    "CO2_Saved_kg": 29.22188180143803,
    "Money_Saved_INR": 374.60123073843135
  },
  {
    "Date": "2024-08-28 12:03:17.301846",
    "Solar_Irradiance_W/m2": 190.4830660958196,
    "Panel_Temperature_C": 34.264989991857554,
    "Ambient_Temperature_C": 51.964239735619955,
    "Cloud_Cover_%": 88.25598767723473,
    "Energy_Generated_kWh": 72.43984201963566,
    "CO2_Saved_kg": 46.79702195463358,
    "Money_Saved_INR": 434.639052117814
  },
  {
    "Date": "2024-08-29 12:03:17.301846",
    "Solar_Irradiance_W/m2": 156.21908733076214,
    "Panel_Temperature_C": 39.81939558397455,
    "Ambient_Temperature_C": 37.39239766346236,
    "Cloud_Cover_%": 46.63097561401701,
    "Energy_Generated_kWh": 84.62891845051145,
    "CO2_Saved_kg": 66.43378155804534,
    "Money_Saved_INR": 507.7735107030687
  },
  {
    "Date": "2024-08-30 12:03:17.301846",
    "Solar_Irradiance_W/m2": 130.8600134517832,
    "Panel_Temperature_C": 46.05261500795676,
    "Ambient_Temperature_C": 31.562672398904116,
    "Cloud_Cover_%": 7.569972730978747,
    "Energy_Generated_kWh": 92.92979075451541,
    "CO2_Saved_kg": 53.60647891435795,
    "Money_Saved_INR": 557.5787445270925
  },
  {
    "Date": "2024-08-31 12:03:17.301846",
    "Solar_Irradiance_W/m2": 246.30887737658207,
    "Panel_Temperature_C": 32.21254107496083,
    "Ambient_Temperature_C": 29.615741995685994,
    "Cloud_Cover_%": 38.782608991693124,
    "Energy_Generated_kWh": 75.68664724904735,
    "CO2_Saved_kg": 41.36506395035066,
    "Money_Saved_INR": 454.1198834942841
  },
  {
    "Date": "2024-09-01 12:03:17.301846",
    "Solar_Irradiance_W/m2": 295.47083202350655,
    "Panel_Temperature_C": 28.150985102104613,
    "Ambient_Temperature_C": 31.998878524003597,
    "Cloud_Cover_%": 80.35376594626034,
    "Energy_Generated_kWh": 62.54077819092599,
    "CO2_Saved_kg": 49.68796511060916,
    "Money_Saved_INR": 375.2446691455559
  },
  {
    "Date": "2024-09-02 12:03:17.301846",
    "Solar_Irradiance_W/m2": 130.07162130904294,
    "Panel_Temperature_C": 34.55858975824373,
    "Ambient_Temperature_C": 33.64785699865537,
    "Cloud_Cover_%": 90.17740285462287,
    "Energy_Generated_kWh": 97.62815057847142,
    "CO2_Saved_kg": 50.18016872044446,
    "Money_Saved_INR": 585.7689034708285
  },
  {
    "Date": "2024-09-03 12:03:17.301846",
    "Solar_Irradiance_W/m2": 228.14846183452855,
    "Panel_Temperature_C": 47.898546688271594,
    "Ambient_Temperature_C": 34.5165091016504,
    "Cloud_Cover_%": 20.347274249759582,
    "Energy_Generated_kWh": 94.42270725091163,
    "CO2_Saved_kg": 54.72630345843406,
    "Money_Saved_INR": 566.5362435054698
  },
  {
    "Date": "2024-09-04 12:03:17.301846",
    "Solar_Irradiance_W/m2": 167.46787154390864,
    "Panel_Temperature_C": 30.981627160151348,
    "Ambient_Temperature_C": 33.88923126202414,
    "Cloud_Cover_%": 6.697361202527152,
    "Energy_Generated_kWh": 61.6745179887255,
    "CO2_Saved_kg": 36.331416367191736,
    "Money_Saved_INR": 370.047107932353
  },
  {
    "Date": "2024-09-05 12:03:17.301846",
    "Solar_Irradiance_W/m2": 175.6437308117652,
    "Panel_Temperature_C": 43.195584027220335,
    "Ambient_Temperature_C": 30.62706476878674,
    "Cloud_Cover_%": 87.73504531328386,
    "Energy_Generated_kWh": 107.10885602210992,
    "CO2_Saved_kg": 55.92567273847331,
    "Money_Saved_INR": 642.6531361326595
  },
  {
    "Date": "2024-09-06 12:03:17.301846",
    "Solar_Irradiance_W/m2": 170.38030378805655,
    "Panel_Temperature_C": 43.388504070382204,
    "Ambient_Temperature_C": 28.618631057848717,
    "Cloud_Cover_%": 38.94049389788753,
    "Energy_Generated_kWh": 103.40397418393208,
    "CO2_Saved_kg": 22.95608368397225,
    "Money_Saved_INR": 620.4238451035925
  },
  {
    "Date": "2024-09-07 12:03:17.301846",
    "Solar_Irradiance_W/m2": 156.8004615160092,
    "Panel_Temperature_C": 32.23205879146003,
    "Ambient_Temperature_C": 28.941087014425417,
    "Cloud_Cover_%": 54.176096426756324,
    "Energy_Generated_kWh": 82.68592994495586,
    "CO2_Saved_kg": 43.70115447636189,
    "Money_Saved_INR": 496.11557966973515
  },
  {
    "Date": "2024-09-08 12:03:17.301846",
    "Solar_Irradiance_W/m2": 202.42608139724135,
    "Panel_Temperature_C": 37.84491539592638,
    "Ambient_Temperature_C": 28.635642037531234,
    "Cloud_Cover_%": 96.80658120507589,
    "Energy_Generated_kWh": 81.59195724752072,
    "CO2_Saved_kg": 45.117261575484555,
    "Money_Saved_INR": 489.55174348512435
  },
  {
    "Date": "2024-09-09 12:03:17.301846",
    "Solar_Irradiance_W/m2": 158.4524941794481,
    "Panel_Temperature_C": 43.14198311564269,
    "Ambient_Temperature_C": 37.93639067806945,
    "Cloud_Cover_%": 6.656472791422285,
    "Energy_Generated_kWh": 91.08115542231815,
    "CO2_Saved_kg": 56.33326826071239,
    "Money_Saved_INR": 546.4869325339089
  },
  {
    "Date": "2024-09-10 12:03:17.301846",
    "Solar_Irradiance_W/m2": 213.52284128899194,
    "Panel_Temperature_C": 33.10436129506257,
    "Ambient_Temperature_C": 34.15489705596603,
    "Cloud_Cover_%": 64.83180074520956,
    "Energy_Generated_kWh": 62.76593859487484,
    "CO2_Saved_kg": 50.22630852676869,
    "Money_Saved_INR": 376.595631569249
  },
  {
    "Date": "2024-09-11 12:03:17.301846",
    "Solar_Irradiance_W/m2": 197.48809452754315,
    "Panel_Temperature_C": 33.98209819948819,
    "Ambient_Temperature_C": 9.417279557350039,
    "Cloud_Cover_%": 7.410542257486707,
    "Energy_Generated_kWh": 80.60062958328164,
    "CO2_Saved_kg": 35.944369461437134,
    "Money_Saved_INR": 483.60377749968984
  },
  {
    "Date": "2024-09-12 12:03:17.301846",
    "Solar_Irradiance_W/m2": 188.05259765667952,
    "Panel_Temperature_C": 32.09159543025678,
    "Ambient_Temperature_C": 34.59130543570833,
    "Cloud_Cover_%": 37.54689284665004,
    "Energy_Generated_kWh": 36.9523291078164,
    "CO2_Saved_kg": 40.15006874182985,
    "Money_Saved_INR": 221.71397464689838
  },
  {
    "Date": "2024-09-13 12:03:17.301846",
    "Solar_Irradiance_W/m2": 154.6218168979201,
    "Panel_Temperature_C": 29.926216346535668,
    "Ambient_Temperature_C": 31.363153363031422,
    "Cloud_Cover_%": 80.38145451934467,
    "Energy_Generated_kWh": 97.52911291005871,
    "CO2_Saved_kg": 51.98680009547407,
    "Money_Saved_INR": 585.1746774603523
  },
  {
    "Date": "2024-09-14 12:03:17.301846",
    "Solar_Irradiance_W/m2": 171.16143347158336,
    "Panel_Temperature_C": 31.753612274669965,
    "Ambient_Temperature_C": 29.86903870487872,
    "Cloud_Cover_%": 43.34722327556344,
    "Energy_Generated_kWh": 48.77013555116281,
    "CO2_Saved_kg": 49.20932658135444,
    "Money_Saved_INR": 292.62081330697686
  },
  {
    "Date": "2024-09-15 12:03:17.301846",
    "Solar_Irradiance_W/m2": 237.7695612912878,
    "Panel_Temperature_C": 28.880298666188718,
    "Ambient_Temperature_C": 27.280370828377798,
    "Cloud_Cover_%": 99.71823539029504,
    "Energy_Generated_kWh": 110.06839656857998,
    "CO2_Saved_kg": 44.20875890364253,
    "Money_Saved_INR": 660.4103794114799
  },
  {
    "Date": "2024-09-16 12:03:17.301846",
    "Solar_Irradiance_W/m2": 225.04585938121903,
    "Panel_Temperature_C": 35.17041734129613,
    "Ambient_Temperature_C": 37.8687890399021,
    "Cloud_Cover_%": 55.905928494660216,
    "Energy_Generated_kWh": 73.39759812067099,
    "CO2_Saved_kg": 45.19166210488021,
    "Money_Saved_INR": 440.385588724026
  },
  {
    "Date": "2024-09-17 12:03:17.301846",
    "Solar_Irradiance_W/m2": 151.12223776007244,
    "Panel_Temperature_C": 31.15013384470679,
    "Ambient_Temperature_C": 36.632685234860006,
    "Cloud_Cover_%": 32.11621526359535,
    "Energy_Generated_kWh": 75.76666036137647,
    "CO2_Saved_kg": 56.961679971592886,
    "Money_Saved_INR": 454.5999621682588
  },
  {
    "Date": "2024-09-18 12:03:17.301846",
    "Solar_Irradiance_W/m2": 204.9666152714613,
    "Panel_Temperature_C": 36.168929558953735,
    "Ambient_Temperature_C": 24.589856325234734,
    "Cloud_Cover_%": 22.011132590475313,
    "Energy_Generated_kWh": 67.44532187830988,
    "CO2_Saved_kg": 44.82307427130785,
    "Money_Saved_INR": 404.67193126985933
  },
  {
    "Date": "2024-09-19 12:03:17.301846",
    "Solar_Irradiance_W/m2": 237.56935616858945,
    "Panel_Temperature_C": 27.220521768981865,
    "Ambient_Temperature_C": 32.849366009871744,
    "Cloud_Cover_%": 35.05205342861618,
    "Energy_Generated_kWh": 74.23922252155847,
    "CO2_Saved_kg": 49.119087559709264,
    "Money_Saved_INR": 445.43533512935085
  },
  {
    "Date": "2024-09-20 12:03:17.301846",
    "Solar_Irradiance_W/m2": 116.52973594393141,
    "Panel_Temperature_C": 36.654401161072286,
    "Ambient_Temperature_C": 23.198402858210997,
    "Cloud_Cover_%": 37.25332737595508,
    "Energy_Generated_kWh": 108.37062690296074,
    "CO2_Saved_kg": 71.69936588080543,
    "Money_Saved_INR": 650.2237614177644
  },
  {
    "Date": "2024-09-21 12:03:17.301846",
    "Solar_Irradiance_W/m2": 227.16800961899676,
    "Panel_Temperature_C": 39.16764480804462,
    "Ambient_Temperature_C": 20.342672846477484,
    "Cloud_Cover_%": 6.8713677723960975,
    "Energy_Generated_kWh": 30.24382686929841,
    "CO2_Saved_kg": 35.76317363116077,
    "Money_Saved_INR": 181.46296121579047
  },
  {
    "Date": "2024-09-22 12:03:17.301846",
    "Solar_Irradiance_W/m2": 166.86881205270765,
    "Panel_Temperature_C": 25.031321787142723,
    "Ambient_Temperature_C": 25.612979427870243,
    "Cloud_Cover_%": 36.95741994267732,
    "Energy_Generated_kWh": 105.53930772176375,
    "CO2_Saved_kg": 31.481572684253415,
    "Money_Saved_INR": 633.2358463305825
  },
  {
    "Date": "2024-09-23 12:03:17.301846",
    "Solar_Irradiance_W/m2": 228.52993342965797,
    "Panel_Temperature_C": 36.87028284923786,
    "Ambient_Temperature_C": 36.03675430667931,
    "Cloud_Cover_%": 46.423851973922496,
    "Energy_Generated_kWh": 86.76046962203417,
    "CO2_Saved_kg": 57.83589664798607,
    "Money_Saved_INR": 520.562817732205
  },
  {
    "Date": "2024-09-24 12:03:17.301846",
    "Solar_Irradiance_W/m2": 161.83704217287416,
    "Panel_Temperature_C": 41.13834496236646,
    "Ambient_Temperature_C": 36.671875317632605,
    "Cloud_Cover_%": 72.27377522388046,
    "Energy_Generated_kWh": 55.85956704285569,
    "CO2_Saved_kg": 43.21356938705897,
    "Money_Saved_INR": 335.1574022571341
  },
  {
    "Date": "2024-09-25 12:03:17.301846",
    "Solar_Irradiance_W/m2": 109.75589496677405,
    "Panel_Temperature_C": 28.951794906543974,
    "Ambient_Temperature_C": 33.59159794068105,
    "Cloud_Cover_%": 65.6729484721608,
    "Energy_Generated_kWh": 58.49375213901524,
    "CO2_Saved_kg": 46.8176247225738,
    "Money_Saved_INR": 350.96251283409146
  },
  {
    "Date": "2024-09-26 12:03:17.301846",
    "Solar_Irradiance_W/m2": 118.62287810584186,
    "Panel_Temperature_C": 43.362861934188516,
    "Ambient_Temperature_C": 35.07567050793598,
    "Cloud_Cover_%": 70.87656552291543,
    "Energy_Generated_kWh": 113.52786054416407,
    "CO2_Saved_kg": 42.18843621868886,
    "Money_Saved_INR": 681.1671632649844
  },
  {
    "Date": "2024-09-27 12:03:17.301846",
    "Solar_Irradiance_W/m2": 202.4042473330691,
    "Panel_Temperature_C": 37.095095046830224,
    "Ambient_Temperature_C": 33.61324800980471,
    "Cloud_Cover_%": 0.8363681876857099,
    "Energy_Generated_kWh": 61.089862401145375,
    "CO2_Saved_kg": 47.40199859232487,
    "Money_Saved_INR": 366.53917440687223
  },
  {
    "Date": "2024-09-28 12:03:17.301846",
    "Solar_Irradiance_W/m2": 212.98612508607408,
    "Panel_Temperature_C": 31.474940721207957,
    "Ambient_Temperature_C": 25.509628833439336,
    "Cloud_Cover_%": 21.766739958053606,
    "Energy_Generated_kWh": 56.93298978808081,
    "CO2_Saved_kg": 65.98538112096341,
    "Money_Saved_INR": 341.59793872848485
  },
  {
    "Date": "2024-09-29 12:03:17.301846",
    "Solar_Irradiance_W/m2": 154.78416874477958,
    "Panel_Temperature_C": 34.72115461171147,
    "Ambient_Temperature_C": 33.02345781271758,
    "Cloud_Cover_%": 66.16842883998565,
    "Energy_Generated_kWh": 102.74629084729459,
    "CO2_Saved_kg": 58.021284586181196,
    "Money_Saved_INR": 616.4777450837676
  },
  {
    "Date": "2024-09-30 12:03:17.301846",
    "Solar_Irradiance_W/m2": 231.9296229388687,
    "Panel_Temperature_C": 37.791634562608614,
    "Ambient_Temperature_C": 35.60286667659378,
    "Cloud_Cover_%": 48.398936817974715,
    "Energy_Generated_kWh": 86.77105752571829,
    "CO2_Saved_kg": 58.62223511886977,
    "Money_Saved_INR": 520.6263451543098
  },
  {
    "Date": "2024-10-01 12:03:17.301846",
    "Solar_Irradiance_W/m2": 116.923996886552,
    "Panel_Temperature_C": 35.38002695706206,
    "Ambient_Temperature_C": 35.280039308695024,
    "Cloud_Cover_%": 0.5313475668345946,
    "Energy_Generated_kWh": 61.24148846927203,
    "CO2_Saved_kg": 35.837729442073545,
    "Money_Saved_INR": 367.44893081563214
  },
  {
    "Date": "2024-10-02 12:03:17.301846",
    "Solar_Irradiance_W/m2": 196.69601006763418,
    "Panel_Temperature_C": 37.693779962231844,
    "Ambient_Temperature_C": 38.3223936003225,
    "Cloud_Cover_%": 80.44946424318223,
    "Energy_Generated_kWh": 84.33249950809238,
    "CO2_Saved_kg": 38.488462634471304,
    "Money_Saved_INR": 505.9949970485543
  },
  {
    "Date": "2024-10-03 12:03:17.301846",
    "Solar_Irradiance_W/m2": 139.44919001187716,
    "Panel_Temperature_C": 30.39663203460317,
    "Ambient_Temperature_C": 34.958126930407445,
    "Cloud_Cover_%": 77.28095732903374,
    "Energy_Generated_kWh": 59.48494632719445,
    "CO2_Saved_kg": 21.60921340514573,
    "Money_Saved_INR": 356.9096779631667
  },
  {
    "Date": "2024-10-04 12:03:17.301846",
    "Solar_Irradiance_W/m2": 167.40819460989204,
    "Panel_Temperature_C": 35.84680412018039,
    "Ambient_Temperature_C": 32.46013745279108,
    "Cloud_Cover_%": 54.841916299356264,
    "Energy_Generated_kWh": 102.0164279684521,
    "CO2_Saved_kg": 41.90619178917246,
    "Money_Saved_INR": 612.0985678107127
  },
  {
    "Date": "2024-10-05 12:03:17.301846",
    "Solar_Irradiance_W/m2": 202.3699335658207,
    "Panel_Temperature_C": 27.9314275154751,
    "Ambient_Temperature_C": 37.49105166821499,
    "Cloud_Cover_%": 6.646332577627212,
    "Energy_Generated_kWh": 101.22741929746267,
    "CO2_Saved_kg": 59.567031863856585,
    "Money_Saved_INR": 607.364515784776
  },
  {
    "Date": "2024-10-06 12:03:17.301846",
    "Solar_Irradiance_W/m2": 156.9793317358024,
    "Panel_Temperature_C": 34.443869693256495,
    "Ambient_Temperature_C": 29.81435118525658,
    "Cloud_Cover_%": 76.65150495325847,
    "Energy_Generated_kWh": 90.64012397643886,
    "CO2_Saved_kg": 55.16946515748371,
    "Money_Saved_INR": 543.8407438586331
  },
  {
    "Date": "2024-10-07 12:03:17.301846",
    "Solar_Irradiance_W/m2": 180.77222278850874,
    "Panel_Temperature_C": 30.480461792676053,
    "Ambient_Temperature_C": 23.826877441405976,
    "Cloud_Cover_%": 58.37135877313639,
    "Energy_Generated_kWh": 87.23322122494034,
    "CO2_Saved_kg": 47.784867370478764,
    "Money_Saved_INR": 523.399327349642
  },
  {
    "Date": "2024-10-08 12:03:17.301846",
    "Solar_Irradiance_W/m2": 250.31464046072202,
    "Panel_Temperature_C": 31.322350287051165,
    "Ambient_Temperature_C": 28.858531252393654,
    "Cloud_Cover_%": 78.19599771579591,
    "Energy_Generated_kWh": 115.22376249734748,
    "CO2_Saved_kg": 49.77699716281947,
    "Money_Saved_INR": 691.3425749840849
  },
  {
    "Date": "2024-10-09 12:03:17.301846",
    "Solar_Irradiance_W/m2": 171.15540652384257,
    "Panel_Temperature_C": 41.18046587605219,
    "Ambient_Temperature_C": 24.785681486354857,
    "Cloud_Cover_%": 75.17469923958404,
    "Energy_Generated_kWh": 79.99372654776451,
    "CO2_Saved_kg": 43.11114457424594,
    "Money_Saved_INR": 479.96235928658706
  },
  {
    "Date": "2024-10-10 12:03:17.301846",
    "Solar_Irradiance_W/m2": 241.7846056032571,
    "Panel_Temperature_C": 40.45655060297135,
    "Ambient_Temperature_C": 25.27375207517933,
    "Cloud_Cover_%": 80.30020719578371,
    "Energy_Generated_kWh": 56.36251749158397,
    "CO2_Saved_kg": 52.04758882401784,
    "Money_Saved_INR": 338.17510494950386
  },
  {
    "Date": "2024-10-11 12:03:17.301846",
    "Solar_Irradiance_W/m2": 143.5146572671191,
    "Panel_Temperature_C": 38.045690604535885,
    "Ambient_Temperature_C": 28.988369304991377,
    "Cloud_Cover_%": 51.80080664046248,
    "Energy_Generated_kWh": 88.98947825664614,
    "CO2_Saved_kg": 57.65878279480615,
    "Money_Saved_INR": 533.9368695398769
  },
  {
    "Date": "2024-10-12 12:03:17.301846",
    "Solar_Irradiance_W/m2": 226.49020889576414,
    "Panel_Temperature_C": 29.538436176637106,
    "Ambient_Temperature_C": 24.45306055300027,
    "Cloud_Cover_%": 14.032451819351499,
    "Energy_Generated_kWh": 121.72094099074228,
    "CO2_Saved_kg": 33.84113212589527,
    "Money_Saved_INR": 730.3256459444536
  },
  {
    "Date": "2024-10-13 12:03:17.301846",
    "Solar_Irradiance_W/m2": 272.078431032895,
    "Panel_Temperature_C": 33.41795775152599,
    "Ambient_Temperature_C": 27.844269292526718,
    "Cloud_Cover_%": 67.11574733796887,
    "Energy_Generated_kWh": 59.70481013628296,
    "CO2_Saved_kg": 52.99647687837348,
    "Money_Saved_INR": 358.22886081769775
  },
  {
    "Date": "2024-10-14 12:03:17.301846",
    "Solar_Irradiance_W/m2": 76.41777499363553,
    "Panel_Temperature_C": 41.06548849989592,
    "Ambient_Temperature_C": 16.7446973313235,
    "Cloud_Cover_%": 62.04737850519706,
    "Energy_Generated_kWh": 72.77074466612028,
    "CO2_Saved_kg": 59.32434870954667,
    "Money_Saved_INR": 436.6244679967217
  },
  {
    "Date": "2024-10-15 12:03:17.301846",
    "Solar_Irradiance_W/m2": 160.15523722647617,
    "Panel_Temperature_C": 35.70858456819953,
    "Ambient_Temperature_C": 31.49305595161057,
    "Cloud_Cover_%": 74.22531871990871,
    "Energy_Generated_kWh": 88.32892076202906,
    "CO2_Saved_kg": 45.848997110366305,
    "Money_Saved_INR": 529.9735245721744
  },
  {
    "Date": "2024-10-16 12:03:17.301846",
    "Solar_Irradiance_W/m2": 228.853606359027,
    "Panel_Temperature_C": 46.59664769990847,
    "Ambient_Temperature_C": 30.00843832753557,
    "Cloud_Cover_%": 16.98810060507353,
    "Energy_Generated_kWh": 78.92190301988522,
    "CO2_Saved_kg": 57.00700612120583,
    "Money_Saved_INR": 473.5314181193113
  },
  {
    "Date": "2024-10-17 12:03:17.301846",
    "Solar_Irradiance_W/m2": 189.84773069785035,
    "Panel_Temperature_C": 36.96658919697186,
    "Ambient_Temperature_C": 24.280379582522666,
    "Cloud_Cover_%": 19.497519990028923,
    "Energy_Generated_kWh": 60.35392839245371,
    "CO2_Saved_kg": 78.14654444472552,
    "Money_Saved_INR": 362.12357035472223
  },
  {
    "Date": "2024-10-18 12:03:17.301846",
    "Solar_Irradiance_W/m2": 218.55729366856545,
    "Panel_Temperature_C": 35.960245582450156,
    "Ambient_Temperature_C": 34.614719679026834,
    "Cloud_Cover_%": 89.04095172193284,
    "Energy_Generated_kWh": 102.43715712460941,
    "CO2_Saved_kg": 48.95657207013108,
    "Money_Saved_INR": 614.6229427476565
  },
  {
    "Date": "2024-10-19 12:03:17.301846",
    "Solar_Irradiance_W/m2": 169.80074066420897,
    "Panel_Temperature_C": 33.4544176789875,
    "Ambient_Temperature_C": 36.56299096338591,
    "Cloud_Cover_%": 74.99777984520708,
    "Energy_Generated_kWh": 126.40081444034519,
    "CO2_Saved_kg": 53.93307050005323,
    "Money_Saved_INR": 758.4048866420711
  },
  {
    "Date": "2024-10-20 12:03:17.301846",
    "Solar_Irradiance_W/m2": 204.329489373645,
    "Panel_Temperature_C": 35.66770452391141,
    "Ambient_Temperature_C": 18.74708094941718,
    "Cloud_Cover_%": 90.82284887003229,
    "Energy_Generated_kWh": 83.92262918047814,
    "CO2_Saved_kg": 42.61942916338609,
    "Money_Saved_INR": 503.53577508286884
  },
  {
    "Date": "2024-10-21 12:03:17.301846",
    "Solar_Irradiance_W/m2": 192.216138230396,
    "Panel_Temperature_C": 34.23765081809728,
    "Ambient_Temperature_C": 24.6609265500365,
    "Cloud_Cover_%": 75.87153211639207,
    "Energy_Generated_kWh": 61.91863420527999,
    "CO2_Saved_kg": 51.8125116260205,
    "Money_Saved_INR": 371.51180523167994
  },
  {
    "Date": "2024-10-22 12:03:17.301846",
    "Solar_Irradiance_W/m2": 258.38910308299035,
    "Panel_Temperature_C": 38.54054338344295,
    "Ambient_Temperature_C": 24.616003551488912,
    "Cloud_Cover_%": 59.71553059903019,
    "Energy_Generated_kWh": 49.0207894989305,
    "CO2_Saved_kg": 54.60271624982304,
    "Money_Saved_INR": 294.124736993583
  },
  {
    "Date": "2024-10-23 12:03:17.301846",
    "Solar_Irradiance_W/m2": 212.72104216506065,
    "Panel_Temperature_C": 39.783511583972924,
    "Ambient_Temperature_C": 23.420678292237948,
    "Cloud_Cover_%": 65.41327370278736,
    "Energy_Generated_kWh": 85.15951962442362,
    "CO2_Saved_kg": 51.94842340270138,
    "Money_Saved_INR": 510.9571177465417
  },
  {
    "Date": "2024-10-24 12:03:17.301846",
    "Solar_Irradiance_W/m2": 216.8801331037601,
    "Panel_Temperature_C": 31.070052697460252,
    "Ambient_Temperature_C": 35.80632389352224,
    "Cloud_Cover_%": 88.91279239400099,
    "Energy_Generated_kWh": 102.07754686632515,
    "CO2_Saved_kg": 39.80304680291143,
    "Money_Saved_INR": 612.4652811979508
  },
  {
    "Date": "2024-10-25 12:03:17.301846",
    "Solar_Irradiance_W/m2": 179.40615169387664,
    "Panel_Temperature_C": 28.34383523221111,
    "Ambient_Temperature_C": 28.643217028590374,
    "Cloud_Cover_%": 57.88067545119405,
    "Energy_Generated_kWh": 89.50335492990763,
    "CO2_Saved_kg": 52.06361771325451,
    "Money_Saved_INR": 537.0201295794458
  },
  {
    "Date": "2024-10-26 12:03:17.301846",
    "Solar_Irradiance_W/m2": 175.61968879637533,
    "Panel_Temperature_C": 25.818973134483517,
    "Ambient_Temperature_C": 28.148396110825725,
    "Cloud_Cover_%": 63.239132432838744,
    "Energy_Generated_kWh": 79.95192318162292,
    "CO2_Saved_kg": 64.62195938717636,
    "Money_Saved_INR": 479.71153908973747
  },
  {
    "Date": "2024-10-27 12:03:17.301846",
    "Solar_Irradiance_W/m2": 178.37209060901895,
    "Panel_Temperature_C": 37.53995663456272,
    "Ambient_Temperature_C": 15.972963449152726,
    "Cloud_Cover_%": 15.647671600360058,
    "Energy_Generated_kWh": 68.21456696421387,
    "CO2_Saved_kg": 54.486357645145276,
    "Money_Saved_INR": 409.28740178528324
  },
  {
    "Date": "2024-10-28 12:03:17.301846",
    "Solar_Irradiance_W/m2": 219.72260711891485,
    "Panel_Temperature_C": 29.483166969130632,
    "Ambient_Temperature_C": 34.44792621146458,
    "Cloud_Cover_%": 47.39212201161027,
    "Energy_Generated_kWh": 58.1567273456382,
    "CO2_Saved_kg": 59.619871890718414,
    "Money_Saved_INR": 348.9403640738292
  },
  {
    "Date": "2024-10-29 12:03:17.301846",
    "Solar_Irradiance_W/m2": 178.95077595898687,
    "Panel_Temperature_C": 24.235547035237587,
    "Ambient_Temperature_C": 21.32519123602569,
    "Cloud_Cover_%": 71.6397111958099,
    "Energy_Generated_kWh": 96.69502652649764,
    "CO2_Saved_kg": 47.629880299873726,
    "Money_Saved_INR": 580.1701591589858
  },
  {
    "Date": "2024-10-30 12:03:17.301846",
    "Solar_Irradiance_W/m2": 214.48874284482065,
    "Panel_Temperature_C": 36.94289302265482,
    "Ambient_Temperature_C": 30.4195284118643,
    "Cloud_Cover_%": 27.09426983163654,
    "Energy_Generated_kWh": 98.2754324277117,
    "CO2_Saved_kg": 57.4990023942371,
    "Money_Saved_INR": 589.6525945662702
  },
  {
    "Date": "2024-10-31 12:03:17.301846",
    "Solar_Irradiance_W/m2": 303.77003993227197,
    "Panel_Temperature_C": 47.46499758716395,
    "Ambient_Temperature_C": 31.941638565707343,
    "Cloud_Cover_%": 20.22541805245349,
    "Energy_Generated_kWh": 49.085404266185336,
    "CO2_Saved_kg": 52.792678382165256,
    "Money_Saved_INR": 294.51242559711204
  },
  {
    "Date": "2024-11-01 12:03:17.301846",
    "Solar_Irradiance_W/m2": 243.5562351715846,
    "Panel_Temperature_C": 34.96964544230053,
    "Ambient_Temperature_C": 39.52461017087056,
    "Cloud_Cover_%": 31.382680822441557,
    "Energy_Generated_kWh": 111.79677956361368,
    "CO2_Saved_kg": 40.49089270312768,
    "Money_Saved_INR": 670.7806773816822
  },
  {
    "Date": "2024-11-02 12:03:17.301846",
    "Solar_Irradiance_W/m2": 183.69882339160793,
    "Panel_Temperature_C": 39.19245387225821,
    "Ambient_Temperature_C": 20.838257206166215,
    "Cloud_Cover_%": 24.150062799283344,
    "Energy_Generated_kWh": 91.48142441788002,
    "CO2_Saved_kg": 53.18521004798875,
    "Money_Saved_INR": 548.8885465072801
  },
  {
    "Date": "2024-11-03 12:03:17.301846",
    "Solar_Irradiance_W/m2": 260.06069610819725,
    "Panel_Temperature_C": 35.40914679273782,
    "Ambient_Temperature_C": 8.863414909254224,
    "Cloud_Cover_%": 21.491263703639586,
    "Energy_Generated_kWh": 107.99189290291586,
    "CO2_Saved_kg": 40.0830333655969,
    "Money_Saved_INR": 647.9513574174952
  },
  {
    "Date": "2024-11-04 12:03:17.301846",
    "Solar_Irradiance_W/m2": 179.59623134892243,
    "Panel_Temperature_C": 34.50555173404429,
    "Ambient_Temperature_C": 31.286946813275865,
    "Cloud_Cover_%": 42.48508428680869,
    "Energy_Generated_kWh": 53.157445030297694,
    "CO2_Saved_kg": 43.67119725115208,
    "Money_Saved_INR": 318.94467018178614
  },
  {
    "Date": "2024-11-05 12:03:17.301846",
    "Solar_Irradiance_W/m2": 98.0937732411073,
    "Panel_Temperature_C": 39.59538241493884,
    "Ambient_Temperature_C": 42.60357827057598,
    "Cloud_Cover_%": 90.78385138835341,
    "Energy_Generated_kWh": 52.68351689169123,
    "CO2_Saved_kg": 51.893283072923744,
    "Money_Saved_INR": 316.10110135014736
  },
  {
    "Date": "2024-11-06 12:03:17.301846",
    "Solar_Irradiance_W/m2": 149.5956844541298,
    "Panel_Temperature_C": 33.548627279056745,
    "Ambient_Temperature_C": 38.67262447057606,
    "Cloud_Cover_%": 50.705964673871826,
    "Energy_Generated_kWh": 77.02061380465406,
    "CO2_Saved_kg": 52.97244273380124,
    "Money_Saved_INR": 462.12368282792437
  },
  {
    "Date": "2024-11-07 12:03:17.301846",
    "Solar_Irradiance_W/m2": 106.46040394870721,
    "Panel_Temperature_C": 36.33696157035951,
    "Ambient_Temperature_C": 31.46761590692238,
    "Cloud_Cover_%": 18.792038081532304,
    "Energy_Generated_kWh": 90.05568853790388,
    "CO2_Saved_kg": 38.10767534922871,
    "Money_Saved_INR": 540.3341312274233
  },
  {
    "Date": "2024-11-08 12:03:17.301846",
    "Solar_Irradiance_W/m2": 182.42432579793456,
    "Panel_Temperature_C": 36.60848903098007,
    "Ambient_Temperature_C": 26.55854670057567,
    "Cloud_Cover_%": 7.697166938087408,
    "Energy_Generated_kWh": 115.92721645853928,
    "CO2_Saved_kg": 60.53985771182876,
    "Money_Saved_INR": 695.5632987512356
  },
  {
    "Date": "2024-11-09 12:03:17.301846",
    "Solar_Irradiance_W/m2": 200.92091895947758,
    "Panel_Temperature_C": 31.659547731784755,
    "Ambient_Temperature_C": 35.64985817646117,
    "Cloud_Cover_%": 69.61561451379252,
    "Energy_Generated_kWh": 94.12157827630263,
    "CO2_Saved_kg": 55.72006278300473,
    "Money_Saved_INR": 564.7294696578158
  },
  {
    "Date": "2024-11-10 12:03:17.301846",
    "Solar_Irradiance_W/m2": 283.82186561376415,
    "Panel_Temperature_C": 39.960211747682614,
    "Ambient_Temperature_C": 23.18517660206872,
    "Cloud_Cover_%": 38.279876443638784,
    "Energy_Generated_kWh": 75.14637446375933,
    "CO2_Saved_kg": 42.95271564389116,
    "Money_Saved_INR": 450.87824678255595
  },
  {
    "Date": "2024-11-11 12:03:17.301846",
    "Solar_Irradiance_W/m2": 216.34636868820814,
    "Panel_Temperature_C": 34.12520121652296,
    "Ambient_Temperature_C": 33.33450438549353,
    "Cloud_Cover_%": 82.18309465853592,
    "Energy_Generated_kWh": 59.47261584668216,
    "CO2_Saved_kg": 34.624152035508246,
    "Money_Saved_INR": 356.83569508009293
  },
  {
    "Date": "2024-11-12 12:03:17.301846",
    "Solar_Irradiance_W/m2": 189.04497355955678,
    "Panel_Temperature_C": 31.221274202535778,
    "Ambient_Temperature_C": 33.53829111416639,
    "Cloud_Cover_%": 65.95107686407702,
    "Energy_Generated_kWh": 104.60001145438301,
    "CO2_Saved_kg": 48.55095420918569,
    "Money_Saved_INR": 627.6000687262981
  },
  {
    "Date": "2024-11-13 12:03:17.301846",
    "Solar_Irradiance_W/m2": 241.47027905917446,
    "Panel_Temperature_C": 37.68254921785202,
    "Ambient_Temperature_C": 37.42146935249216,
    "Cloud_Cover_%": 79.62414505413685,
    "Energy_Generated_kWh": 60.7058914849857,
    "CO2_Saved_kg": 45.540562861388395,
    "Money_Saved_INR": 364.2353489099142
  },
  {
    "Date": "2024-11-14 12:03:17.301846",
    "Solar_Irradiance_W/m2": 89.44323454960575,
    "Panel_Temperature_C": 30.507660091044812,
    "Ambient_Temperature_C": 49.31762027237754,
    "Cloud_Cover_%": 27.194603941844875,
    "Energy_Generated_kWh": 112.56937109544643,
    "CO2_Saved_kg": 51.13140457053023,
    "Money_Saved_INR": 675.4162265726786
  },
  {
    "Date": "2024-11-15 12:03:17.301846",
    "Solar_Irradiance_W/m2": 211.7807279054283,
    "Panel_Temperature_C": 35.14090578684564,
    "Ambient_Temperature_C": 32.74691177025137,
    "Cloud_Cover_%": 69.2358922461058,
    "Energy_Generated_kWh": 74.31230700786982,
    "CO2_Saved_kg": 46.36883338844434,
    "Money_Saved_INR": 445.8738420472189
  },
  {
    "Date": "2024-11-16 12:03:17.301846",
    "Solar_Irradiance_W/m2": 238.54325969434834,
    "Panel_Temperature_C": 34.954405016778985,
    "Ambient_Temperature_C": 26.437254620047508,
    "Cloud_Cover_%": 26.406198469371876,
    "Energy_Generated_kWh": 111.81164145235701,
    "CO2_Saved_kg": 29.925431392549903,
    "Money_Saved_INR": 670.8698487141421
  },
  {
    "Date": "2024-11-17 12:03:17.301846",
    "Solar_Irradiance_W/m2": 126.07068771100792,
    "Panel_Temperature_C": 40.42947782915789,
    "Ambient_Temperature_C": 29.820979814656038,
    "Cloud_Cover_%": 93.90684794502916,
    "Energy_Generated_kWh": 93.57862580118557,
    "CO2_Saved_kg": 46.11653061698841,
    "Money_Saved_INR": 561.4717548071134
  },
  {
    "Date": "2024-11-18 12:03:17.301846",
    "Solar_Irradiance_W/m2": 257.1877021603465,
    "Panel_Temperature_C": 37.373491164399766,
    "Ambient_Temperature_C": 17.61646866577617,
    "Cloud_Cover_%": 63.63742815333744,
    "Energy_Generated_kWh": 77.26009021115084,
    "CO2_Saved_kg": 46.94380888931687,
    "Money_Saved_INR": 463.56054126690503
  },
  {
    "Date": "2024-11-19 12:03:17.301846",
    "Solar_Irradiance_W/m2": 216.9248203747207,
    "Panel_Temperature_C": 34.87486520627428,
    "Ambient_Temperature_C": 25.137008082376592,
    "Cloud_Cover_%": 32.451180017534206,
    "Energy_Generated_kWh": 69.61207256347747,
    "CO2_Saved_kg": 56.33661024774059,
    "Money_Saved_INR": 417.67243538086484
  },
  {
    "Date": "2024-11-20 12:03:17.301846",
    "Solar_Irradiance_W/m2": 179.23560430495994,
    "Panel_Temperature_C": 39.08883149600143,
    "Ambient_Temperature_C": 27.135022933208273,
    "Cloud_Cover_%": 26.951186229227265,
    "Energy_Generated_kWh": 73.1818424530784,
    "CO2_Saved_kg": 43.0180032538895,
    "Money_Saved_INR": 439.09105471847045
  },
  {
    "Date": "2024-11-21 12:03:17.301846",
    "Solar_Irradiance_W/m2": 231.63909330531425,
    "Panel_Temperature_C": 41.951037745086566,
    "Ambient_Temperature_C": 26.331381214457853,
    "Cloud_Cover_%": 19.09265850716435,
    "Energy_Generated_kWh": 88.56633384750475,
    "CO2_Saved_kg": 66.78674673372566,
    "Money_Saved_INR": 531.3980030850284
  },
  {
    "Date": "2024-11-22 12:03:17.301846",
    "Solar_Irradiance_W/m2": 313.5346428902198,
    "Panel_Temperature_C": 37.78905153175931,
    "Ambient_Temperature_C": 31.066484104236054,
    "Cloud_Cover_%": 69.46409588937279,
    "Energy_Generated_kWh": 81.54312992435433,
    "CO2_Saved_kg": 30.88359449348243,
    "Money_Saved_INR": 489.258779546126
  },
  {
    "Date": "2024-11-23 12:03:17.301846",
    "Solar_Irradiance_W/m2": 209.09331275292476,
    "Panel_Temperature_C": 35.051763099216906,
    "Ambient_Temperature_C": 24.243060473324597,
    "Cloud_Cover_%": 21.87156129979273,
    "Energy_Generated_kWh": 68.1237718386259,
    "CO2_Saved_kg": 63.111674978026244,
    "Money_Saved_INR": 408.7426310317554
  },
  {
    "Date": "2024-11-24 12:03:17.301846",
    "Solar_Irradiance_W/m2": 212.4110293150168,
    "Panel_Temperature_C": 28.4408188382492,
    "Ambient_Temperature_C": 37.8472146712713,
    "Cloud_Cover_%": 59.53032659274891,
    "Energy_Generated_kWh": 76.68737179364736,
    "CO2_Saved_kg": 47.756810291218954,
    "Money_Saved_INR": 460.1242307618842
  },
  {
    "Date": "2024-11-25 12:03:17.301846",
    "Solar_Irradiance_W/m2": 177.0319550229878,
    "Panel_Temperature_C": 29.674431684623137,
    "Ambient_Temperature_C": 30.00144945442738,
    "Cloud_Cover_%": 26.463502692535734,
    "Energy_Generated_kWh": 81.571540594383,
    "CO2_Saved_kg": 58.595848723435566,
    "Money_Saved_INR": 489.42924356629794
  },
  {
    "Date": "2024-11-26 12:03:17.301846",
    "Solar_Irradiance_W/m2": 157.50778152676043,
    "Panel_Temperature_C": 33.473876478226664,
    "Ambient_Temperature_C": 29.9348977520297,
    "Cloud_Cover_%": 66.19689447938686,
    "Energy_Generated_kWh": 37.42531811170376,
    "CO2_Saved_kg": 50.79801484058733,
    "Money_Saved_INR": 224.55190867022256
  },
  {
    "Date": "2024-11-27 12:03:17.301846",
    "Solar_Irradiance_W/m2": 241.51679082721228,
    "Panel_Temperature_C": 31.952438989203586,
    "Ambient_Temperature_C": 27.704736984409575,
    "Cloud_Cover_%": 81.49397285405392,
    "Energy_Generated_kWh": 89.16336229577398,
    "CO2_Saved_kg": 61.39555536025469,
    "Money_Saved_INR": 534.9801737746438
  },
  {
    "Date": "2024-11-28 12:03:17.301846",
    "Solar_Irradiance_W/m2": 157.19580870455664,
    "Panel_Temperature_C": 34.06514348507277,
    "Ambient_Temperature_C": 31.086334787012852,
    "Cloud_Cover_%": 77.80252431446532,
    "Energy_Generated_kWh": 60.40557550566386,
    "CO2_Saved_kg": 46.12638035447189,
    "Money_Saved_INR": 362.43345303398314
  },
  {
    "Date": "2024-11-29 12:03:17.301846",
    "Solar_Irradiance_W/m2": 203.57831186096962,
    "Panel_Temperature_C": 35.283249624485535,
    "Ambient_Temperature_C": 35.77568785267344,
    "Cloud_Cover_%": 76.08513309307817,
    "Energy_Generated_kWh": 56.9333519358851,
    "CO2_Saved_kg": 39.01379574822188,
    "Money_Saved_INR": 341.6001116153106
  },
  {
    "Date": "2024-11-30 12:03:17.301846",
    "Solar_Irradiance_W/m2": 176.11712766174418,
    "Panel_Temperature_C": 37.64846377178365,
    "Ambient_Temperature_C": 23.9300884900237,
    "Cloud_Cover_%": 18.772240569225207,
    "Energy_Generated_kWh": 46.2531130577858,
    "CO2_Saved_kg": 64.20504287271064,
    "Money_Saved_INR": 277.51867834671475
  },
  {
    "Date": "2024-12-01 12:03:17.301846",
    "Solar_Irradiance_W/m2": 223.9489912873196,
    "Panel_Temperature_C": 34.647506109704544,
    "Ambient_Temperature_C": 25.393184576473203,
    "Cloud_Cover_%": 8.838494698451871,
    "Energy_Generated_kWh": 44.1221500426422,
    "CO2_Saved_kg": 48.86519354117859,
    "Money_Saved_INR": 264.73290025585317
  },
  {
    "Date": "2024-12-02 12:03:17.301846",
    "Solar_Irradiance_W/m2": 216.6831052643474,
    "Panel_Temperature_C": 37.43250821913101,
    "Ambient_Temperature_C": 27.873917798563348,
    "Cloud_Cover_%": 69.89488284873856,
    "Energy_Generated_kWh": 52.89104993775422,
    "CO2_Saved_kg": 52.21558473624211,
    "Money_Saved_INR": 317.3462996265253
  },
  {
    "Date": "2024-12-03 12:03:17.301846",
    "Solar_Irradiance_W/m2": 251.87699721289496,
    "Panel_Temperature_C": 35.3223720740506,
    "Ambient_Temperature_C": 20.578903535687495,
    "Cloud_Cover_%": 36.83472137943513,
    "Energy_Generated_kWh": 65.8195808473902,
    "CO2_Saved_kg": 62.34751914044795,
    "Money_Saved_INR": 394.9174850843412
  },
  {
    "Date": "2024-12-04 12:03:17.301846",
    "Solar_Irradiance_W/m2": 174.49918005726266,
    "Panel_Temperature_C": 25.12266716823064,
    "Ambient_Temperature_C": 24.265194981949517,
    "Cloud_Cover_%": 43.23462264033473,
    "Energy_Generated_kWh": 119.06518275053136,
    "CO2_Saved_kg": 39.68044757905565,
    "Money_Saved_INR": 714.3910965031882
  },
  {
    "Date": "2024-12-05 12:03:17.301846",
    "Solar_Irradiance_W/m2": 186.50625323533143,
    "Panel_Temperature_C": 30.303323030906228,
    "Ambient_Temperature_C": 26.666453885187387,
    "Cloud_Cover_%": 3.1149092793391064,
    "Energy_Generated_kWh": 69.48240648209593,
    "CO2_Saved_kg": 55.95490897639257,
    "Money_Saved_INR": 416.8944388925755
  },
  {
    "Date": "2024-12-06 12:03:17.301846",
    "Solar_Irradiance_W/m2": 151.06181421088462,
    "Panel_Temperature_C": 34.27956222139192,
    "Ambient_Temperature_C": 36.12072426498909,
    "Cloud_Cover_%": 25.95764492750492,
    "Energy_Generated_kWh": 83.55500212536063,
    "CO2_Saved_kg": 44.10105243537109,
    "Money_Saved_INR": 501.3300127521638
  },
  {
    "Date": "2024-12-07 12:03:17.301846",
    "Solar_Irradiance_W/m2": 177.78533699619442,
    "Panel_Temperature_C": 28.95152628579446,
    "Ambient_Temperature_C": 31.837929303013475,
    "Cloud_Cover_%": 3.3676403874464023,
    "Energy_Generated_kWh": 88.00962773012657,
    "CO2_Saved_kg": 48.67830644355628,
    "Money_Saved_INR": 528.0577663807594
  },
  {
    "Date": "2024-12-08 12:03:17.301846",
    "Solar_Irradiance_W/m2": 218.8650246522426,
    "Panel_Temperature_C": 37.999643649981024,
    "Ambient_Temperature_C": 31.355129379572812,
    "Cloud_Cover_%": 87.91857726012476,
    "Energy_Generated_kWh": 82.62130372431697,
    "CO2_Saved_kg": 50.72278965384289,
    "Money_Saved_INR": 495.7278223459018
  },
  {
    "Date": "2024-12-09 12:03:17.301846",
    "Solar_Irradiance_W/m2": 237.8494308322676,
    "Panel_Temperature_C": 42.65375416171849,
    "Ambient_Temperature_C": 35.956285735175804,
    "Cloud_Cover_%": 24.339668321853047,
    "Energy_Generated_kWh": 78.45113078548013,
    "CO2_Saved_kg": 34.997781385530644,
    "Money_Saved_INR": 470.7067847128808
  },
  {
    "Date": "2024-12-10 12:03:17.301846",
    "Solar_Irradiance_W/m2": 153.89173379111872,
    "Panel_Temperature_C": 41.09380925848659,
    "Ambient_Temperature_C": 29.038397481204225,
    "Cloud_Cover_%": 55.73371695730081,
    "Energy_Generated_kWh": 56.0941247280151,
    "CO2_Saved_kg": 42.211629571795655,
    "Money_Saved_INR": 336.5647483680906
  },
  {
    "Date": "2024-12-11 12:03:17.301846",
    "Solar_Irradiance_W/m2": 243.480296005283,
    "Panel_Temperature_C": 33.93278564534896,
    "Ambient_Temperature_C": 32.73325394950223,
    "Cloud_Cover_%": 3.897932066113041,
    "Energy_Generated_kWh": 109.01855096558424,
    "CO2_Saved_kg": 63.51072892413139,
    "Money_Saved_INR": 654.1113057935054
  },
  {
    "Date": "2024-12-12 12:03:17.301846",
    "Solar_Irradiance_W/m2": 267.78189294024753,
    "Panel_Temperature_C": 42.45363068424976,
    "Ambient_Temperature_C": 29.277447729472527,
    "Cloud_Cover_%": 66.6847391305658,
    "Energy_Generated_kWh": 116.1439328727577,
    "CO2_Saved_kg": 58.86191188584796,
    "Money_Saved_INR": 696.8635972365462
  },
  {
    "Date": "2024-12-13 12:03:17.301846",
    "Solar_Irradiance_W/m2": 220.67174516118504,
    "Panel_Temperature_C": 35.74333728601056,
    "Ambient_Temperature_C": 31.8575364457974,
    "Cloud_Cover_%": 32.30273457540939,
    "Energy_Generated_kWh": 46.346826117546286,
    "CO2_Saved_kg": 49.37360422672765,
    "Money_Saved_INR": 278.0809567052777
  },
  {
    "Date": "2024-12-14 12:03:17.301846",
    "Solar_Irradiance_W/m2": 293.8397906279033,
    "Panel_Temperature_C": 33.31457014440981,
    "Ambient_Temperature_C": 25.920689396718927,
    "Cloud_Cover_%": 89.79191869576658,
    "Energy_Generated_kWh": 59.51942818227241,
    "CO2_Saved_kg": 52.431234585128934,
    "Money_Saved_INR": 357.11656909363444
  },
  {
    "Date": "2024-12-15 12:03:17.301846",
    "Solar_Irradiance_W/m2": 161.31054004482135,
    "Panel_Temperature_C": 31.9329866822953,
    "Ambient_Temperature_C": 12.928279892064996,
    "Cloud_Cover_%": 88.81181889340358,
    "Energy_Generated_kWh": 74.40379315245988,
    "CO2_Saved_kg": 47.05757494363542,
    "Money_Saved_INR": 446.4227589147593
  },
  {
    "Date": "2024-12-16 12:03:17.301846",
    "Solar_Irradiance_W/m2": 137.76726483442914,
    "Panel_Temperature_C": 33.48765156755936,
    "Ambient_Temperature_C": 29.060045864695873,
    "Cloud_Cover_%": 32.529061836174776,
    "Energy_Generated_kWh": 60.70924410179617,
    "CO2_Saved_kg": 63.56583385827982,
    "Money_Saved_INR": 364.25546461077704
  },
  {
    "Date": "2024-12-17 12:03:17.301846",
    "Solar_Irradiance_W/m2": 111.06398755478607,
    "Panel_Temperature_C": 33.05911590729386,
    "Ambient_Temperature_C": 39.959236952699584,
    "Cloud_Cover_%": 90.09608956904678,
    "Energy_Generated_kWh": 90.1193110691173,
    "CO2_Saved_kg": 47.99647422205836,
    "Money_Saved_INR": 540.7158664147038
  },
  {
    "Date": "2024-12-18 12:03:17.301846",
    "Solar_Irradiance_W/m2": 274.8022155744592,
    "Panel_Temperature_C": 35.85208111187744,
    "Ambient_Temperature_C": 36.48350781569115,
    "Cloud_Cover_%": 99.61576734987788,
    "Energy_Generated_kWh": 65.43455595186774,
    "CO2_Saved_kg": 52.31842092134848,
    "Money_Saved_INR": 392.6073357112064
  },
  {
    "Date": "2024-12-19 12:03:17.301846",
    "Solar_Irradiance_W/m2": 232.71828281770289,
    "Panel_Temperature_C": 35.802869905249324,
    "Ambient_Temperature_C": 36.757782392138196,
    "Cloud_Cover_%": 82.5415664123948,
    "Energy_Generated_kWh": 123.30112135613206,
    "CO2_Saved_kg": 61.460301441420654,
    "Money_Saved_INR": 739.8067281367923
  },
  {
    "Date": "2024-12-20 12:03:17.301846",
    "Solar_Irradiance_W/m2": 197.22076645447726,
    "Panel_Temperature_C": 35.01523010076707,
    "Ambient_Temperature_C": 38.65291505264352,
    "Cloud_Cover_%": 84.4871347755229,
    "Energy_Generated_kWh": 103.81097188687193,
    "CO2_Saved_kg": 42.226285151540935,
    "Money_Saved_INR": 622.8658313212316
  },
  {
    "Date": "2024-12-21 12:03:17.301846",
    "Solar_Irradiance_W/m2": 213.998431315991,
    "Panel_Temperature_C": 37.18469084873175,
    "Ambient_Temperature_C": 30.62060313673006,
    "Cloud_Cover_%": 24.90087361090899,
    "Energy_Generated_kWh": 84.2514806126443,
    "CO2_Saved_kg": 65.58789184496894,
    "Money_Saved_INR": 505.50888367586583
  },
  {
    "Date": "2024-12-22 12:03:17.301846",
    "Solar_Irradiance_W/m2": 143.72554763508117,
    "Panel_Temperature_C": 40.95323137393171,
    "Ambient_Temperature_C": 31.381209951839168,
    "Cloud_Cover_%": 57.67023988577563,
    "Energy_Generated_kWh": 100.53972526639464,
    "CO2_Saved_kg": 34.69538590256623,
    "Money_Saved_INR": 603.2383515983679
  },
  {
    "Date": "2024-12-23 12:03:17.301846",
    "Solar_Irradiance_W/m2": 322.2875989808413,
    "Panel_Temperature_C": 39.74777067720662,
    "Ambient_Temperature_C": 25.676436731959548,
    "Cloud_Cover_%": 6.725591396736785,
    "Energy_Generated_kWh": 102.11800848714617,
    "CO2_Saved_kg": 66.29642131112799,
    "Money_Saved_INR": 612.708050922877
  },
  {
    "Date": "2024-12-24 12:03:17.301846",
    "Solar_Irradiance_W/m2": 206.46105909876138,
    "Panel_Temperature_C": 27.575510157750482,
    "Ambient_Temperature_C": 27.787490007810653,
    "Cloud_Cover_%": 9.491793682166971,
    "Energy_Generated_kWh": 68.72105023883513,
    "CO2_Saved_kg": 46.27324416048025,
    "Money_Saved_INR": 412.3263014330108
  },
  {
    "Date": "2024-12-25 12:03:17.301846",
    "Solar_Irradiance_W/m2": 205.46973973024464,
    "Panel_Temperature_C": 22.230394325490224,
    "Ambient_Temperature_C": 34.31039804839799,
    "Cloud_Cover_%": 99.88926120332906,
    "Energy_Generated_kWh": 63.6756551091607,
    "CO2_Saved_kg": 47.57301252174718,
    "Money_Saved_INR": 382.05393065496423
  },
  {
    "Date": "2024-12-26 12:03:17.301846",
    "Solar_Irradiance_W/m2": 236.28833119493459,
    "Panel_Temperature_C": 39.67159955619637,
    "Ambient_Temperature_C": 38.42719106018171,
    "Cloud_Cover_%": 32.663924942591095,
    "Energy_Generated_kWh": 81.56286125939295,
    "CO2_Saved_kg": 31.09989828817057,
    "Money_Saved_INR": 489.3771675563577
  },
  {
    "Date": "2024-12-27 12:03:17.301846",
    "Solar_Irradiance_W/m2": 224.05046158683567,
    "Panel_Temperature_C": 28.165606507922895,
    "Ambient_Temperature_C": 29.023876070233005,
    "Cloud_Cover_%": 74.81839120488463,
    "Energy_Generated_kWh": 97.23272248995889,
    "CO2_Saved_kg": 45.452052826223074,
    "Money_Saved_INR": 583.3963349397534
  },
  {
    "Date": "2024-12-28 12:03:17.301846",
    "Solar_Irradiance_W/m2": 211.19420121395657,
    "Panel_Temperature_C": 33.87617299053658,
    "Ambient_Temperature_C": 26.84867514604012,
    "Cloud_Cover_%": 80.66650530268164,
    "Energy_Generated_kWh": 82.78120797306835,
    "CO2_Saved_kg": 39.60193468973116,
    "Money_Saved_INR": 496.6872478384101
  },
  {
    "Date": "2024-12-29 12:03:17.301846",
    "Solar_Irradiance_W/m2": 160.4762772277344,
    "Panel_Temperature_C": 29.149434869703203,
    "Ambient_Temperature_C": 30.00369571199618,
    "Cloud_Cover_%": 85.80232710072292,
    "Energy_Generated_kWh": 48.460070356180054,
    "CO2_Saved_kg": 43.923536546265275,
    "Money_Saved_INR": 290.76042213708035
  },
  {
    "Date": "2024-12-30 12:03:17.301846",
    "Solar_Irradiance_W/m2": 223.57341785679978,
    "Panel_Temperature_C": 25.9900978120999,
    "Ambient_Temperature_C": 34.2084472425038,
    "Cloud_Cover_%": 99.76282974021565,
    "Energy_Generated_kWh": 63.94351112098315,
    "CO2_Saved_kg": 48.6268903421112,
    "Money_Saved_INR": 383.66106672589893
  },
  {
    "Date": "2024-12-31 12:03:17.301846",
    "Solar_Irradiance_W/m2": 294.1012248237517,
    "Panel_Temperature_C": 37.70731364102394,
    "Ambient_Temperature_C": 19.89301628706521,
    "Cloud_Cover_%": 24.149648525686786,
    "Energy_Generated_kWh": 78.52054272811245,
    "CO2_Saved_kg": 59.57791614472906,
    "Money_Saved_INR": 471.1232563686747
  },
  {
    "Date": "2025-01-01 12:03:17.301846",
    "Solar_Irradiance_W/m2": 267.27100230774886,
    "Panel_Temperature_C": 38.79577580151324,
    "Ambient_Temperature_C": 13.926733328039333,
    "Cloud_Cover_%": 4.035082685969971,
    "Energy_Generated_kWh": 78.4866879134834,
    "CO2_Saved_kg": 52.076033514006255,
    "Money_Saved_INR": 470.92012748090036
  },
  {
    "Date": "2025-01-02 12:03:17.301846",
    "Solar_Irradiance_W/m2": 279.65933133196984,
    "Panel_Temperature_C": 32.1174479963664,
    "Ambient_Temperature_C": 26.146242053558915,
    "Cloud_Cover_%": 41.1191517994586,
    "Energy_Generated_kWh": 119.45084353579617,
    "CO2_Saved_kg": 53.07676653401114,
    "Money_Saved_INR": 716.7050612147771
  },
  {
    "Date": "2025-01-03 12:03:17.301846",
    "Solar_Irradiance_W/m2": 174.43921617844074,
    "Panel_Temperature_C": 22.04478853927545,
    "Ambient_Temperature_C": 21.455013018600887,
    "Cloud_Cover_%": 13.008066982894695,
    "Energy_Generated_kWh": 52.28024115202004,
    "CO2_Saved_kg": 39.044806111544375,
    "Money_Saved_INR": 313.68144691212024
  },
  {
    "Date": "2025-01-04 12:03:17.301846",
    "Solar_Irradiance_W/m2": 150.51975898707096,
    "Panel_Temperature_C": 32.268777758737585,
    "Ambient_Temperature_C": 26.443018616468823,
    "Cloud_Cover_%": 2.2425889162055124,
    "Energy_Generated_kWh": 90.11178483671749,
    "CO2_Saved_kg": 41.192459103972695,
    "Money_Saved_INR": 540.6707090203049
  },
  {
    "Date": "2025-01-05 12:03:17.301846",
    "Solar_Irradiance_W/m2": 193.7106539950176,
    "Panel_Temperature_C": 36.959020027012734,
    "Ambient_Temperature_C": 28.9655377682777,
    "Cloud_Cover_%": 36.04268271414861,
    "Energy_Generated_kWh": 109.7822621665658,
    "CO2_Saved_kg": 67.98725018351311,
    "Money_Saved_INR": 658.6935729993947
  },
  {
    "Date": "2025-01-06 12:03:17.301846",
    "Solar_Irradiance_W/m2": 202.78624561443473,
    "Panel_Temperature_C": 27.605442156129357,
    "Ambient_Temperature_C": 26.827261136838906,
    "Cloud_Cover_%": 78.37382510752364,
    "Energy_Generated_kWh": 125.42899490845592,
    "CO2_Saved_kg": 42.647989652367535,
    "Money_Saved_INR": 752.5739694507355
  },
  {
    "Date": "2025-01-07 12:03:17.301846",
    "Solar_Irradiance_W/m2": 254.70957592354742,
    "Panel_Temperature_C": 35.91679959889578,
    "Ambient_Temperature_C": 40.16727274129522,
    "Cloud_Cover_%": 56.61806912250709,
    "Energy_Generated_kWh": 71.91205153632077,
    "CO2_Saved_kg": 66.56208252057296,
    "Money_Saved_INR": 431.47230921792465
  },
  {
    "Date": "2025-01-08 12:03:17.301846",
    "Solar_Irradiance_W/m2": 115.37676851425903,
    "Panel_Temperature_C": 34.923450754135025,
    "Ambient_Temperature_C": 32.28721335221624,
    "Cloud_Cover_%": 31.277798921035405,
    "Energy_Generated_kWh": 89.82858905440399,
    "CO2_Saved_kg": 47.569388011191336,
    "Money_Saved_INR": 538.9715343264239
  },
  {
    "Date": "2025-01-09 12:03:17.301846",
    "Solar_Irradiance_W/m2": 276.4775159730307,
    "Panel_Temperature_C": 37.89645749800544,
    "Ambient_Temperature_C": 32.1033205172758,
    "Cloud_Cover_%": 65.43420054927196,
    "Energy_Generated_kWh": 91.39520714397294,
    "CO2_Saved_kg": 50.02287936143504,
    "Money_Saved_INR": 548.3712428638377
  },
  {
    "Date": "2025-01-10 12:03:17.301846",
    "Solar_Irradiance_W/m2": 192.09960507105052,
    "Panel_Temperature_C": 35.59790184207077,
    "Ambient_Temperature_C": 34.35545000830381,
    "Cloud_Cover_%": 23.20181803088107,
    "Energy_Generated_kWh": 83.90963463106581,
    "CO2_Saved_kg": 60.703651602299296,
    "Money_Saved_INR": 503.4578077863949
  },
  {
    "Date": "2025-01-11 12:03:17.301846",
    "Solar_Irradiance_W/m2": 178.655946502629,
    "Panel_Temperature_C": 30.13465529559222,
    "Ambient_Temperature_C": 22.028168175534617,
    "Cloud_Cover_%": 1.4381446072085025,
    "Energy_Generated_kWh": 78.02309597521388,
    "CO2_Saved_kg": 62.718924219386565,
    "Money_Saved_INR": 468.13857585128324
  },
  {
    "Date": "2025-01-12 12:03:17.301846",
    "Solar_Irradiance_W/m2": 149.39478123699163,
    "Panel_Temperature_C": 40.982857508322454,
    "Ambient_Temperature_C": 37.27378251194188,
    "Cloud_Cover_%": 76.43533864364274,
    "Energy_Generated_kWh": 88.71950779000092,
    "CO2_Saved_kg": 48.89187439720912,
    "Money_Saved_INR": 532.3170467400055
  },
  {
    "Date": "2025-01-13 12:03:17.301846",
    "Solar_Irradiance_W/m2": 117.25716640671153,
    "Panel_Temperature_C": 34.20735213486515,
    "Ambient_Temperature_C": 29.469649994251782,
    "Cloud_Cover_%": 62.374308486400906,
    "Energy_Generated_kWh": 29.35507829560629,
    "CO2_Saved_kg": 46.11756946478461,
    "Money_Saved_INR": 176.13046977363774
  },
  {
    "Date": "2025-01-14 12:03:17.301846",
    "Solar_Irradiance_W/m2": 241.15852919809572,
    "Panel_Temperature_C": 34.86347730245034,
    "Ambient_Temperature_C": 34.69336432068849,
    "Cloud_Cover_%": 76.23026245009599,
    "Energy_Generated_kWh": 93.64138980125263,
    "CO2_Saved_kg": 49.44079551477787,
    "Money_Saved_INR": 561.8483388075158
  },
  {
    "Date": "2025-01-15 12:03:17.301846",
    "Solar_Irradiance_W/m2": 203.6658983594202,
    "Panel_Temperature_C": 30.333660204634022,
    "Ambient_Temperature_C": 22.49699936871891,
    "Cloud_Cover_%": 3.893801668766561,
    "Energy_Generated_kWh": 82.52355807323934,
    "CO2_Saved_kg": 53.379575282321184,
    "Money_Saved_INR": 495.14134843943606
  },
  {
    "Date": "2025-01-16 12:03:17.301846",
    "Solar_Irradiance_W/m2": 135.5019550129473,
    "Panel_Temperature_C": 32.78358874404245,
    "Ambient_Temperature_C": 19.12368863788755,
    "Cloud_Cover_%": 83.71196278306522,
    "Energy_Generated_kWh": 75.5505020644347,
    "CO2_Saved_kg": 58.91303686869755,
    "Money_Saved_INR": 453.3030123866082
  },
  {
    "Date": "2025-01-17 12:03:17.301846",
    "Solar_Irradiance_W/m2": 135.2460613968192,
    "Panel_Temperature_C": 30.575986429865495,
    "Ambient_Temperature_C": 35.7252276061752,
    "Cloud_Cover_%": 61.95262000363033,
    "Energy_Generated_kWh": 120.93724391439116,
    "CO2_Saved_kg": 50.04229858994152,
    "Money_Saved_INR": 725.623463486347
  },
  {
    "Date": "2025-01-18 12:03:17.301846",
    "Solar_Irradiance_W/m2": 183.21076503549358,
    "Panel_Temperature_C": 34.135269700382885,
    "Ambient_Temperature_C": 32.63486668268261,
    "Cloud_Cover_%": 56.33953507126401,
    "Energy_Generated_kWh": 66.50131962418895,
    "CO2_Saved_kg": 56.188862980231534,
    "Money_Saved_INR": 399.0079177451337
  },
  {
    "Date": "2025-01-19 12:03:17.301846",
    "Solar_Irradiance_W/m2": 283.45107626446963,
    "Panel_Temperature_C": 43.558542400711715,
    "Ambient_Temperature_C": 23.685639119497427,
    "Cloud_Cover_%": 62.46140481145316,
    "Energy_Generated_kWh": 71.93848021869938,
    "CO2_Saved_kg": 66.3835973227094,
    "Money_Saved_INR": 431.63088131219627
  },
  {
    "Date": "2025-01-20 12:03:17.301846",
    "Solar_Irradiance_W/m2": 187.02043243181976,
    "Panel_Temperature_C": 28.140494285343216,
    "Ambient_Temperature_C": 23.912358431077138,
    "Cloud_Cover_%": 86.4433246868364,
    "Energy_Generated_kWh": 119.83106604409468,
    "CO2_Saved_kg": 53.81309612264785,
    "Money_Saved_INR": 718.9863962645682
  },
  {
    "Date": "2025-01-21 12:03:17.301846",
    "Solar_Irradiance_W/m2": 124.8428523440947,
    "Panel_Temperature_C": 26.932193010616295,
    "Ambient_Temperature_C": 37.87804349090339,
    "Cloud_Cover_%": 58.69365065589071,
    "Energy_Generated_kWh": 63.35877390300287,
    "CO2_Saved_kg": 53.11652856004778,
    "Money_Saved_INR": 380.1526434180172
  },
  {
    "Date": "2025-01-22 12:03:17.301846",
    "Solar_Irradiance_W/m2": 187.71284679570277,
    "Panel_Temperature_C": 42.35585163746804,
    "Ambient_Temperature_C": 21.674116749928707,
    "Cloud_Cover_%": 58.095037988817936,
    "Energy_Generated_kWh": 68.99769434126922,
    "CO2_Saved_kg": 34.810891749099326,
    "Money_Saved_INR": 413.98616604761537
  },
  {
    "Date": "2025-01-23 12:03:17.301846",
    "Solar_Irradiance_W/m2": 186.36382151261648,
    "Panel_Temperature_C": 33.95338161424067,
    "Ambient_Temperature_C": 41.498710672791745,
    "Cloud_Cover_%": 99.06791570657658,
    "Energy_Generated_kWh": 77.059491531383,
    "CO2_Saved_kg": 23.692698631709366,
    "Money_Saved_INR": 462.356949188298
  },
  {
    "Date": "2025-01-24 12:03:17.301846",
    "Solar_Irradiance_W/m2": 65.15566785292143,
    "Panel_Temperature_C": 31.654636306700418,
    "Ambient_Temperature_C": 23.69565485746492,
    "Cloud_Cover_%": 75.6730167068568,
    "Energy_Generated_kWh": 96.81468964259099,
    "CO2_Saved_kg": 53.88375729230168,
    "Money_Saved_INR": 580.8881378555459
  },
  {
    "Date": "2025-01-25 12:03:17.301846",
    "Solar_Irradiance_W/m2": 197.28525667410938,
    "Panel_Temperature_C": 40.199523436980385,
    "Ambient_Temperature_C": 34.46874347925868,
    "Cloud_Cover_%": 44.22938054511353,
    "Energy_Generated_kWh": 84.15605014706627,
    "CO2_Saved_kg": 49.05175768719128,
    "Money_Saved_INR": 504.93630088239763
  },
  {
    "Date": "2025-01-26 12:03:17.301846",
    "Solar_Irradiance_W/m2": 188.4532734895661,
    "Panel_Temperature_C": 31.97192230131568,
    "Ambient_Temperature_C": 27.699670669757108,
    "Cloud_Cover_%": 70.73970000329277,
    "Energy_Generated_kWh": 54.147493056954744,
    "CO2_Saved_kg": 44.85217325085258,
    "Money_Saved_INR": 324.88495834172846
  },
  {
    "Date": "2025-01-27 12:03:17.301846",
    "Solar_Irradiance_W/m2": 234.8103182406709,
    "Panel_Temperature_C": 44.13004856773468,
    "Ambient_Temperature_C": 34.2223120175764,
    "Cloud_Cover_%": 38.92304716917885,
    "Energy_Generated_kWh": 69.3566287374562,
    "CO2_Saved_kg": 52.435302041863444,
    "Money_Saved_INR": 416.1397724247372
  },
  {
    "Date": "2025-01-28 12:03:17.301846",
    "Solar_Irradiance_W/m2": 292.44780474726724,
    "Panel_Temperature_C": 38.38962935669635,
    "Ambient_Temperature_C": 26.191201985200653,
    "Cloud_Cover_%": 22.8875462483499,
    "Energy_Generated_kWh": 67.85291133575578,
    "CO2_Saved_kg": 49.395962708030915,
    "Money_Saved_INR": 407.11746801453467
  },
  {
    "Date": "2025-01-29 12:03:17.301846",
    "Solar_Irradiance_W/m2": 256.3282514773879,
    "Panel_Temperature_C": 32.560442959271484,
    "Ambient_Temperature_C": 28.86044965749394,
    "Cloud_Cover_%": 59.68518768877594,
    "Energy_Generated_kWh": 78.4555790955391,
    "CO2_Saved_kg": 61.277802506338986,
    "Money_Saved_INR": 470.73347457323456
  },
  {
    "Date": "2025-01-30 12:03:17.301846",
    "Solar_Irradiance_W/m2": 186.55556547225848,
    "Panel_Temperature_C": 45.786541066327516,
    "Ambient_Temperature_C": 30.286434227770048,
    "Cloud_Cover_%": 92.81820981139515,
    "Energy_Generated_kWh": 88.51687317259658,
    "CO2_Saved_kg": 50.86110868258978,
    "Money_Saved_INR": 531.1012390355795
  },
  {
    "Date": "2025-01-31 12:03:17.301846",
    "Solar_Irradiance_W/m2": 144.6737045629165,
    "Panel_Temperature_C": 31.97142538498331,
    "Ambient_Temperature_C": 22.98468780952969,
    "Cloud_Cover_%": 92.91395200154628,
    "Energy_Generated_kWh": 88.36411511775944,
    "CO2_Saved_kg": 42.53076714929833,
    "Money_Saved_INR": 530.1846907065567
  },
  {
    "Date": "2025-02-01 12:03:17.301846",
    "Solar_Irradiance_W/m2": 328.667990162493,
    "Panel_Temperature_C": 38.71047686004653,
    "Ambient_Temperature_C": 35.18577041794088,
    "Cloud_Cover_%": 34.19052781054903,
    "Energy_Generated_kWh": 44.47976491903196,
    "CO2_Saved_kg": 59.901662389592886,
    "Money_Saved_INR": 266.87858951419173
  },
  {
    "Date": "2025-02-02 12:03:17.301846",
    "Solar_Irradiance_W/m2": 202.9609217007244,
    "Panel_Temperature_C": 36.49646290203246,
    "Ambient_Temperature_C": 26.407505034698904,
    "Cloud_Cover_%": 52.7677466221695,
    "Energy_Generated_kWh": 101.27881975121713,
    "CO2_Saved_kg": 47.82868925053798,
    "Money_Saved_INR": 607.6729185073027
  },
  {
    "Date": "2025-02-03 12:03:17.301846",
    "Solar_Irradiance_W/m2": 200.6964645956473,
    "Panel_Temperature_C": 41.50870644699399,
    "Ambient_Temperature_C": 28.39980059261987,
    "Cloud_Cover_%": 21.16358985698612,
    "Energy_Generated_kWh": 85.05137691993247,
    "CO2_Saved_kg": 55.265366836723075,
    "Money_Saved_INR": 510.3082615195948
  },
  {
    "Date": "2025-02-04 12:03:17.301846",
    "Solar_Irradiance_W/m2": 198.79374564449984,
    "Panel_Temperature_C": 42.807555983634266,
    "Ambient_Temperature_C": 23.039554377740416,
    "Cloud_Cover_%": 99.56311094988834,
    "Energy_Generated_kWh": 107.69064095187812,
    "CO2_Saved_kg": 45.22589293807199,
    "Money_Saved_INR": 646.1438457112688
  },
  {
    "Date": "2025-02-05 12:03:17.301846",
    "Solar_Irradiance_W/m2": 209.90423803839275,
    "Panel_Temperature_C": 35.160020745328836,
    "Ambient_Temperature_C": 12.063664388432827,
    "Cloud_Cover_%": 98.11179078679358,
    "Energy_Generated_kWh": 88.88396654581344,
    "CO2_Saved_kg": 43.50173114502564,
    "Money_Saved_INR": 533.3037992748806
  },
  {
    "Date": "2025-02-06 12:03:17.301846",
    "Solar_Irradiance_W/m2": 192.78197940380286,
    "Panel_Temperature_C": 31.232910648269083,
    "Ambient_Temperature_C": 28.662805661798817,
    "Cloud_Cover_%": 64.95089297074473,
    "Energy_Generated_kWh": 102.02645915471524,
    "CO2_Saved_kg": 50.84168230185696,
    "Money_Saved_INR": 612.1587549282915
  },
  {
    "Date": "2025-02-07 12:03:17.301846",
    "Solar_Irradiance_W/m2": 171.31689965598818,
    "Panel_Temperature_C": 37.29986071469558,
    "Ambient_Temperature_C": 46.888307951290415,
    "Cloud_Cover_%": 80.44140596774734,
    "Energy_Generated_kWh": 89.33090622900254,
    "CO2_Saved_kg": 50.12828643543685,
    "Money_Saved_INR": 535.9854373740152
  },
  {
    "Date": "2025-02-08 12:03:17.301846",
    "Solar_Irradiance_W/m2": 172.65705293798038,
    "Panel_Temperature_C": 31.61142315123947,
    "Ambient_Temperature_C": 35.49223001528617,
    "Cloud_Cover_%": 71.51001612837,
    "Energy_Generated_kWh": 106.92451512405496,
    "CO2_Saved_kg": 54.79827035366833,
    "Money_Saved_INR": 641.5470907443298
  },
  {
    "Date": "2025-02-09 12:03:17.301846",
    "Solar_Irradiance_W/m2": 198.3623364892001,
    "Panel_Temperature_C": 45.066936237633115,
    "Ambient_Temperature_C": 29.865177341859237,
    "Cloud_Cover_%": 59.31582190394682,
    "Energy_Generated_kWh": 90.44501272035558,
    "CO2_Saved_kg": 47.313542466902575,
    "Money_Saved_INR": 542.6700763221335
  },
  {
    "Date": "2025-02-10 12:03:17.301846",
    "Solar_Irradiance_W/m2": 172.82876144331175,
    "Panel_Temperature_C": 35.68267665541369,
    "Ambient_Temperature_C": 28.159764195542127,
    "Cloud_Cover_%": 5.3347996988897695,
    "Energy_Generated_kWh": 78.04169507114192,
    "CO2_Saved_kg": 31.636402162296026,
    "Money_Saved_INR": 468.25017042685147
  },
  {
    "Date": "2025-02-11 12:03:17.301846",
    "Solar_Irradiance_W/m2": 164.3577108661418,
    "Panel_Temperature_C": 33.17339224343946,
    "Ambient_Temperature_C": 30.157261249684325,
    "Cloud_Cover_%": 45.476434255266106,
    "Energy_Generated_kWh": 125.44869440893763,
    "CO2_Saved_kg": 45.672261164116115,
    "Money_Saved_INR": 752.6921664536258
  },
  {
    "Date": "2025-02-12 12:03:17.301846",
    "Solar_Irradiance_W/m2": 205.32151138459483,
    "Panel_Temperature_C": 35.92340152932454,
    "Ambient_Temperature_C": 33.82983380622647,
    "Cloud_Cover_%": 67.47863021674105,
    "Energy_Generated_kWh": 97.78074244559784,
    "CO2_Saved_kg": 57.93818467143816,
    "Money_Saved_INR": 586.684454673587
  },
  {
    "Date": "2025-02-13 12:03:17.301846",
    "Solar_Irradiance_W/m2": 187.25113912895725,
    "Panel_Temperature_C": 28.264368552351517,
    "Ambient_Temperature_C": 21.734310292838085,
    "Cloud_Cover_%": 67.75316138836847,
    "Energy_Generated_kWh": 91.47488842008826,
    "CO2_Saved_kg": 47.026239207568935,
    "Money_Saved_INR": 548.8493305205295
  },
  {
    "Date": "2025-02-14 12:03:17.301846",
    "Solar_Irradiance_W/m2": 275.1996494291344,
    "Panel_Temperature_C": 30.141929807446743,
    "Ambient_Temperature_C": 37.8002518626821,
    "Cloud_Cover_%": 37.31226184223836,
    "Energy_Generated_kWh": 54.47391166923328,
    "CO2_Saved_kg": 47.53616597485452,
    "Money_Saved_INR": 326.8434700153997
  },
  {
    "Date": "2025-02-15 12:03:17.301846",
    "Solar_Irradiance_W/m2": 67.45150958034941,
    "Panel_Temperature_C": 41.00206953972213,
    "Ambient_Temperature_C": 35.00766920808871,
    "Cloud_Cover_%": 94.16919866580305,
    "Energy_Generated_kWh": 54.233847650729246,
    "CO2_Saved_kg": 59.863765059059375,
    "Money_Saved_INR": 325.4030859043755
  },
  {
    "Date": "2025-02-16 12:03:17.301846",
    "Solar_Irradiance_W/m2": 254.57534259612308,
    "Panel_Temperature_C": 31.71552860514302,
    "Ambient_Temperature_C": 35.02730007995554,
    "Cloud_Cover_%": 16.7357032236781,
    "Energy_Generated_kWh": 85.85430964283707,
    "CO2_Saved_kg": 42.880267727410775,
    "Money_Saved_INR": 515.1258578570224
  },
  {
    "Date": "2025-02-17 12:03:17.301846",
    "Solar_Irradiance_W/m2": 262.30425962488147,
    "Panel_Temperature_C": 29.7654450865903,
    "Ambient_Temperature_C": 33.06933017166809,
    "Cloud_Cover_%": 50.03594462155606,
    "Energy_Generated_kWh": 82.91042395536482,
    "CO2_Saved_kg": 34.57196781757101,
    "Money_Saved_INR": 497.4625437321889
  },
  {
    "Date": "2025-02-18 12:03:17.301846",
    "Solar_Irradiance_W/m2": 96.33048837959252,
    "Panel_Temperature_C": 37.68326376263643,
    "Ambient_Temperature_C": 30.13731660385793,
    "Cloud_Cover_%": 69.08839765508228,
    "Energy_Generated_kWh": 67.71754869983367,
    "CO2_Saved_kg": 48.393688804745054,
    "Money_Saved_INR": 406.305292199002
  },
  {
    "Date": "2025-02-19 12:03:17.301846",
    "Solar_Irradiance_W/m2": 182.86562029598255,
    "Panel_Temperature_C": 40.928520773314986,
    "Ambient_Temperature_C": 34.71002865176774,
    "Cloud_Cover_%": 69.71358058918092,
    "Energy_Generated_kWh": 82.8196539922412,
    "CO2_Saved_kg": 45.15826048751263,
    "Money_Saved_INR": 496.9179239534472
  },
  {
    "Date": "2025-02-20 12:03:17.301846",
    "Solar_Irradiance_W/m2": 181.42795670021042,
    "Panel_Temperature_C": 38.594766553325336,
    "Ambient_Temperature_C": 34.142698936189646,
    "Cloud_Cover_%": 64.86389567688155,
    "Energy_Generated_kWh": 111.77253856087191,
    "CO2_Saved_kg": 40.33753680246746,
    "Money_Saved_INR": 670.6352313652314
  },
  {
    "Date": "2025-02-21 12:03:17.301846",
    "Solar_Irradiance_W/m2": 129.62441526410893,
    "Panel_Temperature_C": 39.98023842902908,
    "Ambient_Temperature_C": 27.521715023412835,
    "Cloud_Cover_%": 27.528821345186017,
    "Energy_Generated_kWh": 93.90804949100597,
    "CO2_Saved_kg": 48.24621544101309,
    "Money_Saved_INR": 563.4482969460358
  },
  {
    "Date": "2025-02-22 12:03:17.301846",
    "Solar_Irradiance_W/m2": 161.10916562045622,
    "Panel_Temperature_C": 31.216024557152696,
    "Ambient_Temperature_C": 25.984787589721694,
    "Cloud_Cover_%": 15.620656868662197,
    "Energy_Generated_kWh": 57.179829804945236,
    "CO2_Saved_kg": 54.91505647246784,
    "Money_Saved_INR": 343.0789788296714
  },
  {
    "Date": "2025-02-23 12:03:17.301846",
    "Solar_Irradiance_W/m2": 144.47120772670857,
    "Panel_Temperature_C": 27.89094666629078,
    "Ambient_Temperature_C": 30.712994066833907,
    "Cloud_Cover_%": 63.594032682671084,
    "Energy_Generated_kWh": 77.76982345714113,
    "CO2_Saved_kg": 49.907114384321844,
    "Money_Saved_INR": 466.6189407428468
  },
  {
    "Date": "2025-02-24 12:03:17.301846",
    "Solar_Irradiance_W/m2": 287.6135221711811,
    "Panel_Temperature_C": 42.506668259777435,
    "Ambient_Temperature_C": 40.84314106046631,
    "Cloud_Cover_%": 59.930211613943776,
    "Energy_Generated_kWh": 63.90067038294878,
    "CO2_Saved_kg": 53.06981072686238,
    "Money_Saved_INR": 383.4040222976927
  },
  {
    "Date": "2025-02-25 12:03:17.301846",
    "Solar_Irradiance_W/m2": 246.78391965737305,
    "Panel_Temperature_C": 33.38660080578932,
    "Ambient_Temperature_C": 21.326250470422693,
    "Cloud_Cover_%": 17.935601028924097,
    "Energy_Generated_kWh": 72.24600167182878,
    "CO2_Saved_kg": 68.13407698515422,
    "Money_Saved_INR": 433.4760100309727
  },
  {
    "Date": "2025-02-26 12:03:17.301846",
    "Solar_Irradiance_W/m2": 263.57775474970794,
    "Panel_Temperature_C": 33.745834917724764,
    "Ambient_Temperature_C": 19.72732313973292,
    "Cloud_Cover_%": 70.51391455705634,
    "Energy_Generated_kWh": 71.72768668740714,
    "CO2_Saved_kg": 46.57121138442436,
    "Money_Saved_INR": 430.3661201244429
  },
  {
    "Date": "2025-02-27 12:03:17.301846",
    "Solar_Irradiance_W/m2": 236.08360320216175,
    "Panel_Temperature_C": 41.64097070924529,
    "Ambient_Temperature_C": 31.153325888655615,
    "Cloud_Cover_%": 45.51719917336564,
    "Energy_Generated_kWh": 70.4470883479199,
    "CO2_Saved_kg": 52.78348634644669,
    "Money_Saved_INR": 422.6825300875194
  },
  {
    "Date": "2025-02-28 12:03:17.301846",
    "Solar_Irradiance_W/m2": 143.54741143913856,
    "Panel_Temperature_C": 37.7811500470033,
    "Ambient_Temperature_C": 30.356213912992125,
    "Cloud_Cover_%": 66.7760591603153,
    "Energy_Generated_kWh": 54.8972925605321,
    "CO2_Saved_kg": 44.907866374008655,
    "Money_Saved_INR": 329.3837553631926
  },
  {
    "Date": "2025-03-01 12:03:17.301846",
    "Solar_Irradiance_W/m2": 173.7739866860113,
    "Panel_Temperature_C": 37.279438860408035,
    "Ambient_Temperature_C": 31.213391650592857,
    "Cloud_Cover_%": 83.73670797701507,
    "Energy_Generated_kWh": 77.4469063696362,
    "CO2_Saved_kg": 41.53640280113027,
    "Money_Saved_INR": 464.6814382178172
  },
  {
    "Date": "2025-03-02 12:03:17.301846",
    "Solar_Irradiance_W/m2": 224.4687280613959,
    "Panel_Temperature_C": 45.825011724505416,
    "Ambient_Temperature_C": 31.7076723853595,
    "Cloud_Cover_%": 16.972842857692317,
    "Energy_Generated_kWh": 68.7878472630538,
    "CO2_Saved_kg": 44.1509234658223,
    "Money_Saved_INR": 412.72708357832283
  },
  {
    "Date": "2025-03-03 12:03:17.301846",
    "Solar_Irradiance_W/m2": 138.89360955540275,
    "Panel_Temperature_C": 31.782408848099287,
    "Ambient_Temperature_C": 28.437584217556363,
    "Cloud_Cover_%": 1.9144867996836679,
    "Energy_Generated_kWh": 21.41102619995464,
    "CO2_Saved_kg": 45.212414284783115,
    "Money_Saved_INR": 128.46615719972783
  },
  {
    "Date": "2025-03-04 12:03:17.301846",
    "Solar_Irradiance_W/m2": 235.6499215086194,
    "Panel_Temperature_C": 39.63920064040619,
    "Ambient_Temperature_C": 40.42904407021457,
    "Cloud_Cover_%": 77.91025863957867,
    "Energy_Generated_kWh": 121.05944049003327,
    "CO2_Saved_kg": 53.59475797547125,
    "Money_Saved_INR": 726.3566429401997
  },
  {
    "Date": "2025-03-05 12:03:17.301846",
    "Solar_Irradiance_W/m2": 187.98373009209325,
    "Panel_Temperature_C": 35.28506562448542,
    "Ambient_Temperature_C": 18.793672150664392,
    "Cloud_Cover_%": 60.96974251526159,
    "Energy_Generated_kWh": 101.77539308433344,
    "CO2_Saved_kg": 73.49075786700757,
    "Money_Saved_INR": 610.6523585060006
  },
  {
    "Date": "2025-03-06 12:03:17.301846",
    "Solar_Irradiance_W/m2": 181.25895962252014,
    "Panel_Temperature_C": 36.34296139431628,
    "Ambient_Temperature_C": 24.200520826538277,
    "Cloud_Cover_%": 69.96395696221217,
    "Energy_Generated_kWh": 72.47398550150008,
    "CO2_Saved_kg": 42.8395656372416,
    "Money_Saved_INR": 434.8439130090005
  },
  {
    "Date": "2025-03-07 12:03:17.301846",
    "Solar_Irradiance_W/m2": 235.54799841017456,
    "Panel_Temperature_C": 42.64234213206266,
    "Ambient_Temperature_C": 29.27721667895667,
    "Cloud_Cover_%": 83.81549749886426,
    "Energy_Generated_kWh": 80.37638099481197,
    "CO2_Saved_kg": 45.83374694384538,
    "Money_Saved_INR": 482.2582859688718
  },
  {
    "Date": "2025-03-08 12:03:17.301846",
    "Solar_Irradiance_W/m2": 222.213165574302,
    "Panel_Temperature_C": 37.53917878144812,
    "Ambient_Temperature_C": 18.49767832192083,
    "Cloud_Cover_%": 80.28109348245005,
    "Energy_Generated_kWh": 56.56691305364876,
    "CO2_Saved_kg": 49.36876986888752,
    "Money_Saved_INR": 339.40147832189257
  },
  {
    "Date": "2025-03-09 12:03:17.301846",
    "Solar_Irradiance_W/m2": 181.951691709046,
    "Panel_Temperature_C": 37.69148039524816,
    "Ambient_Temperature_C": 28.7690191689755,
    "Cloud_Cover_%": 96.09201469288247,
    "Energy_Generated_kWh": 113.91445755621731,
    "CO2_Saved_kg": 53.957988487097474,
    "Money_Saved_INR": 683.4867453373039
  },
  {
    "Date": "2025-03-10 12:03:17.301846",
    "Solar_Irradiance_W/m2": 257.96649016821243,
    "Panel_Temperature_C": 40.362536686549014,
    "Ambient_Temperature_C": 41.63029116009613,
    "Cloud_Cover_%": 53.59350788521182,
    "Energy_Generated_kWh": 117.94577389546222,
    "CO2_Saved_kg": 52.63550811954785,
    "Money_Saved_INR": 707.6746433727733
  },
  {
    "Date": "2025-03-11 12:03:17.301846",
    "Solar_Irradiance_W/m2": 145.94683362000512,
    "Panel_Temperature_C": 33.17523635228557,
    "Ambient_Temperature_C": 30.146205418071734,
    "Cloud_Cover_%": 48.84956326599054,
    "Energy_Generated_kWh": 83.1338745649305,
    "CO2_Saved_kg": 62.84095793948117,
    "Money_Saved_INR": 498.80324738958296
  },
  {
    "Date": "2025-03-12 12:03:17.301846",
    "Solar_Irradiance_W/m2": 230.7967803472132,
    "Panel_Temperature_C": 30.803951663304968,
    "Ambient_Temperature_C": 31.614906340030785,
    "Cloud_Cover_%": 40.18871998907301,
    "Energy_Generated_kWh": 100.47061288370689,
    "CO2_Saved_kg": 25.73607929464792,
    "Money_Saved_INR": 602.8236773022413
  },
  {
    "Date": "2025-03-13 12:03:17.301846",
    "Solar_Irradiance_W/m2": 229.6550628984192,
    "Panel_Temperature_C": 29.775954029894834,
    "Ambient_Temperature_C": 21.17884664379194,
    "Cloud_Cover_%": 15.369104284420454,
    "Energy_Generated_kWh": 83.50573557867848,
    "CO2_Saved_kg": 26.130701298043274,
    "Money_Saved_INR": 501.0344134720709
  },
  {
    "Date": "2025-03-14 12:03:17.301846",
    "Solar_Irradiance_W/m2": 184.5226780343005,
    "Panel_Temperature_C": 25.16821705311999,
    "Ambient_Temperature_C": 25.685470143723656,
    "Cloud_Cover_%": 57.26072328820224,
    "Energy_Generated_kWh": 53.26549122248139,
    "CO2_Saved_kg": 45.04121827989851,
    "Money_Saved_INR": 319.5929473348883
  },
  {
    "Date": "2025-03-15 12:03:17.301846",
    "Solar_Irradiance_W/m2": 216.3066511121059,
    "Panel_Temperature_C": 45.28103564970161,
    "Ambient_Temperature_C": 27.37362533773244,
    "Cloud_Cover_%": 27.70125243259788,
    "Energy_Generated_kWh": 71.76353262072685,
    "CO2_Saved_kg": 60.97300187543709,
    "Money_Saved_INR": 430.5811957243611
  },
  {
    "Date": "2025-03-16 12:03:17.301846",
    "Solar_Irradiance_W/m2": 137.44432118073485,
    "Panel_Temperature_C": 29.483958171391585,
    "Ambient_Temperature_C": 27.77599432270636,
    "Cloud_Cover_%": 92.13075122129754,
    "Energy_Generated_kWh": 82.63855933543914,
    "CO2_Saved_kg": 34.34351968394404,
    "Money_Saved_INR": 495.83135601263484
  },
  {
    "Date": "2025-03-17 12:03:17.301846",
    "Solar_Irradiance_W/m2": 246.20135096034505,
    "Panel_Temperature_C": 33.89373188207114,
    "Ambient_Temperature_C": 38.97150656502638,
    "Cloud_Cover_%": 58.31908042770976,
    "Energy_Generated_kWh": 70.90904562513111,
    "CO2_Saved_kg": 19.92367660306243,
    "Money_Saved_INR": 425.4542737507867
  },
  {
    "Date": "2025-03-18 12:03:17.301846",
    "Solar_Irradiance_W/m2": 190.75489317785053,
    "Panel_Temperature_C": 33.6159335005554,
    "Ambient_Temperature_C": 33.90383742507587,
    "Cloud_Cover_%": 59.284018050811014,
    "Energy_Generated_kWh": 75.62693445129928,
    "CO2_Saved_kg": 55.711794062192084,
    "Money_Saved_INR": 453.76160670779564
  },
  {
    "Date": "2025-03-19 12:03:17.301846",
    "Solar_Irradiance_W/m2": 173.86384897404804,
    "Panel_Temperature_C": 36.537033489045506,
    "Ambient_Temperature_C": 22.21979430144078,
    "Cloud_Cover_%": 35.492466087701004,
    "Energy_Generated_kWh": 78.17200884981771,
    "CO2_Saved_kg": 52.43657223702714,
    "Money_Saved_INR": 469.0320530989063
  },
  {
    "Date": "2025-03-20 12:03:17.301846",
    "Solar_Irradiance_W/m2": 252.45046129184448,
    "Panel_Temperature_C": 39.078686062696484,
    "Ambient_Temperature_C": 31.725533449024034,
    "Cloud_Cover_%": 5.198935197770749,
    "Energy_Generated_kWh": 78.38243004269077,
    "CO2_Saved_kg": 39.097915932005705,
    "Money_Saved_INR": 470.2945802561446
  },
  {
    "Date": "2025-03-21 12:03:17.301846",
    "Solar_Irradiance_W/m2": 164.78281547286204,
    "Panel_Temperature_C": 39.30236744179873,
    "Ambient_Temperature_C": 33.487552239477495,
    "Cloud_Cover_%": 3.174376537298862,
    "Energy_Generated_kWh": 81.04516980994967,
    "CO2_Saved_kg": 40.1446039927907,
    "Money_Saved_INR": 486.271018859698
  },
  {
    "Date": "2025-03-22 12:03:17.301846",
    "Solar_Irradiance_W/m2": 129.57693518182202,
    "Panel_Temperature_C": 32.08461280715531,
    "Ambient_Temperature_C": 37.981043269648865,
    "Cloud_Cover_%": 42.33351441531975,
    "Energy_Generated_kWh": 58.78789867206798,
    "CO2_Saved_kg": 40.30256280365326,
    "Money_Saved_INR": 352.7273920324079
  },
  {
    "Date": "2025-03-23 12:03:17.301846",
    "Solar_Irradiance_W/m2": 122.16854132380482,
    "Panel_Temperature_C": 34.16439143106794,
    "Ambient_Temperature_C": 41.063784805978614,
    "Cloud_Cover_%": 8.456537809723786,
    "Energy_Generated_kWh": 65.65967701744128,
    "CO2_Saved_kg": 51.1053531747394,
    "Money_Saved_INR": 393.9580621046477
  },
  {
    "Date": "2025-03-24 12:03:17.301846",
    "Solar_Irradiance_W/m2": 230.30049756728198,
    "Panel_Temperature_C": 36.4128997524415,
    "Ambient_Temperature_C": 22.89434065720492,
    "Cloud_Cover_%": 60.68469555401391,
    "Energy_Generated_kWh": 54.308314686000614,
    "CO2_Saved_kg": 43.73684723816993,
    "Money_Saved_INR": 325.8498881160037
  },
  {
    "Date": "2025-03-25 12:03:17.301846",
    "Solar_Irradiance_W/m2": 135.97853237518586,
    "Panel_Temperature_C": 33.75654436908226,
    "Ambient_Temperature_C": 24.323997421527633,
    "Cloud_Cover_%": 88.09730056396575,
    "Energy_Generated_kWh": 99.55631099372401,
    "CO2_Saved_kg": 54.940639189755196,
    "Money_Saved_INR": 597.337865962344
  },
  {
    "Date": "2025-03-26 12:03:17.301846",
    "Solar_Irradiance_W/m2": 287.7397090992182,
    "Panel_Temperature_C": 43.03672788009996,
    "Ambient_Temperature_C": 21.196954987597685,
    "Cloud_Cover_%": 88.29148165187222,
    "Energy_Generated_kWh": 37.88706116319351,
    "CO2_Saved_kg": 21.45373337095609,
    "Money_Saved_INR": 227.32236697916105
  },
  {
    "Date": "2025-03-27 12:03:17.301846",
    "Solar_Irradiance_W/m2": 95.9035296058139,
    "Panel_Temperature_C": 37.45487475819126,
    "Ambient_Temperature_C": 28.36186098625113,
    "Cloud_Cover_%": 65.90454101322324,
    "Energy_Generated_kWh": 103.0718068663385,
    "CO2_Saved_kg": 41.43148134872201,
    "Money_Saved_INR": 618.430841198031
  },
  {
    "Date": "2025-03-28 12:03:17.301846",
    "Solar_Irradiance_W/m2": 284.8228184145019,
    "Panel_Temperature_C": 38.67438893024909,
    "Ambient_Temperature_C": 33.26450862112434,
    "Cloud_Cover_%": 21.1231831472931,
    "Energy_Generated_kWh": 107.72698794525687,
    "CO2_Saved_kg": 38.7394603908895,
    "Money_Saved_INR": 646.3619276715413
  },
  {
    "Date": "2025-03-29 12:03:17.301846",
    "Solar_Irradiance_W/m2": 210.5508733601309,
    "Panel_Temperature_C": 38.31440634333706,
    "Ambient_Temperature_C": 36.911341616123714,
    "Cloud_Cover_%": 86.29968313588721,
    "Energy_Generated_kWh": 73.95638826034757,
    "CO2_Saved_kg": 47.43659321627508,
    "Money_Saved_INR": 443.73832956208537
  },
  {
    "Date": "2025-03-30 12:03:17.301846",
    "Solar_Irradiance_W/m2": 195.16434440648038,
    "Panel_Temperature_C": 40.86736928742663,
    "Ambient_Temperature_C": 29.46834283450234,
    "Cloud_Cover_%": 88.60934353132082,
    "Energy_Generated_kWh": 27.937258243454025,
    "CO2_Saved_kg": 44.619522415098615,
    "Money_Saved_INR": 167.62354946072415
  },
  {
    "Date": "2025-03-31 12:03:17.301846",
    "Solar_Irradiance_W/m2": 172.7540456595525,
    "Panel_Temperature_C": 35.90510779351853,
    "Ambient_Temperature_C": 27.761067337216094,
    "Cloud_Cover_%": 19.66535849529587,
    "Energy_Generated_kWh": 72.77378876065418,
    "CO2_Saved_kg": 57.978437798957664,
    "Money_Saved_INR": 436.6427325639251
  },
  {
    "Date": "2025-04-01 12:03:17.301846",
    "Solar_Irradiance_W/m2": 219.95680571760354,
    "Panel_Temperature_C": 28.515840260220767,
    "Ambient_Temperature_C": 31.062305945741183,
    "Cloud_Cover_%": 73.74260857706773,
    "Energy_Generated_kWh": 78.71631677422361,
    "CO2_Saved_kg": 31.406632283399425,
    "Money_Saved_INR": 472.29790064534166
  },
  {
    "Date": "2025-04-02 12:03:17.301846",
    "Solar_Irradiance_W/m2": 198.11826487875757,
    "Panel_Temperature_C": 36.99843975876321,
    "Ambient_Temperature_C": 24.15399968858984,
    "Cloud_Cover_%": 28.651954892712293,
    "Energy_Generated_kWh": 59.78803560142173,
    "CO2_Saved_kg": 50.45491476330752,
    "Money_Saved_INR": 358.7282136085304
  },
  {
    "Date": "2025-04-03 12:03:17.301846",
    "Solar_Irradiance_W/m2": 255.16509410082608,
    "Panel_Temperature_C": 31.743215531040853,
    "Ambient_Temperature_C": 44.626771051863415,
    "Cloud_Cover_%": 80.26403123529296,
    "Energy_Generated_kWh": 69.69563212383514,
    "CO2_Saved_kg": 55.583364232117056,
    "Money_Saved_INR": 418.17379274301084
  },
  {
    "Date": "2025-04-04 12:03:17.301846",
    "Solar_Irradiance_W/m2": 205.711382433102,
    "Panel_Temperature_C": 32.35691659125121,
    "Ambient_Temperature_C": 18.74637281017359,
    "Cloud_Cover_%": 99.72378999036027,
    "Energy_Generated_kWh": 110.60390397726702,
    "CO2_Saved_kg": 68.56647436561954,
    "Money_Saved_INR": 663.6234238636022
  },
  {
    "Date": "2025-04-05 12:03:17.301846",
    "Solar_Irradiance_W/m2": 207.5150880730939,
    "Panel_Temperature_C": 37.931820093775464,
    "Ambient_Temperature_C": 31.29318405227007,
    "Cloud_Cover_%": 3.0026005329392813,
    "Energy_Generated_kWh": 93.29854324603482,
    "CO2_Saved_kg": 45.18234028906525,
    "Money_Saved_INR": 559.791259476209
  },
  {
    "Date": "2025-04-06 12:03:17.301846",
    "Solar_Irradiance_W/m2": 181.81938938930722,
    "Panel_Temperature_C": 41.19141535716818,
    "Ambient_Temperature_C": 44.16524353460748,
    "Cloud_Cover_%": 89.73658657909318,
    "Energy_Generated_kWh": 61.508717712438,
    "CO2_Saved_kg": 53.24458604352517,
    "Money_Saved_INR": 369.052306274628
  },
  {
    "Date": "2025-04-07 12:03:17.301846",
    "Solar_Irradiance_W/m2": 197.15271881394662,
    "Panel_Temperature_C": 35.10635788368031,
    "Ambient_Temperature_C": 30.047598911919984,
    "Cloud_Cover_%": 62.26305335986581,
    "Energy_Generated_kWh": 48.04801660809136,
    "CO2_Saved_kg": 31.96137207437635,
    "Money_Saved_INR": 288.28809964854815
  },
  {
    "Date": "2025-04-08 12:03:17.301846",
    "Solar_Irradiance_W/m2": 215.39008844460295,
    "Panel_Temperature_C": 36.54416506299482,
    "Ambient_Temperature_C": 28.66972675498954,
    "Cloud_Cover_%": 97.33826191648211,
    "Energy_Generated_kWh": 73.45965364780457,
    "CO2_Saved_kg": 26.080437956869762,
    "Money_Saved_INR": 440.75792188682743
  },
  {
    "Date": "2025-04-09 12:03:17.301846",
    "Solar_Irradiance_W/m2": 114.49158036716872,
    "Panel_Temperature_C": 43.51107472317619,
    "Ambient_Temperature_C": 27.49788204032701,
    "Cloud_Cover_%": 46.50095175264276,
    "Energy_Generated_kWh": 75.73086441299124,
    "CO2_Saved_kg": 58.447743757817,
    "Money_Saved_INR": 454.3851864779474
  },
  {
    "Date": "2025-04-10 12:03:17.301846",
    "Solar_Irradiance_W/m2": 132.59072889471435,
    "Panel_Temperature_C": 36.20376589744284,
    "Ambient_Temperature_C": 28.737258227663144,
    "Cloud_Cover_%": 84.73879305713737,
    "Energy_Generated_kWh": 89.92398374726633,
    "CO2_Saved_kg": 49.9443970635193,
    "Money_Saved_INR": 539.543902483598
  },
  {
    "Date": "2025-04-11 12:03:17.301846",
    "Solar_Irradiance_W/m2": 237.16320470113575,
    "Panel_Temperature_C": 48.008415570901974,
    "Ambient_Temperature_C": 39.60993932273571,
    "Cloud_Cover_%": 6.239406859827723,
    "Energy_Generated_kWh": 69.29366574864682,
    "CO2_Saved_kg": 61.78512689798423,
    "Money_Saved_INR": 415.7619944918809
  },
  {
    "Date": "2025-04-12 12:03:17.301846",
    "Solar_Irradiance_W/m2": 208.54327190639708,
    "Panel_Temperature_C": 37.827548228157724,
    "Ambient_Temperature_C": 14.516966620693452,
    "Cloud_Cover_%": 33.527905007829574,
    "Energy_Generated_kWh": 90.22999150723723,
    "CO2_Saved_kg": 36.26597111030251,
    "Money_Saved_INR": 541.3799490434234
  },
  {
    "Date": "2025-04-13 12:03:17.301846",
    "Solar_Irradiance_W/m2": 190.80083318236603,
    "Panel_Temperature_C": 26.19618620422091,
    "Ambient_Temperature_C": 40.73403590907428,
    "Cloud_Cover_%": 6.701653775120997,
    "Energy_Generated_kWh": 118.70308080120458,
    "CO2_Saved_kg": 55.199021395287524,
    "Money_Saved_INR": 712.2184848072275
  },
  {
    "Date": "2025-04-14 12:03:17.301846",
    "Solar_Irradiance_W/m2": 200.92169665326966,
    "Panel_Temperature_C": 38.76670810552266,
    "Ambient_Temperature_C": 20.032299932848986,
    "Cloud_Cover_%": 97.53431334790706,
    "Energy_Generated_kWh": 96.31002044888525,
    "CO2_Saved_kg": 68.68817840543853,
    "Money_Saved_INR": 577.8601226933115
  },
  {
    "Date": "2025-04-15 12:03:17.301846",
    "Solar_Irradiance_W/m2": 217.37908526808354,
    "Panel_Temperature_C": 36.90579192441389,
    "Ambient_Temperature_C": 28.133433695359095,
    "Cloud_Cover_%": 81.69739072718367,
    "Energy_Generated_kWh": 79.03822985338455,
    "CO2_Saved_kg": 54.19705608357266,
    "Money_Saved_INR": 474.22937912030727
  },
  {
    "Date": "2025-04-16 12:03:17.301846",
    "Solar_Irradiance_W/m2": 173.01201598453193,
    "Panel_Temperature_C": 41.44876377041373,
    "Ambient_Temperature_C": 26.995289057909368,
    "Cloud_Cover_%": 85.25474212459704,
    "Energy_Generated_kWh": 76.3369905789341,
    "CO2_Saved_kg": 52.76581505591049,
    "Money_Saved_INR": 458.02194347360467
  },
  {
    "Date": "2025-04-17 12:03:17.301846",
    "Solar_Irradiance_W/m2": 161.08476372988437,
    "Panel_Temperature_C": 38.365906756349794,
    "Ambient_Temperature_C": 34.11987288839504,
    "Cloud_Cover_%": 93.79652314338942,
    "Energy_Generated_kWh": 72.86653731640257,
    "CO2_Saved_kg": 50.0855608082435,
    "Money_Saved_INR": 437.1992238984154
  }
    ]
    """
    data = json.loads(json_data)
    df = pd.DataFrame(data)
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    df['solar_irradiance'] = df['Solar_Irradiance_W/m2'] * 0.001
    return df

def create_dashboard():
    # Mobile detection (simple approach)
    is_mobile = st.checkbox("Mobile view", value=False, key="mobile_view", 
                          help="Check if viewing on mobile")  # For testing
    
    # Sidebar - only show config when expanded
    with st.sidebar:
        st.title("⚙️ System Config")
        system_capacity = st.number_input(
            "System Capacity (kW)", 
            min_value=1.0, 
            value=5.0, 
            step=0.5
        )
        electricity_rate = st.number_input(
            "Electricity Rate ($/kWh)",
            min_value=0.01,
            value=0.15,
            step=0.01,
            format="%.2f"
        )

    # Load data
    df = load_solar_data()
    df['energy_kwh'] = df['Energy_Generated_kWh']
    df['co2_saved_kg'] = df['CO2_Saved_kg']
    df['cost_saved'] = df['Money_Saved_INR'] / 83.0

    # Dashboard UI
    st.title("☀️ Solar Dashboard")
    
    # Mobile-optimized metrics
    if is_mobile:  # Or use actual mobile detection
        cols = st.columns(2)
        with cols[0]:
            st.metric("Energy", f"{df['energy_kwh'].iloc[-1]:.1f} kWh")
            st.metric("CO₂ Saved", f"{df['co2_saved_kg'].iloc[-1]:.1f} kg")
        with cols[1]:
            st.metric("Savings", f"${df['cost_saved'].iloc[-1]:.2f}")
            st.metric("Capacity", f"{system_capacity} kW")
    else:
        cols = st.columns(4)
        cols[0].metric("Energy", f"{df['energy_kwh'].iloc[-1]:.1f} kWh")
        cols[1].metric("CO₂ Saved", f"{df['co2_saved_kg'].iloc[-1]:.1f} kg")
        cols[2].metric("Savings", f"${df['cost_saved'].iloc[-1]:.2f}")
        cols[3].metric("Capacity", f"{system_capacity} kW")

    # Time period selector - full width on mobile
    time_period = st.selectbox("Time Period:", 
                             ["Last 7 Days", "Last 30 Days", "All Data"],
                             index=1)

    if time_period == "Last 7 Days":
        plot_data = df.loc[df.index >= (datetime.now() - timedelta(days=7))]
    elif time_period == "Last 30 Days":
        plot_data = df.loc[df.index >= (datetime.now() - timedelta(days=30))]
    else:
        plot_data = df

    # Mobile-optimized charts
    if is_mobile:
        # Single column layout for mobile
        fig = px.line(plot_data, x=plot_data.index, y='energy_kwh',
                     title=f'Energy Generation',
                     height=300)  # Smaller height for mobile
        st.plotly_chart(fig, use_container_width=True)
        
        fig = px.line(plot_data, x=plot_data.index, y='co2_saved_kg',
                     title=f'CO₂ Saved',
                     height=300)
        st.plotly_chart(fig, use_container_width=True)
        
        fig = px.line(plot_data, x=plot_data.index, y='solar_irradiance',
                     title=f'Solar Irradiance',
                     height=300)
        st.plotly_chart(fig, use_container_width=True)
    else:
        # Two-column layout for desktop
        col1, col2 = st.columns(2)
        with col1:
            fig = px.line(plot_data, x=plot_data.index, y='energy_kwh',
                         title=f'Energy Generation')
            st.plotly_chart(fig, use_container_width=True)
            
            fig = px.line(plot_data, x=plot_data.index, y='solar_irradiance',
                         title=f'Solar Irradiance')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.line(plot_data, x=plot_data.index, y='co2_saved_kg',
                         title=f'CO₂ Saved')
            st.plotly_chart(fig, use_container_width=True)
            
            fig = px.line(plot_data, x=plot_data.index, y='cost_saved',
                         title=f'Cost Savings')
            st.plotly_chart(fig, use_container_width=True)

    # Summary table
    st.subheader("Summary")
    st.dataframe(
        plot_data[['energy_kwh', 'co2_saved_kg', 'cost_saved']].describe()
        .style.format("{:.2f}"),
        use_container_width=True
    )

if __name__ == "__main__":
    create_dashboard()
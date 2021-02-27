from pyowm import OWM
from pyowm.utils import config
from pyowm.utils import timestamps
import json

def weather(ao):
    token=''
    with open("config.json") as f:
        data = json.loads(f.read())
        token = data["weather_token"]

    owm = OWM(token)
    
    mgr = owm.weather_manager()


    # Search for current weather in London (Great Britain) and get details
    try: observation = mgr.weather_at_place(ao+', IT')
    except: return "Qualcosa è andato storto"
    
    w = observation.weather
    r=''
    r+=w.detailed_status.capitalize()+'\n'         # 'clouds'
    r+='Velocità del vento(m/s): '+str(w.wind().get('speed'))+'\n'             # {'speed': 4.6, 'deg': 330}
    r+='Umidità: '+str(w.humidity)+'\n'                # 87
    r+='Temperatura attuale: '+str(w.temperature('celsius').get('temp'))+'\n'  # {'temp_max': 10.5, 'temp': 9.7, 'temp_min': 9.0}
    r+='Temperatura max/min: '+str(w.temperature('celsius').get('temp_max'))+'/'+str(w.temperature('celsius').get('temp_min'))+'\n'  # {'temp_max': 10.5, 'temp': 9.7, 'temp_min': 9.0}
    r+='Temperatura percepita: '+str(w.temperature('celsius').get('feels_like'))+'\n'  # {'temp_max': 10.5, 'temp': 9.7, 'temp_min': 9.0}
    r+='Pioggia (mm/h): '+str(w.rain.get('1h'))+'\n'                    # {}
    r+='UV: '+str(w.heat_index)+'\n'              # None
    r+='Nuvole: '+str(w.clouds)+'%'                  # 75
    
    return r

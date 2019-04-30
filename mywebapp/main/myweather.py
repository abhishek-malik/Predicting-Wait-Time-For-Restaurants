from yahoo_weather.weather import YahooWeather
from yahoo_weather.config.units import Unit
weather = YahooWeather(APP_ID="",
                     api_key="",
                     api_secret="")

weather.get_yahoo_weather_by_city("Vellore", Unit.celsius)
print(weather.condition.text)
print(weather.condition.temperature)
print(weather.condition.code)

'''
weather.get_yahoo_weather_by_location(35.67194, 51.424438)
print(weather.condition.text)
print(weather.condition.temperature)
'''
weather_code = [0,0,0,0,0,0,0]
temperature = [0,0,0,0,0,0,0]
new_weather = weather.get_forecasts()
for i in range(0,7):
	weather_code[i] = new_weather[i].code
	temperature[i] = new_weather[i].high
	#print(new_weather[i].text,new_weather[i].code,new_weather[i].high)

for i in range(0,7):
	print(weather_code[i], temperature[i])

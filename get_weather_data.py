import argparse, datetime
from Custom_modules.get_sg_weather_api import *
from Custom_modules.telegram_bot import send_text

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--task", choices=["2h", "24h", "96h"], required=True)
    parser.add_argument("--area", type=str, default="Bukit Merah")
    args = parser.parse_args()
    
    if args.task == "2h":
        weather = get_2hr_forecast()
        output = extract_forecast_2h(weather, args.area, station_name=station_name)
    elif args.task == "24h":
        weather = get_24hr_forecast()
        output = extract_forecast_24h(weather)
    else:
        weather = get_4day_outlook()
        output = extract_forecast_4day(weather)
    
    send_text(f"Weather update ({args.task}):\n{'\n'.join(output)}")
    # print(f"Weather update ({args.task}):\n{'\n'.join(output)}")
    
if __name__ == "__main__":
    main()
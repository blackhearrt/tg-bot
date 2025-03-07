from datetime import datetime

def get_time_info():
    now = datetime.now()
    days_of_week = {0: "Понеділок", 1: "Вівторок", 2: "Середа", 3: "Четвер", 4: "П'ятниця", 5: "Субота", 6: "Неділя"}
    day_name = days_of_week[now.weekday()]
    formatted_time = now.strftime("%H:%M")
    formatted_day = now.strftime("%d.%m.%Y")
    return f"{day_name}, {formatted_time} | {formatted_day}"

def get_greeting():
    now = datetime.now().time()
    if now >= datetime.strptime("05:01", "%H:%M").time() and now <= datetime.strptime("11:30", "%H:%M").time():
        return "Доброго ранку"
    elif now >= datetime.strptime("11:31", "%H:%M").time() and now <= datetime.strptime("16:30", "%H:%M").time():
        return "Доброго дня"
    elif now >= datetime.strptime("16:31", "%H:%M").time() and now <= datetime.strptime("23:00", "%H:%M").time():
        return "Доброго вечора"
    else:
        return "Доброї ночі"
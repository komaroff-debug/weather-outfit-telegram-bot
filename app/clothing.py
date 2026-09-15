def comfort_score(feels, wind, rain_prob, humidity):
    score = 10
    if feels <= -20: score -= 5
    elif feels <= -10: score -= 4
    elif feels <= 0: score -= 2
    elif feels >= 30: score -= 4
    elif feels >= 25: score -= 2
    if wind >= 12: score -= 3
    elif wind >= 8: score -= 2
    elif wind >= 5: score -= 1
    if rain_prob >= 80: score -= 2
    elif rain_prob >= 50: score -= 1
    if humidity >= 90: score -= 1
    return max(1, min(10, score))

def advice(temperature, feels, humidity, rain_prob, wind, snowfall, rain, mode="general"):
    clothes, shoes, accessories, reasons = [], [], [], []

    if feels <= -20:
        clothes += ["очень тёплая зимняя куртка","тёплый свитер или флиска","термобельё","утеплённые брюки"]
        shoes += ["тёплые зимние непромокаемые ботинки"]
        accessories += ["тёплая шапка","утеплённые перчатки","шарф или бафф"]
        reasons.append("очень холодно")
    elif feels <= -10:
        clothes += ["зимняя куртка","тёплый свитер","плотные брюки"]
        shoes += ["утеплённые зимние ботинки"]
        accessories += ["шапка","перчатки"]
        reasons.append("температура ниже −10°C")
    elif feels <= 0:
        clothes += ["тёплая зимняя или демисезонная куртка","свитер или толстовка","плотные брюки"]
        shoes += ["утеплённые ботинки"]
        accessories += ["шапка","перчатки"]
        reasons.append("около нуля или ниже")
    elif feels <= 8:
        clothes += ["тёплая демисезонная куртка","свитер или толстовка","джинсы или плотные брюки"]
        shoes += ["кроссовки или демисезонные ботинки"]
        accessories += ["лёгкая шапка"]
        reasons.append("прохладная погода")
    elif feels <= 15:
        clothes += ["демисезонная куртка","свитер или лёгкая кофта","джинсы или брюки"]
        shoes += ["кроссовки или лёгкие ботинки"]
        reasons.append("умеренно прохладно")
    elif feels <= 20:
        clothes += ["лёгкая куртка или ветровка","футболка","джинсы или лёгкие брюки"]
        shoes += ["кроссовки"]
        reasons.append("комфортная прохладная погода")
    elif feels <= 25:
        clothes += ["футболка","лёгкие брюки или шорты"]
        shoes += ["кроссовки или лёгкая обувь"]
        reasons.append("тепло")
    else:
        clothes += ["лёгкая футболка","шорты или лёгкие брюки"]
        shoes += ["лёгкая обувь"]
        reasons.append("жаркая погода")

    if wind >= 10:
        accessories.append("ветрозащитный верхний слой")
        reasons.append("сильный ветер")
    elif wind >= 6:
        reasons.append("ветер снижает ощущаемую температуру")

    if rain_prob >= 50 or rain > 0:
        shoes = ["непромокаемые кроссовки или ботинки"]
        accessories.append("зонт")
        reasons.append("возможны осадки")

    if snowfall > 0:
        shoes = ["утеплённые непромокаемые ботинки"]
        accessories += ["непромокаемая верхняя одежда"]
        reasons.append("ожидается снег")

    if humidity >= 85 and feels <= 15:
        reasons.append("высокая влажность усиливает ощущение холода")

    if mode == "walk":
        clothes.append("дополнительный слой для длительной прогулки")
    elif mode == "work":
        clothes.append("дополнительный слой для прохладных помещений")
    elif mode == "sport":
        clothes = ["спортивная одежда по погоде"]
        if feels < 10: clothes.append("лёгкий утепляющий слой")
        if wind >= 6: clothes.append("ветрозащитная спортивная куртка")
        shoes = ["спортивные кроссовки"]

    return {
        "clothes": clothes,
        "shoes": list(dict.fromkeys(shoes)),
        "accessories": list(dict.fromkeys(accessories)),
        "reasons": list(dict.fromkeys(reasons)),
        "score": comfort_score(feels, wind, rain_prob, humidity)
    }

import datetime as dt
import statistics
import typing as tp

from homework05.vkapi.friends import get_friends


def age_predict(user_id: int) -> tp.Optional[float]:
    """
    Наивный прогноз возраста пользователя по возрасту его друзей.

    Возраст считается как медиана среди возраста всех друзей пользователя

    :param user_id: Идентификатор пользователя.
    :return: Медианный возраст пользователя.
    """

    items = get_friends(user_id, fields=["bdate"]).items
    today = dt.datetime.now()
    year = today.year
    age = []
    for i in items:
        if "bdate" in i:
            if len(i["bdate"]) >= 9:
                age.append(year - int(i["bdate"][-4:]))
    if age:
        average_age = statistics.mean(age)
    else:
        average_age = None
    return average_age


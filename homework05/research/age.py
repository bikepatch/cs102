import datetime as dt
import statistics
import typing as tp

from vkapi.friends import get_friends


def age_predict(user_id: int) -> tp.Optional[float]:
    """
    Наивный прогноз возраста пользователя по возрасту его друзей.

    Возраст считается как медиана среди возраста всех друзей пользователя

    :param user_id: Идентификатор пользователя.
    :return: Медианный возраст пользователя.
    """
    assert user_id > 0, "user_id must be positive integer"
    ages = []
    friends = get_friends(user_id, "bdate").items  # type: ignore
    for friend in friends:
        try:
            bdate = dt.datetime.strptime(friend["bdate"], "%d.%m.%Y")  # type: ignore
            current_time = dt.datetime.today()
            age = current_time.year - bdate.year
            if (bdate.month > current_time.month) or (
                bdate.month == current_time.month and bdate.day > current_time.day
            ):
                age -= 1
            ages.append(age)
        except (KeyError, ValueError):
            continue
    try:
        return statistics.median(ages)
    except statistics.StatisticsError:
        return None

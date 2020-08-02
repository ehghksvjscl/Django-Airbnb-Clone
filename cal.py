# import calendar하려면 이름이 carendar.py로 해서는 안된다.
from django.utils import timezone
import calendar

class Day:
    def __init__(self, number, past):
        self.number = number
        self.past = past

    def __str__(self):
        return str(self.number)
    
class Calendar(calendar.Calendar):
    def __init__(self, year, month):
        super().__init__(firstweekday=6)
        self.month = month
        self.year = year
        self.day_name = (
            "일",
            "월",
            "화",
            "수",
            "목",
            "금",
            "토",
        )
        self.months_name = (
            "1월",
            "2월",
            "3월",
            "4월",
            "5월",
            "6월",
            "7월",
            "8월",
            "9월",
            "10월",
            "11월",
            "12월",
        )

    def get_days(self):
        weeks = self.monthdays2calendar(self.year, self.month)
        days = []
        for week in weeks:
            for day, _ in week:
                now = timezone.now()
                today = now.day
                month = now.month
                past = False
                if month <= self.month:
                    if day < today:
                        past = True
                new_day =Day(day,past)
                days.append(new_day)
        return days

    def get_month(self):
        return self.months_name[self.month - 1]

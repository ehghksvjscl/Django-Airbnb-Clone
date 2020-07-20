# import calendar하려면 이름이 carendar.py로 해서는 안된다.
import calendar


class Calendar:
    def __init__(self, year, month):
        self.month = month
        self.year = year
        self.day_name = (
            "월",
            "화",
            "수",
            "목",
            "금",
            "토",
            "일",
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

    def get_month(self):
        return self.months_name[self.month - 1]


#dgdsjgsd
class TableParser:
    def __init__(self):
        self.table={"days_number":0,"lessons":[]}
    def parse(self,json_table):
        old_name=""
        for row in json_table:
            day_table = {}
            day_table["dayOfWeek"]=row["dayOfWeekString"]
            day_table["beginLesson"]=row["beginLesson"]
            day_table["endLesson"]=row["endLesson"]
            day_table["kindOfWork"]=row["kindOfWork"]
            day_table["discipline"]=row["discipline"]
            day_table["auditorium"]=row["auditorium"]
            day_table["building"]=row["building"]
            day_table["lecturer"]=row["lecturer"]
            day_table["date"]=row["date"]
            self.table['lessons'].append(day_table)

            if day_table['dayOfWeek']!=old_name:
                self.table['days_number']+=1
            old_name=day_table['dayOfWeek']
        return self.table
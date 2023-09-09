from TableParser import TableParser
from UnnSession import UnnSession
import config

if __name__=="__main__":
    session=UnnSession()
    session.login()
    parsed_table=TableParser(session.get_table()).parse()
    for i in parsed_table:
        print(i)

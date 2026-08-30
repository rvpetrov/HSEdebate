from extras import __connect_to_sheet__, rooms_url, stats_url, conn, cur
from gspread import Worksheet
from time import sleep

cur.execute("""
    create table if not exists speaks (
        name text,
        speaks_data text 
    )
""")
conn.commit()
cur.execute("""
    create table if not exists places (
        name text,
        places_data text 
    )
""")
conn.commit()


def __tuple_to_dict__(__tuple: tuple) -> dict:
    __dict = {}
    for el in __tuple:
        __dict[el[0]] = el[1]
    return __dict


def __dict_to_tuple__(__dict: dict) -> tuple:
    __tuple = []
    for key in __dict.keys():
        __tuple.append(tuple([key, str(__dict[key])]))
    return tuple(__tuple)


def main():
    print("0 - Выгрузить статистику по спикам\n1 - Выгрузить статистику по местам\n2 - Собрать статистику по спикам\n3 - Собрать статистику по местам")
    check = int(input(">>> "))
    match check:
        case 0:
            worksheet: Worksheet = __connect_to_sheet__(url=stats_url)
            worksheet.update_cell(row=1, col=1, value="Спикер")
            worksheet.update_cell(row=1, col=2, value="Динамика (развернуть)")
            worksheet.update_cell(row=1, col=3, value="Средний спик")
            sleep(0.5)
            cur.execute("select * from speaks")
            data = cur.fetchall()
            for el in data:
                next_row: int = len(worksheet.col_values(col=1)) + 1
                worksheet.update_cell(row=next_row, col=1, value=el[0])
                worksheet.update_cell(row=next_row, col=2, value=el[1][1:-1].replace("'", ""))
                worksheet.update_cell(row=next_row, col=3, value=round(sum(int(e) for e in eval(el[1])) / len(eval(el[1])), 3))
                sleep(0.5)
        case 1:
            worksheet: Worksheet = __connect_to_sheet__(url=stats_url)
            worksheet.update_cell(row=1, col=1, value="Спикер")
            worksheet.update_cell(row=1, col=2, value="Динамика (развернуть)")
            worksheet.update_cell(row=1, col=3, value="Среднее место")
            sleep(0.5)
            cur.execute("select * from places")
            data = cur.fetchall()
            for el in data:
                next_row: int = len(worksheet.col_values(col=1)) + 1
                worksheet.update_cell(row=next_row, col=1, value=el[0])
                worksheet.update_cell(row=next_row, col=2, value=el[1][1:-1].replace("'", ""))
                worksheet.update_cell(row=next_row, col=3, value=round(sum(int(e) for e in eval(el[1])) / len(eval(el[1])), 3))
                sleep(0.5)
        case 2:
            worksheet: Worksheet = __connect_to_sheet__(url=rooms_url)
            data = worksheet.get_all_values()
            data_clear = []
            speaks = {}
            for el in data:
                if el.count("Аудитория") == 0 and set(el) != {"ㅤ", ""}:
                    data_clear.append(el)
            for i in range(0, len(data_clear), 2):
                for j in [0, 1, 3, 4]:
                    speaks[data_clear[i][j]] = data_clear[i + 1][j]
            cur.execute("select * from speaks")
            data_people = __tuple_to_dict__(cur.fetchall())
            for key in speaks.keys():
                spks = eval(data_people[key]) if key in data_people else []
                spks.append(speaks[key])
                data_people[key] = spks
            data_people = __dict_to_tuple__(data_people)
            for el in data_people:
                cur.execute("select * from speaks where name = %s", (el[0],))
                if cur.fetchone() is not None:
                    cur.execute("update speaks set speaks_data = %s where name = %s", (el[1], el[0]))
                else:
                    cur.execute("insert into speaks (name, speaks_data) values (%s, %s)", el)
                conn.commit()
        case 3:
            worksheet: Worksheet = __connect_to_sheet__(url=rooms_url)
            data = worksheet.get_all_values()
            data_clear = []
            places = {}
            for el in data:
                if el.count("Аудитория") == 0 and set(el) != {"ㅤ", ""}:
                    data_clear.append(el)

            # todo парсить места из бэллотов
            """
            for i in range(0, len(data_clear), 2):
                for j in [0, 1, 3, 4]:
                    speaks[data_clear[i][j]] = data_clear[i + 1][j]
            cur.execute("select * from places")
            data_people = __tuple_to_dict__(cur.fetchall())
            for key in speaks.keys():
                spks = eval(data_people[key]) if key in data_people else []
                spks.append(speaks[key])
                data_people[key] = spks
            data_people = __dict_to_tuple__(data_people)
            for el in data_people:
                cur.execute("select * from places where name = %s", (el[0],))
                if cur.fetchone() is not None:
                    cur.execute("update places set places_data = %s where name = %s", (el[1], el[0]))
                else:
                    cur.execute("insert into places (name, places_data) values (%s, %s)", el)
                conn.commit()
            """
    print("done!")


if __name__ == "__main__":
    main()

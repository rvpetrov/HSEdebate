from extras import __connect_to_sheet__, regs_url, rooms_url
from random import shuffle, sample
from gspread import Worksheet
from time import sleep


def main():
    worksheet: Worksheet = __connect_to_sheet__(url=regs_url, __is_for_stat=None)
    data = []
    for i in range(len(worksheet.col_values(2)[1:])):
        data.append(worksheet.row_values(i+2)[1:])
    regs = worksheet.col_values(2)[1:]
    wishes = worksheet.col_values(3)[1:]
    if len(set(wishes)) != len(wishes) - wishes.count(""):
        conflicts = []
        for el in wishes:
            if el != "" and wishes.count(el) != 1 and el not in conflicts:
                conflicts.append(el)
    else:
        conflicts = None
    teams = []
    __elements = []
    if len(wishes) != 0:
        for i in range(len(wishes)):
            if wishes[i] != "":
                if [regs[i], wishes[i]] not in teams and [wishes[i], regs[i]] not in teams:
                    teams.append([regs[i].lower().title(), wishes[i].lower().title()])
                    __elements.append(regs[i])
                    if wishes[i] in regs:
                        __elements.append(wishes[i])
        for el in __elements:
            if el in regs:
                del regs[regs.index(el)]
    shuffle(regs)
    for i in range(0, len(regs), 2):
        try:
            teams.append([regs[i].lower().title(), regs[i + 1].lower().title()])
        except IndexError:
            try:
                teams.append([regs[i].lower().title(), regs[i].lower().title()])
            except IndexError:
                pass
    shuffle(teams)
    rooms = []
    extras = None
    while len(teams) != 0:
        try:
            room = sample(teams, 4)
        except ValueError:
            try:
                room = sample(teams, 2)
            except ValueError:
                extras = teams
                break
        rooms.append(room)
        for team in room:
            del teams[teams.index(team)]
    worksheet: Worksheet = __connect_to_sheet__(url=rooms_url, __is_for_stat=None)
    for room in rooms:
        if len(room) == 4:
            data = [
                ["Аудитория", "", "Судья", ""], ["ㅤ"],
                [room[0][0], room[0][1], "", room[1][0], room[1][1]],
                ["ㅤ"],
                [room[2][0], room[2][1], "", room[3][0], room[3][1]],
                ["ㅤ"], ["ㅤ"]
            ]
        else:
            data = [
                ["Аудитория", "", "Судья", ""], ["ㅤ"],
                [room[0][0], room[0][1], "", room[1][0], room[1][1]],
                ["ㅤ"], ["ㅤ"]
            ]
        for row in data:
            next_row = len(worksheet.col_values(col=1)) + 1
            for i in range(len(row)):
                worksheet.update_cell(row=next_row, col=i+1, value=row[i])
            sleep(0.5)
    if extras is not None:
        next_row = len(worksheet.col_values(col=1)) + 1
        worksheet.update_cell(row=next_row, col=1, value="Не поместились")
        sleep(0.5)
        extras_data = ""
        for extra in extras:
            extras_data += f"{extra[0]}, {extra[1]}, "
        next_row = len(worksheet.col_values(col=1)) + 1
        worksheet.update_cell(row=next_row, col=1, value=extras_data)
    if conflicts is not None:
        next_row = len(worksheet.col_values(col=1)) + 1
        worksheet.update_cell(row=next_row, col=1, value="Конфликты")
        sleep(0.5)
        conflicts_data = ""
        for conflict in conflicts:
            conflicts_data += f"{conflict}, "
        next_row = len(worksheet.col_values(col=1)) + 1
        worksheet.update_cell(row=next_row, col=1, value=conflicts_data)
    print("done!")


if __name__ == "__main__":
    main()

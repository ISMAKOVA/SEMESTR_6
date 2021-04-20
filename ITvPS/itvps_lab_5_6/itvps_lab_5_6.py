from bs4 import BeautifulSoup as Bs
import requests
import pandas as pd


url = 'https://soccer365.ru/competitions/13/'

html = requests.get(url).text
soup = Bs(html, 'html.parser')
tables = soup.find_all('table', class_='comp_table_v2')
data = {}
i = 0
for table in tables:
    tr_s = table.select('tr')
    role = table.find('th', class_='title').text.replace('\xa0\xa0', '')
    for tr in tr_s:
        td_s = tr.find_all('td')
        if len(td_s) != 0:
            team = td_s[0].find_all('span')[0]['title']
            player = td_s[0].find_all('span')[1].text
            if i == 0:
                goals = int(td_s[1].text)
                penalty = int(td_s[2].text) if td_s[2].text != "\xa0" else 0
                games = int(td_s[3].text)
                data[player] = [team, player, role, goals, penalty, 0, games, 0, 0, 0, 0, 0]
            elif i == 1:
                passes = int(td_s[1].text)
                games = int(td_s[2].text)
                if player in data:
                    data[player][2] = [data[player][2], role]
                    data[player][5] = passes
                else:
                    data[player] = [team, player, role, 0, 0, passes, games, 0, 0, 0, 0, 0]

            elif i == 2:
                fair_play, yellow_card,  = int(td_s[1].text), int(td_s[2].text)
                yellow_card2 = int(td_s[3].text) if td_s[3].text != "\xa0" else 0
                red_card = int(td_s[4].text) if td_s[4].text != "\xa0" else 0
                is_punishment = 0 if fair_play == 0 else 1
                games = int(td_s[2].text) if td_s[2].text != "\xa0" else 0
                if player in data:
                    data[player][7] = is_punishment
                    data[player][8] = fair_play
                    data[player][9] = yellow_card
                    data[player][10] = yellow_card2
                    data[player][11] = red_card
                else:
                    data[player] = [team, player, "не определено", 0, 0, 0, games, is_punishment, fair_play,
                                    yellow_card, yellow_card2, red_card]

    i += 1

print(data)
df = pd.DataFrame(data.values(), columns=['team', 'name', 'role', 'goals', 'penalty', 'pass', 'games', 'punishment', 'fair_play',
                                 'ycard', 'ycard2', 'rcard'])
print(df)

# Analytics----------------------------------------------------------------

# Первая тройка команд по числу забитых голов с выводом их числа
print("Первая тройка команд по числу забитых голов с выводом их числа")
best_teams = df.groupby('team')['goals'].sum() \
                             .reset_index(name='goals_sum') \
                             .sort_values(['goals_sum'], ascending=False) \
                             .head(3)
print(best_teams)

# Первая тройка команд по числу желтых карточек.
print("Первая тройка команд по числу желтых карточек.")
yellow_cards = df.groupby('team')['ycard'].sum() \
                             .reset_index(name='ycard_sum') \
                             .sort_values(['ycard_sum'], ascending=False) \
                             .head(3)
print(yellow_cards)

# Список игроков, которые участвовали не во всех играх своей команды.
# Число игр команды определить по максимальному числу матчей ее игроков
print("Список игроков, которые участвовали не во всех играх своей команды.")
not_participate = df.groupby('team')['games'].transform(max) != df['games']
print(df[not_participate])

# Доля пенальти по отношению к числу голов для каждой команды.
print("Доля пенальти по отношению к числу голов для каждой команды.")
penalty_part = df.groupby('team').sum().eval('proportion = penalty / goals')
print(penalty_part)

# Корреляция числа голов с количеством очков команды. Очки взять из первой таблицы на странице по рейтингу команд.
print("Корреляция числа голов с количеством очков команды. ")
table2 = soup.find('table', class_='stngs')
tr_s = table2.select('tr')
point = []
for tr in tr_s:
    td = tr.find_all('td')
    if len(td) != 0:
        team = td[1].find('span').text
        point.append([team, int(td[9].text)])

df1 = df.groupby('team')['goals'].sum()
df2 = pd.DataFrame(point, columns=['team', 'point'])
merge_df = pd.merge(df1, df2, on='team')
res = merge_df.corr()
print(res)
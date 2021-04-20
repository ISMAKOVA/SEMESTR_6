import pandas as pd
from selenium import webdriver

driver = webdriver.Chrome()
driver.get("https://soccer365.ru/competitions/13/players/")

table = driver.find_element_by_xpath('//table[@id="players_all"]')
data = [[td.text.replace('\n', '') for td in tr.find_elements_by_xpath('td')
         if len(tr.find_elements_by_xpath('td')) == 14]
        for tr in table.find_elements_by_xpath('//tr')]


df = pd.DataFrame(data, columns=['Player', 'Goal', 'Pass', 'Games', 'Timer', 'Goal_pass',
                                 'Pengoal', 'Goalx2', 'Goalx3', 'Owngoal', 'Ycard', 'Yred', 'Rcard', 'Point'])
print(df)
df.to_csv(r'table.csv', index=False, header=True)
driver.quit()



import numpy as np
import pandas as pd


def max_mean_diabetes(df):
    mark_1 = df.query('mark==1')
    return mark_1['age'].max(), mark_1['age'].mean()


def get_correlation(df):
    correlation = df.corr()
    max = 0
    name_column1 = ""
    name_column2 = ""
    for i in correlation:
        for j in range(len(correlation[i])):
            if correlation[i][j] != 1 and correlation[i][j] > max:
                max = correlation[i][j]
                name_column1 = i
                name_column2 = correlation.columns[j]
    return name_column1, name_column2, max


def get_childfree_part(df):
    no_diabetes = df.query("mark==0")
    return len(no_diabetes.query("num_child==0"))/len(no_diabetes)


def max_glucose(df):
    age50 = df.query("age>=50")
    return age50["glucose"].max()


def pressure(df):
    pressure80 = df.query("art_pressure>=80")
    return pressure80['age'].mean()


def list_patients(df):
    patient60 = df.query("age>=60")
    mean = patient60["insulin"].mean()
    return patient60.query(str.format("insulin>={0}", mean)).sort_values(by="age")


def zero_values(df):
    return df.query("glucose==0 or art_pressure==0 or skin_fat==0 or insulin==0 or bmi==0 or diabetes_pedegree==0 or age==0")

df = pd.read_csv('prima-indians-diabetes.csv',
                 names=['num_child', 'glucose', 'art_pressure', 'skin_fat', 'insulin', 'bmi', 'diabetes_pedegree',
                        'age', 'mark'])

max_mean = max_mean_diabetes(df)
correlation = get_correlation(df)
childfree_part = get_childfree_part(df)
max_glucose = max_glucose(df)
pressure = pressure(df)
list_patients = list_patients(df)
zero_values = zero_values(df)
print("1.	Максимальный и средний возраст пациентов с установленным диабетом: ", max_mean)
print("2.	Параметры с максимальной корреляцией между собой, значение корреляции: ", correlation)
print("3.	Доля бездетных среди пациентов с неустановленным диабетом: ", childfree_part)
print("4.	Максимальная концентрация глюкозы у пациентов старше 50 лет: ", max_glucose)
print("5.	Средний возраст пациентов с диастолическим давлением выше 80: ", pressure)
print("6.	Список пациентов старше 60 с уровнем инсулина выше среднего, отсортированный по возрастанию столбца Возраст: \n", list_patients)
print("7.	Список записей с нулевыми значениями хотя бы одного параметра (за исключением первого и последнего столбцов): \n", zero_values)

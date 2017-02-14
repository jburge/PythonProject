"""
Question 1

select *
from country
where population > 50000000
order by population DESC limit 10

Description: All information about the top 10 countries with populations over 50,000,000 descending by population size.
"""

"""
Question 2
select Continent, count(*) As Number_Countries, sum(population) As Population from country
where population > 0
group by Continent
order by 1 asc

Description: The total number of countries and the total population on each continent, ordered alphabetically.
"""

"""
Question 3
select city.Name As City, city.Population
from city
inner join country ON city.CountryCode = country.code
where country.code = 'USA'
order by city.population DESC limit 10

Description: Top 10 most populous cities in the United States sorted descending by population.
"""

"""
Question 4
select country.Name, Language, (Percentage * population) / 100
from countrylanguage
inner join country on countrylanguage.CountryCode = country.code
where IsOfficial = True
order by 3 DESC limit 10

Description: Find the number of people in each country who speak the official language, then find the top 10 populations and sort descending by population.
"""

"""
Question 5
select Language, sum((Percentage * population) / 100)
from countrylanguage
inner join country ON countrylanguage.CountryCode = country.code
group by Language
order by 2 desc limit 5

Description: Find the top 5 spoken languages in the world.
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pymysql

def CreateConnection():
	'''Creates a connection with the world database and initializes the three tables as Pandas DataFrames.i
	'''
	global df_country, df_city, df_countrylanguage
	cnx = pymysql.connect(user='root', \
	      password='lowell21', \
	      host= '127.0.0.1', \
	      port=3306, \
	      db='world', \
	      autocommit=True)

	df_country = pd.read_sql_query('select * from Country', con=cnx)
	df_city = pd.read_sql_query('select * from city', con=cnx)
	df_countrylanguage = pd.read_sql_query('select * from countrylanguage', con=cnx)

def question1():
	sub = df_country.query('(Population > 50000000)').sort_values(['Population'], ascending = False).head(n = 10).reset_index(drop = True)
	return(sub)

def question2():
	sub = df_country.query('(Population > 0)').groupby(by = ['Continent']).agg({'Name':'count', 'Population':'sum', }).sort_index(ascending = True)
	sub.columns = ['Number of countries', 'Population']
	return(sub)

def question3():
	sub = pd.merge(df_country, df_city, left_on = 'Code', right_on = 'CountryCode')
	sub = sub[sub.Code == 'USA'][['Name_y', 'Population_y']].sort_values('Population_y', ascending = False).head(n = 10).reset_index(drop = True)
	sub.columns = ('City', 'Population')
	return(sub)

def question4():
	sub = pd.merge(df_country, df_countrylanguage, left_on = 'Code', right_on = 'CountryCode')
	sub['(Percentage * population) / 100'] = sub.Percentage * sub.Population / 100
	sub = sub[sub.IsOfficial == 'T'][['Name', 'Language', '(Percentage * population) / 100']].sort_values('(Percentage * population) / 100', ascending = False).head(n = 10).reset_index(drop = True)
	return(sub)

def question5():
	sub = pd.merge(df_country, df_countrylanguage, left_on = 'Code', right_on = 'CountryCode')
	sub['(Percentage * population) / 100'] = sub.Percentage * sub.Population / 100
	sub = sub.groupby('Language').agg({'(Percentage * population) / 100': 'sum'})
	sub = sub.sort_values('(Percentage * population) / 100', ascending = False).head(n = 5)
	sub.columns = (['sum((Percentage * population) / 100)'])
	return(sub)

def Questions():
	'''Prints questions 1 - 5.
    '''
	CreateConnection()
	print('Question 1')
	print(question1())
	print('Question 2')
	print(question2())
	print('Question 3')
	print(question3())
	print('Question 4')
	print(question4())
	print('Question 5')
	print(question5())

Questions()

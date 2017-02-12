import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


class BabyNames:
    def __init__(self, file_path):
        self.data = pd.read_pickle(file_path)
        self.states = sorted(self.data.State.unique())
        self.years = sorted(self.data.Year.unique())
        self.genders = sorted(self.data.Gender.unique())

    def GetInput(self, _state, _year):
        if _state not in self.states:
            _state = self.states
        else:
            _state = [_state]
        if _year not in self.years:
            _year = self.years
        else:
            _year = [_year]
        return _state, _year

    def Count(self, state = '', year = ''):
        state, year = self.GetInput(state, year)
        count = self.data.Count[self.data['State'].isin(state) & self.data['Year'].isin(year)].sum()
        return(count)

    def Top10BabyNames(self, state = '', year = ''):
        n = 10
        state, year = self.GetInput(state, year)
        sub = pd.DataFrame(self.data[self.data['State'].isin(state) & self.data['Year'].isin(year)])
        sub = sub.groupby(by = ['Name', 'Gender']).agg({'Count':sum}).sort_values('Count', ascending = False)
        sub['Name'] = sub.index.get_level_values(0).values
        sub['Gender'] = sub.index.get_level_values(1).values
        sub = sub.reset_index(drop = True)
        m = sub.Name[sub['Gender'] == 'M'].reset_index(drop = True).head(n)
        f = sub.Name[sub['Gender'] == 'F'].reset_index(drop = True).head(n)
        d = {'Rank': [x+1 for x in range(0, 10)], 'Female': f, 'Male':m}
        result = pd.DataFrame(data = d, columns = ['Rank', 'Female', 'Male'])
        return(result)

    def ChangeOfPopularity(self, fromYear = 2014, toYear = 2015, top = 10):
        #sub by year
        #get percentages by year
        #difference between two points in time
        #head and tail for increase and drops
        subFrom = self.data[self.data['Year'] == fromYear].drop(['Gender', 'State', 'Year'], 1).groupby('Name').sum()
        subFrom['Percent'] = subFrom['Count']/subFrom['Count'].sum() * 100
        subFrom['Name'] = subFrom.index.get_level_values(0).values
        subFrom = subFrom.reset_index(drop = True)

        subTo = self.data[self.data['Year'] == toYear].drop(['Gender', 'State', 'Year'], 1).groupby('Name').sum()
        subTo['Percent'] = subTo['Count']/subTo['Count'].sum() * 100
        subTo['Name'] = subTo.index.get_level_values(0).values
        subTo = subTo.reset_index(drop = True)

        temp = subFrom.merge(subTo, how = 'outer', on = 'Name')
        temp = temp.fillna(value = 0)
        temp['Delta'] = -temp['Percent_x'] + temp['Percent_y']
        temp = temp.sort_values('Delta', ascending = False)

        incNames = temp.ix[:,['Name', 'Delta']].head(top).reset_index(drop = True)
        decNames = temp.ix[:,['Name', 'Delta']].tail(top).sort_values('Delta').reset_index(drop = True)
        return incNames, decNames

    def Top5NamesPerYear(self, year, sex = ''):
        n = 5
        if sex not in self.genders:
            sex = self.genders
        else:
            sex = [sex]
        if year not in self.years:
            year = self.years
        else:
            year = [year]
        sub = pd.DataFrame(self.data[self.data['Year'].isin(year) & self.data['Gender'].isin(sex)]).drop('Gender', 1)
        sub = sub.groupby(by = ['State', 'Name', 'Year'], as_index = False).agg({'Count':sum}).sort_values(['State', 'Count'], ascending = [True, False]).reset_index(drop = True)

        list_ = []
        headers = ['State', 'Rank 1', 'Num 1', 'Rank 2', 'Num 2', 'Rank 3', 'Num 3', 'Rank 4', 'Num 4', 'Rank 5', 'Num 5']

        for s in self.states:
            sub_group = sub[sub.State == s].head(n = 5)
            temp_dict = {'State': s}
            for i in range(0, 5):
                temp_dict[headers[i * 2 + 1]] = sub_group.iloc[i, 1]
                temp_dict[headers[i * 2 + 2]] = sub_group.iloc[i, 3]
            list_.append(temp_dict)

        df = pd.DataFrame(list_, columns = headers)
        return(df)

    def NamePopularityPlot(self, name = 'Jim', yearRange = (2000, 2015), state = 'IL', sex = 'M'):
        range_ = [int(s) for s in self.years if s >= yearRange[0] and s <= yearRange[1]]
        sub = self.data[(self.data['State'] == state) & (self.data['Gender'] == sex) & (self.data['Year'].isin(range_))].reset_index(drop = True)
        name_count = {}
        for i in range_:
            name_count[i] = self.data[(self.data['Year'] == i) & (self.data['Name'] == name)].iloc[0,4]
        grouped = sub.groupby(by = ['Year']).agg({'Count':sum})
        year_total = {}
        for i in range_:
            year_total[i] = grouped.ix[i]['Count']
        percentages = {}
        for i in range_:
            percentages[i] = name_count[i] / year_total[i]
        final_df = pd.DataFrame(percentages, index = [0])
        ax = final_df.T.plot(title = 'Popularity of ' + name + ' in ' + state + ' from ' + str(yearRange[0]) + ' to ' + str(yearRange[1]), figsize = (8, 6))
        vals = ax.get_yticks()
        ax.set_yticklabels(['{:1.3f}%'.format(x*100) for x in vals])
        ax.xaxis.set_ticks(range_)
        ax.set_xticklabels(labels = range_, rotation = 30)
        ax.set_xlabel('Years', size = 16)
        ax.set_ylabel('% of Gender Population', size = 16)
        ax.legend([name,], loc = 'best', fontsize = 12)
        plt.show()

    def NameFlip(self, n = 10):
        fromYear = min(self.years)
        toYear = max(self.years)

        subFrom = self.data[self.data['Year'] == fromYear].drop(['State', 'Year'], 1).groupby(['Name', 'Gender']).sum()
        subFrom['Name'] = subFrom.index.get_level_values(0).values
        subFrom['Gender'] = subFrom.index.get_level_values(1).values
        subFrom = subFrom.reset_index(drop = True)
        subFrom['Male'] = subFrom['Gender'] == 'M'
        subFrom['Female'] = subFrom['Gender'] == 'F'
        subFrom = subFrom.merge(subFrom, left_on=['Name', 'Male'], right_on=['Name', 'Female'])
        temp = subFrom['Gender_x'] == 'M'
        subFrom = subFrom.ix[temp,:].drop(['Male_x', 'Female_x', 'Male_y', 'Female_y'], 1)
        subFrom['Total'] = subFrom['Count_x'] + subFrom['Count_y']
        subFrom['Prop_M'] = subFrom['Count_x']/subFrom['Total']
        subFrom['Prop_F'] = subFrom['Count_y']/subFrom['Total']
        subFrom = subFrom.drop(['Count_x', 'Gender_x', 'Count_y', 'Gender_y'], 1)
        subFrom = subFrom.reset_index(drop = True)
        ###
        subTo = self.data[self.data['Year'] == toYear].drop(['State', 'Year'], 1).groupby(['Name', 'Gender']).sum()
        subTo['Name'] = subTo.index.get_level_values(0).values
        subTo['Gender'] = subTo.index.get_level_values(1).values
        subTo = subTo.reset_index(drop = True)
        subTo['Male'] = subTo['Gender'] == 'M'
        subTo['Female'] = subTo['Gender'] == 'F'
        subTo = subTo.merge(subTo, left_on=['Name', 'Male'], right_on=['Name', 'Female'])
        temp = subTo['Gender_x'] == 'M'
        subTo = subTo.ix[temp,:].drop(['Male_x', 'Female_x', 'Male_y', 'Female_y'], 1)
        subTo['Total'] = subTo['Count_x'] + subTo['Count_y']
        subTo['Prop_M'] = subTo['Count_x']/subTo['Total']
        subTo['Prop_F'] = subTo['Count_y']/subTo['Total']
        subTo = subTo.drop(['Count_x', 'Gender_x', 'Count_y', 'Gender_y'],1)
        subTo = subTo.reset_index(drop = True)
        ###
        subDelta = subFrom.merge(subTo, on = 'Name')
        subDelta['Delta'] = -subDelta['Prop_M_x'] + subDelta['Prop_M_y']
        subDelta['Abs_Delta'] = abs(subDelta['Delta'])
        subDelta = subDelta.sort_values('Abs_Delta', ascending = False)
        subDelta = subDelta.reset_index(drop = True)
        return(subDelta.head(n))

def CreateDataFrame(pathToDataDir, df_name):
    states = ['AK', 'DC', 'IN', 'MN', 'NJ', 'RI', 'VT', 'AL', 'DE', 'KS', 'MO', 'NM', 'SC', 'WA', 'AR', 'FL', 'KY', 'MS',
    'NV', 'SD', 'WI', 'AZ', 'GA', 'LA', 'MT', 'NY', 'WV', 'CA', 'HI', 'MA', 'NC', 'OH', 'TN', 'WY', 'IA', 'MD', 'ND', 'OK',
    'TX', 'CO', 'ID', 'ME', 'NE', 'OR', 'UT', 'CT', 'IL', 'MI', 'NH', 'PA', 'VA']
    columns = ['State', 'Gender', 'Year', 'Name', 'Count']
    df = pd.DataFrame(columns = columns)
    for s in states:
        sname = pd.read_csv(r'%(1)s\\%(2)s.TXT' % {"1": pathToDataDir,"2": s}, names=columns)
        print(sname.head(2))
        print(sname.tail(2))
        df = df.append(sname, ignore_index=True)
    df.to_pickle(df_name)

df_name = './names_data.pkl'
#CreateDataFrame(r'.\\namesbystate', df_name)
lib = BabyNames(df_name)

def TestFunctions():
    print('Count Test')
    print(lib.Count(state = 'WA', year = 1993))
    print('Top 10 by state and year')
    print(lib.Top10BabyNames(state = 'WA', year = 1993))
    print('Top 5 Per Year Test')
    print(lib.Top5NamesPerYear(year = 1987, sex = 'M'))
    print(lib.Top5NamesPerYear(year = 1993))
    print('Change of Popularity Test')
    print(lib.ChangeOfPopularity(fromYear = 2014, toYear = 2015, top = 10))
    print('Flip Test')
    print(lib.NameFlip())
    lib.NamePopularityPlot(name = 'Jonathan', state = 'WA')

TestFunctions()

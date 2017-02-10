import numpy as np
import pandas as pd



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
        sub = pd.DataFrame(self.data[self.data['State'].isin(state) & self.data['Year'].isin(year)].groupby(by = ['Name', 'Gender']).Count.sum(), columns = ['Count'])
        sub = sub.sort_values('Count', ascending = False)
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
        year = [year]

        sub = pd.DataFrame(self.data[self.data['Year'].isin(year) & self.data['Gender'].isin(sex)].groupby(by = ['Name', 'State']).Count.sum(), columns = ['Count'])
        sub['Name'] = sub.index.get_level_values(0).values
        sub['State'] = sub.index.get_level_values(1).values
        sub = sub.reset_index(drop = True)
        #loop through states to create new DataFrame
        #index = [x for x in range(0,50)]
        columns = ['State', 'Rank 1', 'Rank 1 Count', 'Rank 2', 'Rank 2 Count', 'Rank 3', 'Rank 3 Count', 'Rank 4', 'Rank 4 Count', 'Rank 5', 'Rank 5 Count']
        rows = list()
        for s in self.states:
            temp = sub[sub['State'] == s].sort_values('Count', ascending = False).head(n)
            t = {'State': temp.iloc[0, 2]}
            for x in range(0, 5):
                t[columns[2*x+1]] = temp.iloc[x, 1]
                t[columns[2*x+2]] = temp.iloc[x, 0]
            rows.append(t)
        result = pd.DataFrame(rows, columns = columns)
        return(result)

    def NamePopularityPlot(self, name, yearRange, state = '', sex = ''):
        return

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

df_name = '.\\names_data.pkl'
#CreateDataFrame(r'.\\namesbystate', df_name)
lib = BabyNames(df_name)
print('Count Test')
print(lib.Count(state = 'WA', year = 1993))
print('Top 5 Per Year Test')
print(lib.Top5NamesPerYear(year = 1987, sex = 'M'))
print(lib.Top5NamesPerYear(year = 1993, sex = 'F'))
print('Change of Popularity Test')
print(lib.ChangeOfPopularity(fromYear = 2014, toYear = 2015, top = 10))
print('Flip Test')
print(lib.NameFlip())

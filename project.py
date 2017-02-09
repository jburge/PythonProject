import numpy as np
import pandas as pd



class BabyNames:
    def __init__(self, file_path):
        self.data = pd.read_pickle(file_path)
        self.states = sorted(self.data.State.unique())
        self.years = sorted(self.data.Year.unique())

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
        d = {'rank': [x+1 for x in range(0, 10)], 'female': f, 'male':m}
        result = pd.DataFrame(data = d)
        return(result)

    def ChangeOfPopularity(self, fromYear, toYear, top = 10):
        return
    def Top5NamesPerYear(self, year, sex = ''):
        return
    def NamePopularityPlot(self, name, yearRange, state = '', sex = ''):
        return
    def NameFlip(self, n = 10):
        return

def CreateDataFrame(pathToDataDir, df_name):
    states = ['AK', 'DC', 'IN', 'MN', 'NJ', 'RI', 'VT', 'AL', 'DE', 'KS', 'MO', 'NM', 'SC', 'WA', 'AR', 'FL', 'KY', 'MS', 'NV', 'SD', 'WI', 'AZ', 'GA', 'LA', 'MT', 'NY', 'WV', 'CA', 'HI', 'MA', 'NC', 'OH', 'TN', 'WY', 'IA', 'MD', 'ND', 'OK', 'TX', 'CO', 'ID', 'ME', 'NE', 'OR', 'UT', 'CT', 'IL', 'MI', 'NH', 'PA', 'VA']
    columns = ['State', 'Gender', 'Year', 'Name', 'Count']
    df = pd.DataFrame(columns = columns)
    for s in states:
        sname = pd.read_csv(r'%(1)s\\%(2)s.TXT' % {"1": pathToDataDir,"2": s}, names=columns)
        print(sname.head(2))
        print(sname.tail(2))
        df = df.append(sname, ignore_index=True)
    df.to_pickle(df_name)

df_name = 'names_data.pkl'
#CreateDataFrame(r'.\\namesbystate', df_name)
lib = BabyNames(df_name)
#print(lib.data.size)
# print(lib.data.head(n=5))
# print(lib.data.tail(n=5))
# print(lib.states)
# print(lib.years)
#print(lib.Count(state = 'WA', year = 1993))
print(lib.Top10BabyNames(state = 'WA', year = 1993))

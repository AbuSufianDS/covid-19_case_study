import numpy as np
import pandas as pd
from datetime import datetime, timedelta

class CovidDataLoader:
    def __init__(self):
        self.df = None
        self.countries = []
    def load_from_csv(self,filename):

        try:
            self.df = pd.read_csv(filename)
            print(f"Loaded data from CSV {len(self.df)}")
            print(f"Our World in Data: {self.df.shape}")
            print(f"Columns: {list(self.df.columns)[:20]}...")
            return True
        except FileNotFoundError:
            print("CSV not found, creating new CSV")
            return self.create_sample_data()


    def create_sample_data(self):
        print("Creating sample data")

        dates = pd.date_range(start = "2023-01-01",periods = 100 , freq = "D")
        countries = ["USA","INDIA","BRAZIL","UK","GERMANY"]

        data = [ ]
        for country in countries:
            base_cases = np.random.randint(1000,5000)
            trend = np.linspace(0,np.random.randint(2000,5000),100)
            seasonal = 1000 * np.sin(np.linspace(0,4*np.pi,100))
            noise = np.random.normal(0,500,100)

            cases =np.abs( base_cases + trend + seasonal + noise).astype(int)

            deaths = (cases * np.random.uniform(0.01,0.02)+np.random.normal(0,10,100)).astype(int)

            recoveries = np.zeros(100)
            for i in range(14, 100):
                recoveries[i] = int(cases[i - 14] * np.random.uniform(0.7, 0.9))

            for i, date in enumerate(dates):
                  data.append({
                          'date': date,
                           'location': country,
                           'new_cases': cases[i],
                           'total_cases': np.sum(cases[ :i + 1]),
                           'new_deaths': deaths[i],
                           'total_deaths': np.sum(deaths[ :i + 1]),
                           'new_recoveries': recoveries[i],
                           'total_recoveries': np.sum(recoveries[ :i + 1]),
                            'active_cases': max(0, np.sum(cases[ :i + 1]) - np.sum(deaths[ :i + 1]) - np.sum(recoveries[ :i + 1]))
                })
        self.df = pd.DataFrame(data)
        self.df.to_csv('sample_data.csv',index = False)
        print(f"Saved data from CSV {len(self.df)}")
        return True

    def clean_data(self):
       if self.df is None:
           print("No data to clean")
           return False
       print("Cleaning data")

       self.df['date'] = pd.to_datetime(self.df['date'])

       numeric_cols = ['new_cases','new_deaths']
       for col in numeric_cols:
           self.df[col] = self.df[col].clip(lower=0)
       self.df.fillna(0,inplace = True)
       self.df.sort_values(['location','date'], inplace = True)
       self.countries = self.df['location'].unique().tolist()
       print(f"Cleaned countries {','.join(self.countries)}")
       return True

    def country_data(self,country):
       return self.df[self.df['location']  == country].copy()

    def get_global_total(self):
       global_df = self.df.groupby('date').agg({
               'new_cases' : 'sum',
               'new_deaths' : 'sum'}).reset_index()

       global_df['total_cases'] = global_df['new_cases'].cumsum()
       global_df['total_deaths'] = global_df['new_deaths'].cumsum()

       return global_df
    def get_summary_stats(self):
       if self.df is None:
           return {}
       summary = {
           'total_countries' : len(self.countries),
           'date_range' : {
               'start' : self.df['date'].min().strftime('%Y-%m-%d'),
               'end': self.df['date'].max().strftime('%Y-%m-%d'),
               'days': (self.df['date'].max()- self.df['date'].min()).days+1
           },
           'global_total' : {
               'total_cases': int(self.df['new_cases'].sum()),
               'total_deaths': int(self.df['new_deaths'].sum()),

           }
       }
       return summary




if __name__ == "__main__":
    loader = CovidDataLoader()
    loader.load_from_csv('owid-covid-data.csv')
    countrydata = loader.country_data('USA')
    countrydata.to_csv('country_data.csv',index = False)
    grouping_data = loader.get_global_total()
    grouping_data.to_csv('Global_data.csv',index = False)
    icu_cols = [col for col in loader.df.columns if 'icu' in col.lower() or 'hosp' in col.lower() or 'million' in col.lower()]

    if icu_cols:
        print(f"Deleting columns: {icu_cols}")
        loader.df = loader.df.drop(columns=icu_cols)

        # Save to new file
    loader.df.to_csv('covid_data_no_icu.csv', index=False)
    print(f"Saved new file without ICU columns!")
    loader.clean_data()
    print(loader.get_summary_stats())


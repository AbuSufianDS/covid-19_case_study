from symbol import comparison

import pandas as pd
import numpy as np
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

class SimpleCOVIDAnalyzer:
    def __init__(self,data_loader):
        self.loader = data_loader
        self.df = data_loader.df
    def get_basic_stats(self,country):
        country_data = self.df[self.df['location'] == country]
        stats = {
            'total_cases' : int(country_data['new_cases'].sum()),
            'total_deaths' : int(country_data['new_deaths'].sum()),
            'peak_cases': int(country_data['new_cases'].max()),
            'avg_daily_cases': int(country_data['new_cases'].mean()),
            'fatality_rate': round(country_data['new_cases']/country_data['new_cases'].sum()*100,2) if country_data['new_cases'].sum()>0 else 0,
        }
        return stats
    def compare_two_countries(self,country1 = "USA",country2 = "INDIA"):
        stats1 = self.get_basic_stats(country1)
        stats2 = self.get_basic_stats(country2)
        comparison = pd.DataFrame({
            country1 : stats1,
            country2 : stats2
        })
        return comparison
if  __name__ == "__main__":
        from data_loader import CovidDataLoader
        loader = CovidDataLoader()
        loader.create_sample_data()
        analyzer = SimpleCOVIDAnalyzer(loader)
        print("\nUsa stats".upper())
        print("=" * 30)
        print(analyzer.get_basic_stats("USA"))

        print("\nusa vs india".upper())
        print("="*30)
        print(analyzer.compare_two_countries("USA","INDIA"))





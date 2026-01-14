from data_loader import CovidDataLoader
from analysis_engine import SimpleCOVIDAnalyzer
from visualizations import plot_simple_comparison

def main():
    print("Covid data explorer".upper())
    print("=" * 30)

    print("\nLoading data".upper())
    loader = CovidDataLoader()
    loader.create_sample_data()

    print("\n Analyzing data".upper())
    analyzer = SimpleCOVIDAnalyzer(loader)

    print("\nStatistics for COVID-19 cases".upper())
    for country in ['USA','INDIA']:
        stats = analyzer.get_basic_stats(country)
        print(f"\n{country}:")
        for key ,value in stats.items():
            print(f"{key}: {value}")
    print("\nCreating Visualization COVID-19 cases".upper())
    plot_simple_comparison(analyzer)
if __name__ == "__main__":
    main()


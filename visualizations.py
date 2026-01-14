from marshal import loads

import matplotlib.pyplot as plt




def plot_simple_comparison(analyzer,save_path = "simple_comparison.png"):
    countries  = ['USA', 'INDIA', 'BRAZIL', 'UK', 'GERMANY']
    total_cases = []
    for country in countries:
        stats = analyzer.get_basic_stats(country)
        total_cases.append(stats['total_cases'])

    plt.figure(figsize=(10,6))
    bars = plt.bar(countries,total_cases,color = ['blue','green','red','yellow','magenta'])
    plt.title('Total COVID Cases by Country',fontsize=20,fontweight='bold',color='black')
    plt.xlabel('Country',fontsize=16,fontweight='bold')
    plt.ylabel('Total Cases',fontsize=16,fontweight='bold')

    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.,height + 1000,f'{int(height):,}',ha = 'center', va = 'bottom')
    plt.tight_layout()
    plt.savefig(save_path)
    plt.show()
    print(f"Saved: {save_path}")
if __name__ == '__main__':
    from data_loader import CovidDataLoader
    from analysis_engine import SimpleCOVIDAnalyzer
    loader = CovidDataLoader()
    loader.create_sample_data()
    analyzer = SimpleCOVIDAnalyzer(loader)
    plot_simple_comparison(analyzer)









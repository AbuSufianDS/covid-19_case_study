\# COVID-19 Data Analyzer



A Python tool to analyze and visualize COVID-19 data.



\## Features

\- Load COVID-19 data from CSV files

\- Calculate statistics by country

\- Create bar charts and visualizations

\- Generate summary reports



\## Installation

```bash

pip install pandas numpy matplotlib



\# Load data

from data\_loader import CovidDataLoader

loader = CovidDataLoader()

loader.load\_from\_csv('sample\_data.csv')



\# Analyze

from analysis\_engine import simpleCovidAnalyzer

analyzer = simpleCovidAnalyzer(loader)

stats = analyzer.get\_basic\_stats('USA')



\# Visualize

import visualizations

visualizations.plot\_simple\_comparison(analyzer)


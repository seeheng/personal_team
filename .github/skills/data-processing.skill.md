# Data Processing Skill

## Skill Metadata
```yaml
name: data-processing
version: 1.0.0
description: Processes and transforms data for the personal assistant
agent: personal-assistant
category: data
status: active
```

## Overview
This skill enables the personal assistant agent to:
- Process and transform data
- Handle various data formats (CSV, JSON, XML, etc.)
- Perform data validation and cleaning
- Generate statistics and insights
- Create data visualizations
- Manage datasets

## Capabilities

### Core Features
- **Data Loading**: Load data from multiple formats
- **Data Transformation**: Transform and manipulate data
- **Data Validation**: Validate data integrity and completeness
- **Data Cleaning**: Handle missing values and outliers
- **Statistics**: Generate statistical summaries
- **Visualization**: Create charts and plots
- **Export**: Save processed data in various formats

### Supported Formats
- CSV, TSV
- JSON
- XML
- Excel (.xlsx, .xls)
- Parquet
- HDF5
- DTA (Strata's native binary data format)
- SAV (SPSS data format)

## Key Methods

### Data Management
- `load_data(file_path, format=None)`
- `save_data(data, file_path, format='csv')`
- `list_data_files(directory)`

### Transformation
- `filter_data(data, criteria)`
- `group_data(data, by_column)`
- `aggregate_data(data, operations)`
- `merge_datasets(dataset1, dataset2, on=None)`
- `transform_columns(data, transformations)`

### Analysis
- `get_statistics(data, columns=None)`
- `detect_outliers(data, method='iqr')`
- `generate_summary(data)`
- `correlate_features(data)`

### Visualization
- `plot_histogram(data, column)`
- `plot_scatter(data, x_col, y_col)`
- `plot_line(data, x_col, y_col)`
- `generate_report(data, output_path)`

### Ref - DTA foramt
Key Characteristics of .dta Files:
Binary Format: Unlike .sav (SPSS) or .csv (text), .dta files are binary, which makes them more compact and faster to read/write.

Stata-Specific: Created and used by Stata statistical software.

Structure:

Contains variable names, labels, value labels, and data
Stores metadata about the dataset (variable types, formats, etc.)
Can handle large datasets efficiently
Version Compatibility: Different versions of Stata may create different .dta versions (e.g., .dta13, .dta14, .dta17). Newer versions can read older ones, but not vice versa.

---

**Version**: 1.0.0  
**Status**: Active  
**Last Updated**: Apr 19, 2026

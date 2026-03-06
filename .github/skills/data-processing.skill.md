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

---

**Version**: 1.0.0  
**Status**: Active  
**Last Updated**: March 6, 2026

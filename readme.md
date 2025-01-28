# Telco Churn Analysis Dashboard

## Introduction

The Telco Churn Analysis Dashboard is a powerful web application designed to provide in-depth exploratory data analysis (EDA) and analytics for telecommunications customer churn data. Built with Streamlit, this interactive dashboard allows users to upload their own datasets and gain valuable insights through visualizations and statistical analysis.

## Technologies Used

- **Programming Language**: Python
- **Libraries**:
  - Data Manipulation: pandas
  - Data Visualization: plotly
  - Web Application Framework: Streamlit
- **Data Formats Supported**: CSV and Excel files (.csv, .xlsx, .xls)

## Launch

To run the application locally:

1. Clone the repository from GitHub.
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the Streamlit app with the command:
   ```bash
   streamlit run edaapp.py
   ```
4. Upload your dataset or use the default dataset provided in the app.

## Features

### Data Loading and Preprocessing
- Supports CSV and Excel file formats
- Handles missing values in the 'TotalCharges' column
- Converts 'TotalCharges' to numeric type

### Interactive Dashboard
- Navigation sidebar for easy switching between EDA and Analytics dashboards
- File uploader for custom dataset analysis

### Visualizations
- The app likely includes various charts and graphs to visualize churn-related data (specific details not provided in the code snippet)

## Scope of Functions

### Key Features:
- **Dataset Loading**: Supports CSV and Excel file formats
- **Data Preprocessing**: Handles missing values and converts data types
- **Interactive Interface**: Built with Streamlit for seamless user interaction
- **Multi-page Layout**: Separate dashboards for EDA and Analytics

### Limitations:
- The app requires datasets with specific columns, including 'TotalCharges'
- Full functionality may depend on the structure of the uploaded dataset

## Future Enhancements

- Implement additional data visualization techniques
- Add machine learning models for churn prediction
- Expand the analytics capabilities with more advanced statistical analyses

## Sources

This project utilizes open-source libraries and frameworks:
- Streamlit for web application development
- Pandas for data manipulation
- Plotly for interactive visualizations

## Contributing

Contributions to improve the Telco Churn Analysis Dashboard are welcome. Please feel free to submit pull requests or open issues for any bugs or feature requests.

## License

[Include license information here]







# Telco Churn Prediction App

## 1️⃣ **Project Title**  
**Telco Churn Prediction App**

## 2️⃣ **Introduction**  
The Telco Churn Prediction App is a machine learning-based web application designed to predict customer churn for a telecommunications company. By analyzing customer data, the app provides insights into which customers are likely to leave and enables businesses to take proactive measures to improve retention rates. The app leverages advanced machine learning models and an intuitive user interface built with Streamlit.

## 3️⃣ **Technologies Used**  
The project incorporates the following technologies:  
- **Programming Language:** Python  
- **Libraries:**  
  - Data Manipulation: `pandas`, `numpy`  
  - Machine Learning: `scikit-learn` (Random Forest, Logistic Regression, Gradient Boosting)  
  - Web Application Framework: `Streamlit`  
- **Data Formats Supported:** CSV and Excel files  

## 4️⃣ **Launch**  
To run the application locally:  
1. Clone the repository from GitHub.  
2. Install the required dependencies using `pip install -r requirements.txt`.  
3. Run the Streamlit app with the command:  
   ```bash
   streamlit run telcochurnapp.py
   ```
4. Upload your dataset or use the default dataset provided in the app.

## 5️⃣ **Table of Contents**  
- [Project Title](#1️⃣-project-title)  
- [Introduction](#2️⃣-introduction)  
- [Technologies Used](#3️⃣-technologies-used)  
- [Launch](#4️⃣-launch)  
- [Table of Contents](#5️⃣-table-of-contents)  
- [Illustrations](#6️⃣-illustrations)  
- [Scope of Functions](#7️⃣-scope-of-functions)  
- [Sources](#8️⃣-sources)

## 6️⃣ **Illustrations**  
The application includes:  
- A user-friendly interface for uploading datasets and configuring model parameters.  
- Visualizations of model performance metrics such as accuracy scores for Random Forest, Logistic Regression, and Gradient Boosting models.  

Example screenshots:  
1. **Main Dashboard:** Displays options for dataset upload and preprocessing.  
2. **Model Training Results:** Shows accuracy scores for each trained model.

## 7️⃣ **Scope of Functions**  

### Key Features:
1. **Dataset Loading and Preprocessing:** 
   - Supports CSV and Excel file formats.
   - Handles missing values and performs one-hot encoding for categorical variables.
2. **Machine Learning Models:** 
   - Trains three models: Random Forest, Logistic Regression, and Gradient Boosting.
   - Evaluates model performance using accuracy scores.
3. **Churn Prediction:** 
   - Allows users to input new customer data for churn prediction.
   - Aligns user input with trained model features to ensure compatibility.
4. **Interactive Interface:** 
   - Built with Streamlit for seamless user interaction.
   - Displays results in real-time after training or prediction.

### Limitations:
- The app requires clean datasets with specific columns such as `customerID`, `Churn`, and `InternetService`. Missing required columns will result in errors.

## 8️⃣ **Sources**  
The project is based on publicly available datasets and tools, including:  
- Cleaned Telco customer data (`CleanedTelco.csv`).  
- Libraries like `scikit-learn` for machine learning algorithms and `Streamlit` for app development.


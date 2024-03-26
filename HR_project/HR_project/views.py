from django.shortcuts import render
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder

def index(request):
    return render(request, 'index.html')

def predict(request):
    return render(request, 'predict.html')

def result(request):
    data = pd.read_csv(r"C:\Users\PC\Desktop\HR_attrition\Attrition.csv")
    
    # Preprocess the data
    categorical_cols = ['BusinessTravel']  # Update with the actual categorical columns in your dataset
    numeric_cols = [col for col in data.columns if col not in categorical_cols + ['Attrition']]
    
    # One-hot encode categorical variables
    encoder = OneHotEncoder(sparse=False)
    encoded_cols = encoder.fit_transform(data[categorical_cols])
    encoded_df = pd.DataFrame(encoded_cols, columns=encoder.get_feature_names_out(categorical_cols))
    
    # Concatenate encoded categorical variables with numeric variables
    X = pd.concat([encoded_df, data[numeric_cols]], axis=1)
    
    Y = data['Attrition']
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)

    # Train RandomForestClassifier model
    model = RandomForestClassifier(n_estimators=1000)
    model.fit(X_train, Y_train)

    # Get user input values from request
    user_input = [float(request.GET[f'n{i}']) for i in range(1, len(X.columns) + 1)]

    # Predict with user input values
    paired = model.predict([user_input])
    
    result1 = ""
    suggestion = ""

    if paired == 'Yes':
        result1 = 'Positive'
        suggestion = "Based on the prediction, this employee may leave. Consider offering career development opportunities, improving work-life balance, and addressing any concerns or issues they may have to increase retention."
    elif paired == 'No':
        result1 = 'Negative'
        suggestion = "Based on the prediction, this employee is likely to stay. However, it's essential to continue focusing on employee retention strategies such as recognizing achievements, providing learning opportunities, and fostering a positive work culture to maintain engagement and satisfaction."
    
    return render(request, "predict.html", {"result2": result1, "suggestion": suggestion})

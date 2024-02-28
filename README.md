# F1PredictionPoints
<b>The project was created to predict the probability of drivers getting points in Formula 1 races based on data from previous races. The telegram bot provides users with a convenient way to get forecasts for specific drivers and analyze the results.</b>
## Project structure
    
    .
    ├── DataCollection  
    |   ├── archive                     # Historical data
    |   └── data.ipynb                  # Data collection and pre-processing
    ├── Research
    |   ├── EDA.ipynb                   # exploratory data analysis
    |   ├── importancepoleposition.csv  # additional data
    |   └── model.ipynb                 # Training, research and evaluation of models
    ├── TelegramBot
    |   ├── __pycache__
    |   ├── ConversationChoice.py       # Module for managing conversational options in the bot
    |   ├── analytics.py                # Module for data analytics and visualization
    |   ├── botsetting.py               # Telegram Bot settings file
    |   ├── loaddata.py                 # Module for uploading data to the bot
    |   ├── main.py                     # The main file that runs the telegram bot
    |   └── prediction.py               # Module for predicting results
    ├── README.md                       # Project description file
    ├── demonstration.mp4               # demo video 
    ├── f1dataset.csv                   # The main dataset
    ├── model_predict                   # The trained model
    └── requirements.txt                # The file with project dependencies
    
## Technologies
 - <b>Programming language:</b>
     - Python
 - <b>Tools</b>:
     - Numpy
     - Pandas
     - fastf1
     - catboost
     - scikit-learn
     - matplotlib
     - seaborn
     - telebot
     - keras
## Data Collection
The final dataset was based on <a href="https://www.kaggle.com/datasets/rohanrao/formula-1-world-championship-1950-2020">Formula 1 World Championship (1950 - 2023)</a> and updated with data downloaded using the api <a href='https://docs.fastf1.dev'>FastF1</a>. 
## Models research
The problem is framed as a classification task, both classical and machine learning (ML) approaches are explored. Classical methods such as logistic regression, as well as boosting models and various ML techniques, are considered for solving the problem.

| Model          | F1   |
|----------------|------|
| CatBoost       | 0.77 |
| Random Forest  | 0.76 |
| LSTM           | 0.76 |
| MLP            | 0.76 |
| Ada Boost      | 0.75 |
| LR_model       | 0.75 |

As a result, the CatBoost model was chosen. 

When evaluating the quality of the results, this project appears as a distinctive and unparalleled undertaking. Currently, there may be projects that have some similarities, but direct comparison is not possible.

## Analytics
The project also offers limited analytics upon user request:
-  Each race track possesses unique conditions, and therefore, the significance of the pole position varies. By leveraging historical data, we can quantify the impact of the pole position on a specific track.
-  Exploring and comparing the telemetry data obtained from the fastest laps of two drivers to gain insights into their performance and racing strategies.
## Telegram Bot
<a href = 'https://t.me/F1PredictorBot'> F1Predictor</b>

A Telegram bot has been crafted to enhance user interaction and streamline operations within the project. This both serves as a user-friendly interface, providing convenient access to various functionalities and features offered by the project. Users can seamlessly navigate through different commands and receive real-time updates, predictions, and analytical insights with the help of Telegram bot.
## Demonstration
[(demonstartion.mp4)](https://github.com/o-frolova/F1PredictionPoints/blob/main/demonstration.mp4)

## References
- https://www.kaggle.com/datasets/rohanrao/formula-1-world-championship-1950-2020
- https://docs.fastf1.dev
- https://towardsdatascience.com/formula-1-race-predictor-5d4bfae887da
- https://www.f1-predictor.com/building-an-f1-prediction-engine-predictive-modelling-part-i/

## Next step
- [ ] Prediction of race results
- [ ] Expanding the analytics functionality
     - [ ] Statistics for each rider
     - [ ] Psychological impact on the results of the rider
     - [ ] Comparison of two pilots based on the results of their performances
- [ ] The ability to provide users with a Grand Prix schedule
- [ ] The ability to provide users session results

## Monetization
The project's monetization strategy revolves around offering users an enhanced experience through a subscription-based model. Users subscribing to a paid plan will gain access to advanced features, providing them with a more comprehensive and premium functionality. This subscription-based approach ensures a sustainable revenue stream while catering to the diverse needs and preferences of users who seek additional benefits and capabilities from the project.

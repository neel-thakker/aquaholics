# Stock Instructor
`Theme = FinTech Education`

# Problem Statement

The world of stock trading can be intimidating and confusing, especially for new traders who may not be familiar with technical terms and analysis. Many beginner traders use popular platforms to invest in stocks, but may not have the necessary knowledge to effectively analyze and predict stock trends using different indicators and charts. As a result, they may miss out on potential opportunities to make profitable trades and may face some serious losses.

# Solution

To help new traders understand technical terms and analysis related to stock trading, we aim to develop a user-friendly platform that simplifies the process of analyzing and predicting stock trends. Our platform will provide educational resources, including a glossary of technical terms and explanations of different indicators and charts. We will also provide a simple and intuitive interface for traders to input their stock preferences and view the necessary data in a clear and concise manner.

Our platform will focus on making the process of stock analysis and prediction accessible and understandable to beginner traders, while also providing valuable insights and predictions based on a complex algorithm. By empowering new traders with the necessary knowledge and tools, we aim to help them make informed decisions and increase their chances of making profitable trades on platforms.

# Working 
Stock Instructor is a React app that fetches stock data from Yahoo Finance API and uses Apex charts to plot stock charts. It provides analysis based on different technical indicators and predictions using a complex algorithm. The app also fetches news related to the stocks and provides a glossary for all the technical terms and indicators used.

# Features
- Fetches stock data from Yahoo Finance API
- Plot stock charts using Apex charts
- Analysis based on different technical indicators
- Predictions using a complex algorithm
- Fetches news related to the stocks and company
- Glossary for all the technical terms and indicators used

# Images

# Algorithms 
### For Analysis Function
Technical indicators are mathematical calculations applied to a stock's price and volume data in order to provide insights into its price movements. They are based on the premise that historical price data can provide information about future price movements.Converting the inferences of these indicators into textual format can provide users with a better understanding of a stock's current market price and potential price movements. We use indiactors like RSI, ADX, SMAs etc for providing textual indiactions to the user which he might miss while analysing the charts on his own. For example:
For example, if the RSI value exeeds 70 , itindicates that a stock is overbought and the price might drop. Similarly, if the ADX has a high value i.e above 50 ,it is showing a strong trend and trend would continue in future. 

### For Prediction Function
For pridiction of buying and selling signals for the share a variety of combinations of indicators are used each giving a value between -100 and 100. Here -100 indicates the maximum selling signal and 100 indicates maximum buying signal.
List of combinations used are:
1. RSI + Bollinger Bands
* It allows us to know whether prices are high and overbought or low and oversold.
* The strategy of using Bollinger Bands and RSI is to watch for moments when prices hit the lower band and RSI hits the oversold region (Below 30). This would 
be a good entry price to buy. If you are looking to sell, you can wait for prices to hit the upper band and RSI hits the overbought region (above 70).
* In the case of bollinger bands, if the price touches either of the lower or upper level, a reversal in direction can be predicted.
* Also if the price crosses the 20 sma line, a continuation in trend can be expected.
2. RSI + MACD
* MACD is a momentum indicator that illustrates the relationship between the 26-day and 12-day exponential moving averages.
* While RSI also measures momentum, it reflects this momentum through a different analytic approach. 
* If one indicator signals momentum in a certain direction, we check the other indicator to see whether it agrees. 
 3. RSI + ADX
* The RSI (Relative Strength Indicator) is a momentum-based technical indicator used to measure the strength of price movement in a market.
* This indicator is plotted as a line that shows values between 0 and 100.
* A divergence between the price and the RSI shows a trend change.
* The ADX indicator is used to measure the strength of the trend.
* When the ADX line is lower than 20, the market is in a consolidation.
* If the ADX line crosses higher than 25, a run in trend of the market is observed.
 
 4. 200 EMA + RSI
* EMA(Exponential Moving Average) is a momentum indicator which gives more importance to a value the more recent it is.
* The slope of the EMA of a stock price can indicate where the price is headed next. Depending on the slope of EMA, it is given a score between -30 and 30. 
* As the slope can be infinite, if |slope| > 5 then it is considered as a very strong trend and given the full score in the respective direction.
* The RSI indicates if a stock is overbought or oversold. If the RSI is less than 30, then it indicates a stock is oversold and if above 70 then it is overbought. Thus, 
a score between -70 and +70 is given and these two are added together.

 5. MACD + ADX
* MACD is a momentum indicator that illustrates the relationship between the 26-day and 12-day exponential moving averages. The MACD is going to 
detect the trend reversals, 
* While the ADX is showing either the trend is strong or fading.

 6. MACD + Bollinger Bands
* MACD above signal and zero line + price touching lower bollinger => buy
* MACD below signal and zero line + price touching upper bollinger => sell
* else undecided

 7. ADL + RSI
* The A/D line is used to help assess price trends and potentially spot forthcoming reversals. 
* If a security’s price is in a downtrend while the A/D line is in an uptrend, then the indicator shows there may be buying pressure and the security’s price 
may increase.
* Find slope => steeper the slope, A strongly rising A/D line confirms a strongly rising price. 
* Similarly, if the price is falling and the A/D is also falling, then there is still plenty of distribution and prices are likely to continue to decline.

 8. OBV + EMA + RSI (Intraday)
* The on-balance volume indicator tells us that the number of positive days are more than those of down days. As a result, it could be a sign that the bullish 
trend will continue for a while.
* On the other hand, a falling OBV means that the volume of down days is falling. Therefore, it could be a sign that there are more sellers in the market than 
buyers.
* We focus on the trend of the indicator instead of the absolute figure.
* Here, we look at the trend or steepness of slope for OBV and EMA-20 as well as RSI value. Each of the 3 indicators have equal share in the final result.

9. Stoc RSI + Bollinger Bands
* Similar to (7), Stoc RSI is given a score between -70 and +70.
* If the Price touches either band then a reversal in the trend is expected. If the price crosses the 20 day SMA, then the trend is indicated to persist.
* Using this, a score between -30 and +30 is given to the Bollinger Bands reading
* These two are added together.

10. Stoc RSI + MACD
* If the MACD line has crossed above the signal line, it is given a score of +100.
* If it has crossed below, then a score of -100. Otherwise, 0.
* A weighted mean is taken with weight = 0.75 for Stoc RSI and 0.25 for MACD.

11. Stoc RSI + ADX
* The value of ADX is divided by 75. Basically, we look at the value of ADX to judge how good the trend indicated by Stoc RSI would hold.
* Finally, the score for Stoc RSI is multiplied by the value obtained above to get the score. 

12. 200 SMA + 50 SMA
* If the 50 SMA crosses above the 200 SMA(Golden Cross) then it indicates a bullish market and a score of +100 is given. If the 50 SMA crosses below the 
200 SMA(Death Cross) then it indicates a bearish market and a score 0f -100 is given. 
* If the two align, then the current trend is indicated to persist and a score of 0 is given.

The score from each function is calculated and averaged to give the final signal.

# Usage
To use the app, follow the steps below:

- Enter the stock symbol in the search bar.
- Select the date range and frequency.
- Click on "Fetch Data" to fetch the stock data and plot the chart.
- Analyze the chart based on different technical indicators and predictions.
- Check out the news related to the stock and the glossary for technical terms and indicators.

# Contributing
Contributions are welcome! To contribute to the project, follow the steps below:

1. Fork the repository
2. Create a new branch: git checkout -b feature-name
3. Make changes and commit: git commit -m "message"
4. Push changes to the branch: git push origin feature-name
5. Submit a pull request

# Credits
The app was built using the following technologies:
- React
- Apex Charts
- Yahoo Finance API
- Ta-Lib
- Flask

# License

This project is licensed under the MIT License. See the LICENSE file for details.

# RoDo_Python_ETL
Project - ETL process for scraping twitter for Mars Data and creating visualizations from it.

The code uses 2 ways to get tweet data from Twitter.
1. Using the Twitter API - We authenticate using the twitter api credentials, and then make api search call to get tweets.
2. Using Web Scraping - Using requests, we make a GET call to twitter handle url using custom headers (google crawler agent) 
                        to avoid the javascript issue to trigger server-side rendering.

After getting the tweets, they are being loaded into a dataframe.
Using RegEx, the required parameters are extracted and appended into new columns. 
The Updated dataframe is then exported into a CSV file. 

Using the MatplotLib package, a scatter plot is created using columns Temperature High and Pressure.

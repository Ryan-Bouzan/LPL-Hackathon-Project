import streamlit as st
from PIL import Image
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
from newspaper import Article
import io
import nltk
import yfinance as yf
from datetime import datetime, timedelta
from dateutil.parser import parse

import ssl

ssl._create_default_https_context = ssl._create_unverified_context
nltk.download('punkt')

def set_custom_style():
    custom_style = """
        <style>
            /* Use Comic Sans MS as the font */
            body {
                font-family: 'Comic Sans', sans-serif;
            }
            /* Additional styling if needed */
            h1 {
                color: pink;
            }
        </style>
    """
    st.markdown(custom_style, unsafe_allow_html=True)

def is_time_within_six_hours(current_time_str, other_time_str):
    """
    Evaluate if another time is within 6 hours of the current time.

    Parameters:
    - current_time_str: A string representing the current time (format: 'Sat, 27 Jan 2024 12:23:02 GMT').
    - other_time_str: A string representing the other time (format: 'Sat, 27 Jan 2024 12:23:02 GMT').

    Returns:
    - True if the other time is within 6 hours of the current time, False otherwise.
    """
    current_time = parse(current_time_str)
    other_time = parse(other_time_str)

    # Calculate the time difference
    time_difference = abs(current_time - other_time)

    # Check if the time difference is within 6 hours
    return time_difference <= timedelta(hours=6)


# Main function responsible for posting a request to the google news site.
# Uses beautiful soup 4 to parse the xml obtained from the request, extracts title, date, link, and summary
# Creates a 2D list of these categories, which is sent as an argument to the show_data function which handles
# populating the UI elememnts.
def get_news(topics):
        #nltk.download('punkt')

        sites_data = []
        for topic in topics:
            site = 'https://news.google.com/news/rss/headlines/section/topic/{}'.format(topic)
            print("Current topic: " + topic)
            op = urlopen(site)  # Open that site
            rd = op.read()  # read data from site
            op.close()  # close the object
            sites_data.append(rd)
            all_data = []
            titles = []
            dates = []
            summaries = []
            links = []
            valid_article = True
            for item in sites_data:
                sp_page = soup(item, 'xml')  # scraping data from site

                temp = sp_page.find_all('item')[:5]
                for element in temp:
                    valid_article = True

                    data = Article(element.find('link').text)
                    try:
                        data.download()
                        data.parse()
                        data.nlp()
                    except Exception as e:
                        print(e)
                        valid_article = False

                    if valid_article:
                        titles.append(element.find('title').text)
                        dates.append(element.find('pubDate').text)
                        summaries.append(data.summary)
                        links.append(element.find('link').text)

            sites_data = []
            if valid_article:
                all_data.append(titles)
                all_data.append(dates)
                all_data.append(summaries)
                all_data.append(links)
                show_data(topic, all_data)


# Using a loop, the top 5 articles from each category are shown as they are passed by the calling function
# In order to enhance responsiveness, the function is designed so only one category is displayed at a time
# This minimizes loading time for the user and helps keep them engaged.
# Streamlit markdown calls are used to implement basic html styling options, giving the UI a more refined look
def show_data(topic, data_list):
    #titles, dates, summaries is expected format
    topicText = f"<div style='font-size: 60px;'>{topic}</div>"
    st.markdown(topicText, unsafe_allow_html=True)
    st.markdown("<hr style='border: 4px solid pink;'>", unsafe_allow_html=True)

    for i in range(len(data_list[0])):
        st.write(f"<a href='{data_list[3][i]}' style='font-size: 40px;'>{data_list[0][i]}'</a>", unsafe_allow_html=True)
        timestamp =  parse(data_list[1][i])
        short_time = timestamp.strftime('%a, %d %b %Y')
        if is_time_within_six_hours(datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT'), data_list[1][i]):
            data_list[1][i] = "*RECENT* " + short_time
            st.subheader(data_list[1][i])

        else:
            st.subheader(short_time)

        styled_text = f"<div style='margin: auto; text-align: center; 20px;'>{data_list[2][i]}</div>"
        if not data_list[2][i]:
            data_list[2][i] = "Sorry, no summary is available for this article."
        st.markdown(data_list[2][i])
        st.markdown("<hr style='border: 2px solid pink;'>", unsafe_allow_html=True)


def run():
    set_custom_style()
    st.title("CYBER DEFENDERS NEWS: The Best Place To Get Your News")
    st.header("Stay Up to Date On The Latest Financial, Technology, and Business Events")
    image = Image.open("finnews2.jpeg")
    st.image(image, caption="Wall Street with Money", use_column_width=True)

    st.title("Live Stock Chart")

    # User input for stock symbol
    stock_ticker = st.text_input("Enter stock ticker symbol (e.g., AAPL):", "AAPL")

    # Fetch stock data based on user input
    stock_data = get_stock_data(stock_ticker)

    # Display the live stock chart
    st.line_chart(stock_data['Close'])

    # topics are hard coded at this time.
    topics = ['BUSINESS', 'WORLD', 'TECHNOLOGY']
    get_news(topics)

    st.title("Read List App")

    # User input for the item to add to the read list
    new_item = st.text_input("Enter item for your read list:", "")
def get_stock_data(ticker, period="1d", interval="1m"):
    # Function to fetch stock data using yfinance
    end_date = datetime.now()
    start_date = end_date - timedelta(days=1)  # Fetch data for the last day
    stock_data = yf.download(ticker, start=start_date, end=end_date, interval=interval, progress=False)
    return stock_data


run()
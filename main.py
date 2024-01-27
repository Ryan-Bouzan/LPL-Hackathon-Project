

import streamlit as st
from PIL import Image
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
from newspaper import Article
import io
import nltk
import yfinance as yf
from datetime import datetime, timedelta
import ssl

ssl._create_default_https_context = ssl._create_unverified_context
nltk.download('punkt')


#st.set_page_config(page_title='InNews🇮🇳: A Summarised News📰 Portal', page_icon='./Meta/newspaper.ico')


def fetch_news_search_topic(topic):
    site = 'https://news.google.com/rss/search?q={}'.format(topic)
    op = urlopen(site)  # Open that site
    rd = op.read()  # read data from site
    op.close()  # close the object
    sp_page = soup(rd, 'xml')  # scrapping data from site
    news_list = sp_page.find_all('item')  # finding news
    return news_list


def fetch_top_news():
    site = 'https://news.google.com/news/rss'
    op = urlopen(site)  # Open that site
    rd = op.read()  # read data from site
    op.close()  # close the object
    sp_page = soup(rd, 'xml')  # scrapping data from site
    news_list = sp_page.find_all('item')  # finding news
    return news_list


def fetch_category_news(topic):
    site = 'https://news.google.com/news/rss/headlines/section/topic/{}'.format(topic)
    op = urlopen(site)  # Open that site
    rd = op.read()  # read data from site
    op.close()  # close the object
    sp_page = soup(rd, 'xml')  # scrapping data from site
    news_list = sp_page.find_all('item')  # finding news
    return news_list


def fetch_news_poster(poster_link):
    try:
        u = urlopen(poster_link)
        raw_data = u.read()
        image = Image.open(io.BytesIO(raw_data))
        st.image(image, use_column_width=True)
    except:
        image = Image.open('./test_image.png')
        st.image(image, use_column_width=True)


def display_news(list_of_news, news_quantity):
    c = 0
    for news in list_of_news:
        c += 1
        # st.markdown(f"({c})[ {news.title.text}]({news.link.text})")
        st.write('**({}) {}**'.format(c, news.title.text))
        news_data = Article(news.link.text)
        try:
            news_data.download()
            news_data.parse()
            news_data.nlp()
        except Exception as e:
            st.error(e)
        fetch_news_poster(news_data.top_image)
        with st.expander(news.title.text):
            st.markdown(
                '''<h6 style='text-align: justify;'>{}"</h6>'''.format(news_data.summary),
                unsafe_allow_html=True)
            st.markdown("[Read more at {}...]({})".format(news.source.text, news.link.text))
        st.success("Published Date: " + news.pubDate.text)
        if c >= news_quantity:
            break


def set_custom_style():
    custom_style = """
        <style>
            /* Use Comic Sans MS as the font */
            body {
                font-family: 'Comic Sans', sans-serif;
            }
            /* Additional styling if needed */
            h1 {
                color: blue;
            }
        </style>
    """
    st.markdown(custom_style, unsafe_allow_html=True)

def get_news(topics):
        nltk.download('punkt')

        sites_data = []
        for topic in topics:
            site = 'https://news.google.com/news/rss/headlines/section/topic/{}'.format(topic)
            print("Current topic: " + topic)
            op = urlopen(site)  # Open that site
            rd = op.read()  # read data from site
            op.close()  # close the object
            sites_data.append(rd)
            titles = []
            summaries = []
            for item in sites_data:
                sp_page = soup(item, 'xml')  # scrapping data from site

                temp = sp_page.find_all('item')[:5]
                for element in temp:
                    titles.append(element.find('title').text)
                    data = Article(element.find('link').text)
                    try:
                        data.download()
                        data.parse()
                        data.nlp()
                    except Exception as e:
                        print(e)
                    summaries.append(data.summary)

            sites_data = []
            for i in range(len(titles)):
                print(titles[i])
                print(summaries[i])
                print("\n")



def run():
    # Initialize session state

    st.title("Read List App")

    # User input for the item to add to the read list
    new_item = st.text_input("Enter item for your read list:", "")


    topics = ['BUSINESS', 'WORLD', 'TECHNOLOGY']
    get_news(topics)
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


def get_stock_data(ticker, period="1d", interval="1m"):
    # Function to fetch stock data using yfinance
    end_date = datetime.now()
    start_date = end_date - timedelta(days=1)  # Fetch data for the last day
    stock_data = yf.download(ticker, start=start_date, end=end_date, interval=interval, progress=False)
    return stock_data



# Function to initialize session state variables



    # with col2:
        #st.image(image, use_column_width=False)


        #with col3:
    #    st.write("")
    #category = ['--Select--', 'Trending News', 'Business News', 'World News']
    #cat_op = st.selectbox('Select your Category', category)
    #if cat_op == category[0]:
    #     st.warning('Please select Type!!')
    # elif cat_op == category[1]:
    #     st.subheader("✅ Here is the Trending🔥 news for you")
    #     no_of_news = st.slider('Number of News:', min_value=5, max_value=25, step=1)
    #     news_list = fetch_top_news()
    #     display_news(news_list, no_of_news)
    # elif cat_op == category[2]:
    #     av_topics = ['Choose Topic', 'WORLD', 'NATION', 'BUSINESS', 'TECHNOLOGY', 'ENTERTAINMENT', 'SPORTS', 'SCIENCE',
    #                  'HEALTH']
    #     st.subheader("Choose your favourite Topic")
    #     chosen_topic = st.selectbox("Choose your favourite Topic", av_topics)
    #     if chosen_topic == av_topics[0]:
    #         st.warning("Please Choose the Topic")
    #     else:
    #         no_of_news = st.slider('Number of News:', min_value=5, max_value=25, step=1)
    #         news_list = fetch_category_news(chosen_topic)
    #         if news_list:
    #             st.subheader("✅ Here are the some {} News for you".format(chosen_topic))
    #             display_news(news_list, no_of_news)
    #         else:
    #             st.error("No News found for {}".format(chosen_topic))
    #
    # elif cat_op == category[3]:
    #     user_topic = st.text_input("Enter your Topic🔍")
    #     no_of_news = st.slider('Number of News:', min_value=5, max_value=15, step=1)

        # if st.button("Search") and user_topic != '':
        #     user_topic_pr = user_topic.replace(' ', '')
        #     news_list = fetch_news_search_topic(topic=user_topic_pr)
        #     if news_list:
        #         st.subheader("✅ Here are the some {} News for you".format(user_topic.capitalize()))
        #         display_news(news_list, no_of_news)
        #     else:
        #         st.error("No News found for {}".format(user_topic))
        # else:
        #     st.warning("Please write Topic Name to Search🔍")



run()
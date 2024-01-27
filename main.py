

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

import streamlit as st
from PIL import Image
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
from newspaper import Article
import io
import ssl
import nltk
nltk.download('punkt')

# Disable SSL certificate verification
ssl._create_default_https_context = ssl._create_unverified_context

#st.set_page_config(page_title='InNews🇮🇳: A Summarised News📰 Portal', page_icon='./Meta/newspaper.ico')


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


    topics = ['BUSINESS', 'WORLD', 'TECHNOLOGY']

    get_news(topics)

    #
    # if cat_op == category[0]:
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
    #
    #     if st.button("Search") and user_topic != '':
    #         user_topic_pr = user_topic.replace(' ', '')
    #         news_list = fetch_news_search_topic(topic=user_topic_pr)
    #         if news_list:
    #             st.subheader("✅ Here are the some {} News for you".format(user_topic.capitalize()))
    #             display_news(news_list, no_of_news)
    #         else:
    #             st.error("No News found for {}".format(user_topic))
    #     else:
    #         st.warning("Please write Topic Name to Search🔍")


run()
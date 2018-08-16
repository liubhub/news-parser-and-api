import sys
import os
import time
import json

import feedparser
import newspaper

import pymongo

from datetime import datetime


ARTICLES_LIMIT = 4
flatten = lambda l: [item for sublist in l for item in sublist]

def get_new_articles_objecs(companies):
    
    _articles = {}
    

    for company, sources in companies.items():
        
        print('Started parsing {}'.format(company))
        
        if 'rss' in sources.keys():
            url = sources['rss']
            data = feedparser.parse(url)
            articles = list(map(lambda article: newspaper.Article(article.link), data.entries))
            
        else:

            print('No rss provided')

            try:
                data = newspaper.build(sources['link'], memoize_articles=False)
                articles = data.articles

            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, '\n', fname, '\n', exc_tb.tb_lineno, '\n', exc_obj)
                continue
        
        _articles[company] = articles
        
    return _articles

def check_and_filter_updates(collection):

    with open(os.path.abspath('source.json')) as data_file:
        companies = json.load(data_file)

    entries = list(collection.find({}))
    current_urls = [entry['url'] for entry in entries]
    
    articles = get_new_articles_objecs(companies)
    
    # some stupid hacks to filter links for parsing
    
    if 'cnn' in articles.keys():
        articles['cnn'] = [el for el in articles['cnn'] \
                       if el.url.split('.')[1] == 'cnn' and 'football' in el.url.split('/')]
    
    new_articles_urls = [entry.url for entry in flatten(list(articles.values()))]
    
    articles = {source: list(filter(lambda ar: ar.url in set(new_articles_urls)-set(current_urls), articles_list)) \
                for source, articles_list in articles.items()}

    # articles_to_add = [entry for entry in articles \
    #                   if entry.url in set(new_articles_urls)-set(current_urls)] 
    # articles_to_add = list(filter(lambda ar:ar.url.split('.')[1] in companies.keys(), articles_to_add))
    
    return articles     


def parse_and_add_updates_to_db(articles_to_add, collection, external_request=False):
    
    data = []

    n = flatten(list(articles_to_add.values()))

    for company, articles_list in articles_to_add.items():

        count = 1

        if company == 'reddit' and count >= ARTICLES_LIMIT:
            print('Limit number of requests on {}. Sleep for 10s'.format(company))
            count = 1
            time.sleep(10)

        for index, entry in enumerate(articles_list):

            print('Parsing {} article from {}'.format(index+1, len(articles_list)))
            try:
                entry.download()
                entry.parse()
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, '\n', fname, '\n', exc_tb.tb_lineno, '\n', exc_obj)
                continue

            entry.nlp()

            article = {}

            article['source'] = company
            article['title'] = entry.title
            article['publish_date'] = str(entry.publish_date)
            article['text'] = entry.text
            article['authors'] = ','.join(entry.authors)
            article['keywords'] = ','.join(entry.keywords)
            article['url'] = entry.url

            count = count + 1

            data.append(article)

            # if external_request:
            # 
            # try: 
            #     collection.insert_one(article)
            #     yield int(len(data)/n*100)
            # except Exception as e:
            #     return
            
    try:
        collection.insert_many(data)
        print('Articles were added')
        return True
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print('Error trying to insert in db:\n', exc_type, '\n', exc_tb.tb_lineno)
        return 

if __name__ == "__main__":

    orig_stdout = sys.stdout
    f = open('upd.log', 'w')
    sys.stdout = f

    print(str(datetime.now()))
    
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client.news
    collection = db.news

    articles = check_and_filter_updates(collection)

    if articles:
        print('Adding articles...')
        parse_and_add_updates_to_db(articles, collection)
    else:
        print('Nothing to add.')

    sys.stdout = orig_stdout
    f.close()

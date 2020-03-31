from uuid import uuid4
import nltk
from urllib.parse import urlparse
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
#from django.views.decorators.csrf import csrf_exempt
from .models import ScraperInformation
from string import punctuation

#for information from forms
from .forms import KeywordForm

#for REST API
from rest_framework import viewsets
from .serializers import ScrapedInformationSerializer

class ScrapedInfoViewSet(viewsets.ModelViewSet):
    queryset = ScraperInformation.objects.all()#.order_by("title")
    serializer_class = ScrapedInformationSerializer

# BOKEH TEST
# BOKEH RUNS!
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import WheelZoomTool, ColumnDataSource
from bokeh.palettes import Spectral6

def bokeh_test_plot(request):
    lang = ['Python', 'JavaScript', 'C#', 'PHP', 'C++', 'Java']
    counts = [25, 30, 8, 22, 12, 17]

    p = figure(x_range=lang, plot_height=450, title="Programming Languages Popularity",
           toolbar_location="below", tools="pan,wheel_zoom,box_zoom,reset, hover, tap, crosshair")
    
    source = ColumnDataSource(data=dict(lang=lang, counts=counts, color=Spectral6))

    p.add_tools(WheelZoomTool())       

    p.vbar(x='lang', top='counts', width=.8, color='color', legend="lang", source=source)
    p.legend.orientation = "horizontal"
    p.legend.location = "top_center"

    p.xgrid.grid_line_color = "black"
    p.y_range.start = 0
    p.line(x=lang, y=counts, color="black", line_width=2)

    script, div = components(p)

    return render(request, 'home.html' , {'script': script, 'div':div})

# plotting plotly graph in django views
from plotly.offline import plot
import plotly.graph_objects as go
def plotly_test_plot(request):
    x_data = [0,1,2,3]
    y_data = [x**2 for x in x_data]
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=[0, 1, 2, 3, 4, 5],
            y=[1.5, 1, 1.3, 0.7, 0.8, 0.9]
        ))

    fig.add_trace(
        go.Bar(
            x=[0, 1, 2, 3, 4, 5],
            y=[1, 0.5, 0.7, -1.2, 0.3, 0.4],
                    ))
    fig.update_layout(
        title_text = "something",
        xaxis_title = 'x-axis',
        yaxis_title = 'y-axis'
    )
    plot_div = plot(fig,
               output_type='div')
    return render(request, "plotly_home.html", context={'plot_div': plot_div})


# getting word to check information for
# processing the information
# get information from forms and prompt download of generated image

def show_word_plot(request):
    if request.method == "POST":
        return word_cloud(request)
    return render(request, "form_index.html")

def get_occurences(stringg, scraped_query):
    occurences = []
    primary_id = []
    for an_entry in scraped_query:
        buff = an_entry.title.lower()
        if stringg.lower() in buff:
            occurences.append(buff)
            primary_id.append(an_entry.id)
    return occurences,primary_id

def tokenize_sentences(list_of_text, exclude_list=[]) -> list:
    tokenized_text = []
    for a_text in list_of_text:
        checker = [i for i in (a_text.split(" ")) if i not in exclude_list and exclude_list[-1] not in i]
        tokenized_text.extend(checker)
    return tokenized_text

from nltk import FreqDist
from pandas import DataFrame
def tokenizer_():
    pass

def top_n_words(frequency,n):
    top_n={}
    top_nvalues=list(frequency.values())
    top_nvalues.sort()
    top_nvalues=top_nvalues[-n:]
    for key in frequency:
        if frequency[key] in top_nvalues:
            top_n[key]=frequency[key]
    top_n = DataFrame.from_dict(top_n, orient='index')
    top_n = top_n.sort_values(by = 0, ascending=False)
    return top_n.to_dict()[0]

def word_cloud(request):
    form = KeywordForm(request.POST)
    if form.is_valid():
        form = form.cleaned_data
        your_name = form['your_name']
        email_add = form['email']
        keyword = form['keyword']
        scraperinformation = ScraperInformation.objects.all()

        to_exclude= ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this','that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]
        filtered_titles, primary_id = get_occurences(keyword, scraperinformation)
        to_exclude.append(keyword)
        to_exclude.extend(['says','cases','us','energency', 'people','show','get','due','could','health','may','new','coronavirus'])
        to_exclude.extend(['-',"'","'s",":",",","?","$",'’'])
        to_exclude.extend(list(punctuation))
#        print(to_exclude)
        filtered_titles = (tokenize_sentences(filtered_titles,
                                exclude_list=to_exclude))

        filtered_titles = top_n_words(FreqDist(filtered_titles),30)
        print("\n\n",filtered_titles,"\n\n")
        fig = go.Figure()
        y_=list(filtered_titles.values())
        fig.add_trace(go.Bar(
            x=list(filtered_titles.keys()),
            y=y_,
            name='Word Occurence Count',
            text=y_,
            textposition='auto',
            ))
        
        fig.update_layout(
        title_text = "Most Occuring Words for `{}`".format(keyword),
        xaxis_title = 'Words',
        yaxis_title = 'Num of Occurence'
        )

        plot_div = plot(fig,
                        output_type='div')
        scraperinformation = ScraperInformation.objects.filter(pk__in=primary_id[-100:]).order_by('-id')
        #print(scraperinformation)
        return render(request, "plotly_home.html", context={'plot_div': plot_div,
                                                            'scraperinformation':scraperinformation,
                                                            'keyword':keyword})

        #from wordcloud import WordCloud
        #import matplotlib.pyplot as plt
        
        # Create the wordcloud object
        #wordcloud = WordCloud(width=1200, height=1200, margin=0).generate(filtered_titles)
        
        # Display the generated image:
        #plt.imshow(wordcloud, interpolation='gaussian')
        #plt.axis("off")
        #plt.margins(x=0, y=0)
        #plt.savefig("fig.png")
        #return HttpResponse((filtered_titles))

    return HttpResponse("Undefined Page!")

def index(request):
    all_scraper_objects = ScraperInformation.objects.all()
    all_scraped_items = {}
    for an_object in all_scraper_objects:
        all_scraped_items[an_object.unique_id] = an_object.title, an_object.link

    return JsonResponse(all_scraped_items)

def index_(request):
    return render(request, "base.html")#, context={'plot_div': plot_div})

# API for the websites scrped and how many times they occured
def showNetlocs(request):
    all_scrapedInformation_objects = ScraperInformation.objects.all()

    netlocs = {'total':0} # last time, total = 832
    for an_object in all_scrapedInformation_objects:
        urlNetloc = urlparse(an_object.link).netloc
        if urlNetloc in list(netlocs.keys()):
            netlocs[urlNetloc] += 1
        else:
            netlocs[urlNetloc] =1
        netlocs['total'] += 1
    return JsonResponse(netlocs)


def are_there_words(string_to_check, scraperInformation_title, single_word = True):
#    string_to_check = [i.lower() for i in string_to_check]
    scraperInformation_title = scraperInformation_title.lower()
    #print("In The are_there_words Function:",string_to_check)
    if single_word:
        if string_to_check in scraperInformation_title:
            return True
        else:
            return False
    else:
        out = 0
        for word in string_to_check:
            if word in scraperInformation_title:
                out += 1
        if out > 0:#= len(string_to_check)-1 and len(string_to_check) > 2:
            return True
        else:
            return False

def getNews(request, string_to_check):
    """
    checks headlines for terms in string_to_check
    and returns headline that contain words in string_to_check
    """
    items = {}
    print(string_to_check)
    string_to_check = (string_to_check.lower()).split(" ")
    all_scrapedInformation_objects = ScraperInformation.objects.all()
    if len(string_to_check) == 1:
        string_to_check = string_to_check[0]
        for an_object in all_scrapedInformation_objects:
            if are_there_words(string_to_check, an_object.title):
                items[an_object.link] = an_object.title
        return JsonResponse(items)
    else:
        for an_object in all_scrapedInformation_objects:
            if are_there_words(string_to_check, an_object.title, single_word=False):
                items[an_object.link] = an_object.title
        return JsonResponse(items)
#    return JsonResponse({'test':"pass"})

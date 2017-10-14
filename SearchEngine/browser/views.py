from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Autocomplete
import json
from django.http import HttpResponse
from .SearchRank.SearchRank import *
from .SearchRank.Queries import Queries
from .SearchRank.Connection import Connection as connect


def index(request):
    q = request.GET.get('term', '')

    results = []
    if (q != ''):
        autocomplete_list = Autocomplete.objects.filter(query__contains=q)

        for word in autocomplete_list:
            word_json = {}
            word_json = word.query
            results.append(word_json)

        data = json.dumps(results)

        mimetype = 'application/json'
        return HttpResponse(data, mimetype)
    return render(request, 'homepage/home.html')


def pages(request):
    parameters = request.GET.get('page', '')

    links_list = []
    titles_list = []
    contents_list = []

    if(parameters == ''):

        links_file = open('links.txt', 'w', encoding = 'utf-8')
        titles_file = open('titles.txt', 'w', encoding = 'utf-8')
        contents_file = open('contents.txt', 'w', encoding = 'utf-8')
        query_file = open('query.txt', 'w')

        query = request.POST['search']
        rankedLinks, linksDetails, linksContent = SearchRank(query)


        # insert into autocomplete
        connection = connect()
        connection.Start_Connection()
        query_object= Queries(connection.cursor)
        query_object.insert_autocomplete(query)
        connection.Close_Connection()

        if(len(rankedLinks) != 0):
            for link in rankedLinks:
                # links
                links_list.append(linksDetails[link[0]][1])
                links_file.write(linksDetails[link[0]][1] + '\n')
                # titles
                titles_list.append(linksDetails[link[0]][0])
                titles_file.write(linksDetails[link[0]][0] + '\n')
                # contents
                contents_list.append(linksContent[link[0]])
                contents_file.write(linksContent[link[0]] + '\n')
                # query
                query_file.write(query + '\n')
        else:
            # links
            links_list.append(' ')
            links_file.write(' ' + '\n')
            # titles
            titles_list.append(' ')
            titles_file.write(' ' + '\n')
            # contents
            if query[0] == "\"" and query[len(query) - 1] == "\"":
                query = query[1:-1]
            contents_list.append('No Links Found for ' + '"' + query + '"')
            contents_file.write('No Links Found for ' + '"' + query + ' "' + '\n')
            # query
            query_file.write(query + '\n')
    else:

        links_file = open('links.txt', 'r', encoding = 'utf-8')
        titles_file = open('titles.txt', 'r', encoding = 'utf-8')
        contents_file = open('contents.txt', 'r', encoding = 'utf-8')
        query_file = open('query.txt', 'r')

        query = query_file.read().splitlines()[0]
        links_list = links_file.read().splitlines()
        titles_list = titles_file.read().splitlines()
        contents_list = contents_file.read().splitlines()

    links_file.close()
    titles_file.close()
    contents_file.close()
    query_file.close()

    paginator_link = Paginator(links_list, 10)
    paginator_title = Paginator(titles_list, 10)
    paginator_content = Paginator(contents_list, 10)

    page = request.GET.get('page')

    try:
        links = paginator_link.page(page)
        titles = paginator_title.page(page)
        contents = paginator_content.page(page)
    except PageNotAnInteger:
        links = paginator_link.page(1)
        titles = paginator_title.page(1)
        contents = paginator_content.page(1)
    except EmptyPage:
        links = paginator_link.page(paginator_link.num_pages)
        titles = paginator_title.page(paginator_title.num_pages)
        contents = paginator_content.page(paginator_title.num_pages)


    myList = zip(links, titles, contents)
    context = {'myList': myList, 'page': page, 'query': query, 'links': links}
    return render(request, 'pages/page.html', context)
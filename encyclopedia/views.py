from os import write
from django.http.response import Http404, HttpResponse
from django.shortcuts import redirect, render
from markdown2 import Markdown
from . import util
import random

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry):
    # Declaring the entry in a variable
    get_entry = util.get_entry(entry)
    # Converting the .md file to a Html file
    if get_entry == None:
        return render(request, "encyclopedia/notfound.html")
    else:
        markdowner = Markdown()
        convert = markdowner.convert(get_entry)
        # Opening the new Html file and writing to it
        with open(f'encyclopedia/templates/encyclopedia/{entry}.html', 'w') as new_file:
            new_file.write('{% extends "encyclopedia/layout.html" %}' + f'{{% block title %}}{entry}{{% endblock %}}' 
            + '{% block body %}' + convert + f"""<a href="/edit/{entry}">Edit Page</a>""" + '{% endblock %}')
        # Render the Html file
        return render(request, f"encyclopedia/{entry}.html")

def create(request):
    if request.method == "POST":
        # Retrieve values from POST
        header = request.POST.get('title')
        content = request.POST.get('content')
        # If no file with the same header exists, open new entry
        if util.get_entry(header) is None:
            # Create the .md file
            util.save_entry(header, content)
            response = redirect(f'wiki/{header}')
            return response
        else:
            # Return error response
            error_response = render(request, "encyclopedia/duplicate.html")
            return error_response
    else:
        return render(request, "encyclopedia/createnewpage.html")

def random_page(get_random_entry):
    get_random_entry = random.choice(util.list_entries())
    return redirect(f'wiki/{get_random_entry}')

def search(request):
    query = request.GET.get('q')
    query_lower = str(query).lower()
    # An empty list which will store the matched search queries
    matched = []
    for entry in enumerate(util.list_entries()):
        if query_lower == entry[1].lower():
            return redirect(f'wiki/{query_lower}')
        elif query_lower in entry[1].lower():
            matched.append(entry[1])
        enumerate(entry)
    if matched == []:
        return render(request, "encyclopedia/notfound.html")
    else:
        return render(request, "encyclopedia/searchresults.html", {
            "query": query,
            "results": matched
        })

def edit(request, entry):
    if request.method == "GET":
        with open(f'entries/{entry}.md', 'r') as ef:
            retrievetext = ef.read()
        return render(request, f"encyclopedia/editpage.html", {
            "title": entry,
            "entry_field": retrievetext
        })
    elif request.method == "POST":
        get_edited_text = request.POST.get('content')
        with open(f'entries/{entry}.md', 'w') as w:
            w.write(get_edited_text)
        markdowner = Markdown()
        # convert the .md file to html
        convert = markdowner.convert(get_edited_text)
        with open(f'encyclopedia/templates/encyclopedia/{entry}.html', 'w') as edited_html:
            edited_html.write('{% extends "encyclopedia/layout.html" %}' + f'{{% block title %}}{entry}{{% endblock %}}' 
            + '{% block body %}' + convert + f"""<a href="/edit/{entry}">Edit Page</a>""" + '{% endblock %}')
        return render(request, f"encyclopedia/{entry}.html")
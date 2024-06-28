from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
nextId = 4
topics = [
    {'id': 1, 'title': 'routing', 'body': 'Routing is...'},
    {'id': 2, 'title': 'views', 'body': 'Views is...'},
    {'id': 3, 'title': 'model', 'body': 'Models is...'},
]


# <input type="hidden" name="id" value={id}>

def htmlTemplate(articleTag, id=None):
    global topics
    ol = ''
    delete = ''
    for topic in topics:
        ol += f'<li><a href="/read/{topic["id"]}">{topic["title"]}</a></li>'

    if id != None:
        delete = f"""<li>
                            <form action="/delete/{id}/" method="post" >
                                <input type="submit" value="Delete">
                            </form>
                        </li>
                        <li><a href="/update/{id}">Update</a></li>
"""
    return (
        f'''
            <html>
                <body>
                    <h1><a href="/">Django</a></h1>
                    <ul>
                        {ol}
                    </ul>
                    {articleTag}
                    <ul>
                        <li><a href="/create/">Create</a></li>
                        {delete}
                    </ul>
                </body>
            </html>
                        '''
    )


def index(request):
    article = '''
        <h2> Welcome </h2>
        Hello, Django
        '''
    return HttpResponse(htmlTemplate(article))


def read(request, id):
    article = ''
    for topic in topics:
        if topic['id'] == int(id):
            article = f'''
                <h2>{topic['title']}</h2>
                {topic['body']}
            '''
    return HttpResponse(htmlTemplate(article, id))


@csrf_exempt
def create(request):
    global nextId
    print('request.method:', request.method)
    if request.method == 'GET':
        article = """
            <form action="/create/" method="post">
                <p><input type="text" name ="title" placeholder="title"></p>
                <p><textarea name="body" placeholder="body"></textarea></p>
                <p><input type="submit"></p>
            </form>
        """
        return HttpResponse(htmlTemplate(article))

    elif request.method == 'POST':
        title = request.POST['title']
        body = request.POST['body']
        newTopic = {'id': nextId, 'title': title, 'body': body}
        topics.append(newTopic)
        url = "/read/" + str(nextId)
        nextId = nextId + 1
        return redirect(url)


@csrf_exempt
def delete(request, id):
    global topics
    newTopics = []
    for topic in topics:
        if topic['id'] != int(id):
            newTopics.append(topic)
    topics = newTopics
    return redirect('/')


@csrf_exempt
def update(request, id):
    global newTitle, newBody
    print('id', id)
    if request.method == 'GET':
        for topic in topics:
            if topic['id'] == int(id):
                newTitle = topic['title']
                newBody = topic['body']

        article = f"""
            <form action="/update/{id}/" method="post">
                <p><input type="text" name ="title" value={newTitle}></p>
                <p><textarea name="body" >{newBody}</textarea></p>
                <p><input type="submit"></p>
            </form>
        """
        return HttpResponse(htmlTemplate(article, id))

    elif request.method == 'POST':
        title = request.POST['title']
        body = request.POST['body']

        for topic in topics:
            if topic['id'] == int(id):
                topic['title'] = title
                topic['body'] = body

        return redirect(f'/read/{id}')

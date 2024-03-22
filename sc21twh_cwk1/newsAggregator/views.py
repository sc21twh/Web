from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout, get_user
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from .models import Story, Author
from datetime import date,datetime
import json
import requests

# Create your views here.

@csrf_exempt
@api_view(['POST'])
def handleLoginRequest(request):
    if request.method == 'POST':

        #Gets user login details
        username = request.data.get('username')
        password = request.data.get('password')

        #Authenticates user
        user = authenticate(request, username=username, password=password)

        #If authenticated, log in user
        if user is not None:
            login(request, user)
            request.session.save()
            return HttpResponse(f"Welcome, {username}! Successful Login.", status=200)
        
        else:
            return HttpResponse('Login Failed. Incorrect Username or Password', status=401)
        
    else:
        return HttpResponse('Incorrect Request Method', status=405)
    
@csrf_exempt
@api_view(['POST'])
def handleLogoutRequest(request):
    #Checks for session
    if request.user is None:
        return HttpResponse('You must be logged in to log out', status=503)
    
    #Logouts user if request is POST
    if request.method == 'POST':
        logout(request)
        return HttpResponse('You have been logged out successfully',status=200)
    
    else:
      return HttpResponse('Incorrect Request Method', status=405)  

@csrf_exempt
@api_view(['POST'])
def handlePostStoryRequest(request):
    #Checks user is logged in 
    if request.user is None:
        return HttpResponse('You must be logged in to post a story', status=503)
    
    #Find user id of user to query Author
    user = request.user
    userId = user.id
    author = Author.objects.get(user_id=userId)

    #Attempt to read data from request
    try:
        data = request.data
        headline = data.get('headline')
        category = data.get('category')
        region = data.get('region')
        details = data.get('details')
    except json.JSONDecodeError:
        return HttpResponse('Invalid JSON input payload', status=400)
    
    #Attempt to create story
    try:
        thisDay = date.today()
        Story.objects.create(author=author, headline=headline, category=category, region=region, details=details, date=thisDay)
        return HttpResponse('Story posted successfully!', status=201)
    except Exception as e:
        return HttpResponse('Failed to post story:', str(e), status=503)
    
@csrf_exempt
@api_view(['GET'])
def handleGetStoryRequest(request):
    #Handle inputs
    data = request.data
    if data is None:
        return HttpResponse('No data provided', status=400)
    
    category = data.get('category')
    region = data.get('region')
    storyDate = data.get('date')

    #Query stories
    stories = Story.objects.all()
    
    #Filters for specific criteria
    if category != '*':
        stories = stories.filter(category=category)
    if region != '*':
        stories = stories.filter(region=region)
    if storyDate != '*':
        dateFormat = datetime.strptime(storyDate, '%d/%m/%Y').date()
        stories = stories.filter(date__gte=dateFormat)

    if stories is None:
        return HttpResponse('No stories found', status=404)
    
    #Create response array
    jsonStories = []
    for each in stories:

        #Set human readable region
        if each.region == 'uk':
            each.region = 'UK News'
        elif each.region == 'eu':
            each.region = 'European News'
        else:
            each.region = 'World News'

        #Set human readable category
        if each.category == 'pol':
            each.category = 'Politics'
        elif each.category == 'art':
            each.category = 'Art'
        elif each.category == 'tech':
            each.category = 'Technology'
        else:
            each.category = 'Trivial'

        #Create JSON for each story
        jsonStory = {
            'key': each.id,
            'headline': each.headline,
            'category': each.category,
            'region': each.region,
            'author': each.author.name,
            'date': each.date,
            'details': each.details
        }

        #Add each story to array
        jsonStories.append(jsonStory)

    if len(jsonStories) == 0:
        return HttpResponse('No stories found', status=404)
    #Return stories in response
    return JsonResponse({'stories': jsonStories}, status=200)

@csrf_exempt
@api_view(['DELETE'])
def handleDeleteStoryRequest(request, key):
    #Check for key
    if key is None:
        return HttpResponse('No key provided', status=400)

    #Query for story in database with given key
    try:
        story = Story.objects.get(id=key)
    except Story.DoesNotExist:
        return HttpResponse('Story not found in database', status=503)
    
    #Ensure user is logged in
    user = request.user
    if request.user is None:
        return HttpResponse('You must be logged in to delete a story', status=503)
    userId = user.id
    author = Author.objects.get(user_id=userId)

    if author is None:
        return HttpResponse('You must be logged in to delete a story', status=503)

    
    #Delete story
    story.delete()

    return HttpResponse('Story deleted successfully!', status=200)

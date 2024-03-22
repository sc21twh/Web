import requests
import json

#Creates the session
session = requests.Session()

def login(url):
    #Url check
    if url != 'http://127.0.0.1:8000' and url != 'http://localhost:8000' and url != 'https://sc21twh.pythonanywhere.com':
        print("Invalid URL")
        return None
    #Prompts user for login details
    username = input("Enter username: ")
    print()
    password = input("Enter password: ")
    print()

    #Sends post request with login credentials
    response = session.post(url+'/api/login', json={"username": username, "password": password})

    #Outputs result to client, returns session if authenticated
    if response.status_code == 200:
        print(response.text)
        print()
        return session
    else:
        print(response.text)
        print()
        return None
    
def logout(session, url):
    if session is None:
        print("You must be logged in to log out")
        print()
        return
    
    #Checks for url
    if url is None:
        print("No URL provided")
        print()
        return
    
    # Obtain CSRF token from cookies
    csrf_token = session.cookies['csrftoken']

    # Set headers to include session cookies and CSRF token
    headers = {
        'Cookie': '; '.join([f'{name}={value}' for name, value in session.cookies.items()]),
        'X-CSRFToken': csrf_token,
        'Referer': url 
    }

    #Sends post request to logout
    response = session.post(url +'/api/logout',headers=headers)

    #Outputs results to client
    if response.status_code == 200:
        print(response.text)
        print()
    else:
        print(response.text)
        print()

def postStory(session ,url):
    # Checks for logged in user
    if session is None:
        print("You must be logged in to post a story")
        print()
        return
    
    #Checks for url
    if url is None:
        print("No URL provided")
        print()
        return  
    
    # Obtain CSRF token from cookies
    csrf_token = session.cookies['csrftoken']

    # Set headers to include session cookies and CSRF token
    headers = {
        'Cookie': '; '.join([f'{name}={value}' for name, value in session.cookies.items()]),
        'X-CSRFToken': csrf_token, 
        'Referer': url
    }

    #Prompts user for the story elements

    headline = input("Enter headline: ")
    print()
    category = input("Enter category: ")
    print()
    region = input("Enter region: ")    
    print()
    details = input("Enter details: ")  
    print()

    if len(headline) > 64:
        print("Headline too long")
        print()
        return
    
    if category not in ['pol', 'art', 'tech', 'trivia']:
        print("Invalid category")
        print()
        return
    
    if region not in ['uk', 'eu', 'w']:
        print("Invalid region")
        print()
        return
    
    if len(details) > 128:
        print("Details too long")
        print()
        return

    #Sends post request to server
    response = session.post(url + '/api/stories', json={"headline": headline, "category": category, "region": region, "details": details}, headers=headers)

    #Checks for response result
    if response.status_code == 200:
        print(response.text)
        print()
    else:
        print(response.text)
        print()


def getStory(commands,url):
    #Sets url as login not needed
    if url is None:
        url = 'https://sc21twh.pythonanywhere.com'
    
    #Checks commands
    region = '*'
    category = '*'
    storyDate = '*'

    #Ignore the 'news' and focus on criteria
    criteria = commands[1:]
    
    #Split criteria before and after the '='
    for c in criteria:
        if '=' in c:
            key, value = c.split('=')
            if key == '-reg':
                if value in ['uk', 'eu', 'w']:
                    region = value
                else:
                    print("Invalid region")
                    print()
                    return
            elif key == '-cat':
                if value in ['pol', 'art', 'tech', 'trivia']:
                    category = value
                else:
                    print("Invalid category")
                    print()
                    return
            elif key == '-date':
                storyDate = value
            else:
                print("Invalid criteria")
                print()
                return
        else:
            print("Invalid criteria")
            print()
            return
        
    #Sends get request for stories using criteria
    response = requests.get(url+'/api/stories/',json={"region":region, "category":category, "date":storyDate})

    #Outputs response to client
    if response.status_code == 200:
        stories = json.loads(response.text)
        for story in stories['stories']:
            print()
            print("Key:", story['key'])
            print("Headline:", story['headline'])
            print("Category:", story['category'])
            print("Region:", story['region'])
            print("Author:", story['author'])
            print("Date:", story['date'])
            print("Details:", story['details'])
            print()

    else:
        print(response.text)

def deleteStory(commands, session, url):
    #Checks for session
    if session is None:
        print("You must be logged in to delete a story")
        print()
        return
    
    # Obtain CSRF token from cookies
    csrf_token = session.cookies['csrftoken']

    # Set headers to include session cookies and CSRF token
    headers = {
        'Cookie': '; '.join([f'{name}={value}' for name, value in session.cookies.items()]),
        'X-CSRFToken': csrf_token,
        'Referer': url 
    }

    #Casts key and checks for integer
    key = int(commands[1])

    if isinstance(key, int) == False:
        print("Key not an integer")
        print()
        return
    
    #Sends delete request to server
    response = session.delete(url + '/api/stories/'+str(key), headers=headers)
    if response.status_code == 200:
        print(response.text)
        print()
    else:
        print(response.text)
        print()

def main():
    #Initialises variables for loop
    running = True
    session = None
    url = None

    #Until exit
    while running:
        #Splits command into parts
        command = input("Enter command: ")
        print()
        commands = command.split(' ')

        #Checks first word for valid command
        first = commands[0]
        if first == 'login':
            url = commands[1]
            session = login(url)
        
        elif first == 'logout':
            logout(session,url)
            session = None
        
        elif first == 'post':
            postStory(session,url)
        
        elif first == 'news':
            getStory(commands,url)
        
        elif first == 'delete':
            deleteStory(commands, session,url)
        
        elif first == 'exit':
            running = False
        
        else:
            print("Invalid Command - Try Again")
            print()

main()

    

        
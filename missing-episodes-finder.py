import os, re, urllib2, json

userName  	   = "joelperry" 								# Mac user account 
showsDirectory = "/Users/" + userName + "/Movies/tv Shows/" # Path to TV shows
directories    = os.listdir(showsDirectory)				 	# Directories for each show
shows  		   = [] 										# Used for storing dictionaries made from JSON returned from API calls
ignore 		   = {'Futurama' : [5]}

def getTVShowDict(show): # Calls IMDB API with the show name
	show 	 = show.replace(' ', '+')
	req 	 = urllib2.Request("http://imdbapi.org/?title=" + show + "&type=json&plot=none&episode=1&limit=1&yg=0&mt=TVS&lang=en-US&offset=&aka=simple&release=simple&business=0&tech=0")
	response = urllib2.urlopen(req)
	data 	 = None

	if response:
		try:
			data = json.loads(response.read())[0]
			print "Data returned for " + data['title']
		except:
			pass
	
	return data

for show in directories:
	if show[0] != '.': # For hidden files (.DSStore)
		showDict = getTVShowDict(str(show)) # Get dictionary for show

		if showDict:
			shows.append(showDict)

for show in shows:
	ignoreSeasons = []

	for episode in show['episodes']:

		if 'episode' in episode and 'season' in episode and 'title' in episode:
			season  = str(episode['season'])
			epNum   = str(episode['episode'])
			title   = show['title']
			matched = False

			if season in ignoreSeasons:
				continue

			showDirectory = showsDirectory + title + "/Season " + season + "/"

			try:
				files = os.listdir(showDirectory)
			except:
				continue

			for file in files:
				
				if re.search("(S?0?" + season + "[x,E]?P?0?" + epNum + ")|(.*" + episode['title'].replace(" ", "\s").replace("*", "\*").replace("'", "\'") + ".*)", file, re.IGNORECASE):
					matched = True

			if matched == False:
				if int(season) < 10:
					season = "0" + season
				if int(epNum) < 10:
					epNum = "0" + epNum

				print title + " S" + season + "E" + epNum + " missing"		
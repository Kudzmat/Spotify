import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# creating spotify object with client ID & Client secret
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id= "put your client id here",
                                                           client_secret= "put your client secret here"))


def search_artist(artist):
    result1 = sp.search(artist, 1, 0, "artist")
    return result1


# this function will show the artists top 10 songs on Spotify
def view_top10(search_results, artist_name):
    # get artist ID
    artist = search_results['artists']['items'][0]
    artist_id = artist['id']
    # use ID to find top tracks
    top_tracks = sp.artist_top_tracks(artist_id)

    print()
    print(f"{artist_name}'s Top 10 Songs: ")
    for track in top_tracks['tracks'][:10]:
        print(f"""
        Track - {track['name']}
        Audio - {track['preview_url']}
        Cover Art - {track['album']['images'][0]['url']}
        """)


# this function will display artist information
def display_artist(search_results):
    artist = search_results['artists']['items'][0]
    print(f"""
    Artist - {artist['name']}
    Followers - {"{:,}".format(artist['followers']['total'])}  
    Genres - {artist['genres'][0:]}
    -------------------------------""")  # "{:,}".format() will add commas to large numbers


# this function will display the artist's album information
def get_albums(search_results, artist_name):
    # get artist ID
    artist = search_results['artists']['items'][0]
    artist_id = artist['id']

    # search for albums using ID
    album_results = sp.artist_albums(artist_id)
    album_results = album_results['items']  # items holds all the album objects

    # using a for loop to to print all the album info
    print(f"{artist_name}'s albums")
    for item in album_results:
        print(f"""
        Album - {item['name']}
        Album ID - {item['id']}
        Album Art - {item['images'][0]['url']}""")


# this function will search for an album by name
def search_album(search_query, user_name):
    results = sp.search(search_query, 1, 0, "album")  # taking in the album request
    album_result = results['albums']['items'][0]  # the actual album info is here
    album_id = album_result['id']  # getting the album id
    artist_name = album_result['artists'][0]['name']  # the artist's name

    # this section of the code will pull out album and track info
    album_info = sp.album(album_id)  # getting album info
    album_name = album_info['name']
    release_date = album_info['release_date']
    tracks = album_info['tracks']  # this section of data holds info on the actual album tracks

    # confirming if this is the album the user was looking for
    print()
    print(f"Please confirm that you are searching for {album_name} by {artist_name}?")
    answer = int(input("(1). Yes   (2). No"))

    if answer == 1:
        print(f"Thanks {user_name}, enjoy listing!")
        print()

        print(f"""
        Album Name - {album_name}
        Artist Name - {artist_name}
        Release Date - {release_date}
        -------------------------------
        """)

        # using enumerate to number the tracks
        for num, item in enumerate(tracks['items']):
            print(f"""{num + 1}. {item['name']}
                Listen On Spotify - {item['external_urls']['spotify']}

                """)
    elif answer == 2:
        print()
        print(f"I'm sorry we couldn't find the album you're looking for {user_name} :(")
        print("Try searching using the album ID instead! You can do this by searching for the artist "
              "and copying the album ID from their album information")


# this function will get the album the user selects using the album id
def get_album(album_id):
    album_info = sp.album(album_id)  # getting album info
    album_name = album_info['name']
    release_date = album_info['release_date']
    tracks = album_info['tracks']  # this section of data holds info on the actual album tracks
    artist_name = album_info['artists'][0]['name']  # the artist's name

    print(f"""
            Album Name - {album_name}
            Artist Name - {artist_name}
            Release Date - {release_date}
            -------------------------------
            """)

    # using enumerate to number the tracks
    for num, item in enumerate(tracks['items']):
        print(f"""{num + 1}. {item['name']}
                    Listen On Spotify - {item['external_urls']['spotify']}

                    """)


logged = False

# getting the user's name for personalisation
while not logged:
    print("Hello, welcome to Spotify friend, could I get your name?")
    name = input("Enter your name: ")
    logged = True

while logged:
    print(f"""
    What would you like to do {name}?
    (1). Search for an artist
    (2). Search for an album
    (3). Exit""")
    option = int(input("Enter Selection: "))

    # user wants to search for an artist
    if option == 1:

        artist_request = input("Which artist are you looking for: ").capitalize()  # Capitalize first letter
        result = search_artist(artist_request)  # looking up artist

        # method to display the artist's information
        display_artist(result)
        option2 = int(input("What would you like to do - (1). View Albums   (2). View Top Songs   (3). Back to menu"))

        if option2 == 1:
            # album information
            get_albums(result, artist_request)

        elif option2 == 2:
            view_top10(result, artist_request)

        elif option2 == 3:
            pass  # back to menu

    # search for an album
    elif option == 2:
        choice = int(input("Please select --->  (1). Search with album ID   (2). Search using album name"))

        # use album ID
        if choice == 1:
            query = input("Enter album ID: ")
            get_album(query)

        # search by album name
        elif choice == 2:
            album_request = input("Which album are you looking for: ")
            search_album(album_request, name)

    # exit program
    elif option == 3:
        print(f"Goodbye {name} :)")
        exit()

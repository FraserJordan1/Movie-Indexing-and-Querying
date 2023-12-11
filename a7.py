from hashtable import Hashtable
import csv

# It's just a Python list with a fancy name
class MovieCorpus(list):
    def __init__(self):
        super().__init__()

## This is essentiall, "FileProcessor" as requested of the assignment but since
#  the test files look for FileParser, I simply changed the name.
#  takes in a filename and MovieCorpus, and create Movies from the data in the 
#  file, putting those Movies in the MovieCorpus.
class FileParser:
    def read_file(self, filename:str, corpus:MovieCorpus) -> MovieCorpus:
        with open(filename, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                movie = Movie()
                movie.populate_from_csv_array(row)
                corpus.append(movie)
        return corpus

# It just holds a bunch of data that is a movie.
class Movie:
    def __init__(self, datarow:str='') -> None:
        self.title = ''
        self.star_rating = ''
        self.content_rating = ''
        self.genre = ''
        self.duration = ''
        self.actors = []
        self.num_actors = 0
        if datarow != '':
            self.parse_row(datarow)

    ## "7.4,My Sister's Keeper,PG-13,Drama,109,['Cameron Diaz', u'Abigail Breslin', u'Alec Baldwin']"
    ## star_rating,title,content_rating,genre,duration,actors_list
    def parse_row(self, datarow:list) -> None:
        parts = datarow.split(',', 5)
        self.star_rating = str(float(parts[0]))
        self.title = parts[1].strip()
        self.content_rating = parts[2]
        self.genre = parts[3]
        self.duration = parts[4]
        actors_str = parts[5].strip('[]')
        self.actors = [actor.strip(" 'u\"") for actor in actors_str.split(', ')]
        self.num_actors = len(self.actors)

    ## populates movie information from csv object
    def populate_from_csv_array(self, csv_dict:dict) -> None:
        self.star_rating = str(float(csv_dict['star_rating']))
        self.title = csv_dict['title']
        self.content_rating = csv_dict['content_rating']
        self.genre = csv_dict['genre']
        self.duration = csv_dict['duration']
        actors_key = 'actors_list' if 'actors_list' in csv_dict else 'actors'
        actors_str = csv_dict[actors_key].strip('[]')
        self.actors = [actor.strip(" 'u\"") for actor in actors_str.split(', ')]

    ## This allows a Movie to be printed via `print(movie)`
    def __str__(self) -> str:
        return f'{self.title}'


"""A Hashtable, with a KVP where the Key is a word and the value is a MovieSet"""
class MovieIndex(Hashtable):
    def __init__(self) -> None:
        super().__init__(5)

    def add(self, movie: Movie) -> None:
        ## Get the movieset associated with the given word
        #  Add the movie to the set
        key = self.compute_key(movie)
        movie_set = self.get(key)
        if not movie_set:
            movie_set = MovieSet(key)
            self.put(key, movie_set)
        movie_set.add_movie_to_set(movie)

    def index(self, corpus: MovieCorpus) -> None:
        ## get index of video 
        for movie in corpus:
            self.add(movie)

    def get_movie_set(self, term:str) -> Movie:
        ## set term in movie set
        return self.get(term)

    ## Returns a list of keys for this movie
    #  This is usually just a single entry, but sometimes multiple (e.g. Actors)
    def compute_key(self, _:Movie) -> NotImplementedError:
        raise NotImplementedError

    # prints key values
    def print(self) -> None:
        for _, item in enumerate(self):
            print(f'Key: {item.key}')
            movie_set = item.value
            movie_set.print()

# Indexes the movies based on the start_rating
class StarRatingIndex(MovieIndex):
    def compute_key(self, movie: Movie) -> str:
        return str(movie.star_rating)

# Indexes the movies based on the content_rating field
class ContentRatingIndex(MovieIndex):
    def compute_key(self, movie: Movie) -> str:
        return str(movie.content_rating)
    
## Indexes the movies based on the actors in them
class ActorIndex(MovieIndex):
    # Couldnt get the original add method to work so I overrided it for actors
    def add(self, movie: Movie) -> None:
        for actor in movie.actors:
            actor = actor.strip() 
            movie_set = self.get(actor)
            if not movie_set:
                movie_set = MovieSet(actor)
                self.put(actor, movie_set)
            movie_set.add_movie_to_set(movie)

# Indexes the movies based on the genre field
class GenreIndex(MovieIndex):
    def compute_key(self, movie: Movie) -> str:
        return str(movie.genre)

# Indexes the movies based on the title field
class TitleIndex(MovieIndex):
    def compute_key(self, movie:Movie) -> str:
        return movie.title

## a container class for holding a set of Movies. You'll see that it consists 
#  of a description attribute and a movies attribute, which is a Python set().
class MovieSet:
    def __init__(self, description:str='') -> None:
        self.description = description
        self.movies = set()

    # add new movie to movie set
    def add_movie_to_set(self, movie:Movie) -> None:
        self.movies.add(movie)

    # creates a new movie set through union
    def union(self, movie_set:Movie):
        """Creates a new MovieSet, which is a union of this MovieSet and the given movie_set"""
        new_description = f'{self.description}{movie_set.description}'
        new_set = MovieSet(new_description)
        new_set.movies = self.movies.union(movie_set.movies)
        return new_set

    ## grab number of elements within movie set
    def num_elems(self) -> int:
        return len(self.movies)

    def print(self) -> None:
        print(f'MovieSet: {self.description} ({self.num_elems()} Movies)')
        for i, item in enumerate(self.movies):
            print(f'Movie {i + 1}: {item}')

## This helps print out an entire MovieIndex
## Feel free to change/tweak it to print nicely
class MovieReport:
    def __init__(self):
        pass
    
    def print_report(self, index: MovieIndex):
        while(self.iterator.next != None):
            self.output_movie_set(index)

    def output_movie_set(self, movieset: MovieSet):
        print(movieset.description)
        for movie in movieset.movies:
            print(movie)

    def output_report(self, index: MovieIndex):
        return self.print_report(index)

    def save_report(self, index: MovieIndex, filename:str):
        file = open(filename, 'w')
        file.write(self.output_report(index))
        return file

## Given a MovieCorpus, it will create a number of MovieIndexes: 
#  each MovieIndex will enable querying on a different field. Then, 
#  your main function will elicit queries from the user, pass them 
#  to the QueryProcessor, and display the results.
class QueryProcessor():
    def __init__(self, corpus: MovieCorpus):
        ## Create MovieIndexes
        ## Populate them from the corpus
        self.corpus = corpus
        self.genre_index = GenreIndex()
        self.star_index = StarRatingIndex()
        self.content_rating_index = ContentRatingIndex()
        self.actor_index = ActorIndex()

        ## Populate each index with movies from the corpus
        for movie in self.corpus:
            self.genre_index.add(movie)
            self.star_index.add(movie)
            self.content_rating_index.add(movie)
            self.actor_index.add(movie)
    
    ## you'll see that the query(field, vals) method takes in two arguments:
    #  The field argument is to indicate "which MovieIndex to use"-- e.g., 
    #  "genre", or "actors", or "star_rating". The vals argument holds the 
    #  values to query for. It's a list of strings. Calling 
    #  query('star_rating', ['8.8', '8.9']) will query the StarRatingIndex 
    #  and find all the Movies with rating 8.8 and 8.9
    def query(self, field: str, vals: list) -> MovieSet:
        if field not in ['rating', 'actor', 'genre']:
            return MovieSet()
        if field == 'rating':
            return self._query_rating(vals)
        elif field == 'actor':
            return self._query_actor(vals)
        elif field == 'genre':
            return self._query_genre(vals)

    ## private function for quering movie ratings
    def _query_rating(self, ratings: list) -> MovieSet:
        result_set = MovieSet()
        for rating in ratings:
            rating = rating.replace(' ', '')
            movie_set = self.star_index.get_movie_set(rating)
            if movie_set:
                result_set = result_set.union(movie_set)
        return result_set

    ## private function for quering actors of movies
    def _query_actor(self, actors: list) -> MovieSet:
        result_set = MovieSet()
        for actor in actors:
            movie_set = self.actor_index.get_movie_set(actor)
            if movie_set:
                result_set = result_set.union(movie_set)
        return result_set
    
    ## private function for querying genres of movies
    def _query_genre(self, genres:str) -> MovieSet:
        result_set = MovieSet()
        for genre in genres:
            genre = genre.replace(' ', '')
            movie_set = self.genre_index.get_movie_set(genre)
            if movie_set:
                result_set = result_set.union(movie_set)
        return result_set
    
def main():

    print('Welcome to the Movie Search system! We\'ll help you find the movie you\'re looking for.')
    # Create a MovieCorpus
    movie_corpus = MovieCorpus()

    ## Use a FileParser to read in Movies and populate MovieCorpus
    ## Create a QueryProcessor, passing in the MovieCorpus
    file_parser = FileParser()
    filename = input('Enter the name of the movie data file: ')
    movie_corpus = file_parser.read_file(filename, movie_corpus)

    # Create a QueryProcessor, passing in the MovieCorpus
    query_processor = QueryProcessor(movie_corpus)

    try:
        ## Interact with the user, passing queries to the QueryProcessor, until we're done
        while True:
            ## Print a message to the user giving guidance on how to query
            print("\nWould you like to find movies based on [G]enre, [R]ating, or [A]ctors?")
            query_type = input("Go ahead, enter a query: (G/A/R/Q): ").strip().lower()

            ## Take the input and process the query
            ## Iterate until the user is done entering queries
            if query_type == 'q':
                break 
            elif query_type in ['g', 'G']:
                vals = input('Okay, what Genre would you like to find? ')

                # Process the query and display results
                result_set = query_processor.query('genre', vals.strip().split(','))
                if result_set and result_set.movies:
                    print('\nI Found:')
                    for movie in result_set.movies:
                        print(movie)
                else:
                    print('No movies were found...')

            elif query_type in ['a', 'A']:
                vals = input('Okay, what Actor(s) would you like to find? ')
                
                # Process the query and display results
                result_set = query_processor.query('actor', vals.strip().split(','))
                if result_set and result_set.movies:
                    print('\nI Found:')
                    for movie in result_set.movies:
                        print(movie)
                else:
                    print('No movies were found...')
            elif query_type in ['r', 'R']:
                vals = input('Okay, what Rating(s) would you like to find? ')

                # Process the query and display results
                result_set = query_processor.query('rating', vals.strip().split(','))
                if result_set and result_set.movies:
                    print('\nI Found:')
                    for movie in result_set.movies:
                        print(movie)
                else:
                    print('No movies were found...')
            else:
                print('Error! Must be either, G, A, R, or Q')
    except KeyboardInterrupt:
        raise KeyboardInterrupt('Interrupted! How Rude!')
    except FileNotFoundError:
        raise FileNotFoundError('Invalid! CSV Movie file could not be found.')
    print('Thank you for using, Movie Query!')

if __name__ == '__main__':
    main()

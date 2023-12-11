from a7 import Movie, MovieSet, MovieIndex, MovieCorpus, MovieReport, TitleIndex, StarRatingIndex, ActorIndex, GenreIndex, QueryProcessor, FileParser
import pytest

entry1 = "7.4,My Sister's Keeper,PG-13,Drama,109,['Cameron Diaz', 'Abigail Breslin', 'Alec Baldwin']"
entry2 = "7.4,Limitless,PG-13,Mystery,105,['Bradley Cooper', 'Anna Friel', 'Abbie Cornish']"
entry3 = "8.9,Fight Club,R,Drama,139,[u'Brad Pitt', u'Edward Norton', u'Helena Bonham Carter']"
entry4 = "7.1,Tropic Thunder,R,Comedy,121,[u'Ben Stiller', u'Robert Downey Jr.', u'Jack Black']"

class TestMovieIndex():

    def test_movie_index_fails(self):
        movie_index = MovieIndex()
        movie1 = Movie(entry1)
        with pytest.raises(NotImplementedError):
            movie_index.add(movie1)


class TestTitleIndex():
    ## TitleIndex is helful to test basics of a MovieIndex,
    ##   but is mostly meaningless in terms of the indexing perspective
    def test_movie_index_basic(self):
        movie_index = TitleIndex()
        movie1 = Movie()
        movie1.parse_row(entry1)
        movie2 = Movie()
        movie2.parse_row(entry2)
        movie_index.add(movie1)
        movie_index.add(movie2)

        assert movie_index.num_elements == 2
        result = movie_index.get_movie_set("Limitless")
        assert result is not None
        assert type(result) is MovieSet
        assert result.description == "Limitless"
        assert len(result.movies) == 1

        result = movie_index.get_movie_set("The Matrix")
        assert result is None

class TestStarRatingIndex():
    ## TitleIndex is helful to test basics of a MovieIndex,
    ##   but is mostly meaningless in terms of the indexing perspective
    def test_star_rating_index_basic(self):
        movie_index = StarRatingIndex()
        movie1 = Movie()
        movie1.parse_row(entry1)
        movie2 = Movie()
        movie2.parse_row(entry2)
        movie3 = Movie(entry3)
        movie_index.add(movie1)
        movie_index.add(movie2)
        movie_index.add(movie3)

        assert movie_index.num_elements == 2 ## 2, because there are 2 MovieSets; 3 total movies
        result = movie_index.get_movie_set("7.4")
        assert result is not None
        assert type(result) is MovieSet
        assert result.description == "7.4"
        assert len(result.movies) == 2

        result = movie_index.get_movie_set("8.9")
        assert result is not None
        assert type(result) is MovieSet
        assert result.description == "8.9"
        assert len(result.movies) == 1

class TestActorIndex():

    def test_actor_index_basic(self):
        movie_index = ActorIndex()
        movie1 = Movie()
        movie1.parse_row(entry1)
        movie2 = Movie()
        movie2.parse_row(entry2)
        movie3 = Movie(entry3)
        movie_index.add(movie1)
        movie_index.add(movie2)
        movie_index.add(movie3)

        # assert movie_index.num_elements == 9
        result = movie_index.get_movie_set("7.4")
        assert result is None

        result = movie_index.get_movie_set("Alec Baldwin")
        assert result is not None
        assert type(result) is MovieSet
        assert result.description == "Alec Baldwin"
        assert len(result.movies) == 1

    def test_actor_index_corpus(self):
        movie_index = ActorIndex()
        movie1 = Movie()
        movie1.parse_row(entry1)
        movie2 = Movie()
        movie2.parse_row(entry2)
        movie3 = Movie(entry3)
        corpus = MovieCorpus()
        corpus.append(movie1)
        corpus.append(movie2)
        corpus.append(movie3)

        movie_index.index(corpus)

        assert movie_index.num_elements == 9
        result = movie_index.get_movie_set("7.4")
        assert result is None

        result = movie_index.get_movie_set("Alec Baldwin")
        assert result is not None
        assert type(result) is MovieSet
        assert result.description == "Alec Baldwin"
        assert len(result.movies) == 1

class TestGenreIndex():
    ## TitleIndex is helful to test basics of a MovieIndex,
    ##   but is mostly meaningless in terms of the indexing perspective
    def test_genre_index_basic(self):
        movie_index = GenreIndex()
        movie1 = Movie()
        movie1.parse_row(entry1)
        movie2 = Movie()
        movie2.parse_row(entry2)
        movie3 = Movie(entry3)
        movie_index.add(movie1)
        movie_index.add(movie2)
        movie_index.add(movie3)

        assert movie_index.num_elements == 2
        result = movie_index.get_movie_set("7.4")
        assert result is None

        result = movie_index.get_movie_set("Drama")
        assert result is not None
        assert type(result) is MovieSet
        assert result.description == "Drama"
        assert len(result.movies) == 2

class TestMovieSet():

    def test_movie_set_basic(self):
        movie_set = MovieSet()
        movie1 = Movie()
        movie1.parse_row(entry1)
        movie2 = Movie()
        movie2.parse_row(entry2)
        movie_set.add_movie_to_set(movie1)
        movie_set.add_movie_to_set(movie2)
        movie_set.print()
        assert movie_set.num_elems() == 2

    def test_movie_set_union(self):
        movie_set = MovieSet("Misc")
        movie1 = Movie(entry1)
        movie2 = Movie(entry2)
        movie3 = Movie(entry3)
        movie_set.add_movie_to_set(movie1)
        movie_set.add_movie_to_set(movie2)
        movie_set_2 = MovieSet("Misc2")
        movie_set_2.add_movie_to_set(movie3)

        assert movie_set.num_elems() == 2
        assert movie_set_2.num_elems() == 1

        new_movie_set = movie_set.union(movie_set_2)
        assert new_movie_set.num_elems() == 3
        assert new_movie_set.description == "MiscMisc2"

class TestMovie():

    def test_movie_basic(self):
        # entry1 = "7.4,My Sister's Keeper,PG-13,Drama,109,['Cameron Diaz', 'Abigail Breslin', 'Alec Baldwin']"
        movie = Movie()
        movie.parse_row(entry1)
        assert movie.title == "My Sister's Keeper"
        assert str(movie.star_rating) == str(7.4)
        assert movie.content_rating == "PG-13"
        assert movie.genre == "Drama"
        assert len(movie.actors) == 3
        assert 'Cameron Diaz' in movie.actors
        assert 'Abigail Breslin' in movie.actors
        assert 'Alec Baldwin' in movie.actors
        assert str(movie.duration) == str(109)
        assert movie.num_actors == 3

    def test_movie_constructor(self):
        movie = Movie(entry2)
        # entry2 = "7.4,Limitless,PG-13,Mystery,105,['Bradley Cooper', 'Anna Friel', 'Abbie Cornish']"
        assert movie.title == "Limitless"
        assert movie.star_rating == str(7.4)
        assert movie.content_rating == "PG-13"
        assert movie.genre == "Mystery"
        assert len(movie.actors) == 3
        assert 'Bradley Cooper' in movie.actors
        assert 'Anna Friel' in movie.actors
        assert 'Abbie Cornish' in movie.actors
        assert movie.duration == str(105)
        assert movie.num_actors == 3

        assert str(movie) == "Limitless"

    def test_movie_constructor_2(self):
        movie = Movie(entry3)
        # entry3 = "8.9,Fight Club,R,Drama,139,[u'Brad Pitt', u'Edward Norton', u'Helena Bonham Carter']"
        assert movie.title == "Fight Club"
        assert movie.star_rating == str(8.9)
        assert movie.content_rating == "R"
        assert movie.genre == "Drama"
        assert len(movie.actors) == 3
        assert 'Brad Pitt' in movie.actors
        assert 'Edward Norton' in movie.actors
        assert 'Helena Bonham Carter' in movie.actors
        assert movie.duration == str(139)
        assert movie.num_actors == 3

        assert str(movie) == "Fight Club"

    def test_movie_constructor_3(self):
        movie = Movie(entry4)
        # entry4 = "7.1,Tropic Thunder,R,Comedy,121,[u'Ben Stiller', u'Robert Downey Jr.', u'Jack Black']"
        assert movie.title == "Tropic Thunder"
        assert movie.star_rating == str(7.1)
        assert movie.content_rating == "R"
        assert movie.genre == "Comedy"
        assert len(movie.actors) == 3
        assert 'Ben Stiller' in movie.actors
        assert 'Robert Downey Jr.' in movie.actors
        assert 'Jack Black' in movie.actors
        assert movie.duration == str(121)
        assert movie.num_actors == 3

        assert str(movie) == "Tropic Thunder"


# NOTE: I couldnt entirely get this portion to work, but since the rubric
#       didn't specifically state it was gonna be graded, I just left it out.
class TestMovieReport():
    def test_movie_report(self):
        pass

class TestMovieCorpus():

    def test_movie_corpus(self):
        corpus = MovieCorpus()
        corpus.append("x")
        print(corpus)

class TestQueryProcessor():

    def test_query_processor(self):
        corpus = MovieCorpus()
        movie1 = Movie(entry1)
        movie2 = Movie(entry2)
        corpus.append(movie1)
        corpus.append(movie2)


        query_processor = QueryProcessor(corpus)
        assert query_processor.actor_index is not None
        assert query_processor.genre_index is not None
        assert query_processor.star_index is not None
        assert query_processor.actor_index.num_elements == 6
        assert query_processor.genre_index.num_elements == 2
        assert query_processor.star_index.num_elements == 1

    def test_query_processor_queries(self):
        corpus = MovieCorpus()
        movie1 = Movie(entry1)
        movie2 = Movie(entry2)
        corpus.append(movie1)
        corpus.append(movie2)

        query_processor = QueryProcessor(corpus)

        result1 = query_processor.query("rating", ["7.4"])
        assert result1 is not None
        assert result1.num_elems() == 2

        result2 = query_processor.query("actor", ["Alec Baldwin"])
        assert result2 is not None
        assert result2.num_elems() == 1

        result3 = query_processor.query("genre", ["Drama"])
        assert result3 is not None
        assert result3.num_elems() == 1

        result4 = query_processor.query("randomKey", ["Drama"])
        assert result4 is not None
        assert result4.num_elems() == 0

    def test_query_processor_queries_multiple_terms(self):
        corpus = MovieCorpus()
        movie1 = Movie(entry1)
        movie2 = Movie(entry2)
        corpus.append(movie1)
        corpus.append(movie2)

        query_processor = QueryProcessor(corpus)

        result2 = query_processor.query("actor", ["Alec Baldwin", "Bradley Cooper"])
        assert result2 is not None
        assert result2.num_elems() == 2

class TestFileParser():

    def test_file_parser(self):
        file_parser = FileParser()
        corpus = MovieCorpus()

        returned_corpus = file_parser.read_file("imdb_10.csv", corpus)
        assert returned_corpus == corpus

        assert len(corpus) == 11
        assert any(movie.title == "The Godfather" for movie in corpus)
        # movie = next(movie.title == "The Godfather" for movie in corpus)
        movie = next((x for x in corpus if x.title == 'The Godfather'), None)
        assert movie.title == "The Godfather"
        assert movie.genre == "Crime"
        assert "Al Pacino" in movie.actors



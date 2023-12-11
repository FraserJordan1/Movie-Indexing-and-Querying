[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/B_iuFaNZ)
# Assignment 7: Movie Indexing and Querying

UW, EE 590a
Fall 2023

### Objectives

* Implement a simple hashtable
* Use the hashtable to do a simple indexing of data
* Write a query processor to allow a user to interact with the program and query the data

## Big Picture

You're going to build a system to process some data files and enable efficient querying of the data. 

* Build a working hashtable
* Build a MovieIndex that will use the hashtable to index some movie data
* Write a file processor that will open a file, read the data and populate the MovieIndex
* Build a QueryProcessor to take query requests from a user and print the results out
* Expand the system by building multiple MovieIndexes to enable querying on multiple fields
* Use your system to answer some provided queries
* Write up everything you did (this should be like a report for your portfolio or your boss)

# The Details

## Build a Hashtable 

We can't do anything without a Hashtable! The file `hashtable.py` has the outline of a Hashtable implementation. 
Fill it in, and use `hashtable_test.py` to help you feel confident about your implementation. 

A few notes: 

* Our hashtable actually stores data in a `KeyValuePair`. This is a helper data class to allow us to store both the key and the data associated with that key.
* You can use Python's provided `hash()` function to calculate a hash on the key.
* You'll see that you've been provided with a Hashtable iterator. This is a helper class that will allow you to do something like:
```python
hashtable = Hashtable()
## put a bunch of things in the hashtable
for index, kvp in enumerate(hashtable): 
    ## Do something with the index or kvp, e.g.: 
    print(f"key: {kvp.key}, value: {kvp.value}")
```


## Build a MovieIndex

We're going to use a class called MovieIndex to index our movies. This means is that for each field we want to query on, 
each value of that field will be a different key in the Index. 

* A `MovieIndex` should extend a `Hashtable`
* A `MovieIndex` should use a function passed as an argument to calculate a key for a movie
  * An "ActorMovieIndex" would use a function that returns the Actor names for a movie as a key 
* In order to build the `MovieIndex`, you'll also need to have an implementation for a `Movie` and a `MovieSet`. 
* A `Movie` is a data class: It just holds a bunch of data that is a movie. 
* A `MovieSet` is a container class for holding a set of `Movies`. You'll see that it consists of a `description` attribute and a `movies` attribute, which is a Python `set()`. 
  * A Python `set` is another data structure, like a list. The difference is that it can only contain a single instance of a thing: we can't have two strings with the same value, for example. 
  * This helps us ensure we don't put duplicate `Movies` in the set. 
* A `MovieIndex` uses the method `compute_key(movie)` to know how to determine the key for a specified movie. You'll notice that in the base class, `compute_key()` raises a `NotImplementedError`. 
  * Each of your Indexes should extend `MovieIndex` and override `compute_key()` appropriately for that Index
  * e.g. a `GenreIndex` would return `movie.genre` when `compute_key(movie)` is called. 
* There are a couple test cases to help you get started on this, but not a lot.
  * Add more tests
* I recommend starting by just building `MovieIndex` and one extension, such as `GenreIndex`. After you get all the pieces working, come back and add more MovieIndexes. 
* For full credit, your program will have: 
  * `GenreIndex`: index the movies based on the genre field
  * `StarRatingIndex`: index the movies based on the start_rating
  * `ContentRatingIndex`: index the movies based on the content_rating field
  * `ActorIndex`: index the movies based on the actors in them
    * Note: this is tricky, because movies have more than a single actor!
  

## Build a FileProcessor and MovieCorpus

`MovieCorpus` is a simple class: it's just a Python list with a fancy name. We use this to hold all of our movies. With this, 
we can manually create a `MovieCorpus` manually for testing. However, our data file has a whole bunch of lines. So, you'll 
create a `FileProcessor` that will take in a filename and `MovieCorpus`, and create Movies from the data in the file, putting 
those Movies in the MovieCorpus. 

* There are many ways to read files: I suggest you use Python's csv module (https://docs.python.org/3/library/csv.html). However, it's optional-- do what you're comfortable with. 
* Feel free to add a method to your Movie class that allows you to populate the fields based on how you choose to read the data file.

## Build a QueryProcessor

The QueryProcessor is where everything comes together. Given a MovieCorpus, it will create a number of MovieIndexes: each MovieIndex 
will enable querying on a different field. Then, your main function will elicit queries from the user, pass them to the 
QueryProcessor, and display the results. 

* Start simple: Implement your `QueryProcessor` to have only one `MovieIndex`, and restrict querying to that index. 
  * Once you have that working all the way, add in more complexity. 
* You'll see that the `query(field, vals)` method takes in two arguments: 
  * The `field` argument is to indicate "which MovieIndex to use"-- e.g., "genre", or "actors", or "star_rating". 
  * The `vals` argument holds the values to query for. It's a list of `strings`.  
    * Calling `query('star_rating', ['8.8', '8.9'])` will query the `StarRatingIndex` and find all the Movies with rating 8.8 and 8.9. 
  * It returns a `MovieSet` that contains all the movies that match the query: this is a Union operator, or an OR (all movies that have star_rating = 8.8 OR star_rating = 8.9)
* 

## Build more MovieIndexes

In the earlier step, you built out the `GenreIndex`. In this step, add the following indexes: 

* `StarRatingIndex`: index the movies based on the start_rating
* `ContentRatingIndex`: index the movies based on the content_rating field
* `ActorIndex`: index the movies based on the actors in them

In addition, modify the user interaction part of the program to ask the user which field they want to query on. 

The interaction may look something like: 

```shell 
Welcome to the Movie Search system! We'll help you find the movie you're looking for. 

Would you like to find movies based on [G]enre, [R]ating, or [A]ctors? 
g
Okay, what Genre would you like to find? 
comedy
Any other genres as well? [y/n]
y
What else? 
drama
Any other genres as well? [y/n]
n

Searching for movies with Genre (comedy, drama)...

I found: 
MovieSet: DramaComedy (434 Movies)
  Fear and Loathing in Las Vegas
  MASH
  Frost/Nixon
  The Player
  Y Tu Mama Tambien
  Short Cuts
  A Hard Day's Night
  Stranger Than Fiction
  Fiddler on the Roof
.... [output omitted...] 

Would you like to search again? 

... 

```

## Write it all up

Write a report describing what you did. This report should summarize what you built. 

* Put the writeup in `README.md`; put the contents of this file into `instructions.md`

As you write this up, you should consider potential audiences:  

* Your boss is reading this after knowing you've been working on it for 2 weeks. Did you waste the company's time? Did you do good, solid work? 
* A potential employer is reading this while deciding whether to hire you. Can you summarize the work? Can you communicate what is interesting about what you did?
* Images are helpful. Lookup on Github how to put images in your markdown file
* At the top should be a short section on how to run the project

# Things to keep in mind

* At some point, it might be nice to be sure to clean up text, such as storing as all lower-case or something
* When processing the data file, be sure to use `strip()` to remove extra white space from fields
* When printing out the results, it might be nice to include some info other than just the title. 
  * For example, if I searched for genre = drama OR comedy, the movie prints as: `Zombieland (Comedy)`
  * If I searched for actor = Woody Harrelson OR Keri Russell, the movie prints as: `Zombieland (Woody Harrelson)`
  * This is a nice to have: if you don't get around to implementing it, describe how you might do it in your write-up. 
* A bonus attempt: As we've spec'd out the system already, it's easy to query for sets of OR'd values (e.g. a Union of sets). Consider how you could extend this system to enable searching for ANDs (e.g. "genre is Comedy AND rating is 8.9")
* Only very basic user interaction is provided. Please iterate on what's provided to make a better user experience.
* You should run your program like this: `python3 a7.py` (or whatever your Python command is)
* For reading the movie file, it might be helpful to use a `DictReader`: `movie_reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')`
* It might be helpful to use the `strip()` command to clean up actor entries: `actor.strip("'[]\" u")`

# A Giant Caveat

If you've worked with Python a whole bunch, especially for data processing, you're going to have a whole bunch of ideas 
of ways to write some code that will give us the same user experience, without all this hassle of building a hashtable, 
indexing the data, and processing queries like this. It's true: Python has a TON of functionality, both native to the language 
and external libraries, that would allow us to do something like this with many fewer lines of code. However, this class isn't 
just about how to be super efficient in lines of Python code: it's about understanding how a language like Python can do all 
the things it does in so few lines of code. It's about understanding how some of these data structures work, and how we might 
put a bunch of things together to do something useful. 

If you are one of those students who are in this camp: I'm happy to offer a challenge. After you complete this assignment 
in the way it's posed above, feel free to duplicate it in as few lines of code as you can, using any external libraries or 
modules that you'd like. Include it in a separate file (e.g. a7_challenge.py), with some information about how to run it. In your 
write-up for the assignment, add a section showing off how close you could get. In addition to comparing things like the 
number of lines of code, consider discussing things like which different queries you can run, runtime efficiencies, memory 
comparisons between the two implementations, etc. 

This would be a great way to show off your capabilities to future employers! 


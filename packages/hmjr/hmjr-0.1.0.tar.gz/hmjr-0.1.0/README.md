# hmjr

hmjr is a package of tools to help researchers as well as users with simpler
needs directly interact with the HMJr diary collection.

## Prerequisites

- Python3
- Pip
- Thats it!

Alternatively, you can use Google Colab to load up a new PyNotebook, which will
automatically have everything you need. For the rest of this documentation, it
 will be assumed that you're using a Python Notebook.

## Getting started

To install our package and import what you need, run the following two lines.

    !pip install hmjr
    from hmjr import Query

`Query` here is the first point of contact for interacting with the
 HMJR Diary database. In order to use it, we need to initialize the object.
Don't worry about what that means behind the scenes, just make sure to follow
 `Query` up with a `()` whenver we use it, like this: `Query()`.

At this point, you may be seeing some suggestions popping up, especially
if you're using a Notebook. The best starting point here is just `run()`, which
 just grabs entries in the simplest way possible, just the order they
 happen to be stored in the database.

So for now, we'll go with that.

    Query().run().entries

`.entries` selects the data the query gave us out of the `Queries` object.
And after running that, you should see the data output!

Before we get to some new queries, lets go over some of the ways we can influence
 the queries we make. One way is with the default argument **max**. It refers to
 the maximum number of entries the query should ask for.
 This can be changed like this:

    Queries().run(max=5).entries

This time we should see a lot fewer entries when we run the query.

Speaking of volumes - lets move on to a more complex query.

    Query().withBookBetween(1,5).run().entries

This query should be self explanatory, but it does have a quirk in that the
book range includes the lower bound, and excludes the upper bound. So this
query will return entries with books 1, 2, 3, 4.

Under the hood, `withBookBetween(start,stop)` uses a different function to query
the database, and that function is simply `withBook()`. It works like this:

    Query().withBook([1,2,3,4]).run().entries

This is the query our previous `withBookBetween(1,5)` generated for us. The
brackets hold a list of book numbers, and they don't have to be in any order.
`[1,2,3,4]` is the same as `[2,4,1,3]`, and it could even be something like `[708,1,66]`.

By the way, all these queries share that default argument **max**. Its used the
same way that we saw earlier.

Heres our next query:

    Query().withKeyword(["Refugee", "refugee"]).run().entries

We see another list, which works the same way as our previous list. This time we
have quotes around words to differentiate them from code - don't forget the quotes.
 If you get a syntax error, that might be why.

Heres the last kind of query we can do:

    Query().withDate({"day": 1, "month": 1, "year":44}).run().entries

Earlier we saw a python list with the square brackets, this notation is called
 a dictionary, and it holds any number of key:value pairs. Here, our query
 expects a dictionary with day, month and year keys.

Now that we've got all the queries working individually, we can combine them
 before we use `run()`.

Try something like:

    Query().withKeyword(["Camp", "camp"]).withBookBetween(738, 349).run().entries

Your results should have entries with "Camp" or "camp" in their text, in a
 volume between 738 and 749.

Now we can make complex queries on the data, lets look at how we can analyze it.

After we use the `run()` method, we get a different object back.

    entries = Query().withKeyword(["Camp", "camp"]).withBookBetween(738, 349).run()

We've dropped the `.entries` off the end of our query, and are storing the result
 of `run()` in the variable entries. This result has more to it than just a list
 of entries. We can call a couple methods on this object. Heres what it looks like:

    entries.associate(["HMJr"])

What the `associate()` method does is take a list of words, and rank the
 appearences of **every** other word in proximity to this word. "Proximity" is defined
 as appearing with at least one of the given words in the content of an **Index**.

This is a project I put together in response to a coding challenge I was given for an engineering
position. Regardless of its origins, I think it makes an interesting portfolio piece.

I had 48 hours to put together a simple reddit clone with the following features:
- Users can sign up using their email address.
- Users can post topics.
- Users can "like" topics. One like per user per topic.

Bonus points were awarded for:
- Allowing users to post comments on topics.
- Basic UI styling.

The technical requirements were:
- Use ReactJS for client-side rendering.
- Use websockets to push real-time content updates to the client, i.e.
if a user posts a topic, all other users should see that topic appear
in their browser without having to reload the page.
- I was allowed to use a back-end technology of my choice.

The non-functional requirements were:
- Use a DRY coding style.
- Include lots of comments.
- Commit regularly with descriptive messages.

The express purpose of this challenge was to evaluate my ability to pick up
new technologies in a short period of time. As such, this was my first attempt
to do anything non-trivial with React, as well as my first time working with
websockets.

For the back-end, I chose Django, and I used [django-channels](https://channels.readthedocs.io/en/stable/)
to provide websocket layer. I chose Django so that I could play to my strengths, and only wrestle with 
two new technologies at a time. This was my first attempt at doing anything with django-channels.

The two most noteworthy technical features of this application are:
1. Pushing application state to React via a websocket. This almost completely
eliminated the need for data binding in the client. Each time there was a change,
React would receive the new state from the server and re-render the DOM automatically.
A convenient side effect of this was that I didn't have to worry about confirming a
user's actions -- if they submitted valid data, they saw their submission reflected
more or less immediately within the application.
1. I recognized very early on that a comment was simply a topic with a parent who
was another topic. So, from the beginning, I decided that topics would be nodes in
a tree. This decision made it extremely easy to realize the bonus goal of allowing
comments on topics later in the process. I used the excellent [django-treebeard](http://django-treebeard.readthedocs.io/en/latest/) 
library for sophisticated implementations of hierarchical data structures in SQL to 
optimize tree operations.

The last commit I made during my allotted 48 hours was [07fc9adf](https://github.com/zbmott/smr-challenge/commit/07fc9adff0bb123e9995fb33f3e11a3ed867fc61).

As of 2017-05-01, you can find a live demo of this project at [http://54.68.44.21/](http://54.68.44.21/).
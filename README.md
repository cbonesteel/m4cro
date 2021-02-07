# m4cro

Carbs. Fat. Protein. Calories.

Made at UGAHacks6

## About

m4cro is a free web application that helps you pick meals from restaurants
in your local area in order to stay in the confines of your diet. You simply
enter your desired macronutrient counts and our database and connected APIs
will recommend a list of meals from local restaurants that fit your macros
and give you estimated travel times for pickup.

## Inspiration

The "If It Fits Your Macros" (IIFYM) mentality has become increasingly popular in meal plans
and dieting over the past few years, especially within the fitness community. Macros are three main
nutrients contributing to calorie-count in a given food: carbs, fat, and protein. Based on one's goals,
whether it be weightloss or bodybuilding, people have been adamantly counting macros more than ever. Rather
than caring about the individual foods' nutrition values, what matters to many are the end-of-the-day macro counts.

m4cro strives to be a tool to help nutrition enthusiasts meet their goals on-the-go. Whether they are on a road
trip, coming home from the gym, or simply tired of the food in their kitchen, m4cro provides a fast way for people
to find restaurant food that works with their diet.

## How it Works

- Users (either logged-in or guests) enter their desired macros for a meal
  - Calories are calculated in real-time to assist more novice users
  - User data and restaurant/meal data are stored using DataStax
- Upon submission, nearby restaurants (and driving time) are queried using Radar.io
  - Our backend uses the Flask Python module
- For nearby restaurants, lists of meals are gathered
- Each meal is then queried for macros
  - This will employ the MyFitnessPal API, but we are waiting for access
- A cost function sorts all meals based on differences between actual and desired macros, as well as travel time
- The top 10 meal recommendations are then returned to the user

## Current Prototype Status

* Due to the fact that we are waiting on MyFitnessPal API access, we only have a handful of approximately 60 meal options in our prototype
  * However, everything is in-place to use this API for its plethora of data once we have access
* We are still finalizing use of Radar.io for travel time to restaurants

## Future Plans

We are already working on a few ideas for the future:

- A tool that combines items from restaurants to create meals, adding the restaurants
  - With a maximum of three meals per restaurants, this only takes up to `O(n^3)` runtime, where `n` is small (the number of meals at a single restaurant)
- Machine Learning for User Preferences
  - We plan on training a reinforcement based model based on how far down the recommendation list the user goes for their meal
- Machine Learning for General Preferences
  - As we gain more users, we can use general data mining techniques to learn trends in preferences
    - For instance, people who like restaurant X also tend to like restaurant Y

## What We Learned

- All four of us are new to web development, so we all learned basic HTML/CSS design components, as well as interactivity using forms and Javascript
- We also all learned how to use Flask for connecting a Python backend to a website
- Through DataStax, we became more experienced with databasing techniques

## Contributors

* Cameron Bonesteel
* Eric Miller
* Evan Tichenor
* Lydia Williams

<hr/>

<small>
m4cro http://m4cro.space

Icons made by <a href="https://www.flaticon.com/authors/google" title="Google">Google</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a>
</small>
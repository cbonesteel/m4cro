# m4cro

Made at UGAHacks6

## About

m4cro is a free web application that helps you pick meals from restaurants
in your local area in order to stay in the confines of your diet. You simply
enter your desired macronutrient counts and our database and connected APIs
will recommend a list of meals from local resteraunts that fit your macros
and give you estimated travel times for pickup.

## How it Works

When the user presses start, they are met with a page to enter the three main macros of nutrition,
fats, carbs, and protiens. Once they enter these values, a calorie count is automatically generated
for the user to see. Once they press submit, ideally the site would take the entered information and
search our database of already parsed resteraunts based on the users locations. If no resteraunts are
found, queries to the MyFitnessPal API would be made to pull data for the user to find. All of the
information collected would then be displayed in a list, ordered by meals closest to the user's
preference for macros. Accompaning information includes travel time to the resteraunt. This time
would be pulled from the Radar.io API to be displayed in the table.

## Known Issues with Demo
MyFitnessPal API was never granted to us so the functionality is not in depth as we want it to be.
Without this specific API, meal data would take LOTS of web scraping to get any sort of functionality.
To demo this idea, we handmade a database with information to demonstrate what the program would do.

## Contributers
* Cameron Bonesteel
* Eric Miller
* Evan Tichenor
* Lydia Williams

<hr/>

<small>
m4cro http://m4cro.space

Icons made by <a href="https://www.flaticon.com/authors/google" title="Google">Google</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a>
</small>
---
### This application is vacation guide.
---

**Summary:**

In our app, the user will enter a city, the country in which the city is located, and the month they intend to travel. The app will contact Calendarific API to request data on what holidays are observed in that country during that month; Trophosphere API to request climate data for the month they are visiting; and windy API to request webcams from around that area for the specified month so the user can see what it looks like.the api allows user to bookmark favorites for later use

**Users should be able to:** - Enter a country, city,month. - User will be presented with a description of what the weather is like during that month (dry, rainy, cold, hot, etc), what holidays will be celebrated in that country during that month, and some images/webcams showing points of interest around the city.

**Requirement:**
Flask
Peewee
redis

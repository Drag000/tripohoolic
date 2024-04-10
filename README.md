The project is still in development. 
Work in progress:
 - Front-end: overall almost nothing has been finished on HTML and CSS. The idea is to implement dynamic features using JavaScript  
 - Others (to implement more error handling, to add more search options, not only by county, etc.)


**Project apps:**

**1. Accounts** 

- App for collecting and storing details about each user profile (first name, last name, email, age and profile picture). Sensitive information like "username" and "password" is stored in django auth UserModel.	
- Extended Django UserModel via UserProfile model for storing public information.	
- User registration combines 2 forms - 1 based on UserModel and 1 based on UserProfile model	


**2. Trips**	

- App for managing and storing information for each user's trip. Each user can create a post about his/her trip.
- The trip can be categorized as Solo, Group or Agency. If the trip is Agecy, it  can be linked to agency name in app 3. Agencies, where all reviews for each Agency can be found. 
- Country field is standardized via django-countries, corresponding to the official ISO 3166-1 list of countries (with a default max_length of 2).
- The user can upload photos. All photos are stored in a separate model Photos, linked to each trip from Trips model.
	

**3. Agencies**	

App for storing and managing information about travel agencies. You can find a list with links by agencies of all trip reviews added by users.	
	

**4. Common**

App for managing the home page. It contains  models for commenting and rating trip posts by users (TripComment and TripRating models). Each user can comment, delete his/her own comment and rate all trip posts published by other users. If a user rerates a trip, his/her rate is being updated.
The home page includes a search bar by country.
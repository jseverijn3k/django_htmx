# Simple webapp to see howfar we can stretch django and htmx before we need JavaScript.

The whole gist of teh project is to have stream where you can post your favourite Flickr (www.flickr.com) images.

The project includes:
* BeautifulSoup to build a webcrawler
  * get images, artist name and artist url from Flickr
* CRUD functionality to view, create update and delete a post (Django Forms)
* Messages (Django messages) to show if an action (Create / Update / Delete) was succesful
* Categories and Tag functionality to tag our posts with a certain category 
  * using a many-to-many relationship between post and tags
  * category filtering -> showing only the posts belonging to a certain category
  * use category images
  * enable a category order
* Django-allauth for user authentication:
  * login
  * logout
  * signup
  * password reset
  * email verification after a signup
  * styling of all allauth templates
* User profiles
  * with profile pictures
* etc...



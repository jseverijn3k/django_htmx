# Simple webapp to see howfar we can stretch django and htmx before we need JavaScript.

The whole gist of teh project is to have stream where you can post your favourite Flickr (www.flickr.com) images.

The project includes:
* webcrawler to get images from Flickr.com
  * get images, artist name and artist url from Flickr
  * use the BeautifulSoup package to build the webcrawler
* CRUD functionality to view, create update and delete a post (using Django Forms)
* Messages (using Django messages) to show if an action (Create / Update / Delete) was succesful
* Categories and Tag functionality to tag our posts with a certain category 
  * using a many-to-many relationship between post and tags
  * category filtering -> showing only the posts belonging to a certain category
  * use category images
  * enable a category order
* Django-allauth package for user authentication:
  * login
  * logout
  * signup
  * password reset
  * email verification after a signup
  * styling of all allauth templates
* User profiles -> in a seperate django app
  * one-to-one connection with the standard django user model
  * profile pictures -> using Pillow package
  * use django signals to synchronise imformation (email address) between the user profile and djangu standard user model
  * use djang0-cleanup package to cleanup old profile pictures. So, we don't have old unused profile images on our server

* etc...



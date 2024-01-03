# Simple webapp to see howfar we can stretch django and htmx before we need JavaScript.

The whole gist of teh project is to have stream where you can post your favourite Flickr (www.filckr.com) images.

The project includes:
* BeautifulSoup webcrawler, to get the images from Flickr
* CRUD functionality to view, create update and delete a post (Django Forms)
* Messages (Django messages) to show if an action (Create / Update / Delete) was succesful
* Categories and Tag functionality to tag our posts with a certain category 
  * using a many-to-many relationship between post and tags
  * category filtering -> showing only the posts belonging to a certain category
  * use category images
  * enable a category order
* etc...



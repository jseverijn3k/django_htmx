# Simple webapp to see howfar we can stretch django and htmx before we need JavaScript.

The whole idea of this project is to build an **Instagram** like webapp 
* where you can post a Flickr (www.flickr.com) image -> using a Flickr link after which a webcrawler fetches the imeage an image info from Flickr.
* see a stream (on a screen) with the latest posts
* you can comment apost and reply on a comment
* you can like posts, comments and replies

The project includes:

# Posts -> in a seperate djamngo app
* Post information like image, author, etc..
* default avatars if no author is known (e.g. when a user leaves (deletes his profile). The posts are not deleted but the author is shown as 'no author'.
* CRUD functionality to view, create update and delete a post (using Django Forms).

# A webcrawler to get images from Flickr.com -> as part of post functionality
* get images, artist name and artist url from Flickr
* use the BeautifulSoup package to build the webcrawler

# Messages (using Django messages) 
* to show if an action was succesfull
  * Create / Update / Delete of a post
  * Delete of a comment
  * Delete of a reply

# Categories and Tag -> in Post app
* to tag our posts with a certain category 
* using a many-to-many relationship between post and tags
* category filtering -> showing only the posts belonging to a certain category
* use category images
* enable a category order

# User authentication using Django-allauth package
* login
* logout
* signup
* password reset
* email verification after a signup
* styling of all allauth templates

# User profiles -> in a seperate django app
* one-to-one connection with the standard django user model
* profile pictures -> using Pillow package
* use django signals to synchronise imformation (email address) between the user profile and djangu standard user model
* use django-cleanup package to cleanup old profile pictures. So, we don't have old unused profile images on our server
* user profile pages, both private (for loggedin users) als public for all users
* username blacklist (in our settings.py file) to avoid conflicts with usernames
* use Django signals (post_save) to create a profile when a user object is added to teh database after a user signs up.
* use Django signals to update the user table when the email is changed on the profile page
* use a Django onboarding page that is shown directly after a user signsup

# Comments and replies -> in Post app
* Comments model -> with create, read and delete (only own comments) functionality.
  * for the create Django Forms is used
* Replies (to comments) model -> with create, read and delete (only own replies) functionality
  * for the create Django Forms is used
* show author next to comments and replies -> and linkl to the user profile

# Likes
* use HTMX



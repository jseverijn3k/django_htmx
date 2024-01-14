from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
import uuid


from .models import Post, Tag, Comment, Reply, LikedPost, LikedComment, LikedReply

class ModelTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.tag = Tag.objects.create(name='Test Tag', slug='test-tag')
        self.post = Post.objects.create(
            title='Test Post',
            artist='Test Artist',
            url='http://example.com',
            image='http://example.com/image.jpg',
            author=self.user,
            body='Test body content'
        )
        self.post.tags.add(self.tag)
        self.comment = Comment.objects.create(
            author=self.user,
            parent_post=self.post,
            body='Test comment'
        )
        self.reply = Reply.objects.create(
            author=self.user,
            parent_comment=self.comment,
            body='Test reply'
        )

    def tearDown(self):
        self.user.delete()

    def test_post_model(self):
        self.assertEqual(str(self.post), 'Test Post')
        self.assertEqual(self.post.likes.count(), 0)

    def test_tag_model(self):
        self.assertEqual(str(self.tag), 'Test Tag')

    def test_comment_model(self):
        self.assertEqual(str(self.comment), 'testuser : Test comment')
        self.assertEqual(self.comment.likes.count(), 0)

    def test_reply_model(self):
        self.assertEqual(str(self.reply), 'testuser : Test reply')
        self.assertEqual(self.reply.likes.count(), 0)

    def test_liked_post_model(self):
        liked_post = LikedPost.objects.create(post=self.post, user=self.user)
        self.assertEqual(str(liked_post), 'testuser : Test Post')

    def test_liked_comment_model(self):
        liked_comment = LikedComment.objects.create(comment=self.comment, user=self.user)
        self.assertEqual(str(liked_comment), 'testuser : Test comment')

    def test_liked_reply_model(self):
        liked_reply = LikedReply.objects.create(reply=self.reply, user=self.user)
        self.assertEqual(str(liked_reply), 'testuser : Test reply')



class PostPageTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

         # Create a post with a valid UUID
        self.post = Post.objects.create(
            title='Test Post',
            artist='Test Artist',
            url='http://example.com',
            image='http://example.com/image.jpg',
            author=self.user,
            body='Test body content'
        )

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    # def test_post_page_view(self):
    #     # Assuming you have a valid UUID for testing, replace 'your_valid_uuid' with an actual UUID
    #     valid_uuid = str(uuid.uuid4())
    #     response = self.client.get(reverse('post-page', kwargs={'pk': valid_uuid}))
    #     self.assertEqual(response.status_code, 200)

    # def test_like_post_view(self):
    #     valid_uuid = str(uuid.uuid4())
    #     response = self.client.get(reverse('like-post', kwargs={'pk': valid_uuid}))
    #     # Assuming that this should return a redirect (status code 302) or some other response based on your implementation
    #     self.assertEqual(response.status_code, 302)

    

import datetime
import tempfile

from django.test import TestCase
from django.urls import reverse
from django.test import override_settings

from posts.forms import PostForm
from posts.tests import util
from posts.models import Post

class CreatePostViewTest(TestCase):

    def test_uses_create_post_template(self):
        response = self.client.get(reverse('posts:create'))
        self.assertTemplateUsed(response, 'posts/create.html')


    def test_create_post_page_uses_post_form(self):
        response = self.client.get(reverse('posts:create'))
        self.assertIsInstance(response.context['form'], PostForm)


class StorePostViewTest(TestCase):

    def assertPostIsSavedCorrectly(self, post, saved_post):
        self.assertEqual(post.title, saved_post.title)
        self.assertEqual(post.content, saved_post.content)
        self.assertEqual(post.image, saved_post.image)
        self.assertEqual(post.expiring_date, saved_post.expiring_date.strftime("%Y-%m-%d"))

    # TODO: test the view with methods that are not post
    def POST_object_to_store_url(self, post):
        return self.client.post(
            reverse('posts:store'),
            data={'title': post.title,
                'content': post.content,
                 'image': post.image,
                'publication_date': post.publication_date,
                'expiring_date': post.expiring_date,
            }
        )

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_POST_redirects_to_show_post_view(self):
        post = util.get_valid_post_object()
        response = self.POST_object_to_store_url(post)
        self.assertRedirects(response, reverse('posts:show'))

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_can_save_a_valid_POST_request(self):
        post = util.get_valid_post_object()
        response = self.POST_object_to_store_url(post)

        self.assertEqual(Post.objects.count(), 1)
        saved_post = Post.objects.first()

        self.assertPostIsSavedCorrectly(post=post, saved_post=saved_post)
        self.assertEqual(saved_post.publication_date, datetime.date.today())


class ShowPostViewTest(TestCase):
    pass

    # def test_uses_show_post_template(self):
    #     response = self.client.get(reverse('posts:show', ))

    # def test_displays_correct_post

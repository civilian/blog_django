import datetime
import tempfile

from django.test import TestCase
from django.urls import reverse
from django.test import override_settings

from posts.forms import PostForm
from posts.tests import util
from posts.tests.util import PostFactory
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
        self.assertEqual(post.expiring_date.strftime("%Y-%m-%d"), saved_post.expiring_date.strftime("%Y-%m-%d"))

    # TODO: test the view with methods that are not post
    def POST_object_to_store_url(self, post):
        return self.client.post(
            reverse('posts:store'),
            data= util.get_dict_from_post(post)
        )

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_POST_redirects_to_show_post_view(self):
        post = util.get_valid_post_object()
        response = self.POST_object_to_store_url(post)
        post = Post.objects.first()
        self.assertRedirects(response, reverse('posts:show', kwargs={'post_id': post.id}))


    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_can_save_a_valid_POST_request(self):
        post = util.get_valid_post_object()
        response = self.POST_object_to_store_url(post)

        self.assertEqual(Post.objects.count(), 1)
        saved_post = Post.objects.first()

        self.assertPostIsSavedCorrectly(post=post, saved_post=saved_post)
        self.assertEqual(saved_post.publication_date, datetime.date.today())


    def post_invalid_post(self):
        post = PostFactory.build(title='')
        return self.POST_object_to_store_url(post)


    def test_for_invalid_post_renders_create_template(self):
        response = self.post_invalid_post()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/create.html')


    def test_for_invalid_post_nothing_saved_to_db(self):
        response = self.post_invalid_post()
        self.assertEqual(Post.objects.count(), 0)


class ShowPostViewTest(TestCase):

    def test_uses_show_post_template(self):
        post = PostFactory()
        response = self.client.get(reverse('posts:show', kwargs={'post_id': post.id}))
        self.assertTemplateUsed(response, 'posts/show.html')


    def test_displays_correct_post(self):
        correct_post = PostFactory()
        other_post = PostFactory(title='other post')

        response = self.client.get(reverse('posts:show', kwargs={'post_id': correct_post.id}))

        self.assertContains(response, correct_post.title)
        self.assertEqual(response.context['post'].image, correct_post.image)
        self.assertContains(response, correct_post.content)
        self.assertContains(response, correct_post.publication_date.strftime('%b. %d, %Y'))
        self.assertContains(response, correct_post.expiring_date.strftime('%b. %d, %Y'))
        self.assertNotContains(response, other_post.title)


    def test_passes_correct_post_to_template(self):
        correct_post = PostFactory()
        other_post = PostFactory(title='other post')

        response = self.client.get(reverse('posts:show', kwargs={'post_id': correct_post.id}))

        self.assertEqual(response.context['post'], correct_post)


class IndexPostView(TestCase):

    def test_uses_index_post_template(self):
        response = self.client.get(reverse('posts:index'))
        self.assertTemplateUsed(response, 'posts/index.html')


    def test_displays_correct_posts(self):
        first_post = PostFactory(title='first post title')
        second_post = PostFactory(title='second post title')

        response = self.client.get(reverse('posts:index'))

        self.assertContains(response, 'first post title')
        self.assertContains(response, 'second post title')

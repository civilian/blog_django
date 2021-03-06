import datetime
import tempfile
import copy

from django.test import TestCase
from django.urls import reverse
from django.test import override_settings
from faker import Faker

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
            data=util.get_dict_from_post(post)
        )


    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_redirects_to_show_post_view(self):
        post = util.get_valid_post_object()
        response = self.POST_object_to_store_url(post)
        post = Post.objects.first()
        self.assertRedirects(response, reverse('posts:show', kwargs={'post_id': post.id}))


    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_can_save_a_valid_post(self):
        post = util.get_valid_post_object()
        self.POST_object_to_store_url(post)

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
        self.post_invalid_post()
        self.assertEqual(Post.objects.count(), 0)


@override_settings(MEDIA_ROOT=tempfile.gettempdir())
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
        PostFactory(title='other post')

        response = self.client.get(reverse('posts:show', kwargs={'post_id': correct_post.id}))

        self.assertEqual(response.context['post'], correct_post)
    

    def test_404_if_post_does_not_exist(self):
        response = self.client.get(reverse('posts:show', kwargs={'post_id': 1 }))

        self.assertEqual(response.status_code, 404)


class IndexPostView(TestCase):

    def test_uses_index_post_template(self):
        response = self.client.get(reverse('posts:index'))
        self.assertTemplateUsed(response, 'posts/index.html')


    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_displays_correct_posts(self):
        PostFactory(title='first post title')
        PostFactory(title='second post title')
        PostFactory.build(title='This post has not been saved')

        response = self.client.get(reverse('posts:index'))

        self.assertContains(response, 'first post title')
        self.assertContains(response, 'second post title')
        self.assertNotContains(response, 'This post has not been saved')
    

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_displays_trimmed_content(self):
        fake = Faker()
        post = util.save_valid_post_object(content=fake.sentence(nb_words=100))

        response = self.client.get(reverse('posts:index'))

        trimmed_content = post.content[:97] + '...'
        self.assertContains(response, trimmed_content)
        


@override_settings(MEDIA_ROOT=tempfile.gettempdir())
class EditPostView(TestCase):

    def test_uses_edit_post_template(self):
        post = PostFactory()
        response = self.client.get(reverse('posts:edit', kwargs={'post_id': post.id}))
        self.assertTemplateUsed(response, 'posts/edit.html')


    def test_404_if_post_does_not_exist(self):
        response = self.client.get(reverse('posts:edit', kwargs={'post_id': 1 }))

        self.assertEqual(response.status_code, 404)


    def test_passes_correct_post_to_template(self):
        correct_post = PostFactory()
        PostFactory(title='other post')

        response = self.client.get(reverse('posts:edit', kwargs={'post_id': correct_post.id}))

        self.assertEqual(response.context['form'].instance, correct_post)
    

    def test_displays_correct_post(self):
        correct_post = PostFactory()
        other_post = PostFactory(title='other post')

        response = self.client.get(reverse('posts:edit', kwargs={'post_id': correct_post.id}))

        self.assertContains(response, correct_post.title)
        self.assertEqual(response.context['form'].instance.image, correct_post.image)
        self.assertContains(response, correct_post.content)
        self.assertContains(response, correct_post.expiring_date.strftime("%Y-%m-%d"))
        self.assertNotContains(response, other_post.title)


class UpdatePostViewTest(TestCase):

    def assertPostIsSavedCorrectly(self, post, saved_post):
        self.assertEqual(post.title, saved_post.title)
        self.assertEqual(post.content, saved_post.content)
        self.assertEqual(post.image, saved_post.image)
        self.assertEqual(post.expiring_date.strftime("%Y-%m-%d"), saved_post.expiring_date.strftime("%Y-%m-%d"))
        self.assertEqual(post.publication_date.strftime("%Y-%m-%d"), saved_post.publication_date.strftime("%Y-%m-%d"))

    def POST_object_to_update_url(self, post):
        return self.client.post(
            reverse('posts:update', kwargs={'post_id': post.id}),
            data=util.get_dict_from_post(post)
        )

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_POST_redirects_to_show_post_view(self):
        post = util.save_valid_post_object()
        response = self.POST_object_to_update_url(post)
        post = Post.objects.first()
        self.assertRedirects(response, reverse('posts:show', kwargs={'post_id': post.id}))


    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_can_save_a_valid_POST_request(self):
        post = util.save_valid_post_object()

        post.title = 'New title'
        post.content = 'New content'
        ## We put a new temporary image
        post.image = util.get_test_image()
        post.publication_date = post.publication_date + datetime.timedelta(3)
        post.expiring_date = post.expiring_date + datetime.timedelta(1)

        self.POST_object_to_update_url(post)

        self.assertEqual(Post.objects.count(), 1)
        saved_post = Post.objects.first()

        self.assertPostIsSavedCorrectly(post=post, saved_post=saved_post)
        
    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def post_invalid_post(self):
        post = util.save_valid_post_object()
        
        post.title = ''

        return self.POST_object_to_update_url(post)


    def test_for_invalid_post_renders_edit_template(self):
        response = self.post_invalid_post()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/edit.html')

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_for_invalid_post_nothing_saved_to_db(self):
        correct_post = util.save_valid_post_object()
        
        incorrect_post = copy.deepcopy(correct_post)
        incorrect_post.title = ''
        
        self.POST_object_to_update_url(incorrect_post)

        saved_post = Post.objects.first()        

        self.assertPostIsSavedCorrectly(correct_post, saved_post)


    def test_404_if_post_does_not_exist(self):
        response = self.client.post(reverse('posts:update', kwargs={'post_id': 1 }))

        self.assertEqual(response.status_code, 404)

class DeletePostTest(TestCase):

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_deletes_view_redirects_to_index(self):
        post = PostFactory()
        response = self.client.post(reverse('posts:delete', kwargs={'post_id': post.id}))
        self.assertRedirects(response, reverse('posts:index'))
    

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_deletes_view_destroys_a_post(self):
        first_post = PostFactory(title='First post')
        PostFactory(title='Second post')

        self.client.post(reverse('posts:delete', kwargs={'post_id': first_post.id}))

        self.assertEqual(Post.objects.count(), 1)


    def test_404_if_post_does_not_exist(self):
        response = self.client.post(reverse('posts:delete', kwargs={'post_id': 1 }))

        self.assertEqual(response.status_code, 404)


class AjaxPublicationDateTest(TestCase):

    def POST_post_object_to_ajax_publication_date_url(self, post):
        return self.client.post(
                    reverse('posts:ajax_publication_date', 
                    kwargs={'post_id': post.id }), 
                    data=util.get_dict_from_post(post),
                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')


    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_POST_correct_date_answers_correct_json(self):
        post = PostFactory()
        post.publication_date = datetime.date.today()

        response = self.POST_post_object_to_ajax_publication_date_url(post)

        self.assertJSONEqual(str(response.content, encoding='utf8'),
                            {'message' : 'The publication date has been saved.'})


    def test_404_if_post_does_not_exist(self):
        response = self.client.post(
                    reverse('posts:ajax_publication_date', 
                    kwargs={'post_id': 1 }), 
                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(response.status_code, 404)


    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_POST_incorrect_date_answers_not_saved_json(self):
        post = PostFactory()
        post.publication_date = '---'

        response = self.POST_post_object_to_ajax_publication_date_url(post)

        self.assertJSONEqual(str(response.content, encoding='utf8'),
                            {'message' : 'Enter a valid date.'})
    

    # TODO: is this possible? it think yes
    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_POST_incorrect_post_answers_not_saved_json(self):
        post = PostFactory()
        post.title = ''
        post.content = ''

        response = self.POST_post_object_to_ajax_publication_date_url(post)

        self.assertJSONEqual(str(response.content, encoding='utf8'),
                            {'message' : 'The publication date has not been saved.'})
    

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_POST_correct_date_saves_new_post(self):
        post = PostFactory()
        post.publication_date = post.publication_date + datetime.timedelta(1)

        self.POST_post_object_to_ajax_publication_date_url(post)

        saved_post = Post.objects.first()

        self.assertEqual(post.publication_date, saved_post.publication_date)


    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_POST_incorrect_post_does_not_change_saved_post(self):
        post = PostFactory()
        post.publication_date = post.publication_date + datetime.timedelta(1)
        post.title = ''

        self.POST_post_object_to_ajax_publication_date_url(post)

        saved_post = Post.objects.first()

        self.assertNotEqual(post.publication_date, saved_post.publication_date)
    
    
    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_POST_incorrect_publication_date_does_not_change_saved_post(self):
        post = PostFactory()
        post.publication_date = '---'

        self.POST_post_object_to_ajax_publication_date_url(post)

        saved_post = Post.objects.first()

        self.assertNotEqual(post.publication_date, saved_post.publication_date)

from django.test import TestCase
from django.contrib.auth.models import AnonymousUser, User

from accounts.views import view_profile, edit_profile


# class SimpleTest(TestCase):
#     def test_signup(self):
#         response = self.client.post("/signup/", {
#             "email": "email@email.com", 
#             "password": "password", 
#             "password-confirm": "password", 
#             "firm": "big law firm"})
#         user = User.objects.get(email="email@email.com")
#         self.assertEqual(user.username, "email@email.com")
#         self.assertEqual(user.firm, "big law firm")
#         self.assertEqual(response.status_code, 302) #if it's successful it redirects


class SimpleTest(TestCase):

    def set_up(self):
        self.user = User.objects.create(username='profile_tester', email='profile_tester@mail.com', password='top_secret')
        login = self.client.login(username='profile_tester', password='top_secret')
        
    def test_profile_anonymous(self):
        # self.client.logout()

        response = self.client.get('/accounts/profile')
        self.assertEqual(response.status_code, 301)

        # request.user = AnonymousUser()
        # response = view_profile(request)
        # self.assertEqual(response.status_code, 302)

    # def test_profile_loginned(self):
    #     request = self.factory.get('/accounts/profile')

    #     request.user = self.user
    #     response = view_profile(request)
    #     self.assertEqual(response.status_code, 200)

    # def tear_down(self):
    # 	self.factory.delete()
    # 	self.user.delete()


# class EditProfileTest(TestCase):

#     def set_up(self):
#     	self.factory = RequestFactory()
#     	self.user = User.objects.create_user(
#     		username='edit_profile_tester', email='edit_profile_tester@mail.com', password='top_secret')

#     def test_edit_profile_anonymous(self):
#     	request = self.factory.get('/accounts/profile/edit')

#     	request.user = AnonymousUser()
#     	response = edit_profile(request)
#     	self.assertEqual(response.status_code, 302)

#     def test_edit_profile_loginned(self):
#     	request = self.factory.get('/accounts/profile/edit')

#     	request.user = self.user
#     	response = edit_profile(request)
#     	self.assertEqual(response.status_code, 200)

#     def tear_down(self):
#     	self.factory.delete()
#     	self.user.delete()


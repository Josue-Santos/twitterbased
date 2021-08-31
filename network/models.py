from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    profile_pic = models.ImageField(null=True, blank= True)
    


class Posts(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.CharField(max_length=1000,blank = False)
    date = models.DateTimeField(auto_now =True)
    likes = models.IntegerField(default=0)
    def __str__(self):
        return f"User: {self.user} post: {self.post} Date: {self.date} likes: {self.likes}"



class Likes(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name ="rel_Likes_user")
    post = models.ForeignKey(Posts,on_delete=models.CASCADE,related_name="rel_Likes_post")
    
    def __str__(self):
        return f"User: {self.user} Post: {self.post}"

class Following(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="follows")
    following = models.ForeignKey(User,on_delete=models.CASCADE,related_name="followed_by")

    def __str__(self):
        return f"User: {self.user} following: {self.following}"

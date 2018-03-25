from django.db import models


class Section(models.Model):
	subject = models.CharField(max_length=10, default="ERROR")
	crn = models.IntegerField()
	course_id = models.CharField(max_length=10, default="ERROR")
	section_number = models.CharField(max_length=200)
	course_attr = models.CharField(max_length=200)
	title = models.CharField(max_length=200)
	instructor = models.CharField(max_length=200)
	credit_hrs = models.CharField(max_length=200)
	meet_time = models.CharField(max_length=200)
	description = models.CharField(max_length=2000)
	location = models.CharField(max_length=200)
	status = models.CharField(max_length=200, choices=(('OPN', 'OPEN'), ('CLSD', 'CLOSED')), default='OPEN')


class WishList(models.Model):
	subject = models.CharField(max_length=10, default="ERROR")
	course_id = models.CharField(max_length=10, default="ERROR")

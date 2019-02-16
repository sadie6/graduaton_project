from django.db import models

# Create your models here.
class Student_Info(models.Model):
    Id = models.IntegerField(primary_key = True)
    name = models.CharField(max_length = 10)
    college = models.CharField(max_length = 20)  #学院
    SEX = (
        ('X', '女'),
        ('Y', '男')
        )
    sex = models.CharField(max_length = 5, choices = SEX)
    age = models.IntegerField()
    birthplace = models.CharField(max_length = 20)   #生源地
    Politics_Status = (
        ('A', '党员'),
        ('B', '预备党员'),
        ('C', '共青团员'),
        ('D', '其他')
        )
    politics_status = models.CharField(max_length = 10, choices = Politics_Status)
    Category = (
        ('A', '农村应届'),
        ('B', '农村往届'),
        ('C', '城市应届'),
        ('D', '城市往届'),
        ('E', '其他')
        )
    category = models.CharField(max_length = 10, choices = Category)
    major = models.CharField(max_length = 20)
    Family_Background = (
        ('A', '贫困'),
        ('B', '非贫困')
        )
    family_background = models.CharField(max_length = 10, choices = Family_Background)
    Educational_History = (
            ('A', '本科'),
            ('B', '硕士'),
            ('C', '博士')
        )
    educational_history = models.CharField(max_length = 10, choices = Educational_History, default = 'A')

class Borrow_Books(models.Model):
    Id = models.AutoField(primary_key = True)
    name = models.CharField(max_length = 30)
    category = models.CharField(max_length = 8)
    callno = models.CharField(max_length = 8)
    time = models.DateField()
    s_id = models.ForeignKey(Student_Info, on_delete = models.CASCADE)

class Student_Grade(models.Model):
    Id = models.AutoField(primary_key = True)
    term = models.IntegerField()
    course_name = models.CharField(max_length = 20)
    grade = models.IntegerField()
    Category = (
        ('A', '正常考试'),
        ('B', '补考'),
        ('C', '重修'),
        )
    category = models.CharField(max_length = 10, choices = Category)
    s_id = models.ForeignKey(Student_Info, on_delete = models.CASCADE)

class Internet_Data(models.Model):
    Id = models.AutoField(primary_key = True)
    login_time = models.DateTimeField()
    exit_time = models.DateTimeField()
    duration = models.IntegerField()
    flow = models.FloatField()
    s_id = models.ForeignKey(Student_Info, on_delete = models.CASCADE)

class Award(models.Model):
    Id = models.AutoField(primary_key = True)
    award_name = models.CharField(max_length = 40)
    s_id = models.ForeignKey(Student_Info, on_delete = models.CASCADE)

class One_Cartoon(models.Model):
    Id = models.AutoField(primary_key = True)
    time = models.DateTimeField()
    amount = models.FloatField()
    s_id = models.ForeignKey(Student_Info, on_delete = models.CASCADE)

class Administrator(models.Model):
    user_id = models.IntegerField(primary_key = True)
    password = models.CharField(max_length = 20)







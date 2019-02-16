from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.db.models.aggregates import Count,Sum,Avg
from student.models import Student_Info, Borrow_Books, Student_Grade, Internet_Data, One_Cartoon
import numpy as np
import random
import time
# Create your views here.
colleges = ['会计学院','计算机与信息工程学院','艺术学院','经济与贸易学院','工商管理学院','公共管理学院','数学与统计学院','外国语学院']
birthplaces = ['湖南','西藏','青海','宁夏','海南','甘肃','贵州','新疆','云南','重庆','吉林','山西','天津','江西','广西',
	'四川','辽宁','河北','河南','浙江','山东','江苏','广东','陕西','黑龙江','内蒙古','安徽','北京','福建','上海','湖北']
categorys = ['经济','管理','商贸', '语言','历史', '生活','哲学','伦理','逻辑','美学','心理', '文学', '艺术', '政治', 
	'天文', '地理', '数学', '电信', '工学', '电脑', '信息']  #21
def index(request):
	#政治面貌
	a = {'X':[0,0,0,0], 'Y':[0,0,0,0]}
	for i in ['X', 'Y']:
		a[i][0] = Student_Info.objects.filter(politics_status = 'A', sex = i).count()
		a[i][1] = Student_Info.objects.filter(politics_status = 'B', sex = i).count()
		a[i][2] = Student_Info.objects.filter(politics_status = 'C', sex = i).count()
		a[i][3] = Student_Info.objects.filter(politics_status = 'D', sex = i).count()
	

	#生源地分布
	b = []
	for place in birthplaces:
		p = {'name':place, 'value':Student_Info.objects.filter(birthplace = place).count()}
		b.append(p)

	#男女比例
	c = [0, 0]
	c[0] = Student_Info.objects.filter(sex = 'X').count()
	c[1] = Student_Info.objects.filter(sex = 'Y').count()

	#学院分布
	d = []
	for i in colleges:
		d1 = {'college': i, 'value':Student_Info.objects.filter(college = i).count()}
		d.append(d1)
	
	#考生类别
	e = [0,0,0,0]
	e[0] = Student_Info.objects.filter(category = 'A').count()
	e[1] = Student_Info.objects.filter(category = 'B').count()
	e[2] = Student_Info.objects.filter(category = 'C').count()
	e[3] = Student_Info.objects.filter(category = 'D').count()

	#学生概括
	f = [[0,0,0,0],[0,0,0,0],[0,0,0,0]]
	for index, i in enumerate(['A', 'B', 'C']):
		f[index][0] = Student_Info.objects.filter(educational_history = i, Id__startswith = 150).count()
		f[index][1] = Student_Info.objects.filter(educational_history = i, Id__startswith = 160).count()
		f[index][2] = Student_Info.objects.filter(educational_history = i, Id__startswith = 170).count()
		f[index][3] = Student_Info.objects.filter(educational_history = i, Id__startswith = 180).count()
	count1 = sum(f[0])
	count2 = sum(f[1])
	count3 = sum(f[2])
	count = count1 + count2 + count3
	f[0].extend([count1, count1/count])
	f[1].extend([count2, count2/count])
	f[2].extend([count3, count3/count])
	ff = {'本科':f[0],'研究生':f[1], '博士':f[2]}
	content = {
		'a' : a,
		'b' : b,
		'c' : c,
		'd' : d,
		'e' : e,
		'f' : ff,
	}
	print(e)
	return render(request, 'student_info.html', content)

def library(request):
	a = []
	for i in range(1,13):
		a.append(Borrow_Books.objects.filter(time__month = i).count())
	b = []
	for i in categorys:
		b1 = {'name':i, 'value':Borrow_Books.objects.filter(category = i).count()}
		b.append(b1)

	c = Borrow_Books.objects.annotate(num=Count('name')).filter(num__gt=0)[:12]
	content = {
	'a':a,
	'b':b,
	'c':c,
	}
	print(a)
	return render(request, 'library_info.html', content)

def grade(request):
	a = []
	for i in range(1,8):
		g1 = Student_Grade.objects.filter(term = i).count()
		g2 = Student_Grade.objects.filter(term = i, grade__lt = 55).count()
		a.append(g2/g1)
	a.append(0)

	b = []
	for i in ['A', 'B', 'C']:
		b.append(Student_Grade.objects.filter(category = i).count())

	c = []
	c.append(Student_Grade.objects.filter(grade__gt = 89).count())
	c.append(Student_Grade.objects.filter(grade__gt = 79, grade__lt = 89).count())
	c.append(Student_Grade.objects.filter(grade__gt = 59, grade__lt = 79).count())
	c.append(Student_Grade.objects.filter(grade__lt = 59).count())

	d = Student_Grade.objects.values('course_name').annotate(num = Count('Id')).filter(grade__lt = 55).order_by('-num')[:10]
	p = []
	for d1 in d:
		t = Student_Grade.objects.filter(course_name = d1['course_name']).aggregate(Avg('grade'))
		x = {'avg_grade':t['grade__avg'], 'num':d1['num'] ,'course_name' : d1['course_name'], 'p':d1['num']/Student_Grade.objects.filter(course_name = d1['course_name']).count()}
		p.append(x)
	#print(p)

	content = {
	'a':a,
	'b':b,
	'c':c,
	'p':p,
	}
	return render(request, 'grade_info.html',content)

def internet(request):
	a = [[],[],[],[]]
	a[0] = Internet_Data.objects.filter(s_id__Id__startswith = 180)
	a[1] = Internet_Data.objects.filter(s_id__Id__startswith = 170)
	a[2] = Internet_Data.objects.filter(s_id__Id__startswith = 160)
	a[3] = Internet_Data.objects.filter(s_id__Id__startswith = 150)

	b = []

	for i in range(0,24):
		b.append(Internet_Data.objects.filter(login_time__hour = i).count())
	print(b)
	content = {
	'a':a,
	'b':b,
	}
	return render(request, 'internet_info.html', content)

def cartoon(request):
	#消费次数随时间变化
	a = [[],[]]
	for i in range(6,23):
		a[0].append(One_Cartoon.objects.filter(time__hour = i, s_id__sex = 'X').count())
		a[1].append(One_Cartoon.objects.filter(time__hour = i, s_id__sex = 'Y').count())

	#单次消费金额分布
	b = []
	b.append(One_Cartoon.objects.filter(amount__lt = 5).count())
	b.append(One_Cartoon.objects.filter(amount__lt = 10, amount__gt = 4).count())
	b.append(One_Cartoon.objects.filter(amount__lt = 15, amount__gt = 9).count())
	b.append(One_Cartoon.objects.filter(amount__lt = 20, amount__gt = 14).count())
	b.append(One_Cartoon.objects.filter(amount__gt = 20).count())


	#平均消费
	c = [0,0]
	c[0] = One_Cartoon.objects.filter(s_id__sex = 'X').aggregate(Avg('amount'))['amount__avg'] * 3
	c[1] = One_Cartoon.objects.filter(s_id__sex = 'Y').aggregate(Avg('amount'))['amount__avg'] * 2.5
	c.append(c[0]*30)
	c.append(c[1]*30)
	print(c)

	content = {
	'a':a,
	'b':b,
	'c':c,
	}
	return render(request, 'cartoon_info.html', content)


def fp_growth(request):
	sample = {1:'成绩好',2:'成绩差',3:'借书多',4:'借书少',5:'上网时间长',6:'上网时间短',7:'获奖',8:'未获奖',
	9:'饮食规律',10:'饮食不规律',11:'农村',12:'城市',13:'贫困',14:'非贫困'}
	


	content = {
	}
	return render(request, 'fp_1.html', content)





#假数据插入函数
def student_info_insert(request):
	Id = 1800000
	name = 'xxx'
	
	majors = {'会计学院' : ['会计学', '财务管理', '审计学'], '计算机与信息工程学院' : ['计算机科学与技术', '软件工程', '信息管理与信息系统', '工程管理', '电子信息工程'],
	'艺术学院' : ['文化产业管理', '视觉传达设计', '环境设计', '动画', '服装与服饰设计'], '经济与贸易学院' : ['电子商务', '经济学', '国际商务', '国际经济与贸易'], 
	'工商管理学院' : ['工商管理', '市场营销', '人力资源管理', '物流管理'], '公共管理学院': ['社会工作', '公共事业管理', '行政管理', '城市管理'],
	'数学与统计学院' : ['经济统计学', '数学与应用数学', '信息与计算科学', '金融数学'], '外国语学院': ['英语', '商务英语', '法语']}
	sex_p = {'会计学院' : [0.8, 0.2], '计算机与信息工程学院' : [0.3, 0.7],'艺术学院' : [0.65, 0.35], '经济与贸易学院' : [0.68, 0.32], 
	'工商管理学院' : [0.65, 0.35], '公共管理学院': [0.55, 0.45],'数学与统计学院' : [0.4, 0.6], '外国语学院': [0.85, 0.15]}
	while(Id < 1800001):
		Id += 1
		college = np.random.choice(colleges, p = [0.25,0.12,0.08,0.15,0.15,0.15,0.07,0.03])
		sex = np.random.choice(['X', 'Y'], p = sex_p[college])
		age = np.random.choice([16, 17, 18, 19, 20, 21, 22, 23], p = [0.02,0.08,0.3,0.4,0.13,0.04,0.02,0.01])  #年龄 跟学年有关
		birthplace = np.random.choice(birthplaces, p = [0.6] + [0.01] * 20 + [0.02] * 10)
		politics_status = np.random.choice(['A', 'B', 'C', 'D'], p = [0.00, 0.1, 0.8, 0.1 ])     #政治背景 跟学年有关
		category = np.random.choice(['A', 'B', 'C', 'D'], p = [0.32, 0.12, 0.38, 0.18 ])
		major = np.random.choice(majors[college])
		family_background = np.random.choice(['A', 'B'], p = [0.7, 0.3 ])
		educational_history = np.random.choice(['A', 'B', 'C'], p = [0.8, 0.16, 0.04 ])
		s1 = Student_Info(Id = Id, name = name, college = college, sex = sex, age = age,
			 birthplace = birthplace, politics_status = politics_status, category = category,
			 major = major, family_background = family_background, educational_history = educational_history)
		#s1.save()
		print(Id, college,sex, age , birthplace, politics_status, category, major, family_background, educational_history )
	return HttpResponse("success")

def library_insert(request):
	callno = 'XXXX'
	
	for i in range(2500,3000):
		name = 'xxx%s' %i
		category = np.random.choice(categorys, p = [0.1] * 2 + [0.06] * 5 + [0.03] * 10 + [0.05] * 4)
		year = np.random.choice([2018])
		month = np.random.choice(['01', '02', '03','04', '05', '06','07', '08', '09','10', '11', '12',], p = [0.18, 0.02, 0.12] + [0.05]*3 + [0.21, 0.04, 0.13] + [0.05]*3)
		day = random.randint(1,28)
		if day//10 == 0:
			day = '0%s' %day 
		time = '%s-%s-%s' %(year, month, day)
		s_id = Student_Info.objects.get(Id = random.randint(1800001, 1801800))
		print(name, category, time, s_id)
		b1 = Borrow_Books(name = name, category = category, callno = callno, time = time, s_id = s_id)
		#b1.save()
		
	return HttpResponse("success")

def grade_insert(request):
	course_names = {1:['高数一','英语一','中国文化概论','体育一','形势与政策'], 2:['高数二','英语二','经济学通论','体育二','应用写作'], 3:['马原', '形式政策二', '离散数学', '线性代数'], 4:['贸易经济学','大学英语拓展','概率论与数理统计A','毛泽东思想'],
	 5:['管理学通论','民俗文化X','毛泽东思想二','西方经济学'], 6:['职业发展二','创新创业X','计算机原理','网络信息安全'], 
	7:['财税实务专题', '课程设计', '物联网技术', '软件过程管理']}
	for i in range(100):
		term = np.random.choice([1, 2])  
		course_name = np.random.choice(course_names[term])
		grade = random.randint(20,40)
		category = np.random.choice(['A', 'B', 'C'], p = [0.5, 0.4, 0.1])
		s_id = Student_Info.objects.get(Id = random.randint(1800001, 1801000))
		g1 = Student_Grade(term = term, course_name = course_name, grade = grade, category = category, s_id = s_id)
		#g1.save()
		print(term, course_name, grade, category, s_id)
	return HttpResponse("success")

def internet_insert(request):
	
	for i in range(1000):
		day = 11
		t = np.random.choice([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,0], 
			p = [0.011,0.01] + [0.01, 0.01, 0.007, 0.003, 0.009] + [0.05,0.07,0.07,0.08,0.08] + [0.02, 0.02] + [0.03, 0.04, 0.06] + [0.06, 0.06 , 0.1, 0.1,0.06] + [0.025, 0.015])
		m = random.randint(0,59)
		login_time = '2018-11-11 %s:%s:%s' %(t,m,m)
		t2 = t + np.random.choice([1,2,3,4,5,6,7,8], p = [0.3, 0.25] + [0.2, 0.1]  + [0.05, 0.05] + [0.03, 0.02])
		if t2 > 23:
			day += 1
			t2 = t2%24
		exit_time = '2018-11-%s %s:%s:%s' %(day,t2,m,m)
		d1 = time.mktime(time.strptime(login_time,"%Y-%m-%d %H:%M:%S"))
		d2 = time.mktime(time.strptime(exit_time, "%Y-%m-%d %H:%M:%S"))
		duration = (d2 - d1)/60
		flow = np.random.choice([1,2,3,4,5,6,7,8,9,10], p = [0.05,0.07,0.07] + [0.12,0.15,0.2] + [0.14,0.08,0.07,0.05]) * duration
		s_id = Student_Info.objects.get(Id = random.randint(1800001, 1801000))
		i1 = Internet_Data(login_time = login_time, exit_time = exit_time, duration = duration, flow = flow, s_id = s_id)
		#i1.save()
		print(login_time,exit_time,duration, flow,s_id)
	return HttpResponse("success")


def cartoon_insert(request):
	for i in range(1000):
		t = np.random.choice([6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22], 
			p = [0.01, 0.06 , 0.13, 0.08 ,0.02] + [0.08, 0.17, 0.05, 0.02] + [0.02, 0.02]  + [0.1, 0.1, 0.08, 0.02] + [0.02, 0.02])
		time = '2018-11-11 %s:00:00' %t
		amount = np.random.choice([3,6,12,18,22], p=[0.15, 0.4, 0.3, 0.1, 0.05])
		s_id = Student_Info.objects.get(Id = random.randint(1800001, 1801000))
		c1 = One_Cartoon(time = time, amount = amount, s_id = s_id)
		#c1.save()
		print(time, amount, s_id)
	return HttpResponse("success")
def award_insert(request):
	pass
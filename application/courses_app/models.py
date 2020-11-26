from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import datetime



class User(AbstractUser):
    role = models.CharField("Роль", max_length=15, default='student')
    tel = models.CharField("Телефон", max_length=15, blank=True, null=True)
    info = models.CharField("О себе",  max_length=1500, blank=True, null=True)
    isu_number = models.IntegerField("номер ису", blank=True, null=True)
    group = models.ForeignKey(
        'StudentGroup', on_delete=models.PROTECT, null=True, blank=True,
        related_name='members'
    )
    access_key = models.CharField("Ключ доступа", max_length=15, default='student')

    courses = models.ManyToManyField(
        'Course', related_name='students_in_course'
    )

    REQUIRED_FIELDS = [
        'email', 'group', 'info', 'isu_number', 'first_name', 'last_name', 'groups'
        # 'first_name', 'last_name', 'email', 'role', 'tel', 'group'
    ]

    def __str__(self):
        return self.username


class StudentStream(models.Model):
    title = models.CharField(max_length=60)
    course_access = models.ManyToManyField(
        'Course', related_name='streams_on_a_course'
    )
    start_date = models.DateTimeField(editable=True, blank=True, null=True, verbose_name='старт')
    deadline_date = models.DateTimeField(editable=True, blank=True, null=True, verbose_name='дедлайн')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.title


class StudentGroup(models.Model):
    title = models.CharField(max_length=255)
    number = models.CharField(max_length=15)
    year_of_receipt = models.IntegerField()
    streams = models.ManyToManyField(
        StudentStream, through='GroupInStream', related_name='groups'
    )
    access_key = models.CharField(max_length=15, blank=True, null=True, verbose_name='ключ доступа к группе')


    class Meta:
        unique_together = ['number', 'year_of_receipt']

    def add_member(self, user_id):
        user_to_add = User.objects.get(id=user_id)
        user_to_add.group = self
        user_to_add.save()

    def __str__(self):
        return self.title


class GroupInStream(models.Model):
    group = models.ForeignKey(StudentGroup, on_delete=models.CASCADE)
    stream = models.ForeignKey(StudentStream, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.stream.title} {self.group.number}'


class Course(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=1024, blank=True, null=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)


    def __str__(self):
        return self.name


class StudentInCourse(models.Model):
    STATUS_TYPES = [
        ('1', 'None'),
        ('2', 'In_progress'),
        ('3', 'Done')
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    status = models.CharField(choices=STATUS_TYPES, default='1', max_length=1)

    # def __str__(self):
    #     return f'{self.stream.title} {self.group.number}'


class Lesson(models.Model):
    LESSON_TYPES = [
        ('1', 'Lecture'),
        ('2', 'Practical work'),
        ('3', 'Laboratory work')
    ]

    stream = models.ForeignKey(StudentStream, on_delete=models.CASCADE, blank=True, null=True)
    # student_group = models.ForeignKey(StudentGroup, on_delete=models.CASCADE, blank=True, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    lesson_type = models.CharField(choices=LESSON_TYPES, default='1', max_length=1)
    date = models.DateField(default=datetime.date.today)

    def __str__(self):
        return 'Course: {} {}'.format(self.course, self.get_lesson_type_display())


class StudentLessonResult(models.Model):
    MARKS = [
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5')
    ]

    VISIT_TYPES = [
        ('1', 'Visited'),
        ('2', 'Missed')
    ]
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name = "students_in_lesson")
    mark = models.CharField(choices=MARKS, default='1', max_length=1)
    visit = models.CharField(choices=VISIT_TYPES, default='2', max_length=1)
    comment = models.CharField(max_length=255)

    def __str__(self):
        return 'Student {}. Mark: {}. {}'.format(self.student, self.get_mark_display(), self.get_visit_display())


class Section(models.Model):
    section = models.CharField(max_length=50, blank=True, null=True)

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name = 'sections_in_course')
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=1024, blank=True, null=True)

    def __str__(self):
        return 'Section {} for course {}'.format(self.section, self.course.name)


class ClassmatesCheckedTask(models.Model):
    number = models.CharField(max_length=10)

    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=1024)
    deadline_in_stream = models.ManyToManyField(
        'StudentStream', related_name='classmates_task_in_stream'
    )


    def __str__(self):
        return 'Task {} for section {}'.format(self.number, self.section.section)


class ClassmatesCheckedTaskInStream(models.Model):
    task_with_classmates = models.ForeignKey(ClassmatesCheckedTask, on_delete=models.CASCADE, related_name = 'deadline_value')
    student_stream = models.ForeignKey(StudentStream, on_delete=models.CASCADE)
    start_date = models.DateTimeField(editable=True, auto_now_add=True, blank=True, null=True, verbose_name='старт')
    deadline_date = models.DateTimeField(editable=True, blank=True, null=True, verbose_name='дедлайн')


class TaskOption(models.Model):
    option = models.ForeignKey(ClassmatesCheckedTask, on_delete=models.CASCADE)
    index_number = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=1024)

    def __str__(self):
        return 'Option for classmates checked task {}'.format(self.option.number)


class StudentResult(models.Model):
    """Associative entity between User, TaskOption"""
    result = models.CharField(max_length=20)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    option = models.ForeignKey(TaskOption, on_delete=models.CASCADE)
    performance = models.CharField(max_length=20)
    description = models.CharField(max_length=1024, default='')

    def __str__(self):
        return 'Result {} (Associative)'.format(self.result)


class Check(models.Model):
    """Associative entity between User, StudentResult"""
    check = models.CharField(max_length=20)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    result = models.ForeignKey(StudentResult, on_delete=models.CASCADE)
    verifier = models.CharField(max_length=20)
    mark = models.CharField(max_length=10, default='')
    comment = models.CharField(max_length=255, default='')
    description = models.CharField(max_length=1024, default='')

    def __str__(self):
        return 'Check {} (Associative)'.format(self.check)


class TaskWithTick(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name = 'task_with_tick_in_section')
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=1024)
    tick_text = models.CharField(max_length=1024, blank=True, null=True)
    points = models.IntegerField(blank=True, null=True)
    index_number = models.IntegerField(blank=True, null=True)
    deadline_in_stream = models.ManyToManyField(
        'StudentStream', through = 'TaskWithTickInStream', related_name='task_with_tick_in_stream'
    )


    def __str__(self):
        return '{}, Task: {}'.format(self.section, self.title)


class TaskWithTickInStream(models.Model):
    task_with_tick = models.ForeignKey(TaskWithTick, on_delete=models.CASCADE, related_name = 'deadline_value')
    student_stream = models.ForeignKey(StudentStream, on_delete=models.CASCADE)
    start_date = models.DateTimeField(editable=True, auto_now_add=True, blank=True, null=True, verbose_name='старт')
    deadline_date = models.DateTimeField(editable=True, blank=True, null=True, verbose_name='Профессия')
#
#
# class TaskWithTickOption(models.Model):
#     task_with_tick = models.ForeignKey(TaskWithTick, on_delete=models.CASCADE)
#     description = models.CharField(max_length=1024)
#     index_number = models.IntegerField(blank=True, null=True)
#
#     def __str__(self):
#         return '{}, Description: {}'.format(self.task_with_tick, self.description)


class TaskWithTickStudentResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #task_with_tick_option = models.ForeignKey(TaskWithTickOption, on_delete=models.CASCADE)
    task_with_tick = models.ForeignKey(TaskWithTick, on_delete=models.CASCADE, blank=True, null=True)
    perform = models.BooleanField(default=False)
    perform_date = models.DateField(default=datetime.date.today, blank=True, null=True)

    def __str__(self):
        return 'Is performed? {}, Date: {}'.format(self.perform, self.perform_date)


class TaskWithTeacherCheck(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name = 'task_with_teacher_check_in_section')
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=1024, blank=True, null=True)
    upload_file = models.BooleanField(default = False, blank=True, null=True)
    points = models.IntegerField(blank=True, null=True)
    index_number = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f'{self.section}, Task: {self.title}'


class TaskWithTeacherCheckInStream(models.Model):
    task_with_teacher = models.ForeignKey(TaskWithTeacherCheck, on_delete=models.CASCADE, related_name = 'deadline_value')
    student_stream = models.ForeignKey(StudentStream, on_delete=models.CASCADE)
    start_date = models.DateTimeField(editable=True, auto_now_add=True, blank=True, null=True, verbose_name='старт')
    deadline_date = models.DateTimeField(editable=True, blank=True, null=True, verbose_name='дедлайн')


class TaskWithTeacherCheckOption(models.Model):
    task = models.ForeignKey(TaskWithTeacherCheck, on_delete=models.CASCADE, related_name = 'option_for_task_with_teacher')
    title = models.CharField(max_length=255, blank = True, null=True)
    description = models.CharField(max_length=1024, blank = True, null=True)

    def __str__(self):
        return f'{self.task}, Description: {self.description}'


class TaskWithTeacherCheckResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    option = models.ForeignKey(TaskWithTeacherCheckOption, on_delete=models.CASCADE)

    perform = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.option}, User: {self.user} Is performed? {self.perform}'


class TaskWithTeacherCheckCheck(models.Model):
    """Associative entity between User, TaskWithTeacherCheckResult"""
    check = models.CharField(max_length=20)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    result = models.ForeignKey(TaskWithTeacherCheckResult, on_delete=models.CASCADE)
    verifier = models.CharField(max_length=20)
    mark = models.CharField(max_length=10, default='')
    comment = models.CharField(max_length=255, default='')
    description = models.CharField(max_length=1024, default='')

    def __str__(self):
        return 'TaskWithTeacherCheckCheck {} (Associative)'.format(self.check)


class TaskWithKeyword(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name = 'task_with_keyword_in_section')
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=1024)
    upload_file = models.BooleanField(default = False, blank=True, null=True)
    index_number = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f'{self.section}, Task: {self.title}'


class TaskWithKeywordInStream(models.Model):
    task_with_keyword = models.ForeignKey(TaskWithKeyword, on_delete=models.CASCADE, related_name = 'deadline_value')
    student_stream = models.ForeignKey(StudentStream, on_delete=models.CASCADE)
    start_date = models.DateTimeField(editable=True, auto_now_add=True, blank=True, null=True, verbose_name='старт')
    deadline_date = models.DateTimeField(editable=True, blank=True, null=True, verbose_name='дедлайн')


class TaskWithKeywordOption(models.Model):
    task = models.ForeignKey(TaskWithKeyword, on_delete=models.CASCADE, related_name = 'option_for_task_with_keyword')
    description = models.CharField(max_length=1024, blank=True, null=True)
    keyword = models.CharField(max_length=128, blank=True, null=True)
    index_number = models.IntegerField(blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f'{self.task}, Description: {self.description}'


class TaskWithKeywordResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    option = models.ForeignKey(TaskWithKeywordOption, on_delete=models.CASCADE)
    user_keyword = models.CharField(max_length=128, blank=True, null=True)
    perform = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.option}, User: {self.user} Is performed? {self.perform}'




class CourseNews(models.Model):
    date = models.DateTimeField(editable=True, blank=True, null=True, verbose_name='Дата публикации')
    stream = models.ForeignKey(StudentStream, on_delete=models.CASCADE)
    #course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=128, blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    to_email = models.BooleanField(default=False)
    tags = models.CharField(max_length=1024, blank=True, null=True)


    def __str__(self):
        return f'{self.title} / {self.date}'


def database_src_path(instance, filename):
    return 'media/sandbox_db_{0}/src/{1}'.format(instance.id, filename)


def database_media_path(instance, filename):
    return 'media/sandbox_db_{0}/media/{1}'.format(instance.id, filename)


class Badge(models.Model):
    title = models.CharField(max_length=128, blank=True, null=True, verbose_name = "Название бейджа")
    description = models.TextField(blank=True, null=True, verbose_name = "Описание бейджа")
    image = models.ImageField(
        upload_to=database_media_path,
        null=True,
        blank=True
    )


class BadgeForUser(models.Model):
    course = models.ForeignKey(StudentInCourse, on_delete=models.CASCADE, verbose_name = "Курс")
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE, verbose_name = "Бейдж")
    date = models.DateField(default=datetime.date.today, verbose_name = "дата получения")



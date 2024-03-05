from models import User, Course, Lesson, Task, Submission

while True:
    print('''Выберите действие:\n 
                1. Регистрация
                2. Авторизация\n''')

    user_choice = int(input('Выберите действие: '))


    if user_choice == 1:
        username = input('username: ')
        password = input('password: ')
        role = input('choice role(student/teacher): ')

        user = User(username=username, password=password, role=role)
        user.save()


    elif user_choice == 2:
        username = input('username: ')
        password = input('password: ')

        try:
            user = User.get((User.username == username) & (User.password == password))
            print('Successfully')
        except User.DoesNotExist:
            print('домой')

        if user.role == 'student':
            while True:
                print('''Выберите действие:
                    1. Просмотреть доступные курсы
                    2. Просмотреть уроки конкретного курса
                    3. Просмотреть задания урока
                    4. Отправить задание
                    5. Выход из аккаунта''')

                user_choice = input('\nВыберите дейсвтие: ')

                if user_choice == '1':
                    courses = Course.select()

                    for course in courses:
                        print(f'{course.id}, {course.title}')

                elif user_choice == '2':
                    courses = Course.select()

                    for course in courses:
                        print(f'{course.id}: {course.title}')

                    title = input('Введите курс: ')

                    try:
                        course = Course.get(Course.title == title)
                        lessons = Lesson.select().where(Lesson.course == course)

                        if lessons:
                            print(f'Курс: {course.id}: {course.title}')
                            for lesson in lessons:
                                print(f'Урок: {lesson.id}: {lesson.title}')
                        elif not lessons:
                            print(f'{course.title} не содержит уроков')

                    except Course.DoesNotExist:
                        print('ошибка')

                elif user_choice == '3':
                    lessons = Lesson.select()

                    for lesson in lessons:
                        print(f'{lesson.id}: {lesson.title}')

                    lesson = input('Введите номер урока: ')

                    try:
                        task = Task.get(lesson=lesson)
                        tasks = Task.select().where(Task.lesson == lesson)

                        if tasks:
                            print(f'{task.id}: {task.lesson}, {task.description}, {task.deadline}')

                    except Task.DoesNotExist:
                        print('ошибка')

                elif user_choice == '4':
                    lessons = Lesson.select()
                    for lesson in lessons:
                        print(f'{lesson.id}: {lesson.title}')

                    lesson_id = input('Введите номер урока для отправки задания: ')

                    try:
                        lesson = Lesson.get(id=lesson_id)
                        tasks = Task.select().where(Task.lesson == lesson)

                        if tasks:
                            print(f'Выберите задание для отправки:')
                            for task in tasks:
                                print(f'{task.id}: {task.description}, Дедлайн: {task.deadline}')

                            task_id = input('Введите номер задания: ')
                            task = Task.get(id=task_id)

                            solution = input('Введите решение задания: ')

                            # Create a new submission
                            submission = Submission.create(student=user, task=task, solution=solution)
                            print(f'Задание успешно отправлено. ID задания: {submission.id}')
                        else:
                            print('Нет доступных заданий для выбранного урока.')

                    except Lesson.DoesNotExist:
                        print('Ошибка: Нет такого урока.')

                elif user_choice == '5':
                    print('Вы вышли из аккаунта!')
                    break


        elif user.role == 'teacher':
            while True:
                print('''Выберите действие:
                    1. Добавить новый курс
                    2. Добавить новый урок 
                    3. Добавить новое задание
                    4. Просмотреть задания студентов
                    5. Оценить задание студента
                    6. Посмтореть все задания
                    7. Выход из аккаунта''')

                user_choice = input('Выберите действие: ')

                if user_choice == '1':
                    title = input('Введите название курса: ')
                    description = input('Введите описание курса: ')
                    course = Course(title=title, description=description)
                    course.save()

                elif user_choice == '2':
                    courses = Course.select()

                    if courses:
                        for course in courses:
                            print(f'{course.id}: {course.title}')

                    course_id = input('Введите номер курса: ')
                    lesson_title = input('Введите название урока: ')
                    lesson_content = input('Введите контент: ')

                    try:
                        course = Course.get(id=course_id)
                        lesson = Lesson(course=course, title=lesson_title, content=lesson_content)
                        lesson.save()
                        print('Урок добавлен!')
                    except Course.DoesNotExist:
                        print('Такого нету')

                elif user_choice == '3':
                    lessons = Lesson.select()

                    if lessons:
                        for lesson in lessons:
                            print(f'{lesson.id}: {lesson.title}, {lesson.content}')

                    lesson_number = int(input('Введите номер урока: '))
                    task_description = input('Введите описание задания: ')
                    deadline = input('Введите дедлайн (гггг-мм-дд чч:мм): ')
                    max_points = int(input('Введите макс баллы: '))

                    try:
                        lesson = Lesson.get(id=lesson_number)
                        new_task = Task(lesson=lesson, description=task_description, deadline=deadline, max_score=max_points)
                        new_task.save()
                        print('Новое задание успешно сохранено!')

                    except Lesson.DoesNotExist:
                        print('не то')

                elif user_choice == '4':
                    lessons = Lesson.select()

                    for lesson in lessons:
                        print(f'{lesson.id}:{lesson.title}')

                elif user_choice == '5':
                    tasks = Task.select()
                    if tasks:
                        for task in tasks:
                            print(f'{task.id}, {task.description}')

                    task_id = input('Введите номер задания для оценки: ')

                    try:
                        task = Task.get(id=task_id)
                        submissions = Submission.select().where(Submission.task == task)

                        if submissions:
                            print(f'Задания для оценки по заданию "{task.description}":')
                            for submission in submissions:
                                print(
                                    f'{submission.id}: {submission.student.username}, Отправлено: {submission.submitted_at}')
                        else:
                            print('Нет поданных заданий для выбранного задания.')

                    except Task.DoesNotExist:
                        print('Ошибка: Нет такого задания.')

                elif user_choice == '6':
                    courses = Course.select()
                    lessons = Lesson.select()
                    tasks = Task.select()

                    for course in courses:
                        print(f'Курсы: {course.id}: {course.title}\n')
                    for lesson in lessons:
                        print(f'Уроки: {lesson.id}: {lesson.title}\n')
                    for task in tasks:
                        print(f'Задания: {task.id}: {task.description}, {task.deadline}\n')

                elif user_choice == '7':
                    print('Вы вышли из аккаунта!')
                    break

                else:
                    print('Введите правильную цифру!')
    else:
        print('нету')
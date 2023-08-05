from . import attempt_cache
from .utils import exit_util
from .models.lesson import Lesson
from .models.section import Section
from .course_cache import CourseCache

FORWARD = 1
BACK = -1

cached_lessons = CourseCache()

def update_step_position(position, steps, direction):
    position += direction
    if position > len(steps) or position < 1:
        # if we get here, it means we've run out of steps in this lesson!
        raise ValueError
    return position

def navigate(user, step_type, direction, data=None, course_cache=None):
    if data is None:
        data = attempt_cache.get_data()
    try:
        position = data['current_position']
        lesson = Lesson.get(user, data['lesson_id'])
        steps = lesson.items()
    except KeyError:
        return False

    # ensure that direction is either -1 or 1
    # idk why we have to do this, but it was in the original code
    direction = (-1,1)[direction > 0]

    lesson_pos = None
    while True:
        try:
            position = update_step_position(position, steps, direction)
        except ValueError:
            if course_cache is None:
                break
            else:
                try:
                    lesson_id, lesson_pos = course_cache.get_next_lesson(
                        lesson.id, direction, lesson_pos
                    )
                except ValueError:
                    break
                lesson = Lesson.get(user, lesson_id)
                data['lesson_id'] = lesson.id
                steps = lesson.items()
                data['steps'] = [s.id for s in steps]
                position = (0, len(steps)+1)[direction < 0]
                continue
        step = steps[position-1]
        if step_type == "all" or step.block['name'] == step_type:
            data['current_position'] = position
            attempt_cache.set_data(data)
            return True
    return False


def _validate_nav(user, data):
    """check that it's possible to navigate through this course"""
    if cached_lessons.load(user):
        if int(data['lesson_id']) not in cached_lessons.data['lessons']:
            exit_util("Unable to locate the current lesson within the course cache. Have you set the course using the 'course' command?")
    else:
        exit_util("Please first set the course ID via the 'course' command.")


def next_step(user, step_type):
    data = attempt_cache.get_data()
    _validate_nav(user, data)
    return navigate(user, step_type, FORWARD, data, cached_lessons)


def prev_step(user, step_type):
    data = attempt_cache.get_data()
    _validate_nav(user, data)
    return navigate(user, step_type, BACK, data, cached_lessons)

def create_course_cache(course):
    global cached_lessons
    cached_lessons = CourseCache(course)
    return cached_lessons

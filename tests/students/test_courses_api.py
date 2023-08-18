import pytest as pytest
from django.forms import model_to_dict
from django.urls import reverse
from rest_framework.test import APIClient
from model_bakery import baker

from students.models import Student, Course

@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)
    return factory


@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)
    return factory


@pytest.mark.django_db
def test_get_first_course(client, course_factory, student_factory):
    course = course_factory(_quantity=1)
    print(course_id)

    url = reverse('courses-detail', args=(course[0].id,))
    response = client.get(url)
    data = response.json()

    assert response.status_code == 200
    assert data['name'] == course[0].name


@pytest.mark.django_db
def test_create_list_courses(client, course_factory, student_factory):
    students = student_factory(_quantity=10)
    courses = course_factory(_quantity=20)

    url = reverse('courses-list')
    response = client.get(url)
    data = response.json()

    assert response.status_code == 200
    assert len(data) == len(courses)


@pytest.mark.django_db
def test_filter_id_courses(client, course_factory, student_factory):
    courses = course_factory(_quantity=10)

    url = reverse('courses-detail', args=(course[2].id,))
    response = client.get(url, {'id': courses[2].id})

    data = response.json()

    assert response.status_code == 200
    assert data['name'] == courses[2].name


@pytest.mark.django_db
def test_filter_name_courses(client, course_factory, student_factory):
    students = student_factory(_quantity=10)
    courses = course_factory(_quantity=5)

    url = reverse('courses-list')
    response = client.get(url, {'name': courses[2].name})
    data = response.json()

    assert response.status_code == 200
    assert data[0]['name'] == courses[2].name


@pytest.mark.django_db
def test_create_course(client):
    count = Course.objects.count()

    url = reverse('courses-list')
    response = client.post(url, data={'name': 'Python'})

    assert response.status_code == 201
    assert Course.objects.count() == count + 1


@pytest.mark.django_db
def test_patch_course(client, course_factory, student_factory):

    students = student_factory(_quantity=30)
    courses = course_factory(_quantity=20)

    url = reverse('courses-detail', args=(course[5].id,))
    response = client.patch(url, data={'name': 'Python'})
    data = response.json()

    assert response.status_code == 200
    assert data['name'] == 'Python'


@pytest.mark.django_db
def test_delete_course(client, course_factory, student_factory):
    students = student_factory(_quantity=30)
    courses = course_factory(_quantity=20)
    course_id = str(courses[7].id)
    count = Course.objects.count()

    url = reverse('courses-detail', args=(course_id,))
    response = client.delete(url)

    assert response.status_code == 204
    assert Course.objects.count() == count - 1
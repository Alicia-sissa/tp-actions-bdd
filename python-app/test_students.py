import pytest
import psycopg2

from students import add_student, get_student, average_grade


@pytest.fixture
def conn():
    connection = psycopg2.connect(
        host="localhost",
        database="tp",
        user="postgres",
        password="postgres"
    )

    with connection.cursor() as cur:
        cur.execute("TRUNCATE students RESTART IDENTITY")

    connection.commit()

    yield connection

    connection.close()


# Test 1 : Ajouter puis retrouver un étudiant
def test_add_and_get_student(conn):
    add_student(conn, "Alicia", 16)

    student = get_student(conn, 1)

    assert student is not None
    assert student[1] == "Alicia"
    assert float(student[2]) == 16.0


# Test 2 : Rechercher un étudiant inexistant
def test_get_nonexistent_student(conn):
    student = get_student(conn, 9999)

    assert student is None


# Test 3 : Calculer la moyenne
def test_moyenne(conn):
    add_student(conn, "cookie", 10)
    add_student(conn, "amanda", 14)

    assert average_grade(conn) == 12.0

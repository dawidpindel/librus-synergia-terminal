from librus_terminal.librus_session import LibrusSession
import librus_scraper


def _print_grade_detailed(grade: librus_scraper.grades.Grade, indentation: str, index: int) -> None:
    print(
        indentation,
        str(index).rjust(2),
        "  " if grade.to_max_points else " Z",
        "  " if grade.mean else "I ",
        "{}/{} ".format(*grade.points),
        f"{round((grade.points[0] / grade.points[1]) * 100, 2)}% " if grade.points[1] else " ",
        grade.category,
        sep=""
    )

    for key in grade.additional:
        print("\t{}- {}: {}".format(
            indentation, key.replace('\n', ' '), grade.additional[key].replace('\n', ' ')
        ))


def _print_semester_grades(semester: librus_scraper.grades.Semester, semester_index: int, detailed: bool = False) -> None:
    print(f"\tSemester {semester_index}:", end=" " if not detailed else "\n")

    if not detailed:
        grades = ["{}/{}".format(*grade.points) for grade in semester.grades]

        print(*grades)
        return

    for index, grade in enumerate(semester.grades, 1):
        _print_grade_detailed(grade, indentation="\t\t", index=index)


def grades_command(session: LibrusSession, *, detailed: bool = False) -> None:
    grades = librus_scraper.grades.get_grades_detailed(session.cookies)

    for subject in grades:
        print(subject.name, f"{subject.points_sum}/{subject.points_max} {round(subject.percentage, 2)}%,", "Oceny:")

        for semester_index, semester in enumerate(subject.semesters, 1):
            _print_semester_grades(semester, semester_index, detailed=detailed)

from .librus_session import LibrusSession
import librus_scraper
import os


def exit_command(session: LibrusSession) -> None:
    exit()


def clear_command(session: LibrusSession) -> None:
    os.system("cls")


def absences_command(session: LibrusSession) -> None:
    cookies = session.cookies

    absences_generator = librus_scraper.get_attendence(cookies)

    for absence in absences_generator:
        message = ""

        for entry in absence["entries"]:
            if entry["Rodzaj"] != "nieobecność":
                continue

            message += (
                f"\t{entry['Godzina lekcyjna']} - {entry['Lekcja']}\n"
            )

        if not message:
            continue

        print(absence["date"], message, sep="\n")

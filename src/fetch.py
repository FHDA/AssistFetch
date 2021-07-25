import sys, getopt
from time import sleep
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager

help_string = """
Usage: python3 fetch.py -<option> <value>
For help, use python3 fetch.py -h or python3 fetch.py --help

Arguments:
[-h] --help: Display help string
[-l] --list: Print a list corresponding of the argument
    Available argument:
        "year": Getting a list of available years on assist.org
        "from_school": Getting a list of available schools on assist.org
        "to_school": Getting a list of agreement schools corresponsing 
                to <to_school> (note: -f or --from_school has to be inputted for this to work)

Note: The arguments below must all be inputted if you want to get a list of majors
[-y] --year: Getting a major list from a specific academic year formatted like "2020-2021"
[-f] --from_school: Getting a major list from this school
[-t] --to_school: Getting a major list to this school
"""


def main():

    # Options
    long_options = ["help", "list=", "year=", "from_school=", "to_school="]
    options = "hl:y:f:t:"

    try:
        opts, args = getopt.getopt(sys.argv[1:], options, long_options)
        arguments = [x[0] for x in opts]
        for cur_arg, cur_val in opts:
            if cur_arg in ("-h", "--help"):
                print(help_string)
                return
            driver = webdriver.Chrome(ChromeDriverManager().install())
            if cur_arg in ("-l", "--list"):
                if cur_val == "year":
                    print(get_year_list(driver))
                    return
                elif cur_val == "from_school":
                    print(get_from_school_list(driver))
                    return
                elif cur_val == "to_school":
                    if "-f" not in arguments and "--from_school" not in arguments:
                        raise Exception(
                            "In order to print to_school, argument --from_school need to be set"
                        )
                    else:
                        for temp_arg, temp_val in opts:
                            if temp_arg in ("-f", "--from_school"):
                                print(get_to_school_list(driver, temp_val))
                                return
            if cur_arg in ["-y", "--year", "-f", "--from_school", "-t", "--to_school"]:
                year = None
                from_school = None
                to_school = None
                for temp_arg, temp_val in opts:
                    if temp_arg in ("-y", "--year"):
                        year = temp_val
                    elif temp_arg in ("-f", "--from_school"):
                        from_school = temp_val
                    elif temp_arg in ("-t", "--to_school"):
                        to_school = temp_val
                if year and from_school and to_school:
                    print(get_year_major_list(driver, year, from_school, to_school))
                    return
                else:
                    raise Exception(
                        "Please check input year/from_school/to_school, received year={}, from_school={}, to_school={}".format(
                            year, from_school, to_school
                        )
                    )
            else:
                raise Exception("Invalid argument!")
    except Exception as e:
        print("Encountered Error: {}!\n".format(e))


def get_year_major_list(driver, year, school_from, school_to):
    """
    Gets a list of transferable major names of the <year> from <school_from> to <school_to>

    Args:
        driver (selenium.webdriver): The webdriver used in this script to fetch data
        year (str): The specific academic year to fetch major list from (in a format like "2020-2021")
        school_from (str): The "transfer from" school
        school_to (str): The "transfer to" school

    Returns:
        A list of transferable major names of the <year> from <school_from> to <school_to>
    """
    try:
        _validate_year(year)
        _enter_assist(driver)

        # Select the academic year
        academic_year = driver.find_element_by_css_selector(
            "ng-select.ng-select-single[formcontrolname='academicYear']"
        )
        academic_year.click()
        years = driver.find_element_by_css_selector("div.ng-dropdown-panel-items")
        year = driver.find_element_by_xpath("//*[contains(text(), '{}')]".format(year))
        year.click()

        # Select the school from
        from_schools = driver.find_element_by_css_selector(
            "ng-select.ng-select-single[formcontrolname='fromInstitution']"
        )
        from_schools.click()
        schools = driver.find_element_by_css_selector("div.ng-dropdown-panel-items")
        from_school = driver.find_element_by_xpath(
            "//*[contains(text(), '{}')]".format(school_from)
        )
        from_school.click()

        # Select the school to
        to_schools = driver.find_element_by_css_selector(
            "ng-select.ng-select-single[formcontrolname='agreement']"
        )
        to_schools.click()
        # Wait for schools to load
        sleep(0.2)
        schools = driver.find_element_by_css_selector("div.ng-dropdown-panel-items")
        to_school = driver.find_element_by_xpath(
            "//*[contains(text(), 'To: {}')]".format(school_to)
        )
        to_school.click()
        return _get_agreement_majors(driver)

    except Exception as e:
        print(e)
        driver = webdriver.Chrome(ChromeDriverManager().install())
        _enter_assist(driver)


def get_year_list(driver):
    """
    Gets a list of available years on assist.org

    Args:
        driver (selenium.webdriver): The webdriver used in this script to fetch data

    Returns:
        A list of available years on assist.org
    """
    try:
        _enter_assist(driver)
        academic_year = driver.find_element_by_css_selector(
            "ng-select.ng-select-single[formcontrolname='academicYear']"
        )
        academic_year.click()
        year_options = [
            x.get_attribute("innerHTML")
            for x in driver.find_elements_by_class_name("ng-option-label")
        ]
        return year_options
    except Exception as e:
        print(e)


def get_from_school_list(driver):
    """
    Gets a list of schools on assist.org

    Args:
        driver (selenium.webdriver): The webdriver used in this script to fetch data

    Returns:
        A list of schools on assist.org
    """
    try:
        _enter_assist(driver)
        from_schools = driver.find_element_by_css_selector(
            "ng-select.ng-select-single[formcontrolname='fromInstitution']"
        )
        from_schools.click()
        school_options = [
            x.get_attribute("innerHTML")
            for x in driver.find_elements_by_class_name("ng-option-label")
        ]
        return school_options
    except Exception as e:
        print(e)


def get_to_school_list(driver, school_from):
    """
    Gets a list of available agreement school with the <school_from>

    Args:
        driver (selenium.webdriver): The webdriver used in this script to fetch data
        school_from (str): The specified end of the agreement schpp;

    Returns:
        A list of available agreement schools with <school_from> on assist.org
    """
    try:
        _enter_assist(driver)
        from_schools = driver.find_element_by_css_selector(
            "ng-select.ng-select-single[formcontrolname='fromInstitution']"
        )
        from_schools.click()
        schools = driver.find_element_by_css_selector("div.ng-dropdown-panel-items")
        from_school = driver.find_element_by_xpath(
            "//*[contains(text(), '{}')]".format(school_from)
        )
        from_school.click()
        to_schools = driver.find_element_by_css_selector(
            "ng-select.ng-select-single[formcontrolname='agreement']"
        )
        to_schools.click()
        # Wait for schools to load
        sleep(0.2)
        # Skip 4 chars to eliminate prefix "To: "
        school_options = [
            x.get_attribute("innerHTML")[4:]
            for x in driver.find_elements_by_class_name("ng-option-label")
            if "From: " not in x.get_attribute("innerHTML")
        ]
        return school_options
    except Exception as e:
        print(e)


def _get_agreement_majors(driver):
    """
    Gets a list majors by entering the agreement page

    Args:
        driver (selenium.webdriver): The webdriver used in this script to fetch data

    Returns:
        A list of majors
    """
    # Enter agreement page
    agreement_button = driver.find_element_by_xpath(
        "//*[contains(text(), 'View Agreements')]"
    )
    agreement_button.click()

    sleep(0.4)

    major_list = [
        x.text for x in driver.find_elements_by_class_name("viewByRowColText")
    ]
    return major_list


def _enter_assist(driver):
    """
    Enters assist.org homepage (works as a refresher in this script)

    Args:
        driver (selenium.webdriver): The webdriver used in this script to fetch data

    """
    driver.get("https://assist.org")


def _validate_year(year):
    """
    Validates the year string

    Args:
        year (str): The specific academic year to fetch major list from (in a format like "2020-2021")

    """
    try:
        splited_year = year.split("-")
        assert int(splited_year[1]) - 1 == int(splited_year[0])
    except Exception as e:
        raise e


if __name__ == "__main__":
    main()

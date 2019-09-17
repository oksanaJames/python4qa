import xml.etree.ElementTree as ET
import traceback
import datetime
import re


def parse_and_remove(filename, path):
    path_parts = path.split('/')
    doc = ET.iterparse(filename, ('start', 'end'))
    # Skip root element
    next(doc)
    tag_stack = []
    elem_stack = []
    for event, elem in doc:
        if event == 'start':
            tag_stack.append(elem.tag)
            elem_stack.append(elem)
        elif event == 'end':
            if tag_stack == path_parts:
                yield elem
            try:
                tag_stack.pop()
                elem_stack.pop()
            except IndexError:
                pass


if __name__ == '__main__':
    try:
        print('\n')
        print('-----start-----')
        print('\n')
        start = datetime.datetime.now()

        unique_governments = []
        country_government = []
        countries = parse_and_remove('mondial-3.0.xml', 'country')
        for country in countries:
            name = country.attrib['name']
            government = country.attrib['government']
            if government not in unique_governments:
                unique_governments.append(government.strip())
            if " " in name:
                country_government.append((name, government.strip()))


        print("\tUnique countries governments: {}\n".format(len(unique_governments)))
        print(', '.join(sorted(unique_governments)))
        print("\n")
        print("\tCountries with two words name and their governments: {}\n".format(len(country_government)))
        for country, gov in sorted(country_government):
            print("{} - {}".format(country, gov))


    # and " " in name
    except Exception as e:
        print("\nError")
        print(e)
        print('\n')
        traceback.print_exc()
    finally:
        duration = str(datetime.datetime.now() - start)  # print the time taken for script execution
        print('\n')
        print('command run complete in duration: %s' % duration)
        print('-----end-----')
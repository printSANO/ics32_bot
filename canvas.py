from canvasapi import Canvas
from secretToken import canvasToken, canvasUrl
import requests
from bs4 import BeautifulSoup

#University of California Irvine
canvas_url = canvasUrl
#Access token
canvas_key = canvasToken
#initialize
canvas = Canvas(canvas_url, canvas_key)

def course_name(num: int):
    name = canvas.get_course(num)
    return str(name)

def assingment_id_extractor(course_num: int) -> list:
    course = canvas.get_course(course_num)
    assignments = course.get_assignments()
    assign_ids = []
    assign_ids.append(course_num)
    for i in assignments:
        assign_ids.append(i)
    return assign_ids

def get_due_dates(assignment_ids: list) -> dict:
    assigned = {}
    for j in range(1,len(assignment_ids)):
        assignment = assignment_ids[j]
        due_date = str(assignment.due_at_date)[0:-9]
        assignment_name = str(assignment.name)
        assigned[str(assignment_name)] = due_date
    return assigned

def get_lecture_link(course_num: int) -> None:
    """write lecture name and link to a text file"""
    response = requests.get(f"{canvas_url}/api/v1/courses/{course_num}/front_page?access_token={canvas_key}")
    data = response.json()
    bodyData = data["body"]
    soup = BeautifulSoup(bodyData, features="html.parser")
    lst = []
    for i in soup.find_all('a', href=True):
        if i["href"][12:16] == "yuja":
            y = i.find_previous().find_previous().find_previous('p').find(text=True)
            lst.append(i["href"])#link of lecture
            lst.append(y)#name of lecture
    file = open("lecturelink.txt", 'w')
    for j in range(0,len(lst),2):
        file.write(lst[j+1]) #lst[j] = name, lst[j+1] = link
        file.write(",, ")
        file.write(lst[j])
        file.write("\n")
    file.close()

if __name__ == "__main__":
    num = 49725
    # print(course_name(num))
    get_lecture_link(num)
    # test = assingment_id_extractor(num)
    # test1 = get_due_dates(test)
    # print(test1)
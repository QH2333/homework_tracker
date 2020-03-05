import sys
import getopt
import datetime
import json
import flask
import mysql.connector

app = flask.Flask(__name__)

db_host = "localhost"
db_user = "root"
db_passwd = "pwd"

@app.route("/data")
def data():
    rst = flask.make_response(get_json())
    rst.headers['Access-Control-Allow-Origin'] = '*'
    return rst


def get_json():
    course_list = ["Search Engine", "Embedded System",
                   "Multimedia", "Database", "毛概"]
    return_list = []

    conn = mysql.connector.connect(
        user=db_user, host=db_host, password=db_passwd, database='homework')
    for course in course_list:
        course_obj = {}
        course_obj["courseName"] = course
        course_obj["assignments"] = []
        cursor = conn.cursor()
        cursor.execute(
            'select * from homework_info where c_name = %s order by deadline desc', (course,))
        values = cursor.fetchall()
        for record in values:
            assignment = {}
            assignment["assignTime"] = record[2].strftime("%Y-%m-%d")
            assignment["detail"] = record[3]
            assignment["expiryTime"] = record[4].strftime("%Y-%m-%d %H:%M:%S")
            assignment["method"] = record[5]
            course_obj["assignments"].append(assignment)
        return_list.append(course_obj)
        cursor.close()
    conn.close()
    return json.dumps(return_list, ensure_ascii=False)


if __name__ == '__main__':
    argv = sys.argv[1:]
    try:
        opts, args = getopt.getopt(argv, "h", ["host=", "user=", "passwd="])
    except getopt.GetoptError:
        print('server.py --host=<db_host> --user=<db_user> --passwd=<db_password>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('server.py --host=<db_host> --user=<db_user> --passwd=<db_password>')
            sys.exit()
        elif opt == "--host":
            db_host = arg
        elif opt == "--user":
            db_user = arg
        elif opt == "--passwd":
            db_passwd = arg

    app.run(host='0.0.0.0', port="7777")

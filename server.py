import sys
import getopt
import datetime
import json
import flask
import mysql.connector

application = flask.Flask(__name__)

db_host = "localhost"
db_user = "root"
db_passwd = "pwd"
db_name = "homework"

server_port = 7777


@application.route("/")
def index():
    return flask.render_template('index.html')


@application.route("/timetable")
def timetable():
    return flask.render_template('timetable.html')


@application.route("/add")
def add():
    return flask.render_template('add.html')


@application.route("/data")
def data():
    rst = flask.make_response(get_json())
    rst.headers['Access-Control-Allow-Origin'] = '*'
    return rst


@application.route("/insert", methods=['post', 'get'])
def insert():
    try:
        conn = mysql.connector.connect(
            user=db_user, host=db_host, password=db_passwd, database=db_name)
        cursor = conn.cursor()
        values = "0, '%s', '%s', '%s', '%s', '%s'" % (
            flask.request.form['c_name'],
            flask.request.form['assigntime'],
            flask.request.form['detail'],
            flask.request.form['deadline'],
            flask.request.form['method'], )
        cursor.execute("insert into homework_info values (%s)" % values)
        conn.commit()
        print("insert into homework_info values (%s)" % values)
        cursor.close()
        conn.close()
        return "Success"
    except:
        return "DB Error"


def get_json():
    course_list = ["Search Engine", "Embedded System",
                   "Multimedia", "Database", "毛概"]
    return_list = []

    try:
        conn = mysql.connector.connect(
            user=db_user, host=db_host, password=db_passwd, database=db_name)
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
    except:
        return "DB Error"


if __name__ == '__main__':
    argv = sys.argv[1:]
    try:
        opts, args = getopt.getopt(
            argv, "h", ["host=", "user=", "passwd=", "dbname=", "port="])
    except getopt.GetoptError:
        print('server.py --host=<db_host> --user=<db_user> --passwd=<db_password> --dbname=<db_name> --port=<server_port>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('server.py --host=<db_host> --user=<db_user> --passwd=<db_password> --dbname=<db_name> --port=<server_port>')
            sys.exit()
        elif opt == "--host":
            db_host = arg
        elif opt == "--user":
            db_user = arg
        elif opt == "--passwd":
            db_passwd = arg
        elif opt == "--dbname":
            db_name = arg
        elif opt == "--port":
            server_port = int(arg)

    application.run(host='0.0.0.0', port=server_port)

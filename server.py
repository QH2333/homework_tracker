import sys
import os.path
import getopt
import datetime
import json
import flask
import mysql.connector


# Read configurations
app_conf = {"db_host": 'localhost',
            "db_user": 'root',
            "db_passwd": 'pwd',
            "db_name": 'homework',
            "server_port": 7777}

server_dir = os.path.dirname(os.path.abspath(__file__))
if (os.path.exists(os.path.join(server_dir, "config.json"))):
    with open(os.path.join(server_dir, "config.json")) as f:
        app_conf = json.loads(f.read())
else:
    print("\033[1;31mError: No configuration file found!\033[0m")
    sys.exit(-1)


application = flask.Flask(__name__)

# Register routes
@application.route("/")
def index():
    return flask.render_template('index.html')


@application.route("/add")
def add():
    return flask.render_template('add.html')


@application.route("/data")
def data():
    rst = flask.make_response(get_json())
    return rst


@application.route("/insert", methods=['post', 'get'])
def insert():
    try:
        conn = mysql.connector.connect(
            user=app_conf["db_user"], host=app_conf["db_host"], password=app_conf["db_passwd"], database=app_conf["db_name"])
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
            user=app_conf["db_user"], host=app_conf["db_host"], password=app_conf["db_passwd"], database=app_conf["db_name"])
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
    # Run the app
    application.run(host='0.0.0.0', port=app_conf["server_port"])

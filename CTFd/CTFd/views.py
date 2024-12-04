from flask import (
    current_app as app,
    render_template,
    request,
    redirect,
    abort,
    url_for,
    session,
    Blueprint,
    Response,
    send_file,
    send_from_directory,
)
from flask.helpers import safe_join

from CTFd.models import db, Users, Admins, Teams, Files, Pages, Notifications, Solves, Challenges, Awards
from CTFd.utils import markdown
from CTFd.cache import cache
from CTFd.utils import get_config, set_config
from CTFd.utils.user import authed, get_current_user
from CTFd.utils import config
from CTFd.utils.uploads import get_uploader
from CTFd.utils.config.pages import get_page
from CTFd.utils.config.visibility import challenges_visible
from CTFd.utils.security.auth import login_user
from CTFd.utils.security.csrf import generate_nonce
from CTFd.utils import user as current_user
from CTFd.utils.dates import ctftime, ctf_ended, view_after_ctf
from CTFd.utils.decorators import authed_only
from CTFd.utils.security.signing import (
    unserialize,
    BadTimeSignature,
    SignatureExpired,
    BadSignature,
)
from sqlalchemy.exc import IntegrityError

import datetime
import glob
import os
import re
import subprocess

views = Blueprint("views", __name__)

deadlines = {
    'Week1' : datetime.datetime(2021,12,10,23,59,00),
    'Week2' : datetime.datetime(2021,12,10,23,59,00),
    'Week3' : datetime.datetime(2021,12,10,23,59,00),
    'Week3-Extra' : datetime.datetime(2021,12,10,23,59,00),
    'Week4' : datetime.datetime(2021,12,10,23,59,00),
    'Week5' : datetime.datetime(2021,12,10,23,59,00),
    'Week5-Extra' : datetime.datetime(2021,12,10,23,59,00),
    'Week6' : datetime.datetime(2021,12,10,23,59,00),
    'Week6-Extra' : datetime.datetime(2021,12,10,23,59,00),
    'Week7' : datetime.datetime(2021,12,10,23,59,00),
    #'Extra-2' : datetime.datetime(2018,3,9,23,59,00),
    #'Week-8' : datetime.datetime(2018,3,16,23,59,00),
    'NSA CC' : datetime.datetime(2021,12,10,23,59,00),
}

orders = [
        'Week1',
        'Week2',
        'Week3',
        'Week4',
        'Week5',
        'Week6',
        'Week7',
        #'Week-8',
        'Week3-Extra',
        'Week5-Extra',
        'Week6-Extra',
        #'Extra-2',
        'NSA CC',
]

@views.route('/grades', methods=['GET'])
@authed_only
def get_grades():
    # get username from login session
    teamid = session['id']
    user = Users.query.filter_by(id=teamid).first_or_404()

    print(user)
    if user.affiliation != None:
        aff = user.affiliation.lower()
    else:
        aff = ''

    # get all solves
    solves = Solves.query.filter_by(user_id=teamid)
    awards = Awards.query.filter_by(user_id=teamid).all()
    chals = Challenges.query.all()


    data = {}
    chals_dict = {}
    for c in chals:
        if not c.category in data:
            data[c.category] = {
                    'solved' : [],
                    'late' : [],
                    'uncount' : [],
                    'unsolved' : [],
                    'total' : [],
                    'total_dict' : {},
            }
        chals_dict[c.id] = c
        data[c.category]['total_dict'][c.id] = c

    data['NSA CC'] = {
            'solved' : [],
            'late' : [],
            'uncount' : [],
            'unsolved' : [],
            'total' : [],
            'total_dict' : {},
    }



    data['Project'] = {
            'solved' : [],
            'late' : [],
            'uncount' : [],
            'unsolved' : [],
            'total' : [],
            'total_dict' : {},
    }

    solves = solves.all()

    for s in solves:
        c = chals_dict[s.challenge_id]
        pst_solve_time = s.date - datetime.timedelta(hours=8)
        if not c.category in orders:
            continue
        deadline = deadlines[c.category]
        deadline_2 = deadlines[c.category] + datetime.timedelta(days=7)

        if pst_solve_time < deadline:
            data[c.category]['solved'].append(c)
        elif pst_solve_time < deadline_2:
            if user.name == 'NahGuava':
                data[c.category]['solved'].append(c)
            else:
                data[c.category]['late'].append(c)
        else:
            data[c.category]['uncount'].append(c)

    categories = data.keys()

    for category in orders:
        try:
            d = data[category]
        except KeyError:
            print("Key %s not found" % category)
            continue

        d['solved_score'] = sum([c.value for c in d['solved']])
        d['late_score'] = sum([c.value/2 for c in d['late']])
        if not 'Extra' in category:
            d['full_score'] = sum([d['total_dict'][k].value for k in d['total_dict']])

    #print(awards)
    for a in awards:
        data[a.category]['solved_score'] += a.value



    data['Project']['late_score'] = 0
    data['Project']['solved_score'] = 0 #sum([c.value for c in awards])
    data['Project']['full_score'] = 0 #sum([c.value for c in awards])
    data['orders'] = orders
    data['deadlines'] = deadlines
    data['all_score'] = {
            'solved_score' : 0,
            'late_score' : 0,
            'full_score' : 0,
        }
    for cat in orders:
        try:
            d = data[cat]
        except KeyError:
            print("Key %s not found" % cat)
            continue
        if not 'NSA CC' in cat:
            data['all_score']['solved_score'] += d['solved_score']
            data['all_score']['late_score'] += d['late_score']
        if 'Extra' in cat:
            pass
        else:
            data['all_score']['full_score'] += d['full_score']

    sum_score = data['all_score']['solved_score']+ data['all_score']['late_score']
    if(data['all_score']['full_score'] == 0):
        data['all_score']['full_score'] = 1

    data['percent'] = (float(sum_score) / data['all_score']['full_score'] * 100)

    oval = data['percent']
    if ('grad' in aff) and (not 'under' in aff):
        adj = 5
    else:
        adj = 0

    def get_grade(grade_value):
        if grade_value >= 94.9 + adj:
            return 'A+ (A at OSU)'
        elif grade_value >= 89.9 + adj:
            return 'A'
        elif grade_value > 84.9 + adj:
            return 'A-'
        elif grade_value > 79.9 + adj:
            return 'B+'
        elif grade_value > 74.9 + adj:
            return 'B'
        elif grade_value > 69.9 + adj:
            return 'B-'
        elif grade_value > 64.9 + adj:
            return 'C+'
        elif grade_value > 59.9 + adj:
            return 'C'
        elif grade_value > 54.9 + adj:
            return 'C-'
        elif grade_value > 49.9 + adj:
            return 'D+'
        elif grade_value > 44.9 + adj:
            return 'D'
        elif grade_value > 39.9 + adj:
            return 'D-'
        else:
            return 'F'
    grade_value = (data['percent']) * 0.8
    nsa_cc_score = int((float(data['NSA CC']['solved_score'])/6) * 20)
    """
    nsa_cc_score = 0
    if nsa_cc_score != 0:
        grade_string_1 = "%s (%3.2f%%): %3.2f%%" \
            % (get_grade(grade_value + nsa_cc_score), grade_value + nsa_cc_score, data['percent'])
        grade_string_2 = ''
    else:
        grade_string_1 = "%s (%3.2f%%): %3.2f%%" \
            % (get_grade(grade_value), grade_value, data['percent'])
        grade_string_2 = ""
    """

    if nsa_cc_score != 0:
        grade_string_1 = "%s (%3.2f%%): %3.2f%% * 0.8 + 100%% * 0.2 (NSA CC)" \
            % (get_grade(grade_value + nsa_cc_score), grade_value + nsa_cc_score, data['percent'])
        grade_string_2 = ''
    else:
        grade_string_1 = "%s (%3.2f%%): %3.2f%% * 0.8 + 100%% * 0.2 (NSA CC)" \
            % (get_grade(grade_value + 20), grade_value + 20, data['percent'])
        grade_string_2 = "%s (%3.2f%%): %3.2f%% * 0.8 + 0%% * 0.2 (NSA CC)" \
            % (get_grade(grade_value + 0), grade_value + 0, data['percent'])




    data['percent'] = "%3.2f%%" % data['percent']
    #data['grade'] += " ( %3.2f%%, %3.2f%% * 0.8 + NSA Codebreaker %d%% )" % (grade_value, oval, data['Project']['full_score'])
    data['grade'] = [grade_string_1, grade_string_2]
    data['index'] = """Grade scale: A >= 90%, A- >= 85%, B+ >= 80%, B >= 75%, B- >= 70%, C+ >= 65%,
  C >= 60%, C- >= 55%, D+ >= 50%, D >= 45%, D- >= 40%, F < 40% (Grad students: +5%)"""


    return render_template('grades.html', teamid=teamid, team=user, grades=data)



@views.route("/setup", methods=["GET", "POST"])
def setup():
    if not config.is_setup():
        if not session.get("nonce"):
            session["nonce"] = generate_nonce()
        if request.method == "POST":
            ctf_name = request.form["ctf_name"]
            set_config("ctf_name", ctf_name)

            # CSS
            set_config("start", "")

            # Admin user
            name = request.form["name"]
            email = request.form["email"]
            password = request.form["password"]
            admin = Admins(
                name=name, email=email, password=password, type="admin", hidden=True
            )

            user_mode = request.form["user_mode"]

            set_config("user_mode", user_mode)

            # Index page
            index = """<div class="row">
    <div class="col-md-6 offset-md-3">
        <img class="w-100 mx-auto d-block" style="max-width: 400px;padding: 50px;padding-top: 14vh;" src="themes/core/static/img/cad.png" />
        <h3 class="text-center">
            <p>The scoring system for CS 419/579 Cyber Attacks and Defense.</p>
        </h3>
    </div>
</div>""".format(request.script_root)

            page = Pages(title=None, route="index", content=index, draft=False)
            # Visibility
            set_config("challenge_visibility", "private")
            set_config("registration_visibility", "public")
            set_config("score_visibility", "public")
            set_config("account_visibility", "public")

            # Start time
            set_config("start", None)
            set_config("end", None)
            set_config("freeze", None)

            # Verify emails
            set_config("verify_emails", None)

            set_config("mail_server", None)
            set_config("mail_port", None)
            set_config("mail_tls", None)
            set_config("mail_ssl", None)
            set_config("mail_username", None)
            set_config("mail_password", None)
            set_config("mail_useauth", None)

            set_config("setup", True)

            try:
                db.session.add(admin)
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

            try:
                db.session.add(page)
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

            login_user(admin)

            db.session.close()
            app.setup = False
            with app.app_context():
                cache.clear()

            return redirect(url_for("views.static_html"))
        return render_template("setup.html", nonce=session.get("nonce"))
    return redirect(url_for("views.static_html"))


@views.route("/notifications", methods=["GET"])
@authed_only
def notifications():
    notifications = Notifications.query.order_by(Notifications.id.desc()).all()
    return render_template("notifications.html", notifications=notifications)

@views.route('/delete-file', methods=['GET'])
@authed_only
def delete_file():
    # get username from login session
    teamid = session['id']
    user = Users.query.filter_by(id=teamid).first_or_404()

    # get user directory
    userdir = "%s/student-files/%s" % (os.getcwd(), user.name)

    # make a user directory if not exists
    if not os.path.exists(userdir):
        os.makedirs(userdir)

    fn = request.args.get('file')
    if '..' in fn:
        return render_template('bad-download.html', teamid=teamid, team=user, fn=fn)

    re_result = re.match("^[0-9a-zA-Z\-_][0-9a-zA-Z\-_\.]*", fn)
    if re_result == None:
        return render_template('bad-download.html', teamid=teamid, team=user, fn=fn)

    print("Delete %s" % fn)
    file_path = "%s/%s" % (userdir, fn)
    if os.path.exists(file_path):
        os.unlink(file_path)

    return redirect(url_for('views.upload'))



@views.route('/download-file', methods=['GET'])
@authed_only
def download_file():
    # get username from login session
    teamid = session['id']
    user = Users.query.filter_by(id=teamid).first_or_404()

    # get user directory
    userdir = "%s/student-files/%s" % (os.getcwd(), user.name)

    # make a user directory if not exists
    if not os.path.exists(userdir):
        os.makedirs(userdir)

    fn = request.args.get('file')
    if '..' in fn:
        return render_template('bad-download.html', teamid=teamid, team=user, fn=fn)

    re_result = re.match("^[0-9a-zA-Z\-_][0-9a-zA-Z\-_\.]*", fn)
    if re_result == None:
        return render_template('bad-download.html', teamid=teamid, team=user, fn=fn)

    print("Download %s" % fn)
    return send_from_directory(directory=userdir, filename=fn, as_attachment=True, cache_timeout=1, add_etags=False, last_modified = datetime.datetime.now())



@views.route('/upload-file', methods=['POST'])
@authed_only
def upload_files():
    print('Upload running')
    try:
        # get username from login session
        teamid = session['id']
        user = Users.query.filter_by(id=teamid).first_or_404()

        # get user directory
        userdir = "%s/student-files/%s" % (os.getcwd(), user.name)
        print("Userdir :%s" % userdir)
        # make a user directory if not exists
        if not os.path.exists(userdir):
          os.makedirs(userdir)

        f = request.files['file']

        if f == None:
          return redirect(url_for('views.upload'))

        if '..' in f.filename:
          return render_template('bad-download.html', teamid=teamid, team=user, fn=f.filename)

        t = request.form['type']

        print(f)
        print(t)

        if f:
          print("Fn: %s t %s" % (f.filename, t))
          fn = '%s.tar.gz' % t
          if 'week' in t:
              fn = 'writeup-%s.tar.gz' % t

          f.save(os.path.join(userdir, fn))
          return redirect(url_for('views.upload'))
    except:
        return redirect(url_for('views.upload'))


@views.route('/upload', methods=['GET'])
@authed_only
def upload():
    # get username from login session
    teamid = session['id']
    print('user_id %d' % teamid)
    print(repr(Users.query.filter_by(id=teamid).first()))
    user = Users.query.filter_by(id=teamid).first_or_404()

    # get user directory
    userdir = "%s/student-files/%s" % (os.getcwd(), user.name)

    # make a user directory if not exists
    if not os.path.exists(userdir):
        os.makedirs(userdir)

    # get file lists
    lists = glob.glob("%s/*" % userdir)
    lists.sort()
    files = []
    for fn in lists:
        stat = os.stat(fn)
        time_string = datetime.datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
        file_size = str(stat.st_size)
        arg = ['', '', '', '']
        if 'week' in fn:
            arg[0] = 'writeup'
        else:
            arg[0] = 'file'

        arg[1] = os.path.basename(fn)
        arg[2] = time_string
        arg[3] = file_size
        files.append(arg)

    return render_template('upload.html', teamid=teamid, team=user, files=files)


@views.route("/settings", methods=["GET"])
@authed_only
def settings():
    user = get_current_user()
    name = user.name
    email = user.email
    website = user.website
    affiliation = user.affiliation
    country = user.country
    prevent_name_change = get_config("prevent_name_change")
    confirm_email = get_config("verify_emails") and not user.verified
    return render_template(
        "settings.html",
        name=name,
        email=email,
        website=website,
        affiliation=affiliation,
        country=country,
        prevent_name_change=prevent_name_change,
        confirm_email=confirm_email,
    )


@views.route("/static/user.css")
def custom_css():
    """
    Custom CSS Handler route
    :return:
    """
    return Response(get_config("css"), mimetype="text/css")


@views.route("/", defaults={"route": "index"})
@views.route("/<path:route>")
def static_html(route):
    """
    Route in charge of routing users to Pages.
    :param route:
    :return:
    """
    page = get_page(route)
    if page is None:
        abort(404)
    else:
        if page.auth_required and authed() is False:
            return redirect(url_for("auth.login", next=request.full_path))

        return render_template("page.html", content=markdown(page.content))


@views.route("/files", defaults={"path": ""})
@views.route("/files/<path:path>")
def files(path):
    """
    Route in charge of dealing with making sure that CTF challenges are only accessible during the competition.
    :param path:
    :return:
    """
    f = Files.query.filter_by(location=path).first_or_404()
    if f.type == "challenge":
        if challenges_visible():
            if current_user.is_admin() is False:
                if not ctftime():
                    if ctf_ended() and view_after_ctf():
                        pass
                    else:
                        abort(403)
        else:
            if not ctftime():
                abort(403)

            # Allow downloads if a valid token is provided
            token = request.args.get("token", "")
            try:
                data = unserialize(token, max_age=3600)
                user_id = data.get("user_id")
                team_id = data.get("team_id")
                file_id = data.get("file_id")
                user = Users.query.filter_by(id=user_id).first()
                team = Teams.query.filter_by(id=team_id).first()

                # Check user is admin if challenge_visibility is admins only
                if (
                    get_config("challenge_visibility") == "admins"
                    and user.type != "admin"
                ):
                    abort(403)

                # Check that the user exists and isn't banned
                if user:
                    if user.banned:
                        abort(403)
                else:
                    abort(403)

                # Check that the team isn't banned
                if team:
                    if team.banned:
                        abort(403)
                else:
                    pass

                # Check that the token properly refers to the file
                if file_id != f.id:
                    abort(403)

            # The token isn't expired or broken
            except (BadTimeSignature, SignatureExpired, BadSignature):
                abort(403)

    uploader = get_uploader()
    try:
        return uploader.download(f.location)
    except IOError:
        abort(404)


@views.route("/themes/<theme>/static/<path:path>")
def themes(theme, path):
    """
    General static file handler
    :param theme:
    :param path:
    :return:
    """
    filename = safe_join(app.root_path, "themes", theme, "static", path)
    if os.path.isfile(filename):
        return send_file(filename)
    else:
        abort(404)


PRIVATE_KEY_PATH = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) +
"../../../ssh/id_ed25519")

def check_banned_chars(banned_list, target):
    for c in banned_list:
        if c in target:
            return True
    return False


def check_username(username, server):
    output = subprocess.check_output('ssh -i %s ' % PRIVATE_KEY_PATH +
            'cs519@%s.eecs.oregonstate.edu' % server +
            ' cat /etc/passwd', shell=True)
    output = output.decode('utf-8')
    ids = [l.split(':')[0].strip() for l in output.split("\n")]

    if username in ids:
        message = "Username %s duplicated." % username
        message += " Please use other username."
        error = True
        return (error, message)
    else:
        return (False, )


def register_user(username, pubkey, server):
    # register here!
    cmd = "~/create-user"
    output = subprocess.check_output(
            'ssh -i %s' % PRIVATE_KEY_PATH +
            ' cs519@%s.eecs.oregonstate.edu ' % server +
            '"%s" "%s" "\'%s\'"' % (cmd, username, pubkey),
            shell=True)
    output = output.decode('utf-8')
    print(output)

    message = "Register OK for %s" % username
    error = False

    return (error, message)


@views.route("/register_account", methods=["GET", "POST"])
@authed_only
def register_account():
    if request.method == 'GET':
        return render_template('account.html')
    if request.method != 'POST':
        return render_template('account.html')

    # POST here.
    username = request.form['username'].strip()
    pubkey = request.form['pubkey'].strip()

    banned_chars = ['`', '"', '\x00', '>', '<', '&',
            '|', '!', '$', '~', '(', ')', '?', ';', '[', ']']

    if check_banned_chars(banned_chars, username):
        message = 'Please do not include special characters in the username.'
        error = True
        return render_template('account_msg.html', err=error, msg=message)

    if check_banned_chars(banned_chars, pubkey):
        message = 'Please do not include weird characters in the public key.'
        error = True
        return render_template('account_msg.html', err=error, msg=message)

    # check username
    re_result = re.match("^[0-9a-z][0-9a-z\-_]*", username)
    if re_result == None:
        message = "Please use characters in [0-9a-z\-_] for your username"
        error = True
        return render_template('account_msg.html', err = error, msg=message)

    if 'level' in username:
        message = "Please do not use the word 'level' in your username"
        error = True
        return render_template('account_msg.html', err = error, msg=message)

    servers = ['vm-ctf1', 'vm-ctf2', 'vm-ctf3']

    for server in servers:
        ret = check_username(username, server)
        if ret[0] == True:
            return render_template('account_msg.html', err=ret[0], msg=ret[1])

    # register here!
    for server in servers:
        ret = register_user(username, pubkey, server)
        error = ret[0]
        message = ret[1]

    return render_template('account_msg.html', err = error, msg=message)

@views.route("/register-syssec", methods=["GET", "POST"])
def register_syssec():
    if request.method == 'GET':
        return render_template('account.html')
    if request.method != 'POST':
        return render_template('account.html')

    # POST here.
    username = request.form['username'].strip()
    pubkey = request.form['pubkey'].strip()

    banned_chars = ['`', '"', '\x00', '>', '<', '&',
            '|', '!', '$', '~', '(', ')', '?', ';', '[', ']']

    if check_banned_chars(banned_chars, username):
        message = 'Please do not include special characters in the username.'
        error = True
        return render_template('account_msg.html', err=error, msg=message)

    if check_banned_chars(banned_chars, pubkey):
        message = 'Please do not include weird characters in the public key.'
        error = True
        return render_template('account_msg.html', err=error, msg=message)

    # check username
    re_result = re.match("^[0-9a-z][0-9a-z\-_]*", username)
    if re_result == None:
        message = "Please use characters in [0-9a-z\-_] for your username"
        error = True
        return render_template('account_msg.html', err = error, msg=message)

    if 'level' in username:
        message = "Please do not use the word 'level' in your username"
        error = True
        return render_template('account_msg.html', err = error, msg=message)

    servers = ['vm-ctf5']

    for server in servers:
        ret = check_username(username, server)
        if ret[0] == True:
            return render_template('account_msg.html', err=ret[0], msg=ret[1])

    # register here!
    for server in servers:
        ret = register_user(username, pubkey, server)
        error = ret[0]
        message = ret[1]

    return render_template('account_msg.html', err = error, msg=message)

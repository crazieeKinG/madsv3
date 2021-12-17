from werkzeug.wrappers.response import _clean_accept_ranges
from mads import mads_app
from flask import render_template, request, redirect, session, flash
import sqlite3 as sql
from datetime import datetime

def get_category(id):
    with sql.connect('./database/MADS v3.db') as con:
        con.row_factory = sql.Row   
        cur = con.cursor()
        return cur.execute("select * from Category where user_id=? ORDER BY name",(id,)).fetchall()

def get_entries(id, category="all"):
    with sql.connect('./database/MADS v3.db') as con:
        con.row_factory = sql.Row   
        cur = con.cursor()
        if category == "all":
            return cur.execute("select Entries.*,Category.name as category_name from Entries, Category where Entries.user_id=? and Entries.category_id=Category.id ORDER BY Entries.entry_name",(id,)).fetchall()
        else:
            return cur.execute("select Entries.*,Category.name as category_name from Entries, Category where Entries.user_id=? and Entries.category_id=? and Entries.category_id=Category.id ORDER BY Entries.entry_name",(id,category)).fetchall()

def update_entries(data, user_id):
     with sql.connect('./database/MADS v3.db') as con:
        cur = con.cursor()
        date = datetime.now().date()  
            
        cur.execute("UPDATE Entries Set category_id=?, user_id=?, entry_name=?, description=?, status=?, favourite=?, episode=?, last_modified=? WHERE id=?",(data['category'], user_id, data['title'],'No data', data['status'], data['favourite'], data['episode'], date, data['id']) ) 

        con.commit()

def search_entries(keyword, user_id):
    with sql.connect('./database/MADS v3.db') as con:
        con.row_factory = sql.Row   
        cur = con.cursor()
        return cur.execute("select Entries.*,Category.name as category_name from Entries, Category where Entries.user_id=? and Entries.category_id=Category.id and Entries.entry_name LIKE ? ORDER BY Entries.entry_name",(user_id,f"%{keyword}%")).fetchall()

@mads_app.route('/mads/',  defaults={'username': None}, methods=['GET'])
@mads_app.route('/mads/<username>', methods=['GET','POST'])
def Home(username):
    if 'user_id' not in session :
        return redirect('/mads/login')
    elif username != session['username']:
        return redirect('/mads/{}'.format(session['username']))
    else:
        delete_id = request.values.get("delete_id") 
        delete_title = request.values.get("delete_title") 
        if delete_id is not None and delete_title is not None:
            delete_entry(delete_id, delete_title)
        

        category = get_category(session['user_id'])
        search_keyword = request.values.get("search")
        if search_keyword is not None:
            entries = search_entries(search_keyword, session['user_id'])
        else:
            entries = get_entries(session['user_id'])

        user_info = {'id':session['user_id'], 'username': session['username']}
        if request.method == 'POST':
            data = dict()
            for key, val in request.form.items():
                data[key]=val
            try:
                update_entries(data, user_info['id'])
                flash(f"Updated entry [ {data['title']} ]")
            except:
                flash("Error!! Record was unable to be updated")
            return redirect('/mads/')
            
        return render_template('/public/index.html',category=category, entry=entries, user=user_info, current="index", search = search_keyword)

@mads_app.route('/mads/<username>/<category_id>/<category_name>', methods=['GET','POST'])
def each_category(username, category_id, category_name):
    if 'user_id' not in session :
        return redirect('/mads/login')
    elif username != session['username']:
        return redirect('/mads/{}/{}/{}'.format(session['username'], category_id, category_name))
    else:
        delete_id = request.values.get("delete_id") 
        delete_title = request.values.get("delete_title") 
        if delete_id is not None and delete_title is not None:
            delete_entry(delete_id, delete_title)
        
        search_keyword = request.values.get("search")
        if search_keyword is not None:
            return redirect(f"/mads/{session['username']}?search={search_keyword}")

        category = get_category(session['user_id'])
        entries = get_entries(id=session['user_id'], category=category_id)
        user_info = {'id':session['user_id'], 'username': session['username']}

        if request.method == 'POST':
            data = dict()
            for key, val in request.form.items():
                data[key]=val
            try:
                update_entries(data, user_info['id'])
                flash(f"Updated entry [ {data['title']} ]")
            except:
                flash("Error!! Record was unable to be updated")
            return redirect('/mads/{}/{}/{}'.format(username, category_id, category_name))
            
        return render_template('/public/each-category.html',category=category, entry=entries, user=user_info, current=category_name)

@mads_app.route('/mads/new-user', methods=['GET','POST'])
def user_registration():
    if request.method == 'POST':
        fullname = request.form['fullname']
        username = request.form['username']
        password = request.form['password']
        security_key = request.form['security_key']
        date = datetime.now().date()
        
        with sql.connect('./database/MADS v3.db') as con:
            cur = con.cursor()
            cur.execute("INSERT INTO User (fullname,username,password,security_key,date_added) VALUES (?,?,?,?,?)",(fullname, username, password, security_key, date) )            
            con.commit()

            return redirect('/mads/login')
    return render_template('/public/register-user.html')
    
@mads_app.route('/mads/new-category', methods=['GET','POST'])
def new_category():
    if 'user_id' not in session :
        return redirect('/mads/login')
    else:
        search_keyword = request.values.get("search")
        if search_keyword is not None:
            return redirect(f"/mads/{session['username']}?search={search_keyword}")

        category = get_category(session['user_id'])
        user_info = {'id':session['user_id'], 'username': session['username']}
        if request.method == 'POST':
            with sql.connect('./database/MADS v3.db') as con:
                for key, title in request.form.items():
                    cur = con.cursor()
                    try:
                        date = datetime.now().date()    
                        cur.execute("INSERT INTO Category (name,user_id,date_added,description) VALUES (?,?,?,'No data')",(title, user_info['id'], date) ) 
                        flash(f"Added category [ {title} ]")
                        con.commit()
                    except:
                        flash("Error!! adding category - You might have same entry multiple times")
                        return redirect('/mads/new-category')
            return redirect('/mads/')
        return render_template('/public/new-category.html', user=user_info, category=category, current="category")
    
@mads_app.route('/mads/new-entry', methods=['GET','POST'])
def new_entry():
    if 'user_id' not in session :
        return redirect('/mads/login')
    else:
        search_keyword = request.values.get("search")
        if search_keyword is not None:
            return redirect(f"/mads/{session['username']}?search={search_keyword}")

        category = get_category(session['user_id'])
        user_info = {'id':session['user_id'], 'username': session['username']}

        if request.method == 'POST':
            with sql.connect('./database/MADS v3.db') as con:
                data = list()
                for key, val in request.form.items():
                    data.append(val)

                cur = con.cursor()

                for i in range(0, len(data), 5):
                    title = data[i]
                    category = data[i+1]
                    status = data[i+2]
                    eps = data[i+3]
                    fav = data[i+4]
                    date = datetime.now().date()  
                
                    try:  
                        cur.execute("INSERT INTO Entries (category_id, user_id,entry_name, description, status, favourite, episode, date_added, last_modified) VALUES (?,?,?,'No data',?,?,?,?,?)",(category, user_info['id'], title, status, fav, eps, date, date) ) 
                        flash(f"Added entry [ {title} ]")
                        con.commit()
                    except:
                        flash("Error!! adding entry - You might have same entry multiple times")
                        return redirect('/mads/new-entry')
            return redirect('/mads/')
        return render_template('/public/new-entry.html',category=category, user=user_info, current="entry")

def delete_entry(id, title):
    with sql.connect('./database/MADS v3.db') as con:
        try:
            cur = con.cursor()
            cur.execute("DELETE FROM Entries WHERE id=?",(id,))
            con.commit()
            flash(f"Record deleted [ {title} ]")
        except:
            flash(f"Error!! Record [ {title} ] was unable to be deleted")


@mads_app.route('/mads/login', methods=['get','post'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        with sql.connect('./database/MADS v3.db') as con:
            con.row_factory = sql.Row   
            cur = con.cursor()
            cur.execute("select * from User where username=? and password=?",(username, password))  

            rows = cur.fetchall()
            if len(rows) == 1:
                session['user_id'] = rows[0]['id']
                session['username'] = rows[0]['username']
                return redirect('/mads/{}'.format(username))
            else:            
                flash("Error!! Username or password is incorrect.")
    return render_template("/public/login.html")

@mads_app.route('/mads/logout')
def logout():
    session.pop('user_id', default=None)
    session.pop('username', default=None)
    return redirect('/mads/login')
import sqlite3
from sqlite3 import Error
def contact():
    try:
        cursor.execute('create table if not exists contact(fname text,laname text,contact number,email text,city text)')
        c.commit()
    except Error as e:
        print(e)
def validate():
    try:
        cur.execute("""create trigger validate_email
                        before insert on contact
                        begin
                        select
                        case
                            when new.email not like'%_@_%._%' then
                            raise(abort,"invalid email")
                            end;
                        end;""")
        c.commit()
    except Error as e:
        print(e)
    
def log():
    try:
        cur.execute('create table if not exists insert_log(f_name text,la_name text,contact number,email text,date_time text)')
        c.commit()
        # for maintan insert log
        cur.execute("""create trigger log
                    after insert on contact
                    begin
                        insert into insert_log values(new.fname,new.laname,new.contact,new.email,strftime('%s', 'now'));
                    end;""")
        c.commit()
        # for maintain update log
        cur.execute(""" create table if not exists update_log(
                        old_fname text,
                        new_fname text,
                        old_laname text,
                        new_laname text,
                        old_contact number,
                        new_contact number,
                        old_email text,
                        new_email text,
                        old_city text,
                        new_city text,
                        date_time text) """)
        # for maintain delete log
        cur.execute(""" create table if not exists delete_log(
                        old_fname text,
                        old_laname text,
                        old_contact number,
                        old_email text,
                        old_city text,
                        date_time text) """)
    except Error as e:
        print(e)

        
def insert():
    try:
        i1="insert into contact values(?,?,?,?,?)"
        l=[]
        for i in range(5):
            f=input("Enter first name:")
            la=input("Enter last name:")
            cn=int(input("Enter contact number:"))
            e=input("Enter email:")
            p=input("Enter city:")
            li=[f,la,cn,e,p]
            l.append(li)
            cur.executemany(i1,l)
            c.commit()
    except Error as e:
        print(e)
def update():
    try:
         cur.execute(""" create trigger record_update
                    after update on contact
                    when  old_laname<>new_laname or old_contact<> new_contact
                    or old_email<> new_email or old_city<>new_city
                    begin
                        insert into update_log values
                        (old.fname,new.fname,old.laname,new.laname,old.contact,new.contact,old.email,new.email,old.city,new.city,
                        strftime('%s', 'now'))
                    end;""")
         u="update contact set email='buti@gmail.com' where fname='vibhuti'"
         cur.execute(u)
         c.commit()
    except Error as e:
        print(e)
def delete():
    try:
        cur.execute(''' create trigger record_delete
                after delete on contact
                begin
                        insert into delete_log values
                        (old.fname,old.laname,old.contact,old.email,old.city,
                        datetime('now', 'localtime'));
                end;''')

        d="delete from contact where fname='margi'"
        cur.execute(d)
        c.commit()
        c.close()
    except Error as e:
        print(e)
def search():
    try:
        cur.execute(" select fname,lname from contact;")
        rows=cur.fetchall()
        for i in rows:
            print(i)
        n=input("Enter name to be searched:")
        cur.execute('select * from contact where fname="{n}"')
        row=cur.fetchone()
        print(row)
        c.commit()
    except Error as e:
        print(e)
#main function
c=sqlite3.connect("c:\\sqlite3\\contact.db")
cur=c.cursor()
contact();
validate();
log();
choice=1
while(choice!=0):
    print(""" --------------Menu---------------------
                1.Insert records
                2.Update records
                3.Delete records
                4.Search records
            """)
    choice=int(input("Enter your choice"))
    if choice==1:
        insert();
    elif choice==2:
        update();
    elif choice==3:
        delete();
    elif choice==4:
        search();
    else:
        print("Invalid choice")
c.commit();
c.close();

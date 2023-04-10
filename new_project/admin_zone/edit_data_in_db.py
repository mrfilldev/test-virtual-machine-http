from flask import render_template

from ..db.database import db_test, client


def list_all_cols_in_db():
    for db_name in client.list_database_names():
        db = client[db_name]
        for coll_name in db.list_collection_names():
            print("db: {}, collection:{}".format(db_name, coll_name))
            for r in db[coll_name].find({}):
                print(r)
            print('\n\n')
    list_of_cols = db_test.collection_names()
    print(list_of_cols)
    context = {'list': list_of_cols}
    return render_template('admin/work_with_db/list_all_cols_in_db.html', context=context)

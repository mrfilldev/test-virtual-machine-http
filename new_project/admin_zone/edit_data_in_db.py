from flask import render_template

from ..db.database import db_test


def list_all_cols_in_db():
    list_of_cols = db_test.collection_names()
    print(list_of_cols)
    context = {'list': list_of_cols}
    return render_template('admin/work_with_db/list_all_cols_in_db.html', context=context)

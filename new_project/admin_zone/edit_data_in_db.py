from flask import render_template

from ..db.database import db_test


def list_all_cols_in_db():
    list = db_test.list_collection_names()
    context = {list}
    return render_template('admin/work_with_db/list_all_cols_in_db.html', context=context)

===========
krx-hj3415
===========

This is a program gets corporation data from https://kind.krx.co.kr

Quick start
------------

1. At first, refresh database using follow code::

    from krx import krx
    krx.make_db()


2. Useful methods::

    return_all_code_tuple = krx.get_codes()
    return_all_code_name_dictionary = krx.get_name_codes()


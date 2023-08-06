# -*- coding: utf-8 -*-
# :Project:   pglast -- Cython interface with libpg_query
# :Created:   mer 02 ago 2017 15:12:49 CEST
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2017, 2018, 2019 Lele Gaifax
#

#cython: language_level=3


import json

from . import Error


class ParseError(Error):
    "Exception representing the error state returned by the PG parser."

    def __init__(self, message, location):
        super().__init__(message)
        self.location = location

    def __str__(self):
        message = self.args[0]
        return f"{message}, at location {self.location}"


cdef extern from "pg_query.h" nogil:

    int PG_VERSION_NUM

    ctypedef struct PgQueryError:
        char *message
        int lineno
        int cursorpos

    ctypedef struct PgQueryParseResult:
        char *parse_tree
        PgQueryError *error

    ctypedef struct PgQueryPlpgsqlParseResult:
        char *plpgsql_funcs
        PgQueryError *error

    ctypedef struct PgQueryFingerprintResult:
        char *hexdigest
        char *stderr_buffer
        PgQueryError *error

    PgQueryParseResult pg_query_parse(const char* input)
    void pg_query_free_parse_result(PgQueryParseResult result)

    PgQueryPlpgsqlParseResult pg_query_parse_plpgsql(const char* input)
    void pg_query_free_plpgsql_parse_result(PgQueryPlpgsqlParseResult result)

    PgQueryFingerprintResult pg_query_fingerprint(const char* input)
    void pg_query_free_fingerprint_result(PgQueryFingerprintResult result)


def get_postgresql_version():
    "Return the PostgreSQL version as a tuple (`major`, `minor`)."

    version = PG_VERSION_NUM
    major, minor = divmod(version, 10_000)
    return (major, minor)


def parse_sql(str query):
    cdef PgQueryParseResult parsed
    cdef const char *cstring

    utf8 = query.encode('utf-8')
    cstring = utf8

    with nogil:
        parsed = pg_query_parse(cstring)

    try:
        if parsed.error:
            message = parsed.error.message.decode('utf8')
            cursorpos = parsed.error.cursorpos
            raise ParseError(message, cursorpos)

        return json.loads(parsed.parse_tree.decode('utf8'))
    finally:
        with nogil:
            pg_query_free_parse_result(parsed)


def parse_plpgsql(str query):
    cdef PgQueryPlpgsqlParseResult parsed
    cdef const char *cstring

    utf8 = query.encode('utf-8')
    cstring = utf8

    with nogil:
        parsed = pg_query_parse_plpgsql(cstring)

    try:
        if parsed.error:
            message = parsed.error.message.decode('utf8')
            cursorpos = parsed.error.cursorpos
            raise ParseError(message, cursorpos)

        return json.loads(parsed.plpgsql_funcs.decode('utf8'))
    finally:
        with nogil:
            pg_query_free_plpgsql_parse_result(parsed)


def fingerprint(str query):
    cdef PgQueryFingerprintResult result
    cdef const char *cstring

    utf8 = query.encode('utf-8')
    cstring = utf8

    with nogil:
        result = pg_query_fingerprint(cstring)

    try:
        if result.error:
            message = result.error.message.decode('utf8')
            cursorpos = result.error.cursorpos
            raise ParseError(message, cursorpos)

        return result.hexdigest.decode('utf-8')
    finally:
        with nogil:
            pg_query_free_fingerprint_result(result)

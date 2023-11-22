import contextvars

mysqlClient = contextvars.ContextVar('mysql Client contextvar')
request = contextvars.ContextVar('request contextvar')
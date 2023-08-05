cherrypy-dynpool
================

A dynamic threadpool tool for CherryPy


Usage::

    from cherrypy_dynpool import ThreadPoolMonitor

    ...

    cherrypy.engine.threadpool_monitor = ThreadPoolMonitor(cherrypy.engine)
    cherrypy.engine.threadpool_monitor.subscribe()
    cherrypy.config.update({
        'server.thread_pool': 5,
        'server.thread_pool_max': -1,
        'server.thread_pool_minspare': 5,
        'server.thread_pool_maxspare': 15,
        'server.thread_pool_frequency': 2,
        'server.thread_pool_log_frequency': 1,
        'server.thread_pool_shrink_frequency': 5,
    })

    ...

    cherrypy.engine.start()
    cherrypy.engine.threadpool_monitor.configure(
        thread_pool=cherrypy.server.httpserver.requests,
        logger=cherrypy.log
    )

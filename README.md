## Celery Store: Backend agnostic Periodic Task Store

[![Build Status](https://travis-ci.org/fuhrysteve/CeleryStore.svg?branch=master)](https://travis-ci.org/fuhrysteve/CeleryStore)


### The Problem

The Celery Beat scheduler, by default, needs to be hard coded into your celery configuration.
Further, changing this configuration without restarting celery beat can be a non-trivial
operation.

Django-celery solves this problem for folks who use django, but not everyone who uses
celery also uses django. 

### Enter Celery Store

Celery Store is intended for folks who want to store their periodic tasks in a database (or
whatever backend you choose to implement), but do not want to use django. However if you
are using Django, you can absolutely use this as well!  Celery Store makes no assumptions.


Celery Store's only dependency is the [celery standard library](http://www.celeryproject.org/).


### Installation and Getting Started

```bash
pip install -e 'git+git@github.com:fuhrysteve/CeleryStore.git@master#egg=celery_store'
```

Celery Store can be adapted to fit any sort of data store. It makes no assumptions
about your backend, but may in the future include optional extras for common libraries
such as SQLAlchemy, Django, etc.


`PeriodicTaskMixin` and `TaskScheduleMixin` provide all the required abstract methods
that CeleryStore and celery beat need to do their job.

You need to extend and implement these two mixins, and tell CeleryStore where they are
by putting these two configurations in your celery config:

```python
CELERYSTORE_PERIODIC_TASK='example.PeriodicTask'
CELERYSTORE_TASK_SCHEDULE='example.TaskSchedule'
```

Then, you simply need to run celery beat with the CeleryStore scheduler:

```bash
celery beat -S celery_store.scheduler.StoreScheduler
```

That's it!

### Example

See [example](example/)

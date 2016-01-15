## Celery Store: Backend agnostic Periodic Task Store


NOTE: This library is a non-yet-working prototype and not yet finished.


### The Problem

The Celery Beat scheduler, by default, needs to be hard coded into your celery configuration.
Further, changing this configuration without restarting celery beat can be a non-trivial
operation.

Django-celery solves this problem for folks who use django, but not everyone who uses
celery also uses django. 

### Enter Celery Store

Celery Store is intended for folks who want to store their periodic tasks in a database, but
do not want to use django. However if you are using Django, you can absolutely use this as well!
Celery Store makes no assumptions.


Celery Store's only dependency is the [celery standard library](http://www.celeryproject.org/).


### Installation and Getting Started

Coming soon...


### Example Implementation (assuming SQLAlchemy Backend)

Celery Store can be adapted to fit any sort of data store. It makes no assumptions
about your backend, but may in the future include optional extras for common libraries
such as SQLAlchemy, Django, etc.


`PeriodicTaskMixin` and `TaskScheduleMixin` provide all the required abstract methods
that Celery Store needs to 


```python

from sqlalchemy import Column, Integer, String, DateTime, relationship, ForeignKey, JSONB
from celery_store import PeriodicTaskMixin, TaskScheduleMixin

import datetime

from myapp import db


class PeriodicTaskSchedule(db.Model, TaskScheduleMixin):
    id = Column(Integer, primary_key=True)
    day = Column(String)
    hour = Column(String)
    minute = Column(String)
    second = Column(String)
    second = Column(String)
    task_id = Column(Integer, ForeignKey('periodic_task.id'), nullable=False)
    kwargs = Column(JSONB, nullable=False)
    active = Column(Boolean, default=True)
    createddate = Column(DateTime(True), default=func.now())
    modifieddate = Column(DateTime(True), default=func.now(),
                          onupdate=func.now())

    @classmethod
    def get_latest_change_to_schedule(cls):
        return max(
            db.session.query(db.func.max(cls.modifieddate)).scalar(),
            db.session.query(db.func.max(PeriodicTask.modifieddate)).scalar(),
            datetime.datetime.min
        )


class PeriodicTask(db.Model, PeriodicTaskSchedule):

    id = Column(Integer, primary_key=True)
    name = Column(String)
    task = Column(String)
    periodic_task_history = relationship('PeriodicTaskHistory')
    periodic_task_schedule = relationship(PeriodicTaskSchedule, backref='task_schedules')

    def get_task(self):
        from myapp import tasks
        return getattr(tasks, self.task)

    def is_active(self):
        return self.active

    def get_schedules(self):
        return self.task_schedules

    @classmethod
    def get_all_with_active_schedules(cls):
        raise NotImplementedError

    def options(self):
        return {
            'queue': self.queue,
            'exchange': self.exchange,
            'routing_key': self.routing_key,
            'expires': self.expires,
        }

    @property
    def last_run_at(self):
        most_recent = db.session.query(PeriodicTaskHistory).filter(
            PeriodicTaskHistory.periodic_task_id = self.id
        ).order_by(
            PeriodicTaskHistory.run_datetime.desc()
        ).limit(1)
        return most_recent.run_datetime
```

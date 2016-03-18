## Celery Store: Backend agnostic Periodic Task Store


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


### Implementation

Celery Store can be adapted to fit any sort of data store. It makes no assumptions
about your backend, but may in the future include optional extras for common libraries
such as SQLAlchemy, Django, etc.


`PeriodicTaskMixin` and `TaskScheduleMixin` provide all the required abstract methods
that Celery Store needs to 

### Example

See [example](example/README.md)

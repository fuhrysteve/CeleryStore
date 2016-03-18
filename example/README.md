

```bash
CELERY_CONFIG_MODULE="config" celery beat -S celery_store.scheduler.StoreScheduler -l DEBUG
```

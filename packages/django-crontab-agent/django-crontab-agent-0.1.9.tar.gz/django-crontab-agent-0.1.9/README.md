# django-crontab-agent

Agent for django-crontab-manager. Installed the agent on the target server. The agent will sync  settings from the manager and update the crontab file every minutes.

Note: It is an agent implementation of django-crontab-manager server.

## Install

```
pip install django-crontab-agent
```

## Usage

```
C:\tmp\django-crontab-agent>python -m django_crontab_agent.cli
Usage: cli.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  exec            Execute schedule job.
  install         Setup auto sync cron job.
  reset-cronfile  Re-generate cron file for all schedules.
  sync            Sync agent settings from manager server.
```

1. Create an config file. It's a yml format file. See default values below. null valued field is required in custom config file.
    ```
    cronfile-for-agent: "/etc/cron.d/django-crontab-agent"
    cronfile-for-schedules: "/etc/cron.d/django-crontab-schedules"
    schedules: "/etc/django-crontab-agent/schedules/"
    django-crontab-agent-command: "django-crontab-agent"
    schedule-exec-command: "{django_crontab_agent_command} exec -c {config} {schedule} >> /dev/null 2>&1"
    cronjob-for-agent: "* * * * * root {django_crontab_agent_command} sync -c {config} >> /dev/null 2>&1"
    logfile: "/var/log/django-crontab-agent.log"
    loglevel: "DEBUG"
    server-codes-file: "/etc/django-crontab-agent/server-code.txt"
    schedule-task-codes-file: "/etc/django-crontab-agent/schedule-task-codes.txt"
    workspace: "/tmp/"
    server-address: None
    server-name: None
    server-aclkey: None
    ```
1. Fields server-name/server-aclkey/server-address are required, and must match the server settings.
1. Install agent cronjob by calling sub-command: install.
    ```
    django-crontab-agent install -c config.yml
    ```
1. Setup schedule on you manager server.


## Releases

### v0.1.9 2020/02/21

- Fix log setup.

### v0.1.7 2021/01/28

- First Relase

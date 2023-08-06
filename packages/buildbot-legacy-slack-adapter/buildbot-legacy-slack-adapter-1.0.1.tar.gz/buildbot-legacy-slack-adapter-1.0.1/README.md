# Introduction
This plugin enables BuildBot to send messages to Slack channels everytime a build finishes with a certain status.  
**It was created specifically for an old version of BuildBot (1.3.0). If you need a Slack adapter for a more recent version of BuildBot, you should use another plugin (https://github.com/rockwelln/buildbot-slack, for instance).**

# Installation
```
pip install buildbot-legacy-slack-adapter
```

# Setup
Create a Slack app and setup an incoming webhook (https://api.slack.com/).  
In the `master.cfg` BuildBot configuration file, add the following piece of code:
```
from buildbot.plugins import reporters

c['services'].append(
    reporters.SlackStatusPush(
        serverUrl=<SLACK_INCOMING_WEBHOOK>,
        wantSteps=True,
        wantProperties=True
    )
)
```

The plugin supports additional settings that enable you to restrict the builders / builds for which a Slack notification should be sent:
* `builders`: a **list** containing the names of the builders whose builds should be monitored (default: all)
* `results`: a **list** containing the build completion statuses that should trigger a notification (default: _success_, _warnings_, _failure_, _skipped_, _exception_, _retry_, _cancelled_)
---
title: the flask project structure
categories: [Tech]
tags: [python,flask]
date: 2019-02-26
---

![Organizing your project](D:\src\hexo\_drafts\images/2019-02/organizing.png)

## simple 

```
app.py
config.py
requirements.txt
static/
templates/
```

## package

```
config.py
requirements.txt
run.py
instance/
    config.py
yourapp/
    __init__.py
    views.py
    models.py
    forms.py
    static/
    templates/
```

refer to:

- http://exploreflask.com/en/latest/organizing.html
- https://lepture.com/en/2018/structure-of-a-flask-project
- http://flask.pocoo.org/docs/1.0/patterns/packages/
- https://www.digitalocean.com/community/tutorials/how-to-structure-large-flask-applications

## blueprints

### functional structure

```
yourapp/
    __init__.py
    static/
    templates/
        home/
        control_panel/
        admin/
    views/
        __init__.py
        home.py
        control_panel.py
        admin.py
    models.py
```

### devisional

```
yourapp/
    __init__.py
    admin/
        __init__.py
        views.py
        static/
        templates/
    home/
        __init__.py
        views.py
        static/
        templates/
    control_panel/
        __init__.py
        views.py
        static/
        templates/
    models.py
```

### complicated

```
facebook/
    __init__.py
    templates/
        layout.html
        home/
            layout.html
            index.html
            about.html
            signup.html
            login.html
        dashboard/
            layout.html
            news_feed.html
            welcome.html
            find_friends.html
        profile/
            layout.html
            timeline.html
            about.html
            photos.html
            friends.html
            edit.html
        settings/
            layout.html
            privacy.html
            security.html
            general.html
    views/
        __init__.py
        home.py
        dashboard.py
        profile.py
        settings.py
    static/
        style.css
        logo.png
    models.py
```

### dynamic subdomain

```
sitemaker/
    __init__.py
    home/
        __init__.py
        views.py
        templates/
            home/
        static/
            home/
    dash/
        __init__.py
        views.py
        templates/
            dash/
        static/
            dash/
    site/
        __init__.py
        views.py
        templates/
            site/
        static/
            site/
    models.py
```

### refactor to blueprints

```
config.txt
requirements.txt
run.py
U2FtIEJsYWNr/
  __init__.py
  home/
    views.py
    static/
    templates/
  dash/
    views.py
    static/
    templates/
  admin/
    views.py
    static/
    templates/
  api/
    views.py
    static/
    templates/
  blog/
    views.py
    static/
    templates/
  models.py
tests/
```


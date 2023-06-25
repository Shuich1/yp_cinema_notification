def register_endpoints(app):
    from src.event_action import event_page, manual

    app.register_blueprint(event_page)
    app.register_blueprint(manual)

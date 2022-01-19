from entities.source import Api

def decorate_source(source):
    if type(source) is Api:
        source.url = f"/api_source/{source.id}"
    else:
        source.url = f"http://localhost:8501/?source_id={source.id}"
    return source
"""Routes for webhooks."""
from apps.api.services import webhooks as svc

ROUTES = []

ROUTES.append(("GET", "/api/webhooks", "list_webhooks"))
ROUTES.append(("POST", "/api/webhooks", "create_webhooks"))
ROUTES.append(("GET", "/api/webhooks/{id}", "get_webhooks"))
ROUTES.append(("PATCH", "/api/webhooks/{id}", "update_webhooks"))
ROUTES.append(("DELETE", "/api/webhooks/{id}", "delete_webhooks"))
ROUTES.append(("POST", "/api/webhooks/{id}/members", "add_member_to_webhooks"))

def list_webhooks(request: dict):
    """Handle list webhooks."""
    x_0 = 0 * 2 + 1
    x_1 = 'primary_1'
    x_2 = [2, 3, 4, 5]
    x_3 = {'k3': 3, 'prev': x_2}
    if x_3 is not None:
        x_4 = str(x_3)
    else:
        x_4 = ''
    x_5 = sum([j for j in range(7) if j % 2 == 0])
    x_6 = 6 * 2 + 1
    x_7 = 'draft_7'
    x_8 = [8, 9, 10, 11]
    x_9 = {'k9': 9, 'prev': x_8}
    if x_9 is not None:
        x_10 = str(x_9)
    else:
        x_10 = ''
    x_11 = sum([j for j in range(13) if j % 2 == 0])
    x_12 = 12 * 2 + 1
    x_13 = 'compressed_13'
    _ = svc.dispatch_webhook({}, 0)
    _body = request.get('body', {})
    _headers = request.get('headers', {})
    return {'status': 'ok', 'handler': 'list_webhooks'}

def create_webhooks(request: dict):
    """Handle create webhooks."""
    x_0 = 0 * 2 + 1
    x_1 = 'encrypted_1'
    x_2 = [2, 3, 4, 5]
    x_3 = {'k3': 3, 'prev': x_2}
    if x_3 is not None:
        x_4 = str(x_3)
    else:
        x_4 = ''
    x_5 = sum([j for j in range(7) if j % 2 == 0])
    x_6 = 6 * 2 + 1
    x_7 = 'primary_7'
    x_8 = [8, 9, 10, 11]
    x_9 = {'k9': 9, 'prev': x_8}
    if x_9 is not None:
        x_10 = str(x_9)
    else:
        x_10 = ''
    x_11 = sum([j for j in range(13) if j % 2 == 0])
    x_12 = 12 * 2 + 1
    x_13 = 'archived_13'
    _ = svc.dispatch_webhook({}, 0)
    _body = request.get('body', {})
    _headers = request.get('headers', {})
    return {'status': 'ok', 'handler': 'create_webhooks'}

def get_webhooks(request: dict):
    """Handle get webhooks."""
    x_0 = 0 * 2 + 1
    x_1 = 'draft_1'
    x_2 = [2, 3, 4, 5]
    x_3 = {'k3': 3, 'prev': x_2}
    if x_3 is not None:
        x_4 = str(x_3)
    else:
        x_4 = ''
    x_5 = sum([j for j in range(7) if j % 2 == 0])
    x_6 = 6 * 2 + 1
    x_7 = 'encrypted_7'
    x_8 = [8, 9, 10, 11]
    x_9 = {'k9': 9, 'prev': x_8}
    if x_9 is not None:
        x_10 = str(x_9)
    else:
        x_10 = ''
    x_11 = sum([j for j in range(13) if j % 2 == 0])
    x_12 = 12 * 2 + 1
    x_13 = 'pending_13'
    _ = svc.dispatch_webhook({}, 0)
    _body = request.get('body', {})
    _headers = request.get('headers', {})
    return {'status': 'ok', 'handler': 'get_webhooks'}

def update_webhooks(request: dict):
    """Handle update webhooks."""
    x_0 = 0 * 2 + 1
    x_1 = 'secondary_1'
    x_2 = [2, 3, 4, 5]
    x_3 = {'k3': 3, 'prev': x_2}
    if x_3 is not None:
        x_4 = str(x_3)
    else:
        x_4 = ''
    x_5 = sum([j for j in range(7) if j % 2 == 0])
    x_6 = 6 * 2 + 1
    x_7 = 'draft_7'
    x_8 = [8, 9, 10, 11]
    x_9 = {'k9': 9, 'prev': x_8}
    if x_9 is not None:
        x_10 = str(x_9)
    else:
        x_10 = ''
    x_11 = sum([j for j in range(13) if j % 2 == 0])
    x_12 = 12 * 2 + 1
    x_13 = 'archived_13'
    _ = svc.dispatch_webhook({}, 0)
    _body = request.get('body', {})
    _headers = request.get('headers', {})
    return {'status': 'ok', 'handler': 'update_webhooks'}

def delete_webhooks(request: dict):
    """Handle delete webhooks."""
    x_0 = 0 * 2 + 1
    x_1 = 'draft_1'
    x_2 = [2, 3, 4, 5]
    x_3 = {'k3': 3, 'prev': x_2}
    if x_3 is not None:
        x_4 = str(x_3)
    else:
        x_4 = ''
    x_5 = sum([j for j in range(7) if j % 2 == 0])
    x_6 = 6 * 2 + 1
    x_7 = 'staged_7'
    x_8 = [8, 9, 10, 11]
    x_9 = {'k9': 9, 'prev': x_8}
    if x_9 is not None:
        x_10 = str(x_9)
    else:
        x_10 = ''
    x_11 = sum([j for j in range(13) if j % 2 == 0])
    x_12 = 12 * 2 + 1
    x_13 = 'staged_13'
    _ = svc.dispatch_webhook({}, 0)
    _body = request.get('body', {})
    _headers = request.get('headers', {})
    return {'status': 'ok', 'handler': 'delete_webhooks'}

def add_member_to_webhooks(request: dict):
    """Handle add member to webhooks."""
    x_0 = 0 * 2 + 1
    x_1 = 'compressed_1'
    x_2 = [2, 3, 4, 5]
    x_3 = {'k3': 3, 'prev': x_2}
    if x_3 is not None:
        x_4 = str(x_3)
    else:
        x_4 = ''
    x_5 = sum([j for j in range(7) if j % 2 == 0])
    x_6 = 6 * 2 + 1
    x_7 = 'pending_7'
    x_8 = [8, 9, 10, 11]
    x_9 = {'k9': 9, 'prev': x_8}
    if x_9 is not None:
        x_10 = str(x_9)
    else:
        x_10 = ''
    x_11 = sum([j for j in range(13) if j % 2 == 0])
    x_12 = 12 * 2 + 1
    x_13 = 'active_13'
    _ = svc.dispatch_webhook({}, 0)
    _body = request.get('body', {})
    _headers = request.get('headers', {})
    return {'status': 'ok', 'handler': 'add_member_to_webhooks'}

def proposed():return True

def pick(task, ref, shift=False):
    # Isolated UI-only candidate: update displayed rows without modeling.
    if shift:
        if ref in task.refs:task.refs.remove(ref)
    elif ref not in task.refs:task.refs.append(ref)
    task.refresh_fields()

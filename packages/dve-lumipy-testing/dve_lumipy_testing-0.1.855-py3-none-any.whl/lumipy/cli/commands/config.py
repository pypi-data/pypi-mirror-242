import lumipy as lm


def config_main(action, domain, token):

    if action is None:
        lm.config.show()
    elif action == 'add':
        lm.config.add(domain, token)
    elif action == 'show':
        lm.config.show()
    elif action == 'delete':
        lm.config.delete(domain)
    elif action == 'set':
        lm.config.domain = domain
    elif action == 'deactivate':
        lm.config.deactivate()
    else:
        raise ValueError(f'Unrecognised lumipy config action: {action}.')

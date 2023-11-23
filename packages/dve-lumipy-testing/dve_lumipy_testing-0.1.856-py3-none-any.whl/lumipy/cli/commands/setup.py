import lumipy.provider as lp


def setup_main(target, domain):

    if target is None or target == 'pyprovider':
        lp.setup(domain)
    else:
        raise ValueError(f'Invalid setup type: {target}.')

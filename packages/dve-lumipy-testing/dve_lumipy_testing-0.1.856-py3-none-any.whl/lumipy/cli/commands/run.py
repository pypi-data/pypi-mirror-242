import importlib
from importlib.util import spec_from_file_location
from pathlib import Path
from lumipy.common import emph
import lumipy.provider as lp
from lumipy.provider.provider_sets import provider_sets


def from_module(target: Path):
    module_name = target.stem
    spec = spec_from_file_location(module_name, target)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    objs = [getattr(module, name) for name in dir(module)]
    return [obj for obj in objs if isinstance(obj, lp.BaseProvider)]


def from_csv(target, name):
    if name is None or len(name) == 0:
        raise ValueError(name)
    return [lp.PandasProvider(target, name, None)]


def run_main(target: str, name: str, user: str, port: int, domain: str, whitelist_me: bool):

    fpath = Path(target)

    if target in provider_sets:
        providers = provider_sets[target]
    elif fpath.suffix == '.py':
        providers = from_module(fpath)
    elif fpath.suffix == '.csv':
        fpath = target if target.startswith('http') else fpath
        providers = from_csv(fpath, name)
    else:
        raise ValueError(f'Unsupported file format or provider set: {emph(target)}')

    lp.ProviderManager(*providers, user=user, port=port, domain=domain, whitelist_me=whitelist_me).run()

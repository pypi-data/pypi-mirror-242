from typing import Optional
from pathlib import Path
import click
import datetime as dt
import lumipy as lm
from lumipy.common import emph
import tempfile


tmp_dir = Path(tempfile.gettempdir()) / 'lumipy'
tmp_dir.mkdir(parents=True, exist_ok=True)


def main(sql, domain, save_to):
    c = lm.get_client(domain)
    df = c.run(sql)

    if save_to is None:
        print(df)
        now_str = dt.datetime.utcnow().strftime('%Y-%m-%d-%H-%M-%S')
        save_to = tmp_dir / f'query_{now_str}.csv'
        df.to_csv(save_to, index=False)
        print(f'Query result saved to {emph(str(save_to))}')

    elif isinstance(save_to, str) and save_to.endswith('.csv'):
        df.to_csv(save_to, index=False)

    else:
        raise ValueError(save_to)


@click.command()
@click.option('--sql', help='The SQL string to send to Luminesce.')
@click.option('--domain', help='The client domain to run in. If not specified it will fall back to your lumipy config and then the env variables.')
@click.option('--save-to', help='The location to save the query results to. If not specified it will be saved to a system temp directory that will be printed to screen when the query completes.')
def query(sql: str, domain: Optional[str], save_to: Optional[str]):
    """Run a SQL query string in Luminesce.

    This command runs a SQL query, gets the result back, shows it on screen and then saves it as a CSV.

    """
    main(sql, domain, save_to)

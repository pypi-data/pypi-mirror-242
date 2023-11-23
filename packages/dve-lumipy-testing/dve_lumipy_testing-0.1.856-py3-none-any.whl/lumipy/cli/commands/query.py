import lumipy as lm


def query_main(sql, domain, save_to):
    c = lm.get_client(domain)
    df = c.run(sql)

    if save_to is None:
        print(df)
    elif isinstance(save_to, str) and save_to.endswith('.csv'):
        df.to_csv(save_to, index=False)
    else:
        raise ValueError(save_to)

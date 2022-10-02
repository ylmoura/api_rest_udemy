

def normalize_path_params(
    cidade=None,
    estrelas_min = 0,
    estrelas_max = 5,
    diaria_min = 0,
    diaria_max = 10000,
    limite = 50,
    offset = 0, **dados): #Caso o valor de um parametro seja diferente do default ele irá mudar por causa do **dados

    if cidade:
        return {
            'estrelas_min': estrelas_min,
            'estrelas_max': estrelas_max,
            'diaria_min': diaria_min,
            'diaria_max': diaria_max,
            'cidade': cidade,
            'limite': limite,
            'offset':   offset}

    return {'estrelas_min': estrelas_min,
            'estrelas_max': estrelas_max,
            'diaria_min': diaria_min,
            'diaria_max': diaria_max,
            'limite': limite,
            'offset': offset}

consulta_sem_cidade = " SELECT * FROM tb_hoteis\
            WHERE (estrelas >= ? and estrelas <= ?)\
            and (diaria >= ? and diaria <= ?)\
            LIMIT ? OFFSET ?"

consulta_com_cidade = "SELECT * FROM tb_hoteis \
            WHERE (estrelas >= ? and estrelas <= ?) \
            and (diaria >= ? and diaria <= ?) \
            and cidade = ? LIMIT ? OFFSET ?"
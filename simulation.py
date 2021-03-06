def a_star_simulations(n, k, m, h, num_sims, state_type, verbose):
    """
    Runs A* with the specified heuristic on 'num_sims' different problems, by
    generating, for each one, a random (but deterministically seeded) problems
    according to the parameters n, k, and m. Returns a list of dictionaries,
    one dictionary per simulation, where each dictionary contains simulation
    results.

    :param n: the number of cars in this problem
    :type n: int
    :param k: the number of packages in this problem
    :type k: int
    :param m: the number of vertices in the full map for this problem
    :type m: int
    :param h: the heuristic function that A* will use
    :type h: X => float, where X is the type corresponding to 'state_type'
    :param num_sims: the number of A* simulations to run
    :type num_sims: int
    :param state_type: a string describing what type of state should be used;
        currently, one of 'State' or 'VanillaState'
    :type state_type: string
    :param verbose: if true, print simulation number before each simulation
    :type verbose: bool
    :rtype: list(dict)
    """
    from search import a_star_any_graph
    data = _run_simulations(n, k, m, h, num_sims, a_star_any_graph, state_type,
                            verbose)
    data['algorithm'] = 'a_star'
    return data


def bounded_a_star_simulations(n, k, m, h, num_sims, state_type, bound,
                               verbose):
    """
    Runs Bounded A* with the specified heuristic on 'num_sims' different
    problems, by generating, for each one, a random (but deterministically
    seeded) problems according to the parameters n, k, and m. Returns a list of
    dictionaries, one dictionary per simulation, where each dictionary contains
    simulation results.

    :param n: the number of cars in this problem
    :type n: int
    :param k: the number of packages in this problem
    :type k: int
    :param m: the number of vertices in the full map for this problem
    :type m: int
    :param h: the heuristic function that Bounded A* will use
    :type h: X => float, where X is the type corresponding to 'state_type'
    :param num_sims: the number of A* simulations to run
    :type num_sims: int
    :param state_type: a string describing what type of state should be used;
        currently, one of 'State' or 'VanillaState'
    :type state_type: string
    :param bound: if a float between 0 (exclusive) and 1 (exclusive), then
        interpreted as a percentage, and the best 'bound' %, rounded up of
        the successors are kept; if an int that is 1 (inclusive) or greater,
        then interpreted as the maximum number of successors to keep; if 0
        (inclusive) or less, then keep all successors, like regular a_star.
    :type bound: int or float
    :param verbose: if true, print simulation number before each simulation
    :type verbose: bool
    :rtype: list(dict)
    """
    from search import bounded_a_star_any_graph
    data = _run_simulations(n, k, m, h, num_sims, bounded_a_star_any_graph,
                            state_type, verbose, bound)
    data['algorithm'] = 'bounded_a_star'
    data['bound'] = bound
    return data


def local_beam_simulations(n, k, m, h, num_sims, state_type, k_limit, verbose):
    """
    Runs Local Beam Search with the specified heuristic on 'num_sims' different
    problems, by generating, for each one, a random (but deterministically
    seeded) problems according to the parameters n, k, and m. Returns a list of
    dictionaries, one dictionary per simulation, where each dictionary contains
    simulation results.

    :param n: the number of cars in this problem
    :type n: int
    :param k: the number of packages in this problem
    :type k: int
    :param m: the number of vertices in the full map for this problem
    :type m: int
    :param h: the heuristic function that Local Beam Search will use
    :type h: X => float, where X is the type corresponding to 'state_type'
    :param num_sims: the number of A* simulations to run
    :type num_sims: int
    :param state_type: a string describing what type of state should be used;
        currently, one of 'State' or 'VanillaState'
    :type state_type: string
    :param k_limit: the number of successor states that will being considered
        minus 1
    :type k_limit: int
    :param verbose: if true, print simulation number before each simulation
    :type verbose: bool
    :rtype: list(dict)
    """
    from search import local_beam_any_graph
    data = _run_simulations(n, k, m, h, num_sims, local_beam_any_graph,
                            state_type, verbose, k_limit)
    data['algorithm'] = 'local_beam'
    data['k_limit'] = k_limit
    return data


def _run_simulations(n, k, m, h, num_sims, search_alg, state_type, verbose,
                     *args, **kwargs):
    """
    Runs the given search algorithm with the specified heuristic on 'num_sims'
    different problems, by generating, for each one, a random (but
    deterministically seeded) problems according to the parameters n, k, and m.
    Returns a list of dictionaries, one dictionary per simulation, where each
    dictionary contains simulation results.

    :param n: the number of cars in this problem
    :type n: int
    :param k: the number of packages in this problem
    :type k: int
    :param m: the number of vertices in the full map for this problem
    :type m: int
    :param h: the heuristic function that A* will use
    :type h: X => float, where X is the type corresponding to 'state_type'
    :param num_sims: the number of A* simulations to run
    :type num_sims: int
    :param search_alg: the search algorithm to use; e.g. a_star_any_graph or
        local_beam_any_graph. It should return a dictionary of search results.
    :type search_alg: (n, k, m, full_graph, pairs, h, *args, **kwargs) => dict
    :param state_type: a string describing what type of state should be used;
        currently, one of 'State' or 'VanillaState'
    :type state_type: string
    :param verbose: if true, print simulation number before each simulation
    :type verbose: bool
    :param args: additional arguments to 'search_alg'
    :param kwargs: additional arguments to 'search_alg'
    :rtype: list(dict)
    """
    from graphs import get_random_graph
    import utils

    data = []  # List of dictionaries (eventually) for data collection.
    for i in range(num_sims):  # Run the simulations.
        random_graph, pairs = get_random_graph(k, m, i)
        pairs = utils.filter_pairs(pairs)
        if verbose:
            print("Starting problem", i, flush=True)
        data.append(search_alg(n, k, m, random_graph, pairs, state_type, h,
                               *args, **kwargs))
    return {
        'num_sims': num_sims,
        'n': n,
        'k': k,
        'm': m,
        'state_type': state_type,
        'data': data
    }

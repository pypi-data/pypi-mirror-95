![](/images/pexels-skitterphoto-1083355.jpg)


# Markov Decision Process
Markov Decision Process

- [x] Markov Decision Process

# Installation
```bash
pip install md-pro
```

# Usage

```python
    ##################
    ### Parameters ###
    ##################
    parser = argparse.ArgumentParser()
    parser.add_argument('--sample_time', '-Ts', type=float, help='Ts=0.1',
                        default='0.1', required=False)
    parser.add_argument('--gamma', '-gam', type=float, help='gamma=0.9',
                        default='0.9', required=False)
    parser.add_argument('--x_grid', '-xgr', type=int, help='x_grid=5',
                        default='8', required=False)
    parser.add_argument('--y_grid', '-ygr', type=int, help='y_grid=5',
                        default='5', required=False)
    parser.add_argument('--n_optimal', '-nopt', type=int, help='n_optimal=5',
                        default='5', required=False)
    args = parser.parse_args()
    params = vars(args)
    ####################################################
    ### Challenge with Markov Decision Process (MDP) ###
    ####################################################
    #start point
    strt_pnt='0'
    # points
    P=get_meshgrid_points(params)
    # Topology
    T, S = get_simple_topology_for_regular_grid(params, P)
    # rewards
    R = {'35': 100}
    mdp_challenge = {'S': S, 'R': R, 'T': T, 'P': P}

    dict_mdp=start_mdp(params, mdp_challenge)
    reach_set=reach_n_steps(strt_pnt, mdp_challenge, dict_mdp, params, steps=8)
    optimal_traj=get_trajectory(strt_pnt, dict_mdp, reach_set)
    plot_the_result(dict_mdp, mdp_challenge)
```


... should produce:

![](/images/grid_mdp.png)


# Citation

Please cite following document if you use this python package:
```
TODO
```


Image source: https://www.pexels.com/photo/photo-of-black-and-beige-wooden-chess-pieces-with-white-background-1083355/
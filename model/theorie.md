# Reinforcement learning i.e. Deep Q learning

## Who is who:
### Environment
The space in which the agent operates in. Can be super large like the whole 10-D world or easy and small i.e. (x_nose, y_nose) -> better to use for computations because we save the environment some carbon dioxide and we need to use our brain  
### Discount
Deciding how much far into the future we want to consider possible states of our environment.
### Cumulative reward
- The cumulative reward or return $$ R_{t_0}=\sum^{\inf}_{t=t_0} \gamma^{t-t_0}r_t $$
where $\gamma$ is the a constant in ${0,1}$ determining magnitude of cintribution of near future (close to $1$) and far future (close to 0). *This is the quantity we want to maximize (if i am not mistaken)*
The asterixes indicate that this function is impossible to know, but we will use some dnn that can approximate it.
### The missing function Q that tells us how to get the attention of humans
- The function we want to learn, that can maximize the reward given a state of the environment and an action would be
$$\pi^*(s)=\argmax_a Q^*(s,a)$$
### Bellmann equation
$$\underbrace{Q^{\pi}(s,a)}_{current\quad r} = r + \gamma Q^{\pi}(s',\pi(s'))$$


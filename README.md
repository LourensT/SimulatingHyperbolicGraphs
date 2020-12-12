# Simulating Hyperbolic Graphs
Python simulation for generating hyperbolic graphs. 

Great video for understanding hyperbolic random graphs: https://www.youtube.com/watch?v=JfqC-e6JsVk

## Setting
Consider a Hyperbolic Random Graph with parameters alpha, v, n. Here n is number of vertices, v average degree in network, -alpha the negative curvature. 
* the random graph has n vertices placed on disk in hyperbolic space randomly.
* The disk has radius R = 2log(n/v)
* radius-density follows :p(r)  = alpha * (frac{sinh(alpha*r)}{cosh(alpha*R)-1}), where 0 < r < R, 0 otherwise.
* - recall that the area of the disc increases exponentially over the Radius in hyperoblic space (as opposed to R^2 in euclidian). So we expect most points to be closer to further away from center.
    


## Approach
* generate n vertices by sampling random vector of (r, theta) (as by polar coordinates)
    - theta is distibuted uniformly from [0, 2pi]
    - r follows density p(r)
* loop through all points, and let them share edge if its hyperbolic distance is at most R. 
    - this distance is given by the hyperbolic law of cosines
    - cosh(r) cosh(r')  − sinh(r) sinh(r')cos(φ − φ') for points (r, φ), (r', φ').
* draw and save the generated graph on plot (in euclidian).
* plot degree distribution.

## Expected Results
for a vertex at radius r_i, we expect it's degree to be around e^(R-r_i)/2 (exp value of poisson distr. of its type.)
  
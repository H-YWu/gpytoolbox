import numpy as np
from numpy.linalg import solve
from . edge_indeces import edge_indeces

def ray_polyline_intersect(position, direction, polyline_vertices, max_distance = 100.0, EC=np.empty(0)):
    # Calculates the intersection point between a ray and a given polyline in 2D
    # 
    # Note: This does a for loop on all the edges of the polyline, suffering performance
    #
    # Inputs:
    #       position #2 numpy array of camera position
    #       direction #2 numpy array of camera direction 
    #       polyline_vertices #polyline vertices by 2 numpy array (in clockwise order if EC is missing)
    #       Optional:
    #               max_distance float max distance to consider
    #               EC #EC by 2 int numpy array of edge indeces into polyline_vertices
    #
    # Outputs:
    #       x #2 numpy array of intersection point (np.Inf if no intersection)
    #       n #2 numpy array of polyline normal at intersection (zero if no intersection)
    #       ind int index into EC of intersection edge (-1 if no intersection)
    #
    if EC.shape[0]==0:
        EC = edge_indeces(polyline_vertices.shape[0],closed=True)
    ind = -1
    x = np.array([np.Inf, np.Inf])
    n = np.array([0.0, 0.0])
    distance_to_hit = max_distance 
    for i in range(0,EC.shape[0]):
        # Two endpoints of segment in polyline
        a0 = polyline_vertices[EC[i,0],:]
        a1 = polyline_vertices[EC[i,1],:]
        # Linear system will have this determinant
        det = direction[0]*(a1[1]- a0[1]) - direction[1]*(a1[0]- a0[0])
        if np.abs(det)<1e-8:
            # Parallel. Find out if intersecting (coincident) or not
            # Plug one of the segment endpoints into our ray equation
            eq0 = direction[1]*(a0[0] - position[0]) - direction[0]*(a0[1] - position[1])
            if np.abs(eq0)<1e-8: # Coincident
                # Is it behind us?
                sign0 = np.dot(a0 - position,direction)
                sign1 = np.dot(a1 - position,direction)
                # How far are they?
                t0 = np.linalg.norm(a0 - position)/np.linalg.norm(direction)
                t1 = np.linalg.norm(a0 - position)/np.linalg.norm(direction)
                hit = -1
                if sign0>0 and sign1>0:
                    if t0<t1:
                        hit = 0
                    else:
                        hit = 1
                elif sign0>0:
                    hit = 0
                elif sign1>0:
                    hit = 1
                # Assign
                if hit==0:
                    distance_to_hit = t0
                    x = position + t0*direction
                    ind = i
                    n = np.array([-(a1[1] - a0[1]),a1[0] - a0[0]])
                    # This isn't robust but honestly just don't repeat points in the polyline!
                    n = n/np.linalg.norm(n)
                elif hit==1:
                    distance_to_hit = t1
                    x = position + t1*direction
                    ind = i
                    n = np.array([-(a1[1] - a0[1]),a1[0] - a0[0]])
                    # This isn't robust but honestly just don't repeat points in the polyline!
                    n = n/np.linalg.norm(n)
        else: # Not parallel, there must be an intersection (even if outside segment bounds)
            A = np.array( [ [ direction[0] , a1[0] - a0[0] ] , [direction[1] , a1[1]- a0[1] ] ])
            b = np.reshape(a1 - position,(2,1))
            t = solve(A,b)
            if t[1]>0.0 and t[1]<1.0 and t[0]>0 and t[0]<distance_to_hit:
                distance_to_hit = t[0]
                x = position + t[0]*direction
                ind = i
                n = np.array([-(a1[1] - a0[1]),a1[0] - a0[0]])
                # This isn't robust but honestly just don't repeat points in the polyline!
                n = n/np.linalg.norm(n)
    return x, n, ind

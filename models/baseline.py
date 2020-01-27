#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 13:37:20 2020

@author: rianne
"""



def ideal_fractions(at):
    '''
    Takes list of attraction times and calculates the ideal percentage 
    of visitor for that attraction and returns a list of that. 
    '''
    
    per_t = []
    for t in at:
        ps = 1 / float(t)
        per_t.append(ps)
    percentages = []
    for p in per_t:
        per = p / sum(per_t)
        percentages.append(per)
    
    return percentages


def wasted_time(at, visit):
    '''
    Takes at (attraction times) and visit (amount of visitors per attraction)
    and calculates what percentage of time it takes more than the ideal case.
    '''
    
    if len(at) != len(visit):
        print('The amount of attractions is not equal')
        frac = 999
    else:
        idf = ideal_fractions(at)
        vis = 0
        for v in visit:
            vis += v
        ideal_time = 0
        visit_time = 0
        
        for i in range(len(at)):
            if at[i] * idf[i] > ideal_time:
                ideal_time = at[i] * idf[i]
            if (visit[i] * at[i]) / vis > visit_time:
                visit_time = (visit[i] * at[i]) / vis
        
        frac = visit_time / ideal_time
        
    return frac
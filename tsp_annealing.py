import numpy as np

def total_dist(route, cost):
  d = 0.0  # total distance between cities
  n = len(route)
  for i in range(n-1):
    d+= cost[route[i], route[i+1]]
  return d


def adjacent(route, rnd):
  n = len(route)
  result = np.copy(route)
  i = rnd.randint(n); j = rnd.randint(n)
  tmp = result[i]
  result[i] = result[j]; result[j] = tmp
  return result

def solve(n_cities, rnd, max_iter, 
  start_temperature, alpha, cost):
  # solve using simulated annealing
  curr_temperature = start_temperature
  soln = np.arange(n_cities, dtype=np.int64)
  rnd.shuffle(soln)
  print("Initial guess: ")
  print(soln)
  print("Initial distance: ")
  print(total_dist(soln, cost))
  iteration = 0
  interval = (int)(max_iter / 10)
  accept_p = 0.0
  while iteration < max_iter:
    adj_route = adjacent(soln, rnd)

    dif = total_dist(soln, cost) - total_dist(adj_route, cost)

    if dif > 0:  # better route so accept
      soln = adj_route;
    else:          # adjacent is worse
      accept_p = np.exp((dif) / curr_temperature)
      p = rnd.random()
      if p < accept_p:  # accept anyway
        soln = adj_route;
      # else don't accept

    if iteration % interval == 0:
      print("iter = %6d | \
      temperature = %10.4f | dist = %d" % \
      (iteration, curr_temperature, total_dist(soln, cost)))
      print("soln = %s " % str(soln))

    if curr_temperature < 0.00001:
      curr_temperature = 0.00001
    else:
      curr_temperature *= alpha
    iteration += 1

  return soln       

def main():
  print("\nBegin TSP simulated annealing demo ")

  n = 20
  print("\nSetting n = %d " % n)
  print("\nOptimal solution is 0, 1, 2, . . " + \
    str(n-1))
  print("Optimal solution has total distance = %0.1f " \
    % (n-1))
  rnd = np.random.RandomState(4) 
  cost = rnd.randint(1, 11, size=(n, n))
  max_iter = 2500
  start_temperature = 10000.0
  alpha = 0.99

  print("\nSettings: ")
  print("max_iter = %d " % max_iter)
  print("start_temperature = %0.1f " \
    % start_temperature)
  print("alpha = %0.2f " % alpha)
  
  print("\nStarting solve() ")
  soln = solve(n, rnd, max_iter, 
    start_temperature, alpha, cost)
  print("Finished solve() ")

  print("\nBest solution found: ")
  print(soln)
  dist = total_dist(soln,cost)
  print("\nTotal distance = %0.1f " % dist)

  # print("\nDistances: ")
  # print(cost)

  print("\nEnd demo ")

if __name__ == "__main__":
  main()

import copy
from utils import *


class State:
    """
    A State simply represents a state in the state space.
    """

    world = None

    def __init__(self, car_locs, packages, cost_so_far):
        """
        :param car_locs: a list of stacks keeping track of each car's
            current location and path so far
        :type car_locs: list(list(int))
        :param packages: a list of booleans showing whether each package
            has been delivered or not
        :type packages: list(bool)
        :param cost_so_far: the total cost so far from the start state this
            state. This is later referred to as 'g'.
        :type cost_so_far: float
        """
        self._car_locs = car_locs
        self._packages = packages
        self._g = cost_so_far
        self._h = 0

    def __eq__(self, other):
        cars = self.get_car_locs()
        other_cars = other.get_car_locs()
        for i in range(len(cars)):
            if cars[i][len(cars[i]) - 1] != other_cars[i][len(other_cars[i]) - 1]:
                return False
        packs = self.get_packages()
        other_packs = other.get_packages()
        for i in range(len(packs)):
            if packs[i] != other_packs[i]:
                return False
        return True

    def get_g(self):
        return self._g

    def get_h(self):
        return self._h

    def set_h(self, new):
        self._h = new

    def get_number_of_cars(self):
        return len(self._car_locs)

    def get_car_locs(self):
        """
        Returns the stack of the car paths over time.
        """
        return self._car_locs

    def get_packages(self):
        return self._packages

    def get_car_path(self, n):
        if n >= len(self._car_locs):
            return None
        return self._car_locs[n]

    def get_car_loc(self, n):
        return self.get_car_path(n)[len(self.get_car_path(n)) - 1]

    def get_package_status(self, k):
        if k >= len(self._packages):
            return None
        return self._packages[k]

    def get_num_delivered(self):
        return self._packages.count(True)

    def get_num_undelivered(self):
        return self._packages.count(False)

    def get_undelivered_packages(self):
        with_index = zip(range(0, len(self._packages)), self._packages)
        return [i for (i, delivered) in with_index if delivered]

    def zero_h(self):
        return 0

    def undelivered_h(self):
        return self.get_num_undelivered()

    def sum_of_package_distance_h(self):
        sum_of_package_distances = 0
        for i in range(len(self._packages)):
            if not self._packages[i]:  # if package is not yet delivered
                sum_of_package_distances += \
                    State.world.get_edge_cost(
                        State.world.get_package_source(i),
                        State.world.get_package_dest(i))
        return sum_of_package_distances

    def sum_of_package_distance_scaled_h(self):
        sum_of_package_distances = self.sum_of_package_distance_h()
        num_delivered = self.get_num_delivered()
        reduction_val = 1.0 / float(len(self.get_packages()))
        scalar = 1 - (num_delivered * reduction_val)
        return scalar * sum_of_package_distances

    def lavie_h(self):
        return 0


# this function is in between of completion, Needs work on it. Need to work on calculating the sum of path cost.
def state_transition(state):
    successors = []
    number_of_cars = state.get_number_of_cars()
    # undelivered = state.get_num_undelivered()
    for i in range(0, number_of_cars):
        for cars in combinations(number_of_cars, i + 1):
            perms = 0
            # print("undelivered: " + str(state.get_num_undelivered()) + ", i: " + str(i))
            # for packs_perm in permutations(state.get_num_undelivered(), i + 1):
            for packs_perm in permutations_exclude(len(state.get_packages()), i + 1, state.get_packages()):
                # print(packs_perm)
                perms += 1
                # print("Permutation " + str(perms), flush=True)
                car_with_pack = [-1] * number_of_cars
                new_car_locs = copy.deepcopy(state.get_car_locs())
                new_packages = copy.deepcopy(state.get_packages())
                new_g = state.get_g()
                for j in range(0, i + 1):
                    car_with_pack[cars[j]] = packs_perm[j]
                    # update the values of the list state.get_car_locs() for the new state
                    new_car_locs[cars[j]].append(
                        State.world.get_package_dest(car_with_pack[cars[j]]))
                    # update the values of the list state.get_packages() for the new state
                    if car_with_pack[j] != -1:
                        new_packages[car_with_pack[j]] = True
                        new_g += State.world.get_edge_cost(
                            state.get_car_loc(cars[j]),
                            State.world.get_package_source(packs_perm[j]))
                        new_g += State.world.get_edge_cost(
                            State.world.get_package_source(packs_perm[j]),
                            State.world.get_package_dest(packs_perm[j]))
                        # new_state is added to list of successors
                new_state = State(new_car_locs, new_packages, new_g)
                # print("Appending state", flush=True)
                successors.append(new_state)
    return successors

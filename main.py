# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import random
import simpy

RANDOM_SEED = 11
NEW_CUSTOMERS = 5  # Total number of customers
INTERVAL_CUSTOMERS = 10.0  # Generate new customers roughly every x seconds
SERVICE_TIME = 5.0  # This is mean service time for customers at counter
MIN_PATIENCE = 1  # Min. customer patience
MAX_PATIENCE = 3  # Max. customer patience


def customer_creator_process(env, number, interval, counter):
    """Generates customers' arrivals randomly.
       Inter-arrival times are exponentially distributed with given mean interval
    """
    print(' time     name       message')
    for i in range(number):
        c = customer(env, f'Customer_{i:02d}', counter)
        env.process(c)
        t = random.expovariate(1.0 / interval)
        yield env.timeout(t)


def customer(env, name, counter):
    """Customer arrives, is served and leaves."""
    arrive = env.now
    print(f'{arrive:7.4f} {name}: Arrived')

    with counter.request() as req:
        patience = random.uniform(MIN_PATIENCE, MAX_PATIENCE)  # random patience time from uniform distribution
        # Wait for the teller or abort once customers patience runs out.
        results = yield req | env.timeout(patience)  # this will yield either req or timeout -- the first one to occur

        wait = env.now - arrive

        if req in results:
            # We got to the counter
            print(f'{env.now:7.4f} {name}: Waited in line: {wait:6.3f}')

            tac = random.expovariate(1.0 / SERVICE_TIME)
            yield env.timeout(tac)
            print(f'{env.now:7.4f} {name}: Service time: {tac}')

        else:
            # We reneged
            print(f'{env.now:7.4f} {name}: Ran out of patience after after {wait:6.3f}')


# Setup and start the simulation
print('Bank Renege')
random.seed(RANDOM_SEED)
env = simpy.Environment()

# Start processes and run
counter = simpy.Resource(env, capacity=1)
env.process(customer_creator_process(env, NEW_CUSTOMERS, INTERVAL_CUSTOMERS, counter))
env.run()

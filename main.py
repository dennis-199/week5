"""
Based on 'Bank Renege' example from SimPy docs.

Scenario:
  A teller with a random service time and customers who run out of patience after a while

"""
import random

import simpy

RANDOM_SEED = 11
NEW_CUSTOMERS = 5  # Total number of customers
INTERVAL_CUSTOMERS = 10.0  # Generate new customers roughly every x seconds
SERVICE_TIME = 5.0  # This is mean service time for customers at counter
MIN_PATIENCE = 9999999  # Set minimum patience time to effectively infinite
MAX_PATIENCE = 99999999  # Set maximum patience time to effectively infinite

IA_iterator = iter([0.4, 0.3, 0.4, 1.7, 1.7, 0.5, 0.9])
service_iterator = iter([1.6, 0.5, 1.0, 0.3, 0.8, 0.4, 1.2])

def customer_creator_process(env, counter):
    """Generates customers' arrivals according to the hardwired inter-arrival times sequence."""
    print('Time\tCustomer\tMessage')
    i = 0
    while True:
        c = customer(env, f'Customer_{i:02d}', counter)
        env.process(c)
        t = next(IA_iterator, None)
        if t is None:
            break
        yield env.timeout(t)
        i += 1

def customer(env, name, counter):
    """Customer arrives, is served and leaves."""
    arrive = env.now
    print(f'{arrive:.2f}\t{name}\tArrived')

    with counter.request() as req:
        # Wait for the teller
        yield req
        wait = env.now - arrive

        # Start service
        service_time = next(service_iterator, None)
        if service_time is None:
            return
        yield env.timeout(service_time)
        print(f'{env.now:.2f}\t{name}\tDeparted\tTotal wait time: {wait:.2f}')

# Setup and start the simulation
print('Bank Simulation')
env = simpy.Environment()
counter = simpy.Resource(env, capacity=1)
env.process(customer_creator_process(env, counter))

# Run the simulation until no more customers
env.run(until=None)
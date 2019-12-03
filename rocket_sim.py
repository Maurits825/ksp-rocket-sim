import math
import matplotlib.pyplot as plt

mass_at_launch = 4.6 * 1000  # float(thingy.d)
mass_after_burn = 2.6 * 1000  # float(thingy.e)
burn_time = 29  # int(thingy.f)
start_thrust = 167.79 * 1000  # float(thingy.h)
end_thrust = 245 * 1000  # float(thingy.j)

diameter = 1.3
rocket_radius = diameter / 2

fuel_mass = mass_at_launch - mass_after_burn  # weight of fuel
mass_loss = fuel_mass / burn_time  # mass loss rate

mass_at_time = []
time_Interval = []
effects_gravity = []
rocket_velocity = []
resultant_force_list = []
rocket_acceleration = []
drag_at_time = []
air_density = []
pos_y_list = []

dt = 0.2
drag_coeff = 0.75

#Air density constants
sea_level_pressure = 101325  # sea level standard atmospheric pressure measured in Pa
sea_level_temp = 288.15  # sea level standard temp measure in K
grav_accel = 9.8  # earth surface gravitaional accel measured in m/s
temp_lapse_rate = 0.0065  # measure in K/m
gas_constant = 8.31447  # ideal universal gas constant measured in J/(mol K)
molar_mass_air = 0.0289654  # molar mass of dry air measured in kg/mol
cross_section = math.pi * rocket_radius**2
iterations = int((5 * (burn_time / dt)) + 1)

planet_gravity = 9.8  # TODO param

def get_air_density(current_height):
    temp_at_alt = sea_level_temp - temp_lapse_rate*current_height #calcs temp at altitude
    pressure_at_alt = sea_level_pressure*(1 - (temp_lapse_rate*current_height)/sea_level_temp)**((grav_accel*molar_mass_air)/(gas_constant*temp_lapse_rate)) #calcs pressure at altitude
    return (pressure_at_alt*molar_mass_air) / (gas_constant*temp_at_alt)


def calcMassAtTime(planet_grav): ##mass of rocket at any time t. Requires burn time, mass before launch, and loss of mass rate
    for t in range(0, iterations):
        if t >= (burn_time / dt):
            mass_at_time.append(mass_after_burn)
        else:
            mass_at_time.append(mass_at_launch - mass_loss * (t * dt)) #mass as a function of time

        effects_gravity.append(planet_grav*mass_at_time[t]) #part of net force calculation - (W)

        planet_grav * mass_at_launch - mass_loss * (t * dt)


def velocity_of_rocket():
    pos_y = 0
    velocity = 0
    #pos_y_list.append(pos_y) why ignore?
    mass = mass_at_launch

    for t in range(0, iterations):
        if t == 243:
            print("break")

        if t >= (burn_time / dt):
            average_thrust = 0
        else:
            average_thrust = (start_thrust + end_thrust) / 2

        drag_force = 0.5 * get_air_density(pos_y) * cross_section * velocity
        resultant_force = average_thrust - ((mass * planet_gravity) + drag_force)

        accel = resultant_force / mass

        new_velocity = velocity + (accel * dt)
        new_pos_y = pos_y + (new_velocity * dt)

        velocity = new_velocity
        pos_y = new_pos_y
        pos_y_list.append(pos_y)

        if t >= (burn_time / dt):
            mass = mass_after_burn
        else:
            mass = mass - (mass_loss * dt)



def earth(): ##calculation for earth
    planet_grav = 9.8 #planets gravity
    calcMassAtTime(planet_grav)
    velocity_of_rocket()
    #print(rocket_acceleration, "\n")
    #print(rocket_velocity)
    print(pos_y_list)  # TODO fix!
    print("done")
    plt.plot(range(0, iterations), pos_y_list)
    plt.show()


def Kerbin():
    planet_grav = 9.8 #analogus to earth
    calcMassAtTime(planet_grav)

earth()
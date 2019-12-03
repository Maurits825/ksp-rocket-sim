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

pos_y_list = []

dt = 1/100
drag_coeff = 0.75

# Air density constants
sea_level_pressure = 101325  # sea level standard atmospheric pressure measured in Pa
sea_level_temp = 288.15  # sea level standard temp measure in K
grav_accel = 9.8  # earth surface gravitaional accel measured in m/s
temp_lapse_rate = 0.0065  # measure in K/m
gas_constant = 8.31447  # ideal universal gas constant measured in J/(mol K)
molar_mass_air = 0.0289654  # molar mass of dry air measured in kg/mol
cross_section = math.pi * rocket_radius**2
iterations = int((5 * (burn_time / dt)) + 1)

planet_gravity = 9.8  # TODO param

# dump


def get_air_density_old(current_height):
    temp_at_alt = sea_level_temp - temp_lapse_rate*current_height  # calcs temp at altitude
    pressure_at_alt = sea_level_pressure*(1 - (temp_lapse_rate*current_height)/sea_level_temp)**((grav_accel*molar_mass_air)/(gas_constant*temp_lapse_rate)) #calcs pressure at altitude
    return (pressure_at_alt*molar_mass_air) / (gas_constant*temp_at_alt)


def get_air_density_new(current_height):
    if current_height < 2500:
        return 1.225
    elif current_height < 5000:
        return 0.898
    elif current_height < 7500:
        return 0.642
    elif current_height < 10000:
        return 0.446
    elif current_height < 15000:
        return 0.288
    elif current_height < 20000:
        return 0.108
    elif current_height < 25000:
        return 0.040
    elif current_height < 30000:
        return 0.015
    elif current_height < 40000:
        return 0.006
    elif current_height < 50000:
        return 0.001
    else:
        return 0


# TODO turn to class at some point?
def velocity_of_rocket():
    pos_y = 0
    velocity = 0
    pos_y_list.append(pos_y)
    mass = mass_at_launch
    average_thrust = (start_thrust + end_thrust) / 2

    for t in range(0, iterations):
        if t == 243:
            print("break")

        drag_force = 0.5 * get_air_density_old(pos_y) * velocity**2 * drag_coeff * cross_section
        resultant_force = average_thrust - ((mass * planet_gravity) + drag_force)

        accel = resultant_force / mass

        velocity = velocity + (accel * dt)
        pos_y = pos_y + (velocity * dt)

        pos_y_list.append(pos_y)

        if t >= (burn_time / dt):
            average_thrust = 0
            mass = mass_after_burn
        else:
            average_thrust = (start_thrust + end_thrust) / 2
            mass = mass - (mass_loss * dt)


def earth():  # calculation for earth
    velocity_of_rocket()
    print(pos_y_list)  # TODO fix! global var
    print("done")
    plt.plot(range(0, iterations + 1), pos_y_list)
    plt.show()


earth()

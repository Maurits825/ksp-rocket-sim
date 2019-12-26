import math
import matplotlib.pyplot as plt
import numpy as np

mass_at_launch = 6.6 * 1000
mass_after_burn = 2.6 * 1000
burn_time = 51
asl_thrust = 205.52 * 1000
vac_thrust = 240 * 1000
launch_pad_y = 75

diameter = 1.3
rocket_radius = diameter / 2

fuel_mass = mass_at_launch - mass_after_burn  # weight of fuel
mass_loss = fuel_mass / burn_time  # mass loss rate

pos_y_list = []
drag_force_list = []
accel_list = []
velocity_list = []
mass_list = []
thrust_list = []
gravity_list = []
reynold_list = []

dt = 1/100
drag_coeff = 0.08

# Air density constants
sea_level_pressure = 101325  # sea level standard atmospheric pressure measured in Pa
sea_level_temp = 288.15  # sea level standard temp measure in K
grav_accel = 9.8  # earth surface gravitational accel measured in m/s
temp_lapse_rate = 0.0065  # measure in K/m
gas_constant = 8.31447  # ideal universal gas constant measured in J/(mol K)
molar_mass_air = 0.0289654  # molar mass of dry air measured in kg/mol
cross_section = math.pi * rocket_radius**2
iterations = int((15 * (burn_time / dt)) + 1)
kerbin_atm_cutoff = 44000
vaccum_h = 70000

gravity_constant = 6.67430 * 10**(-11)
kerbin_mass = 5.2915158 * 10**22
kerbin_radius = 600000
kerbin_thrust_curve = -0.16


def get_air_density(current_height):
    if current_height < kerbin_atm_cutoff:
        temp_at_alt = sea_level_temp - temp_lapse_rate*current_height
        pressure_at_alt = sea_level_pressure*(1 - (temp_lapse_rate*current_height)/sea_level_temp)**((grav_accel*molar_mass_air)/(gas_constant*temp_lapse_rate))
        return (pressure_at_alt*molar_mass_air) / (gas_constant*temp_at_alt)
    else:
        return 0


def get_thrust(asl_t, vac_t, h):
    a = (asl_t - vac_t) / 1000
    b = kerbin_thrust_curve
    ret = (a * math.e**(b * (h / 1000)) + (vac_t / 1000)) * 1000
    return ret


def get_reynold(density, velocity):
    air_vis = 18.5 * 10**(-6)
    return (density * velocity * diameter) / air_vis


# TODO turn to class at some point?
def velocity_of_rocket():
    pos_y = launch_pad_y
    velocity = 0
    mass = mass_at_launch
    thrust = get_thrust(asl_thrust, vac_thrust, pos_y)

    pos_y_list.append(pos_y)
    drag_force_list.append(0)
    velocity_list.append(velocity)
    mass_list.append(mass)
    thrust_list.append(thrust)
    reynold_list.append(get_reynold(get_air_density(pos_y), velocity))

    for i in range(iterations):
        drag_force = 0.5 * get_air_density(pos_y) * velocity**2 * drag_coeff * cross_section
        force_gravity = gravity_constant * ((mass * kerbin_mass) / (pos_y + kerbin_radius)**2)

        if velocity >= 0:
            resultant_force = thrust - (force_gravity + drag_force)
        else:
            resultant_force = drag_force - force_gravity

        accel = resultant_force / mass

        velocity = velocity + (accel * dt)
        pos_y = pos_y + (velocity * dt)

        if i >= (burn_time / dt):
            thrust = 0
            mass = mass_after_burn
        else:
            thrust = get_thrust(asl_thrust, vac_thrust, pos_y)
            mass = mass - (mass_loss * dt)

        pos_y_list.append(pos_y)
        drag_force_list.append(drag_force)
        accel_list.append(accel)
        velocity_list.append(velocity)
        mass_list.append(mass)
        thrust_list.append(thrust)
        gravity_list.append(force_gravity)
        reynold_list.append(get_reynold(get_air_density(pos_y), velocity))


def sub_plot():
    time = np.asarray(range(iterations)) * dt
    time_1 = np.asarray(range(iterations + 1)) * dt

    plt.subplot(2, 3, 1)
    plt.plot(time_1, pos_y_list)
    print(max(pos_y_list))
    plt.title('Height')

    plt.subplot(2, 3, 2)
    plt.plot(time, accel_list)
    plt.title('Acceleration')

    plt.subplot(2, 3, 3)
    plt.plot(time_1, velocity_list)
    plt.title('Velocity')

    plt.subplot(2, 3, 4)
    plt.plot(time_1, drag_force_list)
    plt.title('Drag')

    plt.subplot(2, 3, 5)
    #plt.plot(time, gravity_list)
    print(min(gravity_list))
    #plt.title('Gravity')

    plt.plot(time_1, reynold_list)
    plt.title('Reynold')

    plt.subplot(2, 3, 6)
    burn_ind = int(burn_time / dt)
    plt.plot(time_1[0:burn_ind], thrust_list[0:burn_ind])
    plt.title('Thrust')

    plt.show()


def earth():  # calculation for earth
    velocity_of_rocket()
    #print(pos_y_list)  # TODO fix! global var?
    #plt.plot(range(iterations + 1), pos_y_list)
    #plt.plot(range(iterations), accel_list)
    #plt.plot(range(iterations + 1), velocity_list)
    #plt.plot(range(iterations + 1), drag_force_list)
    #plt.plot(range(iterations + 1), mass_list)
    #plt.show()
    sub_plot()


earth()

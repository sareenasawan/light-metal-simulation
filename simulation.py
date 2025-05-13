'''
Filename:       simulation.py
Author:         Sareena Awan
Date Created:   February 19, 2025
Date Modified:  May 12, 2025
Description:    A simple simulation to study surface interactions of metals with visible light at normal or oblique incidence
'''

#References:
'''
    [1] P. B. Johnson and R. W. Christy, "Optical Constants of the Noble Metals", Phys. Rev. B, 1972.
    [2] E. D. Palik, "Handbook of Optical Constants of Solids", Academic Press, 1985.
    [3] E. Hecht, "Optics", 5th ed., Addison-Wesley, 2016.
'''

import numpy as np
import matplotlib.pyplot as plt

#Constants
c= 3e8 #m/s
PI= np.pi

#Drude model parameters for some common metals (in SI units)
#Format: {metal_name: {"omega_p": plasma_frequency, "gamma": damping_rate, "epsilon_inf": high_freq_dielectric_constant}}
preset_metals= {
    "gold":     {"omega_p": 1.37e16, "gamma": 1.05e14, "epsilon_inf": 9.84},
    "silver":   {"omega_p": 1.38e16, "gamma": 2.73e13, "epsilon_inf": 3.7},
    "copper":   {"omega_p": 1.32e16, "gamma": 1.22e14, "epsilon_inf": 10.8},
    "aluminum": {"omega_p": 2.24e16, "gamma": 1.21e14, "epsilon_inf": 1.0},
    "nickel":   {"omega_p": 1.83e16, "gamma": 1.58e15, "epsilon_inf": 1.0}
}
    
#Defining functions
def dielectric_function(omega, omega_p, gamma, epsilon_inf):
    '''
    dielectric_function(): computes the dielectric function for a given metal
    
    Arguments: 
        omega: angular frequency of light/electromagnetic wave
        omega_p: plasma frequency of metal
        gamma: damping rate of metal
        epsilon_inf: high-frequency dielectric constant
        
    Output:
        complex dielectric function of the metal using the Drude Model
    
    '''
    
    return epsilon_inf - (omega_p**2)/(omega**2 + 1j*gamma*omega)


def wavelength_to_omega(lambda_input):
    '''
    wavelength_to_omega(): converts given wavelength of light to angular frequency, omega
    
    Argument:
        lambda_input: wavelength of light in nm
        
    Output:
        angular frequency
    '''
    lambda_input= lambda_input*1e-9
    return 2*PI*c/lambda_input

def fresnel_coefficients(complex_dielectric_function, theta_i= 0, dielectric_constant=1.0):  #theta is in degrees
    
    '''
    Calculates the fresnel coefficients
    '''
    
    theta_i= np.radians(theta_i)
    n1= np.sqrt(dielectric_constant)
    n2= np.sqrt(complex_dielectric_function)
    
    #Snell's law
    sin_theta_t= n1 * np.sin(theta_i) / n2
    cos_theta_t= np.sqrt(1 - sin_theta_t**2)
    cos_theta_i= np.cos(theta_i)

    r_s= ((n1 * cos_theta_i) - (n2 * cos_theta_t)) / ((n1 * cos_theta_i) + (n2 * cos_theta_t))
    r_p= ((n1 * cos_theta_t) - (n2 * cos_theta_i))/ (n2 * cos_theta_i + n1 * cos_theta_t)

    R_s= np.abs(r_s)**2
    R_p= np.abs(r_p)**2

    return R_s, R_p


#Simulation function/ user interface
def metal_info():
    while(True):
        print("Select a metal from the list below: ")
        print(" 1: Gold")
        print(" 2: Silver")
        print(" 3: Copper")
        print(" 4: Aluminum")
        print(" 5: Nickel")
        print(" 6: Custom metal")
    
        try:
            choice= int(input())
            if choice < 1 or choice > 6:
                print("Invalid choice. Please select a number between 1 and 6.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a valid integer between 1 and 6.")
            continue
    
    
    if choice== 6:
        metal_name= input("Enter the name of the metal: ")
        try:
            omega_p= float(input("Enter the plasma frequency in rad/s: "))
            gamma= float(input("Enter the damping rate in rad/s: "))
            epsilon_inf= float(input("Enter the high-frequency dielectric constant (epsilon inf): "))
        except ValueError:
            print("Invalid input. Please enter numerical values for plasma frequency, damping rate, and epsilon_inf.")
            return metal_info()
    else:
        metals= ["gold", "silver", "copper", "aluminum", "nickel"]
        metal_name= metals[choice - 1]
        omega_p= preset_metals[metal_name]["omega_p"]
        gamma= preset_metals[metal_name]["gamma"]
        epsilon_inf= preset_metals[metal_name]["epsilon_inf"]
        
    print(f"\nUsing {metal_name.capitalize()} with properties: Plasma Frequency = {omega_p} rad/s, Damping Rate = {gamma} rad/s, Epsilon(infinity) = {epsilon_inf}")
    
    return metal_name, omega_p, gamma, epsilon_inf



def plot_reflection_vs_angle(metal_name, omega_p, gamma, epsilon_inf, wavelength_nm, angle_range=(0, 90)):
    
    omega= wavelength_to_omega(wavelength_nm)
    epsilon= dielectric_function(omega, omega_p, gamma, epsilon_inf)
    angles= np.linspace(angle_range[0], angle_range[1], 1000)
    
    R_s_values= []
    R_p_values= []
    
    for angle in angles:
        R_s, R_p= fresnel_coefficients(epsilon, theta_i=angle)
        R_s_values.append(R_s)
        R_p_values.append(R_p)
        
    plt.figure(figsize=(10, 6))
    plt.plot(angles, R_s_values, label='R_s (s-polarized)', color='b', linestyle='-', linewidth=2)
    plt.plot(angles, R_p_values, label='R_p (p-polarized)', color='r', linestyle='--', linewidth=2)
    plt.xlabel('Incident Angle (degrees)')
    plt.ylabel('Reflection Coefficient (R)')
    plt.title(f'Reflection vs Incident Angle for {metal_name.capitalize()} at {wavelength_nm} nm')
    plt.legend()
    plt.grid()
    plt.show()
        
#Main Program

def main():
    print("Welcome to the Light-Metal Interaction Simulation!\n")
    
    metal_name, omega_p, gamma, epsilon_inf= metal_info()
    
    while True:
        try:
            wavelength_nm= float(input("Enter the wavelength of light in nm: "))
            if wavelength_nm <= 0:
                print("Wavelength must be a positive value. Please try again.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a valid number for the wavelength.")
    
    plot_reflection_vs_angle(metal_name, omega_p, gamma, epsilon_inf, wavelength_nm)

main()
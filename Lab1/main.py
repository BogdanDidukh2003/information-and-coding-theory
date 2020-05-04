from scipy.integrate import quad as integrate
from math import ceil, floor, sin, pi
import matplotlib.pyplot as plt
import numpy as np
from libs.basic_units import radians


def draw_plot(x_arguments, y_values, title="", x_label="", y_label="", figsize=None,
              is_grid=True, vlines=False, xticks=False, in_radians=False):
    plot = plt.figure(figsize=figsize).gca()

    if not vlines:
        plot.plot(x_arguments, y_values)
    else:
        if in_radians:
            plot.plot(x_arguments, list(map(lambda y: y * radians, y_values)), marker='.')
        else:
            plot.plot(x_arguments, y_values, marker='.')
        plot.vlines(x_arguments, 0, y_values)

    if xticks:
        plt.xticks(x_arguments)

    plot.set_title(title)
    plot.set_xlabel(x_label)
    plot.set_ylabel(y_label)
    plt.grid(b=is_grid)
    plt.show()


def input_signal_function(t, t_i, amplitude, period):
    period_time_point = abs(t) - (ceil(abs(t) / period) - 1) * period

    if period_time_point < (t_i / 4):
        value = 4 * amplitude * period_time_point / t_i
    elif period_time_point < (t_i / 2):
        value = amplitude - (4 * amplitude * (period_time_point - t_i / 4) / t_i)
    elif period_time_point > (period - t_i / 4):
        value = (4 * amplitude * (period_time_point - period + t_i / 4) / t_i) - amplitude
    elif period_time_point > (period - t_i / 2):
        value = -1 * (4 * amplitude * (period_time_point - period + t_i / 2) / t_i)
    else:
        value = 0

    if t < 0:
        return value * -1
    return value


def plot_input_signal(input_signal, start, end, step=0.01, title='Input Signal'):
    time_points = []
    values = []

    while start < end:
        time_points.append(start)
        values.append(input_signal(start))
        start += step

    draw_plot(time_points, values, title, 't', 's(t)', figsize=(8, 2))


def main():
    period = 40 * 10 ** -3
    t_i = period / 8
    amplitude = 4
    delta_frequency = 280
    number_of_harmonics = 20

    omega = 2 * pi / period
    print(f'ω = {omega}')
    f1 = 1 / period
    print(f'f1 = {f1}')

    original_input_signal = lambda t: input_signal_function(t, t_i, amplitude, period)

    plot_input_signal(input_signal=original_input_signal, start=-0.08, end=0.08, step=0.0001,
                      title='Original Input Signal')

    def find_coefficient_b(k):
        return 4 / period * integrate(
            lambda t, k: input_signal_function(t, t_i, amplitude, period) * sin(omega * k * t),
            0, period / 2, args=(k,))[0]

    coefficients_b = [find_coefficient_b(k + 1) for k in range(number_of_harmonics)]

    calculated_input_signal = lambda t: sum(
        [coefficients_b[k] * sin((k + 1) * omega * t) for k in range(number_of_harmonics)]
    )

    print('\n\tCoefficients:')
    for k in range(len(coefficients_b)):
        print('b%d = %.3f' % (k + 1, coefficients_b[k]))

    plot_input_signal(input_signal=calculated_input_signal, start=-0.08, end=0.08, step=0.0001,
                      title='Calculated Input Signal')

    psi = [(pi / 2) if coefficients_b[k] >= 0 else (- pi / 2) for k in range(number_of_harmonics)]
    print('\n\tψ(t) values:')
    for k in range(len(psi)):
        print('ψ%d = %.3f' % (k + 1, psi[k]))

    draw_plot(list(np.arange(number_of_harmonics + 1)), [0] + [abs(b) for b in coefficients_b],
              title='Amplitude Spectre', x_label='k', y_label='A, v', vlines=True, xticks=True)
    draw_plot(list(np.arange(1, number_of_harmonics + 1)), psi,
              title='Phase Frequency Spectre', x_label='k', y_label='ψ, rad', vlines=True, xticks=True, in_radians=True)

    print('\n\tCalculations')
    harmonics_quantity = min(floor(delta_frequency / f1), number_of_harmonics)
    print('Harmonics quantity n = %d' % harmonics_quantity)
    signal_power = 0.5 * sum([coefficients_b[i] ** 2 for i in range(harmonics_quantity)])
    print('Power of signal P = %.3f' % signal_power)
    full_average_signal_power = 1 / period * integrate(lambda t: calculated_input_signal(t) ** 2, 0, period)[0]
    print('Full average power of signal S^2 = %.3f' % full_average_signal_power)
    absolute_error = abs(full_average_signal_power - signal_power)
    print('Absolute error Δ = %.3f' % absolute_error)
    relative_error = absolute_error / full_average_signal_power * 100
    print('Relative error δ = %.3f' % relative_error, '%')


if __name__ == '__main__':
    main()

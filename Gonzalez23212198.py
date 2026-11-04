"""
Practica 3: Sistema Musculoesqueletico

Departamento de Ingenieria Electrica y Electronica
Ingenieria Biomedica
Tecnologico Nacional de Mexico [TecNM - Tijuana]

Nombre: Gonzalez Holguin Martin Alonso
Numero de control: 23212198
Correo: l23212181@tectijuana.edu.mx

Asignatura: Modelado de Sistemas Fisiologicos
Docente: Dr. Paul Antonio Valle Trujillo
"""


import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

F0 = 1.0
alpha = 0.25

Cg = 10e-6
Cp = 100e-6

R_control = 100
R_caso = 10e3

Kp = 0.0214581683425368
Ki = 42291.2654382088

t = np.arange(0, 10.001, 1e-3)

F = np.zeros_like(t)
F[(t >= 1) & (t < 2)] = F0

def transferencia(R):
    num = [R * 1e-6, 1 - alpha]
    den = [R * (Cp + Cg), 1]
    return signal.TransferFunction(num, den)

def respuesta(sys, entrada, t):
    _, y, _ = signal.lsim(sys, U=entrada, T=t)
    return y

G_control = transferencia(R_control)
Fs_control = respuesta(G_control, F, t)

G_caso = transferencia(R_caso)
Fs_caso = respuesta(G_caso, F, t)

num_G = [R_caso * 1e-6, 1 - alpha]
den_G = [R_caso * (Cp + Cg), 1]

num_PI = [Kp, Ki]
den_PI = [1, 0]

num_L = np.polymul(num_PI, num_G)
den_L = np.polymul(den_PI, den_G)

num_T = num_L
den_T = np.polyadd(den_L, num_L)

T_cerrado = signal.TransferFunction(num_T, den_T)

PI_caso = respuesta(T_cerrado, Fs_control, t)

plt.rcParams['font.family'] = 'serif'
plt.rcParams['mathtext.fontset'] = 'cm'

fig, ax = plt.subplots(
    figsize=(11, 4.5),
    facecolor='white'
)

ax.plot(
    t, F, '-',
    color='#FFC800',
    linewidth=1.5,
    label=r'$F(t)$'
)

ax.plot(
    t, Fs_control, '--',
    color='#1B2CC1',
    linewidth=2.5,
    label=r'$Fs(t):\ Control$'
)

ax.plot(
    t, Fs_caso, '-',
    color='#FF8C00',
    linewidth=1.8,
    label=r'$Fs(t):\ Caso$'
)

ax.plot(
    t, PI_caso, '-',
    color='#FF69B4',
    linewidth=2,
    label=r'$PI(t):\ Tratamiento$'
)

ax.set_xlim(0, 10)
ax.set_ylim(-0.1, 1.1)

ax.set_xticks(np.arange(0, 11, 1))
ax.set_yticks(np.arange(-0.1, 1.11, 0.1))

ax.set_xlabel(r'$t\ [s]$')
ax.set_ylabel(r'$F(t)\ [V]$')

legend = ax.legend(
    loc='lower center',
    bbox_to_anchor=(0.5, 1.06),
    ncol=4,
    frameon=True,
    fancybox=False,
    edgecolor='black',
    fontsize=9,
    title='Control y caso input'
)

legend.get_title().set_fontsize(9)

ax.tick_params(direction='in', top=True, right=True)

for spine in ax.spines.values():
    spine.set_linewidth(1)

ax.grid(False)

plt.tight_layout()

plt.savefig(
    'Sistema_Musculoesqueletico_final.pdf',
    format='pdf',
    bbox_inches='tight'
)

plt.show()

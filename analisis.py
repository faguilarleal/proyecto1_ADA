import time
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from Reader import Reader
from MT import MT

# Función para medir el tiempo de ejecución
def MeasureExecutionTime(input_string, turing_machine):
    """
    Mide el tiempo que toma ejecutar una cadena de entrada en la máquina de Turing.
    
    """
    turing_machine.initializeTape(input_string)
    
    start_time = time.time()
    turing_machine.simulateMT()
    end_time = time.time()
    
    return end_time - start_time

# Funciones de regresión
def LinearFunc(x, a, b):
    """Modelo de regresión lineal: f(x) = ax + b"""
    return a * x + b

def QuadraticFunc(x, a, b, c):
    """Modelo de regresión cuadrática: f(x) = ax^2 + bx + c"""
    return a * x**2 + b * x + c

def ExpFunc(x, a, b, c):
    """Modelo de regresión exponencial: f(x) = ae^(bx) + c"""
    return a * np.exp(b * x) + c

def GenerateTestInputs(count, pattern="|"):
    """
    Genera entradas de prueba con longitudes incrementales.

    """
    return [pattern * i for i in range(1, count + 1)]

def CalculateMSE(actual, predicted):
    """Calcula el error cuadrático medio entre valores reales y predichos"""
    return np.mean((np.array(actual) - np.array(predicted))**2)

def PerformRegression(input_sizes, execution_times):
    """
    Realiza análisis de regresión con diferentes modelos.
    """
    try:
        # Convertir a arrays para cálculos
        x = np.array(input_sizes)
        y = np.array(execution_times)
        
        # Regresión lineal
        popt_linear, _ = curve_fit(LinearFunc, x, y)
        y_linear = LinearFunc(x, *popt_linear)
        mse_linear = CalculateMSE(y, y_linear)
        
        # Regresión cuadrática
        popt_quadratic, _ = curve_fit(QuadraticFunc, x, y)
        y_quadratic = QuadraticFunc(x, *popt_quadratic)
        mse_quadratic = CalculateMSE(y, y_quadratic)
        
        # Regresión exponencial
        popt_exp, _ = curve_fit(ExpFunc, x, y, bounds=([0, 0, -np.inf], [np.inf, 1, np.inf]))
        y_exp = ExpFunc(x, *popt_exp)
        mse_exp = CalculateMSE(y, y_exp)
        
        # Determinar el mejor modelo
        mse_values = {
            "Lineal": mse_linear,
            "Cuadrático": mse_quadratic,
            "Exponencial": mse_exp
        }
        best_model = min(mse_values, key=mse_values.get)
        
        return {
            "linear": (popt_linear, mse_linear),
            "quadratic": (popt_quadratic, mse_quadratic),
            "exponential": (popt_exp, mse_exp),
            "best_model": best_model,
            "mse_values": mse_values
        }
        
    except Exception as e:
        print(f"Error en el ajuste de curva: {e}")
        return None

def PlotResults(input_sizes, execution_times, regression_results):
    """
    Genera visualizaciones de los resultados.
    """
    plt.figure(figsize=(10, 6))
    plt.scatter(input_sizes, execution_times, color='blue', label='Datos medidos')
    plt.xlabel('Tamaño de entrada (número de palitos)')
    plt.ylabel('Tiempo de ejecución (segundos)')
    plt.title('Tiempo de ejecución vs Tamaño de entrada')
    plt.grid(True)
    
    if regression_results:
        x_range = np.linspace(min(input_sizes), max(input_sizes), 100)
        
        # Extraer parámetros
        popt_linear, mse_linear = regression_results["linear"]
        popt_quadratic, mse_quadratic = regression_results["quadratic"]
        popt_exp, mse_exp = regression_results["exponential"]
        
        # Graficar modelos
        plt.plot(x_range, LinearFunc(x_range, *popt_linear), 'r-', 
                 label=f'Lineal: {popt_linear[0]:.6f}x + {popt_linear[1]:.6f} (ECM: {mse_linear:.6f})')
        
        plt.plot(x_range, QuadraticFunc(x_range, *popt_quadratic), 'g-', 
                 label=f'Cuadrático: {popt_quadratic[0]:.6f}x² + {popt_quadratic[1]:.6f}x + {popt_quadratic[2]:.6f} (ECM: {mse_quadratic:.6f})')
        
        plt.plot(x_range, ExpFunc(x_range, *popt_exp), 'm-', 
                 label=f'Exponencial: {popt_exp[0]:.6f}e^({popt_exp[1]:.6f}x) + {popt_exp[2]:.6f} (ECM: {mse_exp:.6f})')
    
    plt.legend()
    plt.savefig('analisis_empirico.png')
    print("\nGráfica guardada como 'analisis_empirico.png'")

def GenerateReport(inputs, input_sizes, execution_times, regression_results):
    """
    Genera un informe de texto con los resultados del análisis.

    """
    with open('informe_analisis_empirico.txt', 'w') as f:
        f.write("===== ANÁLISIS EMPÍRICO DE LA MÁQUINA DE TURING PARA FIBONACCI =====\n\n")
        f.write("a) Listado de entradas de prueba usadas para medir tiempos de ejecución:\n")
        for i, input_str in enumerate(inputs):
            f.write(f"   {i+1}. '{input_str}' (tamaño: {len(input_str)})\n")
        
        f.write("\nb) Los resultados de tiempos medidos son:\n")
        f.write("Entrada | Tamaño | Tiempo (segundos)\n")
        f.write("--------------------------------\n")
        for i in range(len(inputs)):
            f.write(f"{inputs[i]} | {input_sizes[i]} | {execution_times[i]:.6f}\n")
        
        f.write("\nc) Regresión que mejor se ajusta a los datos:\n")
        
        if regression_results:
            best_model = regression_results["best_model"]
            f.write(f"El mejor modelo es: {best_model}\n")
            
            if best_model == "Lineal":
                popt_linear = regression_results["linear"][0]
                f.write(f"Función: {popt_linear[0]:.6f}x + {popt_linear[1]:.6f}\n")
                f.write(f"Esto sugiere una complejidad temporal de O(n)\n")
                
            elif best_model == "Cuadrático":
                popt_quadratic = regression_results["quadratic"][0]
                f.write(f"Función: {popt_quadratic[0]:.6f}x² + {popt_quadratic[1]:.6f}x + {popt_quadratic[2]:.6f}\n")
                f.write(f"Esto sugiere una complejidad temporal de O(n²)\n")
                
            else:  # Exponencial
                popt_exp = regression_results["exponential"][0]
                f.write(f"Función: {popt_exp[0]:.6f}e^({popt_exp[1]:.6f}x) + {popt_exp[2]:.6f}\n")
                f.write(f"Esto sugiere una complejidad temporal exponencial O(c^n)\n")
        else:
            f.write("No se pudo determinar el mejor modelo debido a un error en el ajuste.\n")
            
        f.write("\nNota: La complejidad teórica del cálculo de Fibonacci en una Máquina de Turing\n")
        f.write("suele ser exponencial debido a la naturaleza del problema y las limitaciones\n")
        f.write("de una máquina de una sola cinta.\n")
    
    print("Informe guardado como 'informe_analisis_empirico.txt'")

def PrintResults(inputs, input_sizes, execution_times, regression_results):
    """
    Muestra los resultados de la regresión en la consola con formato mejorado.
    """
    print("\n" + "="*50)
    print(" "*15 + "ANÁLISIS EMPÍRICO")
    print("="*50)
    
    # Crear encabezado con formato
    print(f"{'Entrada':<15} | {'Tamaño':<10} | {'Tiempo (segundos)':<18}")
    print("-"*50)
    
    # Imprimir datos en formato tabular
    for i, input_str in enumerate(inputs):
        print(f"{input_str:<15} | {input_sizes[i]:<10} | {execution_times[i]:<18.6f}")
    
    if regression_results:
        print("\n" + "="*50)
        print(" "*10 + "RESULTADOS DE REGRESIÓN")
        print("="*50)
        
        popt_linear, mse_linear = regression_results["linear"]
        print(f"• Función lineal:      {popt_linear[0]:.6f}x + {popt_linear[1]:.6f}")
        print(f"  ECM lineal:          {mse_linear:.6f}")
        
        popt_quadratic, mse_quadratic = regression_results["quadratic"]
        print(f"\n• Función cuadrática:  {popt_quadratic[0]:.6f}x² + {popt_quadratic[1]:.6f}x + {popt_quadratic[2]:.6f}")
        print(f"  ECM cuadrático:      {mse_quadratic:.6f}")
        
        popt_exp, mse_exp = regression_results["exponential"]
        print(f"\n• Función exponencial: {popt_exp[0]:.6f}e^({popt_exp[1]:.6f}x) + {popt_exp[2]:.6f}")
        print(f"  ECM exponencial:     {mse_exp:.6f}")
        
        best_model = regression_results["best_model"]
        mse_values = regression_results["mse_values"]
        print("\n" + "-"*50)
        print(f"✓ El mejor modelo es: {best_model} con ECM = {mse_values[best_model]:.6f}")
        print("-"*50)


def Analisis():
    """Función principal que coordina todo el análisis."""
    # Cargar la máquina de Turing
    reader = Reader("maquina.yml")
    mt = MT(reader.states, reader.initial_state, reader.final_state, 
            reader.alphabet, reader.tape_alphabet, reader.function)
    
    # Generar entradas de prueba
    inputs = GenerateTestInputs(10, "|")
    
    # Medir tiempos de ejecución
    input_sizes = []
    execution_times = []
    
    for input_str in inputs:
        size = len(input_str)
        time_taken = MeasureExecutionTime(input_str, mt)
        
        input_sizes.append(size)
        execution_times.append(time_taken)
    
    # Realizar análisis de regresión
    regression_results = PerformRegression(input_sizes, execution_times)
    PrintResults(inputs, input_sizes, execution_times, regression_results)
    PlotResults(input_sizes, execution_times, regression_results)
    GenerateReport(inputs, input_sizes, execution_times, regression_results)
    plt.show()


Analisis()
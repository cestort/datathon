## ------------------------------------------------------------------------------------------------
## Aplicación de transformaciones para conseguir distribución normal
## ------------------------------------------------------------------------------------------------

## Box-Cox. Conjunto de fórmulas que dependen de un parámetro (lambda) y que solo pueden aplicarse a datos estrictamente positivos (> 0).
## Yeo-Johnson. Variante de Box-Cox. Conjunto de fórmulas que dependen de un parámetro (lambda) y que pueden aplicarse a datos con valores nulos, positivos o negativos.

from scipy.stats import boxcox, yeojohnson, norm
import numpy as np
import matplotlib.pyplot as plt


def FitTransformColumn(column, method='boxcox'):
    
    """
    Ajusta y transforma una columna del conjunto de entrenamiento usando Box-Cox o Yeo-Johnson.
    También genera un gráfico comparando la distribución antes y después de la transformación.
    
    Parámetros:
    - column: Pandas Series o array con los datos de la columna (entrenamiento).
    - method: 'boxcox' o 'yeojohnson', método de transformación.
    
    Salida:
    - transformed: Columna transformada.
    - lambda_: Valor lambda encontrado durante la transformación.
    """
    
    ## Colores
    colors = ['#3498db', '#e74c3c']  ## Azul y rojo
    
    ## Check para Box-Cox
    if method == 'boxcox' and np.any(column <= 0):
        raise ValueError("Box-Cox requiere valores estrictamente positivos.")
    
    ## Aplicar transformación
    if method == 'boxcox':
        transformed, lambda_ = boxcox(column)
    elif method == 'yeojohnson':
        transformed, lambda_ = yeojohnson(column)
    else:
        raise ValueError("El método debe ser 'boxcox' o 'yeojohnson'.")

    ## Muestro comparación antes y después de la transformación
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    axes[0].hist(column, bins=30, color=colors[0], alpha=0.7, density=True)
    xmin, xmax = axes[0].get_xlim()
    x = np.linspace(xmin, xmax, 100)
    p = norm.pdf(x, np.mean(column), np.std(column))
    axes[0].plot(x, p, 'k-', linewidth=2, label='Densidad')  ## Densidad
    axes[0].set_title(f'Antes de {method.capitalize()}')
    axes[1].hist(transformed, bins=30, color=colors[1], alpha=0.7, density=True)
    xmin, xmax = axes[1].get_xlim()
    x = np.linspace(xmin, xmax, 100)
    p = norm.pdf(x, np.mean(transformed), np.std(transformed))
    axes[1].plot(x, p, 'k-', linewidth=2, label='Densidad')  ## Densidad
    axes[1].set_title(f'Después de {method.capitalize()}')
    plt.tight_layout()
    plt.show()
    
    return transformed, lambda_
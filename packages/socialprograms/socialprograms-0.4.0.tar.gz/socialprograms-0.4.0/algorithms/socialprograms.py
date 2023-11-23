
import pandas as pd
import numpy as np
import random
from statistics import mode
from geopy.distance import geodesic
from statistics import mean



class NearestGroup:


  def __init__(self, metric='euclidean', c=None):
    '''
    Inputs :
      base : muestra de referencia arreglo n x m. m filas (latitud y longitud)
      groups : diccionario con k muestras de comparación
    '''
    # grupos de comparación
    self._samples = None
    # nombre de cada grupo de comparación
    self._names = None
    self._metric = metric
    self._c = c
    self._coeff = None
    self._means = None
    self._base_shape = None
    self._samples_shape = None

  # Métricas:
  def _distance(self, x, y, type='euclidean'):
    # euclidean distance
    if type=='euclidean':
      dist = np.sqrt(np.sum([(a-b)**2 for a,b in zip(x,y)]))
    # geodesic distance
    elif type == 'geodesic':
      dist = geodesic(x, y).km
    else:
      raise TypeError('Type of distance is not available')
    return dist

  # función para calcular distancias de los puntos (muestra base) a puntos de otra muestra.
  def _dist_between_two_groups(self, sample_1, sample_2, d_norm=True):

    '''
    Function to estimate distance between two groups

    inputs:
      sample1: muestra con n1 filas y m columnas : latitud y longitud
      sample2: muestra con n2 filas y m columnas : latitud y longitud

    Outputs:
      d     : list of distaces between two groups
      means : average distances
      coeff : similarity coefficient
    '''
    d = []
    dnorm = []
    min = []
    mean = []
    dnorm_mean = []
    coeff = []
    for x1 in sample_1:
      dist = []
      for x2 in sample_2:
        dist_i = self._distance(x1,x2, type=self._metric)
        dist.append(dist_i)
      d.append(dist)
      # minimo
      dmin = np.min(dist)
      min.append(dmin)
      # máximo
      # dmax = np.max(dist)
      # max.append(dmax)
      # promedio
      dmean = np.mean(dist)
      mean.append(dmean)
      # distancias normalizadas
      if d_norm == True:
        return d

      d_norm = [dij/self._c for dij in dist]
      dnorm.append(d_norm)
      # mean dnorm
      d_norm_mean = np.mean(d_norm)
      dnorm_mean.append(d_norm_mean)
      # coeficiente
    sh = [1 if m==0 else 1-d for m,d in zip(min, dnorm_mean)]
    # coeff
    coeff = np.mean(sh)
    means = np.mean(mean)

    return d, means, coeff

  # funtion to get the maximum distance
  def _get_max(self, base, groups):

    '''
    This function returns the maximum distance between one group to the rest groups
    '''
    # extract samples
    samples = []
    self.names = []
    for key, val in groups.items():
      samples.append(val)
      self.names.append(key)

    # list of k groups
    list_samples = samples
    # distances per group
    dg = []
    # coefficients per group
    coeffg = []
    # means per group
    meansg = []
    # loop to save distances per group
    for k in range(len(list_samples)):
      g_comparacion = list_samples[k]
      d = self._dist_between_two_groups(base, g_comparacion, d_norm=True)
      dg.append(d)

    return max([max(max(g)) for g in dg])

  # funtion to get the similarity coefficient
  def fit(self, base, groups):
    '''
    Inputs :
      base   : muestra de referencia arreglo n x m. m filas (latitud y longitud)
      groups : diccionario con k muestras de comparación

    Outputs :
       dg     : list of distaces for each group
      meansg  : average distances for each group
      coeffg  : similarity coefficient each group
    '''
    # validación
    self._base_shape = np.array(base).shape[0]
    self._samples_shape = []
    samples = []
    self._names = []
    for key, val in groups.items():
      samples.append(val)
      self._samples_shape.append(np.array(val).shape[0])
      self._names.append(key)

    # validación de la muestra base
    if isinstance(base, list):
      pass
    else:
      raise TypeError("La muestra base debe ser una lista")
    # validación de las muestras de comparación
    for sample in samples:
      if isinstance(sample, list):
        pass
      else:
        raise TypeError("Las muestras de comparación deben ser listas")
    # condition for constant c
    if self._c is None:
      self._c = self._get_max(base, groups)
    else:
      self._c = float(self._c)

    # list of groups
    list_samples = samples
    dg = []
    coeffg = []
    meansg = []
    # loop to iterate all the groups
    for k in range(len(list_samples)):
      g_comparacion = list_samples[k]
      d, means, coeff = self._dist_between_two_groups(base, g_comparacion, d_norm=False)
      dg.append(d)
      coeffg.append(coeff)
      meansg.append(means)
    # instance atributes
    self._coeff = coeffg
    self._means = meansg

    return dg, meansg, coeffg

  # Function to estimate distance to centroids
  def get_centroids(self, base, groups):
    '''
    Inputs :
      base : muestra de referencia arreglo n x m. m filas (latitud y longitud)
      groups : diccionario con k muestras de comparación
    '''

    samples = []
    names = []
    for key, val in groups.items():
      samples.append(val)
      names.append(key)
    # validation
    if isinstance(base, list):
      pass
    else:
      raise TypeError("La muestra base debe ser una lista")
    # validation
    for sample in samples:
      if isinstance(sample, list):
        pass
      else:
        raise TypeError("Las muestras de comparación deben ser listas")

    list_samples = samples.copy()
    # centroide for each comparison group
    centrosx = [x[0] for x in base]
    centrosy = [y[1] for y in base]
    base_centroidex = np.mean(centrosx)
    base_centroidey = np.mean(centrosy)
    base_centroide = [base_centroidex, base_centroidey]
    # list to save centroids
    sample_centroides = []
    dist_centroides_list = []
    for sample in list_samples:
      sample_centrosx = [x[0] for x in sample]
      sample_centrosy = [y[1] for y in sample]
      sample_centroidex = np.mean(sample_centrosx)
      sample_centroidey = np.mean(sample_centrosy)
      sample_centroide = [sample_centroidex, sample_centroidey]
      sample_centroides.append([sample_centroidex, sample_centroidey])
      # distance to centroids
      dist = self.distance(base_centroide, sample_centroide, type=self._metric)
      dist_centroides_list.append(dist)

    return np.round(dist_centroides_list,4)

  # funtion to return summary of estimations
  def summary(self):
    # results
    result_min = self._names[pd.Series(self._coeff).idxmax()]
    result_means =  np.round(self._means,4)
    result_coeff = np.round(self._coeff,4)
    # summary
    head = f"{'-'*120}- \n-{' '*55} Summary{' '*55} -\n{'-'*120}- \n"
    intro = f" Base (Obs): \t \t {self._base_shape} \n Groups (Obs): \t \t {self._samples_shape} \n \n"
    body = f" Nearest Group: \t {result_min} \n Avg. Distance: \t {result_means} \n Coeff. Similitud: \t {result_coeff} \n"
    pie = f"{'-'*120}"
    return print(head + intro + body + pie)
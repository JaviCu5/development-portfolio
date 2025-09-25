import numpy as np
import random as rd
import os
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from PIL import Image

maxIteration = 10000
## GIF parameters
frame_freq = 50
frame_duration = 200
GIF_images_directory = 'Images'
GIF_name = 'Temporal_evolution'
createGIF = False

lateral_size = 50
occupancy = 0.8
satisfaction = 0.85 # Local segregation >= satisfaction means agent is happy

total_cells = lateral_size*lateral_size
total_individuals = total_cells*occupancy

A_ratio = 0.5 #We will use -1 for this individuals
A_value = -1
A_indiv = round(total_individuals*A_ratio)

B_ratio = 1.-A_ratio #We will use 1 for this individuals
B_value = 1
B_indiv = int(total_individuals-A_indiv)

# We Will use 0 for blank places
void_value = 0

def rand_initial_configuration_square_lattice(lateral_size, A_individuals, B_individuals):
      initial_conf = np.zeros((lateral_size,lateral_size), dtype=int)
      indexes = [(i, j) for i in range(lateral_size) for j in range(lateral_size)]
      indexes = np.array(indexes)
      
      np.random.shuffle(indexes)
      
      A_indexes = indexes[:A_individuals]
      B_indexes = indexes[A_individuals:A_individuals + B_individuals]
      void_indexes = indexes[A_individuals+B_individuals:]
      
      for dupla_A in A_indexes:
            initial_conf[dupla_A[0], dupla_A[1]] = -1
      
      for dupla_B in B_indexes:
            initial_conf[dupla_B[0], dupla_B[1]] = 1
      
      return initial_conf, void_indexes

def local_segregation_numNeighbors(matrix, row, col):
      rows, cols = len(matrix), len(matrix[0])
      local_value = matrix [row, col]
      neighbors_equal = 0
      neighbors = 0
      
      for i in range(row - 1, row + 2):
            for j in range(col - 1, col + 2):
                  if (0 <= i < rows and 0 <= j < cols) and (i != row or j != col):
                        if matrix[i, j] != 0:
                              neighbors +=1
                              if matrix[i, j] == local_value:
                                    neighbors_equal += 1
      
      if neighbors != 0:
            local_segregation = float(neighbors_equal)/float(neighbors)
      else:
            local_segregation = 1. # We define full segregation for no neighbors
      
      return local_segregation, neighbors

#Comput of the magnitudes for the initial random system
def initial_matrix_evaluation(lateral_size, satisfaction, system_matrix):
      unhappy_indexes = np.empty((0, 2), dtype=int)
      total_neighbors = 0
      happiness, segregation = 0, 0
      for i in range(lateral_size):
            for j in range(lateral_size):
                  local_value = system_matrix[i,j]
                  if local_value != 0:
                        local_segregation, neigbor_count = local_segregation_numNeighbors(system_matrix, i, j)
                        segregation += local_segregation
                        total_neighbors += neigbor_count
                        if local_segregation >= satisfaction:
                              happiness += 1
                        else:
                              unhappy_indexes = np.append(unhappy_indexes, np.array([[i,j]]), axis=0)
      return happiness, segregation, total_neighbors, unhappy_indexes

def local_neighbors(matrix, row, col):
      rows, cols = len(matrix), len(matrix[0])
      neighbors_array = np.empty((0, 2), dtype=int)
      
      for i in range(row - 1, row + 2):
            for j in range(col - 1, col + 2):
                  if (0 <= i < rows and 0 <= j < cols) and (i != row or j != col):
                        if matrix[i, j] != 0:
                              neighbors_array = np.append(neighbors_array, np.array([[i, j]]), axis=0)
      return neighbors_array

def cmap_creator(matrix, fig_name, A_value, B_value, directory_name):
      if not os.path.exists(directory_name):
            os.mkdir(directory_name)
      cmap = plt.get_cmap('bwr')

      # Definir los límites de color según tu rango (-1 a 1)
      vmin, vmax = A_value, B_value

      # Mostrar la matriz con el colormap y los límites
      plt.imshow(matrix, cmap=cmap, vmin=vmin, vmax=vmax, origin='lower')
      plt.savefig(directory_name+'/'+fig_name+'.png')
      plt.close()

def graphic_2_magnitudes_time(x, y1, y1_name, y2, y2_name, y3, y3_name, y4, y4_name, file_name):
      fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))  # 1 fila, 2 columnas

      # Configurar el primer gráfico
      ax1.plot(x, y1, linestyle='-', color='b', label=y1_name)
      ax1.plot(x, y2, linestyle='--', color='r', label=y2_name)
      ax1.set_xlabel('time')
      ax1.legend()
      ax1.grid(True)

      # Configurar el segundo gráfico
      ax2.plot(x, y3, linestyle='--', color='r', label=y3_name)
      ax2.plot(x, y4, linestyle='--', color='g', label=y4_name)
      ax2.set_xlabel('time')
      ax2.legend()
      ax2.grid(True)

      plt.tight_layout()  # Ajusta el espacio entre los gráficos

      plt.savefig(file_name+'.png')
      plt.close()

def neighbor_acc_magnitudes(matrix, neighbors_positions, unhappy_indexes, satisfaction):
      ''' Neighborhood accumulative magnitudes '''
      delta_happiness, delta_segregation = 0,0
      for neighbor_position in neighbors_positions:
            local_segregation,_ = local_segregation_numNeighbors(matrix, neighbor_position[0], neighbor_position[1])
            delta_segregation += local_segregation
            # We delete the neighbor if happy from the unhappy neighbors
            if local_segregation >= satisfaction:
                  delta_happiness += 1
                  ubication = np.where(np.all(unhappy_indexes == neighbor_position, axis=1))
                  if len(ubication[0]) > 0:
                        unhappy_indexes = np.delete(unhappy_indexes, ubication, axis=0)
            # We add it if is unhappy
            else:
                  unhappy_indexes = np.append(unhappy_indexes, np.array([neighbor_position]), axis=0)
      
      return delta_happiness, delta_segregation, unhappy_indexes

def find_agent_to_move(unhappy_indexes, matrix):
      movingAgent = unhappy_indexes[0]
      unhappy_indexes = np.delete(unhappy_indexes, 0, axis=0)

      local_segregation,_ = local_segregation_numNeighbors(matrix, movingAgent[0], movingAgent[1])
      
      return unhappy_indexes, movingAgent, local_segregation

def color_changing(matrix, agent_index, unhappy_indexes, satisfaction):
      neighbors_index = local_neighbors(matrix, agent_index[0], agent_index[1])
      old_neighbor_happiness, old_neighbor_segregation, unhappy_indexes = neighbor_acc_magnitudes(matrix, neighbors_index, unhappy_indexes, satisfaction)
      
      # We change the color
      matrix[agent_index[0], agent_index[1]] = -matrix[agent_index[0], agent_index[1]]
      
      new_neighbor_happiness, new_neighbor_segregation, unhappy_indexes = neighbor_acc_magnitudes(matrix, neighbors_index, unhappy_indexes, satisfaction)
      
      delta_happiness = new_neighbor_happiness-old_neighbor_happiness
      delta_segregation = new_neighbor_segregation-old_neighbor_segregation
      
      return unhappy_indexes, delta_happiness, delta_segregation

def position_changing(matrix, agent_index, unhappy_indexes, void_indexes, satisfaction):
      np.random.shuffle(void_indexes)
      agent_value = matrix[agent_index[0], agent_index[1]]
      
      matrix[agent_index[0], agent_index[1]] = 0
      actual_segregation = 0
      aux_index = 0
      while actual_segregation < satisfaction:
            void_index = void_indexes[aux_index]
            matrix[void_index[0], void_index[1]] = agent_value
            actual_segregation,_ = local_segregation_numNeighbors(matrix, void_index[0], void_index[1])
            matrix[void_index[0], void_index[1]] = 0
            aux_index += 1
      
      old_neighbors = local_neighbors(matrix, agent_index[0], agent_index[1])
      new_neighbors = local_neighbors(matrix, void_index[0], void_index[1])
      
      # Old metrics
      matrix[agent_index[0], agent_index[1]] = agent_value
      neg_old_happiness, neg_old_segregation, unhappy_indexes = neighbor_acc_magnitudes(matrix, old_neighbors, unhappy_indexes, satisfaction)
      neg_new_happiness, neg_new_segregation, unhappy_indexes = neighbor_acc_magnitudes(matrix, new_neighbors, unhappy_indexes, satisfaction)
      
      # New Metrics
      matrix[agent_index[0], agent_index[1]] = 0
      matrix[void_index[0], void_index[1]] = agent_value
      pos_old_happiness, pos_old_segregation, unhappy_indexes = neighbor_acc_magnitudes(matrix, old_neighbors, unhappy_indexes, satisfaction)
      pos_new_happiness, pos_new_segregation, unhappy_indexes = neighbor_acc_magnitudes(matrix, new_neighbors, unhappy_indexes, satisfaction)
      
      # We rewrite the index lists
      void_ubication = aux_index-1
      void_indexes = np.delete(void_indexes, void_ubication, axis=0)
      void_indexes = np.append(void_indexes, np.array([agent_index]), axis=0)
      
      delta_happiness = pos_old_happiness + pos_new_happiness - neg_old_happiness - neg_new_happiness
      delta_segregation = actual_segregation + pos_new_segregation + pos_old_segregation - neg_new_segregation - neg_old_segregation
      
      return unhappy_indexes, delta_happiness, delta_segregation, void_indexes

def find_new_position(void_indexes, matrix, moving_agent_value, satisfaction):
      np.random.shuffle(void_indexes)
      local_happiness = False
      aux_index = 0
      while not local_happiness:
            new_position = void_indexes[aux_index]
            position_i = new_position[0]
            position_j = new_position[1]
            local_segregation,_ = local_segregation_numNeighbors(matrix, position_i, position_j)
            aux_index += 1
      neighborsPosition = local_neighbors(matrix, new_position[0], new_position[1])
      void_indexes = np.delete(void_indexes, aux_index-1, axis=0)
      
      return void_indexes, new_position, neighborsPosition, local_segregation

def old_neighborhood_magnitudes(neigbors, matrix, satisfaction):
      neg_delta_happiness, neg_delta_segregation = 0, 0
      for neigbor in neigbors:
            position_i, position_j = neigbor[0], neigbor[1]
            neg_delta_segregation,_ = local_segregation_numNeighbors(matrix, position_i, position_j)
            
            if neg_delta_segregation >= satisfaction:
                  neg_delta_happiness += 1
      return neg_delta_happiness, neg_delta_segregation

def GIF_creator(directory, image_files, GIF_name, frame_duration):
      if image_files:
            # We create a list of objects of PIL images
            images = [Image.open(os.path.join(directory, filename)) for filename in image_files]

            # Save the images in a GIF
            images[0].save(GIF_name+'.gif', save_all=True, append_images=images[1:], duration=frame_duration, loop=0)

system_matrix, void_indexes = rand_initial_configuration_square_lattice(lateral_size, A_indiv, B_indiv)

# Vector declaration
happiness_vec, segregation_vec, A_indiv_vec, B_indiv_vec  = [],[],[],[]

# Absolute happiness and segregation minus the possible individuals affected
abs_happiness, abs_segregation, total_neighbors, unhappy_indexes = initial_matrix_evaluation(lateral_size, satisfaction, system_matrix)

# Average neighbors
av_neigbhors = total_neighbors/total_individuals

happiness = abs_happiness/total_individuals
segregation = abs_segregation/(av_neigbhors*total_individuals)
happiness_vec.append(happiness)
segregation_vec.append(segregation)
A_indiv_vec.append(A_indiv/total_individuals)
B_indiv_vec.append(B_indiv/total_individuals)

# Initial configuration and values
cmap_creator(system_matrix, 'initial', A_value, B_value, GIF_images_directory)

time_iter = 0
iteration = 0
while ((len(unhappy_indexes) > 0) and (iteration < maxIteration)):
      valid_try = True
      #Finding the agent to move or color change
      np.random.shuffle(unhappy_indexes)
      unhappy_indexes, agent_index, agent_segregation = find_agent_to_move(unhappy_indexes, system_matrix)
      
      delta_happiness, delta_segregation = 0, 0
      # We decide if the agent walks or adopt the opinion depending on how many agents of the other poblation is sorrounded by
      if (((1.-agent_segregation) >= satisfaction) and (agent_segregation < rd.random())):
            # If the agent is sorrounded by a lot of contrary agents will change its color but only if is happy changing the color
            unhappy_indexes, delta_neighbor_happiness, delta_neighbor_segregation = color_changing(system_matrix, agent_index, unhappy_indexes, satisfaction)
            
            delta_happiness = 1 + delta_neighbor_happiness
            delta_segregation = 1.-2.*agent_segregation + delta_neighbor_segregation
            
            if system_matrix[agent_index[0], agent_index[1]] == A_value:
                  A_indiv += 1
                  B_indiv -= 1
            else:
                  A_indiv -= 1
                  B_indiv += 1
      else:
            # If the agent cannot change its color he will move if he can
            try:
                  unhappy_indexes, delta_happiness, delta_segregation, void_indexes = position_changing(system_matrix, agent_index, unhappy_indexes, void_indexes, satisfaction)
                  delta_happiness = 1 + delta_happiness
                  delta_segregation = delta_segregation - agent_segregation
            except:
                  # Maybe it cannot move either so we discount this movememtn try
                  time_iter -= 1
                  unhappy_indexes = np.append(unhappy_indexes, np.array([agent_index]), axis=0)
                  valid_try = False
      
      iteration += 1
      time_iter += 1
      
      abs_happiness = abs_happiness + delta_happiness
      abs_segregation = abs_segregation + delta_segregation
      
      happiness, segregation = abs_happiness/total_individuals, abs_segregation/(av_neigbhors*total_individuals)
      
      if valid_try:
            happiness_vec.append(happiness)
            segregation_vec.append(segregation)
            A_indiv_vec.append(A_indiv/total_individuals)
            B_indiv_vec.append(B_indiv/total_individuals)
      '''
      if ((iteration % frame_freq) and (createGIF)):
            cmap_creator(system_matrix, str(iteration//frame_freq), A_value, B_value, GIF_images_directory)
      '''

graphic_2_magnitudes_time([i for i in range(time_iter+1)], happiness_vec, 'Happiness', segregation_vec, 'Segregation',
                        A_indiv_vec, 'A individuals',B_indiv_vec, 'B individuals', 'magnitudes_overtime')
cmap_creator(system_matrix, str((time_iter-1)//frame_freq + 1), A_value, B_value, GIF_images_directory)
"""
image_files = [str(f)+'.png' for f in range((644-1)//frame_freq + 1)]
if (createGIF):
      GIF_creator(GIF_images_directory, image_files, GIF_name, frame_duration)
"""
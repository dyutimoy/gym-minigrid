from gym_minigrid.minigrid import *
from gym_minigrid.register import register
from operator import add
from random import random

class SimpleWarehouseEnv(MiniGridEnv):

	"""
	Simple warehouse with single agent and multiple stack to station
	"""

	def __init__(
			self,
			size=32,
			agent_start_pos=(1,1),
			agent_start_dir=0,
			n_pods =4,  #now mostly would be kept zero
			n_cluster=4,
	):
		print("of")
		self.agent_start_pos = agent_start_pos
		self.agent_start_dir = agent_start_dir

		self.n_cluster=n_cluster
		# reduce bots if two many to accomadate
		if n_pods <= size/3 + 1:
			self.n_pods = int(n_pods)
		else:
			self.n_pods = int(size/3)
		super().__init__(
			grid_size  = size,
			max_steps = 4 * size * size,
			see_through_walls = True,
		)

		#self.action_space = spaces.Discrete(self.actions.forward + 1)
		self.reward_range = (-1,1)


	def _gen_grid(self, width, height):
		# Create an empty grid
		self.grid = Grid(width, height)
		
		# Generate the surrounding walls
		self.grid.wall_rect(0, 0, width, height)

		# Place a goal square in the bottom-right corner
		#self.grid.set(width -2,height -2, Goal())

		
		#!!!!!!!!!!!!!!!!!!!
		# set multiple goals or based on time steps

		if self.agent_start_pos is not None:
			self.agent_pos = self.agent_start_pos
			self.agent_dir = self.agent_start_dir
		else:
			self.place_agent()



		self.pods = np.empty([self.n_pods,self.n_pods,self.n_cluster],dtype=object)
		for i_pod_x in range(self.n_pods):
			for i_pod_y in range(self.n_pods):
				for i_cluster in range(self.n_cluster):
					self.pods[i_pod_x][i_pod_y][i_cluster]=Ball()

					#change this to bot
					#!!!!!!!!!!!!!!
					
					self.place_obj(self.pods[i_pod_x][i_pod_y][i_cluster], top=(2+i_pod_x*3,2+i_pod_y*3),size=(2,2),max_tries=100)

		self.pick_station = []
		for i_pod_x in range(self.n_pods):
			self.pick_station.append(Dropzone())
			self.place_obj(self.pick_station[i_pod_x], top=(3+i_pod_x*3,height-2),size=(1,1),max_tries=100)



		self.mission = "complete as many tasks as possible"


	def step(self,action):

		#if action >= self.action_space.n:
		#	action = 0

		
		front_cell_initial = self.grid.get(*self.front_pos)
		#ADD NEW GREEN

		for i_pod_x in range(self.n_pods):
			for i_pod_y in range(self.n_pods):
				for i_cluster in range(self.n_cluster):
					if random()>.99 and self.pods[i_pod_x][i_pod_y][i_cluster].color != 'green':
						#print(random())
						self.pods[i_pod_x][i_pod_y][i_cluster].color= 'green'

		# Update obstacle postions

		"""
		

			obs, reward, done, info = MiniGridEnv.step(self, action)
		
			if action == self.actions.forward and not_clear:
				reward = -1
				done = True
				return obs, reward, done, info
		"""
		

		obs, reward, done, info = MiniGridEnv.step(self, action)

		front_cell = self.grid.get(*self.front_pos)
		if self.front_pos[0]+ np.array(-1) >= 0 and self.front_pos[0]+ np.array(-1)< self.width and self.front_pos[1]+ np.array(0) >= 0 and  self.front_pos[1]+ np.array(0) < self.height:
			front_right_cell=self.grid.get(*self.front_pos+ np.array((-1, 0)))
		else:
			front_right_cell = None
		
		print("front",front_cell)
		if front_cell_initial is not None:
			
			if action == self.actions.pickup and front_cell_initial.type== 'ball':
				if self.carrying and self.carrying.color == 'green':
					reward += 0.1
		print("front right",front_right_cell)
		if action == self.actions.drop and front_right_cell is not None and front_cell_initial is None:	
			if front_right_cell.type == 'dropzone':
				reward+=0.5

		if action == self.actions.pickup:
			

			if self.carrying and self.carrying.color == 'green' and front_right_cell is not None and front_right_cell.type == 'dropzone' and front_cell_initial is not None:
				print("carry", self.carrying)
				print("color", self.carrying.color)
				self.carrying.color = 'blue'
				reward += 0.3


		
		return obs,reward, done, info

class SimpleWarehouseEnv32x32(SimpleWarehouseEnv):
	def __init__(self):
		super().__init__(size=10, n_pods=2, n_cluster=2)




register(
	id='MiniGrid-Simple-Warehouse-32x32-v0',
	entry_point = 'gym_minigrid.envs:SimpleWarehouseEnv32x32'
)
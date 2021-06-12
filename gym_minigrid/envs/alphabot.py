from gym_minigrid.minigrid import *
from gym_minigrid.register import register
from operator import add
from random import random

class SimpleAlphabotEnv(MiniGridEnv):

	"""
	Simple warehouse with single agent and multiple stack to station
	"""

	def __init__(
			self,
			size=32,
			agent_start_pos=(1,1),
			agent_start_dir=0,
			n_pod_row =6,  #now mostly would be kept zero
			n_pod_col= 8,
	):
		#print("of")
		self.agent_start_pos = agent_start_pos
		self.agent_start_dir = agent_start_dir

		self.n_pod_row= n_pod_row
		self.n_pod_col= n_pod_col
		
		super().__init__(
			grid_size  = size,
			max_steps = 10 * size * size,
			see_through_walls = True,
		)

		self.action_space = spaces.Discrete(self.actions.forward + 2)
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

		self.pick_station = []
		for i_pod_y in range(2):
			self.pick_station.append(Dropzone())
			self.place_obj(self.pick_station[i_pod_y], top=(1,(i_pod_y+1)*self.n_pod_col/2 -1),size=(1,1),max_tries=100)


		
		self.pods = np.empty([self.n_pod_row,self.n_pod_col],dtype=object)
		for i_pod_x in range(self.n_pod_row):
			for i_pod_y in range(self.n_pod_col):
				if i_pod_y %2 ==0:
					if random()>.5:
							self.pods[i_pod_x][i_pod_y]=Rackzone(color = "yellow",contains= Ball())
					else:
						self.pods[i_pod_x][i_pod_y]=Rackzone(color = "red",contains= None, is_occupied = False, is_unoccupied = True)

					#change this to bot
					#!!!!!!!!!!!!!!
					
					self.place_obj(self.pods[i_pod_x][i_pod_y], top=(3+i_pod_x,1+i_pod_y),size=(1,1),max_tries=100)
				else:
					self.pods[i_pod_x][i_pod_y]=Wall()
					self.place_obj(self.pods[i_pod_x][i_pod_y], top=(3+i_pod_x,1+i_pod_y),size=(1,1),max_tries=100)
		
		
		

		self.mission = "complete as many tasks as possible"


	def step(self,action):

		#if action >= self.action_space.n:
		#	action = 0

		
		front_cell_initial = self.grid.get(*self.front_pos)
		#ADD NEW GREEN

		for i_pod_x in range(self.n_pod_row):
			for i_pod_y in range(self.n_pod_col):
				
				if random()>.99 and self.pods[i_pod_x][i_pod_y].contains != None and self.pods[i_pod_x][i_pod_y].color != 'green' and  self.pods[i_pod_x][i_pod_y].color == 'yellow': 
					#print(random())
					self.pods[i_pod_x][i_pod_y].contains.set_time_count(self)
					self.pods[i_pod_x][i_pod_y].color= 'green'

		# Update obstacle postions
		# introduce orders by poisson distribution
		# schdule them rewards
		# better results
		

		"""
		

			obs, reward, done, info = MiniGridEnv.step(self, action)
		
			if action == self.actions.forward and not_clear:
				reward = -1
				done = True
				return obs, reward, done, info
		"""
		

		obs, reward, done, info = MiniGridEnv.step(self, action)
		#print(done)
		reward -= 0.001

		return obs,reward, done, info

class SimpleAlphabotEnv32x32(SimpleAlphabotEnv):
	def __init__(self):
		super().__init__(size=10)




register(
	id='MiniGrid-Simple-Alphabot-32x32-v0',
	entry_point = 'gym_minigrid.envs:SimpleAlphabotEnv32x32'
)
import numpy as np
import random
import time
from copy import copy,deepcopy

import Play
class House_move(object):
	"""docstring for House_move"""
	def __init__(self, m, n):
		self.N = n
		self.M = m

		self.n = 0
		self.m = 0
		self.size = 0
		self.start_pos = 0
		self.all_direct = [(1,-2),(1,2),(-1,2),(-1,-2),(2,1),(2,-1),(-2,1),(-2,-1)]
		self.cccc = 0
		self.cmp_ = lambda x: x[1]
		self.Map = 0

		self.start = 0
		self.end = 0

		self.count_step = 0 # 统计语句次数

		self.array_database = {}

	def save_array(self):
		for i in range(6,14,2):
			for j in range(6,14,2):
				if (i == 12 and j == 12) or (abs(i-j) > 2):
					continue
				self.m = i
				self.n = j
				self.Map = np.zeros((self.m,self.n))
				self.size = self.n*self.m
				if (i,j) in [(6,6) ,(8,8), (6,8), (10,10)]:
					self.start_pos = (1,2)					
				elif 12 in (i,j):
					self.start_pos = (6,5)
				else:
					self.start_pos = (2,1)
				self.DFS(self.start_pos,1)
				self.array_database[(i,j)] = self.Map

	def run(self):
		self.start = time.time()
		self.save_array()
		self.Map = self.Map_split(self.M,self.N)
		self.end = time.time()
		self.Print()
	def Single_run(self):
		self.m = self.M
		self.n = self.N
		self.Map = np.zeros((self.m,self.n))
		self.size = self.n*self.m
		self.start_pos = (1,2)
		self.DFS(self.start_pos,1)

	def count(self,cen):
		count = 0
		for i in self.all_direct:
			x = cen[0]+i[0]
			y = cen[1]+i[1]
			if (0 <= x < self.m) and (0 <= y < self.n) and (self.Map[x,y] == 0):
				count += 1
		return count
		
	def DFS(self,point,tag):
		
		#print(all_direct)
		if tag == self.size+1:
			if point == self.start_pos:
				return 'Done'
			else:
				return False
		x = point[0]
		y = point[1]
		self.Map[x,y] = tag
			#print("Center -->: {}\n".format(center))	
			#
		follow_point = []
		for (i,j) in self.all_direct:
			x0 = point[0]+i
			y0 = point[1]+j
			if (0 <= x0 < self.m) and (0 <= y0 < self.n) and (self.Map[x0,y0] == 0):
				follow_point.append((x0,y0))
			if tag == self.size and (x0,y0) == self.start_pos:
				follow_point.append(self.start_pos)

		follow_point = {i:self.count(i) for i in follow_point}
		follow_point = sorted(follow_point.items(),key=self.cmp_)

		for f_point in follow_point: 
			result = self.DFS(f_point[0],tag+1)
			if result == 'Done':
				return 'Done'
		self.Map[x,y] = 0

	def Map_split(self,tmpm,tmpn):
		self.cccc += 1
		if (tmpm <= 12 and tmpn <= 12) and (tmpm != 12 or tmpn != 12):
			return self.array_database[(tmpm,tmpn)]
		else:
			if tmpm % 4 == 0:
				newm1 = newm2 =  (tmpm // 2)
			else:
				newm1 = tmpm // 2 + 1
				newm2 = tmpm // 2 - 1
			if tmpn % 4 == 0:
				newn1 = newn2 =  (tmpn // 2)
			else:
				newn1 = tmpn // 2 + 1
				newn2 = tmpn // 2 - 1
			map1 = deepcopy((self.Map_split(newm1,newn1)))
			map2 = deepcopy((self.Map_split(newm1,newn2)))
			map3 = deepcopy((self.Map_split(newm2,newn1)))
			map4 = deepcopy((self.Map_split(newm2,newn2)))
			return self.merge_map(map1,map2,map3,map4)		

	def merge_map(self,map1,map2,map3,map4):
		# map1,map2,map3,map4:[1 2]
		# 					  [3 4]
		A1 = map1[-1,-3]
		A2 = map1[-2,-1]
		size1 = map1.shape[0]*map1.shape[1]
		size2 = map2.shape[0]*map2.shape[1]
		size3 = map3.shape[0]*map3.shape[1]
		size4 = map4.shape[0]*map4.shape[1]
		if A1 < A2: # 逆时针
			# 旋转
			map1 = size1-map1+1
			self.count_step += size1
		A1 = map1[-1,-3]
		A2 = map1[-2,-1]
		B1 = map2[-1,0]
		B2 = map2[-3,1]
		if B1 > B2 or (B2 == size2 and B1 == 1):
			map2 = size2-map2+1
			self.count_step += size2
		B2 = map2[-3,1] # 重新索引
		map2[map2<B2] += size2
		self.count_step += size2
		if A2 > B2:
			map2 += (A2-B2+1)
			self.count_step += size2
		else:
			map2 -= (B2-A2-1)
			self.count_step += size2

		D1 = map4[1,0]
		D2 = map4[0,2]
		if D1 > D2 or (D2 == size4 and D1 == 1):
			map4 = size4-map4+1
			self.count_step += size4
		B1 = map2[-1,0]
		D2 = map4[0,2]
		map4[map4<D2] += map4.shape[0]*map4.shape[1]
		self.count_step += size4
		if B1 > D2:
			map4 += (B1-D2+1)
			self.count_step += size4
		else:
			map4 -= (D2-B1-1)
			self.count_step += size4

		C2 = map3[0,-1]
		C1 = map3[2,-2]
		if C2 > C1 or (C1 == size3 and C2 == 1):
			map3 = size3-map3+1
			self.count_step += size3
		C1 = map3[2,-2]
		D1 = map4[1,0]
		map3[map3<C1] += map3.shape[0]*map3.shape[1]
		self.count_step += size3
		if D1 > C1:
			map3 += (D1-C1+1)
			self.count_step += size3
		else:
			map3 -= (C1-D1-1)
			self.count_step += size3

		C2 = map3[0,-1]
		map1[map1>=A1] += (C2-A1+1)
		self.count_step += size1
		
		map12 = np.hstack((map1,map2))
		map34 = np.hstack((map3,map4))
		
		map1234 = np.vstack((map12,map34))
		self.count_step += (size1+size2+size3+size4)
		return map1234

	def is_correct(self):
		array = self.Map
		shape = array.shape
		size = shape[0]*shape[1]
		tmp = set(i+1 for i in range(size))
		arr = set(np.ravel(array))
		sub = tmp-arr
		if len(sub) == 0:
			return True
		else:
			print(arr)
			return sub

	def test_funtion(self):
		self.Map = self.merge_map(deepcopy(self.Map),deepcopy(self.Map),
								deepcopy(self.Map),deepcopy(self.Map))

	def Print(self):
		print(self.Map)
		print("Rusult if Correct? : {}".format(self.is_correct()))
		print("Map_split COUNT: {}".format(self.cccc))
		print("Sum time:{}".format(self.end-self.start))
		print("Sum count_step: {}".format(self.count_step))

	def get_map(self):
		return self.Map

if __name__ == '__main__':
	#拼接测试
	
	N = int(input("Please input Even N:\n"))
	while(N % 2 != 0):
		N = int(input("Please input Even N:\n"))
	ff = input("Wanted play this result? y/n\n")
	
	House = House_move(N,N)
	House.run()
	if ff == 'y':
		MAP = House.get_map()
		Play.play_move(MAP)
	#单点测试
	'''
	House = House_move(10,10)
	House.Single_run()
	House.test_funtion()
	House.Print()
	House.is_correct()
	'''
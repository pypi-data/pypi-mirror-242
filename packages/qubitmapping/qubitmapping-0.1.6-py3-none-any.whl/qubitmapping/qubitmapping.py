
import os
import numpy as np
import time
from datetime import datetime
import collections
from icecream import ic


initial_mapping_options = ["random", "periodic_random", "periodic_fixed", "random_diagonal", "fcfs", 
						"vertical_separation", "horizontal_separation"]

# note for the mapping option
# "random" : the algorithm qubits are randomly arranged 
# "periodic_random" : the algorithm qubits are randomly arranged, but there are fixed space chosen randomly
# "periodic_fixed" : the algorithm qubits are randomly arranged, but there are fixed space given as input
# "fcfs" : the algorithm qubits are arranged in the order they are appearing in the algorithm (protocol)
# "horizontal_separation" : the whole quantum chip is separated as block in horizontal direction first. 
# 							each algorithm qubit is randomly arranged in each area
# "2d_random_distribution" : the whole quantum chip is separated as block in vertical direction first. 
# 							each algorithm qubit is randomly arranged in each area


def initialize_qubit_mapping(algorithm_qubits, qchip_size, **kwargs):
	"""
		초기 큐빗 매핑을 랜덤하게 생성하는 함수
		arg: 알고리즘 큐빗 리스트와 양자칩 사이즈
	"""
	
	number_algorithm_qubits = len(algorithm_qubits)
	
	if number_algorithm_qubits > qchip_size:
		raise Exception("the number of qubits in algorithm ({}) exceeds the size of a quantum chip({}).".format(number_algorithm_qubits, qchip_size))

	else:
		mapping_option = kwargs.get("option")
		if mapping_option is None or mapping_option not in initial_mapping_options: 
			mapping_option = "random"

		position_fixed_qubits = kwargs.get("fixed_qubits")
		if position_fixed_qubits is None: position_fixed_qubits = {}

		offset = kwargs.get("offset")

		# un_allocated algorithm qubits : 알고리즘 큐빗 중 기존에 allocated 되지 않은 큐빗 --> 처음으로 등장한 큐빗
		unallocated_algorithm_qubits = list(set(algorithm_qubits) - set(list(position_fixed_qubits.keys())))

		# null_qubits = 전체 양자칩 - fixed_qubits - unallocated_algorithm_qubits
		size_null_qubits = qchip_size - (len(position_fixed_qubits.keys()) + len(unallocated_algorithm_qubits))
		null_qubits = ["dummy{}".format(i) for i in range(size_null_qubits)]

		qubits = unallocated_algorithm_qubits + null_qubits

		if mapping_option in ["random", "periodic_random", "periodic_fixed"]:
			# 이미 고정된 큐빗 배치
			mapping_table = {k: v for k, v in position_fixed_qubits.items()}
			# unallocated physical qubits 을 대상으로 회로 합성 수행
			# |unallocated physical qubits| = |qchip_size| - |이미 고정된 큐빗|
			remaining_position = list(set(list(range(qchip_size))) - set(list(mapping_table.values())))

			remaining_qubit = list(set(qubits) - set(list(mapping_table.keys())))
			
			size_remaining_position = len(remaining_position)
			
			np.random.seed(offset)
			# np.random.seed(int(seed))
			
			# 큐빗 초기 배치가 필요한 부분에 대해서 완전 무작위적으로 큐빗 배치함
			if mapping_option == "random":
				# 반복이 발생하지 않는 난수 리스트
				random_int_dist = np.random.choice(remaining_position, size_remaining_position, replace=False)
				
				# 논리적 큐빗 (알고리즘 큐빗 + 패딩 큐빗) 을 물리적 큐빗에 매핑
				temp_mapping = {k: int(v) for k, v in zip(remaining_qubit, random_int_dist)}
				mapping_table.update({k:v for k, v in temp_mapping.items()})
		

			# periodic 한 큐빗 배치

			elif mapping_option in ["periodic_random", "periodic_fixed"]:
				# 랜덤 초기 값과 주기
				position = int(np.random.randint(size_remaining_position+1, size=1)[0])
				
				if mapping_option == "periodic_random":
					period = int(np.random.randint(size_remaining_position+1, size=1)[0])
				
				elif mapping_option == "periodic_fixed":
					period = kwargs.get("period")

				inverse_qubit_mapping = {v: k for k, v in mapping_table.items()}
				
				while len(remaining_qubit):
					qubit = remaining_qubit.pop()
					position %= qchip_size

					while True:
						if inverse_qubit_mapping.get(position) is None: 
							inverse_qubit_mapping[position] = qubit
							break
						else:
							position = (position + 1) % qchip_size
					
					position += period
				
				mapping_table = {v : k for k, v in inverse_qubit_mapping.items()}


		elif mapping_option in ["vertical_separation", "horizontal_separation"]:
			area = int(qchip_size/number_algorithm_qubits)
			qubits_in_area = collections.defaultdict(list)
			qchip_architecture = kwargs.get("qchip_dimension")

			if mapping_option == "horizontal_separation":
				for i in range(number_algorithm_qubits-1):
					for k in range(area):
						qubits_in_area[i].append(i*area + k)

				qubits_in_area[number_algorithm_qubits-1].extend(range(area*(number_algorithm_qubits-1) ,qchip_size))

			else:
				depth_first_list = []
				for j in range(qchip_architecture["width"]):
					for i in range(qchip_architecture["height"]):
						depth_first_list.append(i*qchip_architecture["width"]+j)				

				for i in range(number_algorithm_qubits-1):
					qubits_in_area[i].extend(depth_first_list[i*area:(i+1)*area])

				qubits_in_area[number_algorithm_qubits-1].extend(depth_first_list[(number_algorithm_qubits-1)*area:])


			mapping_table = {}

			for idx, qubit in enumerate(algorithm_qubits):
				choice = np.random.randint(len(qubits_in_area[idx]), size=1)[0]
				mapping_table[qubit] = qubits_in_area[idx][choice]

			remaining_position = list(set(list(range(qchip_size))) - set(list(mapping_table.values())))

			remaining_qubit = list(set(qubits) - set(list(mapping_table.keys())))
			size_remaining_position = len(remaining_position)
			# 큐빗 초기 배치가 필요한 부분에 대해서 완전 무작위적으로 큐빗 배치함
			# 반복이 발생하지 않는 난수 리스트
			random_int_dist = np.random.choice(remaining_position, size_remaining_position, replace=False)

			# 논리적 큐빗 (알고리즘 큐빗 + 패딩 큐빗) 을 물리적 큐빗에 매핑
			temp_mapping = {k: int(v) for k, v in zip(remaining_qubit, random_int_dist)}
			mapping_table.update({k:v for k, v in temp_mapping.items()})


		elif mapping_option == "random_diagonal":
			# lattice size is n x n and place data qubits on diagonal only
			# first make random sequence 0 ~ n-1 first
			number_data_qubits = sum(1 if "data" in qubit else 0 for qubit in algorithm_qubits)
			data_qubit_sequence = np.random.choice(number_data_qubits, number_data_qubits, replace=False)

			mapping_table = {"data{}".format(data_qubit_sequence[i]): i + i*number_data_qubits for i in range(number_data_qubits)}

			remaining_position = list(set(list(range(qchip_size))) - set(list(mapping_table.values())))
			remaining_qubit = list(set(qubits) - set(list(mapping_table.keys())))

			
			size_remaining_position = len(remaining_position)
			
			seed = kwargs.get("seed")
			if seed is None: seed = datetime.now().microsecond%9
			
			np.random.seed(int(seed))
			
			# 큐빗 초기 배치가 필요한 부분에 대해서 완전 무작위적으로 큐빗 배치함
			# 반복이 발생하지 않는 난수 리스트
			random_int_dist = np.random.choice(remaining_position, size_remaining_position, replace=False)
			
			# 논리적 큐빗 (알고리즘 큐빗 + 패딩 큐빗) 을 물리적 큐빗에 매핑
			temp_mapping = {k: int(v) for k, v in zip(remaining_qubit, random_int_dist)}
			mapping_table.update({k:v for k, v in temp_mapping.items()})
			

		elif mapping_option == "fcfs":
			# naive mapping : 순서대로
			random_int_dist = range(qchip_size)
			mapping_table = {k: int(v%qchip_size) for k, v in zip(qubits, random_int_dist)}	

		else:
			raise Exception("mapping option {} is not correct one. please choose it from [random, periodic_random, periodic_fixed, random_diagonal, fcfs]")

		return mapping_table



if __name__ == "__main__":
	algorithm_qubits = ["d0", "d1", "d2", "d3", ]
	ret = initialize_qubit_mapping(algorithm_qubits, 30, option="vertical_separation", qchip_dimension={"height": 5, "width": 6})
	ic(ret)
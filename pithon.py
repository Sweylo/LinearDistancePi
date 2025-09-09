#!.venv/bin/python

from argparse import ArgumentParser
from decimal import Decimal, getcontext
from tqdm import tqdm
import matplotlib.pyplot as plt


class Circle:

	def __init__(self, radius:Decimal=Decimal(1), precision:int=32):
		getcontext().prec = precision
		if type(radius) is not Decimal:
			radius = Decimal(radius)
		if radius <= 0:
			raise ValueError("radius must be positive")
		self.radius = radius

	def f(self, x:Decimal) -> Decimal:
		if type(x) is Decimal:
			if x < 0 or x > self.radius:
				raise ValueError("x must be in [0, radius]")
			getcontext().prec += 2
			result = (self.radius**2 - x**2).sqrt()
			getcontext().prec -= 2
			return result
		else:
			raise TypeError("x must be a Decimal")
		

class PiEstimator:

	def __init__(self, radius:Decimal = None, circle:Circle = None):
		if circle is not None:
			self.circle = circle
		elif radius is not None:
			self.circle = Circle(radius)
		else:
			raise ValueError("Either radius or circle must be provided")
		
	def estimate(self, n:int) -> Decimal:
		raise NotImplementedError("Subclasses must implement this method")


class LinearDistance(PiEstimator):

	def __init__(self, radius:Decimal = None, circle:Circle = None):
		super().__init__(radius, circle)

	def get_n_dec(self, n:int, pow:int) -> Decimal:
		if pow <= 3:
			raise ValueError("pow must be greater than 3")
		else:
			pow -= 2
		n_dec = Decimal(n)
		cos_expansion = Decimal(2).sqrt()
		getcontext().prec += 2
		for _ in range(pow - 1):
			cos_expansion = (Decimal(2) + cos_expansion).sqrt()
		n_dec = n_dec / (Decimal(0.5) * (Decimal(2) - cos_expansion).sqrt())
		getcontext().prec -= 2
		return n_dec


	def estimate(self, n:int, pow:int) -> Decimal:
		getcontext().prec += 2
		arclen = Decimal(0.0)
		x1 = Decimal(0.0)
		y1 = self.circle.f(x1)
		# getcontext().prec += 2
		# n_dec = Decimal(n)
		# n_dec = Decimal(n) * Decimal(2)
		# n_dec = Decimal(n) * (Decimal(4) / (Decimal(-1) + Decimal(5).sqrt()))
		# n_dec = Decimal(n) * (Decimal(2) * Decimal(2).sqrt()) / (Decimal(-1) + Decimal(3).sqrt())
		# n_dec = Decimal(n) / (Decimal(0.5) * (Decimal(2) - (Decimal(2) + Decimal(2).sqrt()).sqrt()).sqrt())
		# n_dec = Decimal(n) / (
		# 	Decimal(0.5) * (
		# 		Decimal(2) - (
		# 			Decimal(2) + (
		# 				Decimal(2) + (
		# 					Decimal(2) + (
		# 						Decimal(2) + (
		# 							Decimal(2) + (
		# 								Decimal(2) + (
		# 									Decimal(2) + (
		# 										Decimal(2) + (
		# 											Decimal(2)
		# 										).sqrt()
		# 									).sqrt()
		# 								).sqrt()
		# 							).sqrt()
		# 						).sqrt()
		# 					).sqrt()
		# 				).sqrt()
		# 			).sqrt()
		# 		).sqrt()
		# 	).sqrt()
		# )
		# getcontext().prec -= 2
		# pow = 30
		n_dec = self.get_n_dec(n, pow)
		i = Decimal(0)
		for i in tqdm(range(int(self.circle.radius) * n)):
			x2 = (Decimal(i) + Decimal(1)) / n_dec
			y2 = self.circle.f(x2)
			arclen += LinearDistance.pythag(x2 - x1, y2 - y1)
			x1 = x2
			y1 = y2
		# pi = Decimal(2) * arclen / self.circle.radius
		# pi = Decimal(6) * arclen / self.circle.radius
		# pi = Decimal(10) * arclen / self.circle.radius
		# pi = Decimal(12) * arclen / self.circle.radius
		# pi = Decimal(16) * arclen / self.circle.radius
		pi = Decimal(2).__pow__(Decimal(pow)) * arclen / self.circle.radius
		getcontext().prec -= 2
		return +pi
	
	def graph_estimate(self, n:int):
		circum = Decimal(0.0)
		x1 = Decimal(0.0)
		y1 = self.circle.f(x1)
		xs = [x1]
		ys = [y1]
		for i in range(int(self.circle.radius) * n):
			x2 = Decimal(i + 1) / n
			y2 = self.circle.f(x2)
			xs.append(float(x2))
			ys.append(float(y2))
			circum += LinearDistance.pythag(x2 - x1, y2 - y1)
			x1 = x2
			y1 = y2
		return circum / (self.circle.radius / Decimal(2)), xs, ys
	
	@staticmethod
	def pythag(a:Decimal, b:Decimal) -> Decimal:
		getcontext().prec += 2
		c = (a**2 + b**2).sqrt()
		getcontext().prec -= 2
		return c
	

class RectangularArea(PiEstimator):

	def __init__(self, radius:Decimal = None, circle:Circle = None):
		super().__init__(radius, circle)
		
	def estimate(self, n:int) -> Decimal:
		area = Decimal(0.0)
		for i in tqdm(range(int(self.circle.radius) * n)):
			x = Decimal(i + 1) / n
			y = self.circle.f(x)
			area += y / n
		return area * 4 / (self.circle.radius**2)
	

class TrapezoidalArea(PiEstimator):

	def __init__(self, radius:Decimal = None, circle:Circle = None):
		super().__init__(radius, circle)
		
	def estimate(self, n:int) -> Decimal:
		area = Decimal(0.0)
		x1 = Decimal(0.0)
		y1 = self.circle.f(x1)
		for i in tqdm(range(int(self.circle.radius) * n)):
			x2 = Decimal(i + 1) / n
			y2 = self.circle.f(x2)
			area += (y1 + y2) / (2 * n)
			x1 = x2
			y1 = y2
		return area * 4 / (self.circle.radius**2)


class MonteCarloArea(PiEstimator):

	def __init__(self, radius:Decimal = None, circle:Circle = None):
		super().__init__(radius, circle)
		
	def estimate(self, n:int) -> Decimal:
		import random
		hits = Decimal(0)
		for _ in tqdm(range(n)):
			x = Decimal(random.uniform(0, float(self.circle.radius)))
			y = Decimal(random.uniform(0, float(self.circle.radius)))
			if y <= self.circle.f(x):
				hits += Decimal(1)
		return hits * Decimal(4) / Decimal(n)
	

class WallisProduct(PiEstimator):

	def __init__(self, radius:Decimal = None, circle:Circle = None):
		super().__init__(radius, circle)
		
	def estimate(self, n:int) -> Decimal:
		product = Decimal(1.0)
		for i in tqdm(range(1, n + 1)):
			numerator = Decimal(4 * i * i)
			denominator = Decimal(numerator - 1)
			product *= numerator / denominator
		return product * Decimal(2)
	

class NewtonLeibniz(PiEstimator):

	def __init__(self, radius:Decimal = None, circle:Circle = None):
		super().__init__(radius, circle)
		
	def estimate(self, n:int) -> Decimal:
		getcontext().prec += 2
		pi = Decimal(0.0)
		for k in tqdm(range(n)):
			pi += (Decimal((-1)**k) / Decimal(2 * k + 1))
		pi *= Decimal(4)
		getcontext().prec -= 2
		return +pi  # unary plus applies the precision
	

class Nilakantha(PiEstimator):

	def __init__(self, radius:Decimal = None, circle:Circle = None):
		super().__init__(radius, circle)
		
	def estimate(self, n:int) -> Decimal:
		getcontext().prec += 2
		pi = Decimal(3.0)
		for k in tqdm(range(1, n + 1)):
			term = Decimal(4) / (Decimal((2 * k) * (2 * k + 1) * (2 * k + 2)))
			if k % 2 == 1:
				pi += term
			else:
				pi -= term
		getcontext().prec -= 2
		return +pi  # unary plus applies the precision



if __name__ == "__main__":

	parser = ArgumentParser()
	parser.add_argument('-n', '--iterations', action='store')
	parser.add_argument('-r', '--radius', action='store')
	parser.add_argument('-p', '--precision', action='store', default=40)
	parser.add_argument('-e', '--pow', action='store')
	parser.add_argument('--graph', action='store_true')
	parser.add_argument('--multi', action='store_true')
	parser.add_argument('--animate', action='store_true')
	parser.add_argument('-d', '--delay', action='store')
	parser.add_argument('-s', '--step', action='store')
	args = parser.parse_args()

	if args.iterations is not None:
		n = int(args.iterations)
	else:
		n = 1000

	if args.precision is not None:
		precision = int(args.precision)
	else:
		precision = 32

	if args.radius is not None:
		radius = Decimal(args.radius)
		circle = Circle(radius=radius, precision=precision)
	else:
		radius = Decimal(1)
		circle = Circle(radius=radius, precision=precision)

	if args.pow is not None:
		pow = int(args.pow)
	else:
		pow = 4

	if args.delay is not None:
		delay = float(args.delay)
	else:
		delay = 0.5

	if args.step is not None:
		step = int(args.step)
	else:
		step = 1

	graph = bool(args.graph)
	multi = bool(args.multi)
	animate = bool(args.animate)

	pi = Decimal('3.141592653589793238462643383279502884197169399375105820974944592307816406286208998628034825342117067982148086513282306647093844609550582231725359408128481117450284102701938521105559644622948954930381964428810975665933446128475648233786783165271201909145648566923460348610454326648213393607260249141273724587006606315588174881520920962829254091715364367892590360011330530548820466521384146951941511609433057270365759591953092186117381932611793105118548074462379962749567351885752724891227938183011949129833673362440656643086021394946395224737190702179860943702770539217176293176752384674818467669405132000568127145263560827785771342757789609173637178721468440901224953430146549585371050792279689258923542019956112129021960864034418159813629774771309960518707211349999998372978049951059731732816096318595024459455346908302642522308253344685035261931188171010003137838752886587533208381420617177669147303598253490428755468731159562863882353787593751957781857780532171226806613001927876611195909216420198938095257201065485863278865936153381827968230301952035301852968995773622599413891249721775283479131515574857242454150695950829533116861727855889075098381754637464939319255060400927701671139009848824012858361603563707660104710181942955596198946767837449448')

	if not graph:

		if multi:

			print(f'Estimating π with Monte Carlo method where n = {n}')
			mc_pi = MonteCarloArea(circle=circle).estimate(n)
			print(f'Estimating π with Rectangular Area method where n = {n}')
			ra_pi = RectangularArea(circle=circle).estimate(n)
			print(f'Estimating π with Trapezoidal Area method where n = {n}')
			ta_pi = TrapezoidalArea(circle=circle).estimate(n)
			print(f'Estimating π with Linear Distance method where n = {n}')
			ld_pi = LinearDistance(circle=circle).estimate(n, pow)
			print(f'Estimating π with Wallis Product method where n = {n}')
			wp_pi = WallisProduct(circle=circle).estimate(n)
			print(f'Estimating π with Newton-Leibniz method where n = {n}')
			nl_pi = NewtonLeibniz(circle=circle).estimate(n)
			print(f'Estimating π with Nilakantha method where n = {n}')
			nk_pi = Nilakantha(circle=circle).estimate(n)

			print(f'Monte Carlo Area:   {mc_pi:.{precision}f}   error: {Decimal(100.0) * abs(mc_pi - pi) / pi:.{precision - 2}f} %')
			print(f'Rectangular Area:   {ra_pi:.{precision}f}   error: {Decimal(100.0) * abs(ra_pi - pi) / pi:.{precision - 2}f} %')
			print(f'Trapezoidal Area:   {ta_pi:.{precision}f}   error: {Decimal(100.0) * abs(ta_pi - pi) / pi:.{precision - 2}f} %')
			print(f'Linear Distance:    {ld_pi:.{precision}f}   error: {Decimal(100.0) * abs(ld_pi - pi) / pi:.{precision - 2}f} %')
			print(f'Wallis Product:     {wp_pi:.{precision}f}   error: {Decimal(100.0) * abs(wp_pi - pi) / pi:.{precision - 2}f} %')
			print(f'Newton-Leibniz:     {nl_pi:.{precision}f}   error: {Decimal(100.0) * abs(nl_pi - pi) / pi:.{precision - 2}f} %')
			print(f'Nilakantha:         {nk_pi:.{precision}f}   error: {Decimal(100.0) * abs(nk_pi - pi) / pi:.{precision - 2}f} %')

		else:

			print(f'Estimating π with Linear Distance method where n = {n}')
			ld_pi = LinearDistance(circle=circle).estimate(n, pow)
			print(f'Linear Distance:    {ld_pi:.{precision}f}   \nerror: {Decimal(100.0) * abs(ld_pi - pi) / pi:.{precision - 2}f} %')

	else:

		cir_x = []
		cir_y = []

		for i in range(1000):
			cir_x.append(float(radius * Decimal(i) / Decimal(1000)))
			cir_y.append(float((radius**2 - (radius * Decimal(i) / Decimal(1000))**2).sqrt()))

		# est, xs, ys = LinearDistance(circle=circle).graph_estimate(n)
		# print(f'Linear Distance:    {est:.28f}')

		if multi:
			if animate:
				import time
				plt.ion()
				fig, ax = plt.subplots(num='Linear Distance π Estimate Animation')
				while True:
					for i in range(1, n + 1, step):
						est, xs, ys = LinearDistance(circle=circle).graph_estimate(i)
						print(f'Linear Distance:    {est:.28f}   n={i}')
						fig.suptitle(f'Estimate π with {i} segments = {est:.8f}')
						ax.clear()
						ax.plot(cir_x, cir_y, label='y=sqrt(1 - x**2)', color='red', linestyle='dashed')
						ax.plot(xs, ys, label='Estimation segments', color='blue')
						ax.grid(True)
						fig.gca().set_aspect('equal', adjustable='box')
						ax.legend()
						plt.pause(delay)
					plt.ioff()
			else:
				for i in range(n, 0, -1):
					est, xs, ys = LinearDistance(circle=circle).graph_estimate(i)
					print(f'Linear Distance:    {est:.28f}   n={i}')
					fig, ax = plt.subplots(num=f'Linear Distance π Estimate with n={i}')
					ax.plot(cir_x, cir_y, label='y=sqrt(1 - x**2)', color='red', linestyle='dashed')
					ax.plot(xs, ys, label='Estimated Circle Arc', color='blue')
					ax.grid(True)
					fig.gca().set_aspect('equal', adjustable='box')
		else:
			est, xs, ys = LinearDistance(circle=circle).graph_estimate(n)
			print(f'Linear Distance:    {est:.28f}   n={n}')
			fig, ax = plt.subplots(num=f'Linear Distance π Estimate with n={n}')
			ax.plot(cir_x, cir_y, label='y=sqrt(1 - x**2)', color='red', linestyle='dashed', width=3)
			ax.plot(xs, ys, label='Estimated Circle Arc', color='blue', alpha=0.5)
			ax.grid(True)
			fig.gca().set_aspect('equal', adjustable='box')
		plt.show()

	# for i in range(100000):
	# 	print(f"{i} {estimate(i)} ")
	# print()
from decimal import Decimal


class ComplexDecimal(object):

	def __init__(self, value):
		if value is not None:
			if type(value) is Decimal:
				self.real = value
				self.imag = Decimal(0)
			elif type(value) is float or type(value) is int:
				self.real = Decimal(value)
				self.imag = Decimal(0)
			elif type(value) is complex or type(value) is ComplexDecimal:
				self.real = Decimal(value.real)
				self.imag = Decimal(value.imag)
			else:
				raise TypeError("Unsupported type for ComplexDecimal")
		else:
			self.real = Decimal(0)
			self.imag = Decimal(0)

	def __add__(self, other:"ComplexDecimal"):
		result = ComplexDecimal(self)
		result.real += Decimal(other.real)
		result.imag += Decimal(other.imag)
		return result
	
	def __sub__(self, other:"ComplexDecimal"):
		result = ComplexDecimal(self)
		result.real -= Decimal(other.real)
		result.imag -= Decimal(other.imag)
		return result
	
	def __mul__(self, other:"ComplexDecimal"):
		result = ComplexDecimal(self)
		result.real = self.real * other.real - self.imag * other.imag
		result.imag = self.real * other.imag + self.imag * other.real
		return result
	
	def __truediv__(self, other:"ComplexDecimal"):
		result = ComplexDecimal(self)
		denom = other.real**2 + other.imag**2
		result.real = (self.real * other.real + self.imag * other.imag) / denom
		result.imag = (self.imag * other.real - self.real * other.imag) / denom
		return result
	
	def __pow__(self, powerNumerator:Decimal, powerDenominator:Decimal=1):
		if self.imag != 0:
			raise NotImplementedError("Power function not implemented for complex numbers with non-zero imaginary part")
		if self.real < 0 and powerDenominator % 2 == 0:
			raise ValueError("Cannot raise negative real number to a fractional power with even denominator")
		result = ComplexDecimal(self)
		result.real = self.real ** (powerNumerator / powerDenominator)
		result.imag = Decimal(0)
		if self.real < 0 and powerDenominator % 2 == 1:
			result.imag = ( -self.real ) ** (powerNumerator / powerDenominator)
			result.real = Decimal(0)
		return result
		
		
	
	def __neg__(self):
		result = ComplexDecimal(self)
		result.real = -self.real
		result.imag = -self.imag
		return result
	
	def __pos__(self):
		return ComplexDecimal(self)
	
	def __abs__(self):
		return (self.real**2 + self.imag**2).sqrt()
	
	def __complex__(self):
		return complex(float(self.real), float(self.imag))
	
	def __float__(self):
		if self.imag != 0:
			raise ValueError("Cannot convert complex number with non-zero imaginary part to float")
		return float(self.real)
	
	def __int__(self):
		if self.imag != 0:
			raise ValueError("Cannot convert complex number with non-zero imaginary part to int")
		return int(self.real)
	
	def __decimal__(self):
		if self.imag != 0:
			raise ValueError("Cannot convert complex number with non-zero imaginary part to Decimal")
		return self.real
	
	def __eq__(self, value:"ComplexDecimal"):
		if type(value) is ComplexDecimal:
			return self.real == value.real and self.imag == value.imag
		elif type(value) is complex:
			return self.real == Decimal(value.real) and self.imag == Decimal(value.imag)
		elif type(value) is Decimal or type(value) is float or type(value) is int:
			return self.real == Decimal(value) and self.imag == Decimal(0)
		else:
			return False
		
	def __gt__(self, value:"ComplexDecimal"):
		if self.imag != 0 or (type(value) is ComplexDecimal and value.imag != 0) or (type(value) is complex and value.imag != 0):
			raise ValueError("Cannot compare complex numbers with non-zero imaginary parts")
		if type(value) is ComplexDecimal:
			return self.real > value.real
		elif type(value) is complex:
			return self.real > Decimal(value.real)
		elif type(value) is Decimal or type(value) is float or type(value) is int:
			return self.real > Decimal(value)
		else:
			raise TypeError("Unsupported type for comparison")
		
	def __lt__(self, value:"ComplexDecimal"):
		if self.imag != 0 or (type(value) is ComplexDecimal and value.imag != 0) or (type(value) is complex and value.imag != 0):
			raise ValueError("Cannot compare complex numbers with non-zero imaginary parts")
		if type(value) is ComplexDecimal:
			return self.real < value.real
		elif type(value) is complex:
			return self.real < Decimal(value.real)
		elif type(value) is Decimal or type(value) is float or type(value) is int:
			return self.real < Decimal(value)
		else:
			raise TypeError("Unsupported type for comparison")
		
	def __lte__(self, value:"ComplexDecimal"):
		return self.__lt__(value) or self.__eq__(value)
	
	def __gte__(self, value:"ComplexDecimal"):
		return self.__gt__(value) or self.__eq__(value)
		
	def __neq__(self, value:"ComplexDecimal"):
		return not self.__eq__(value)

	__radd__ = __add__
	__rsub__ = __sub__
	__rmul__ = __mul__
	__rtruediv__ = __truediv__
	__rgt__ = __gt__
	__rlt__ = __lt__
	__rlte__ = __lte__
	__rgte__ = __gte__
	__rneq__ = __neq__
	__req__ = __eq__

	def __str__(self):
		return f'({str(self.real)} + {str(self.imag)}i)'

	def sqrt(self):
		result = ComplexDecimal(self)
		if self.imag:
			raise NotImplementedError
		elif self.real > 0:
			result.real = self.real.sqrt()
			return result
		else:
			result.imag = (-self.real).sqrt()
			result.real = Decimal(0)
			return result
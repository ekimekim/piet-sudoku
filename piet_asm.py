import sys

def find_label(label, code):
	for n, (instr, args) in enumerate(code):
		if instr == label + ":":
			return n
	raise Exception("unknown label: {!r}".format(label))

def process(pc, code, stack, input, output):
	instr, args = code[pc]
	if not instr or instr.endswith(':'): # blank or label
		return pc + 1
	if instr == 'inchar':
		if input:
			stack.append(ord(input.pop(0)))
	if instr == 'outchar':
		output.append(chr(stack.pop()))
	if instr == 'not':
		value = stack.pop()
		stack.append(0 if value else 1)
	if instr == 'greater':
		v1 = stack.pop()
		v2 = stack.pop()
		stack.append(1 if v2 > v1 else 0)
	if instr == 'add':
		stack.append(stack.pop() + stack.pop())
	if instr == 'subtract':
		v1 = stack.pop()
		v2 = stack.pop()
		stack.append(v2 - v1)
	if instr == 'push':
		value, = args
		stack.append(int(value))
	if instr == 'pop':
		stack.pop()
	if instr == 'multiply':
		stack.append(stack.pop() * stack.pop())
	if instr == 'divide':
		v1 = stack.pop()
		v2 = stack.pop()
		stack.append(v2/v1)
	if instr == 'modulus':
		v1 = stack.pop()
		v2 = stack.pop()
		sign = -1 if v1 < 0 else 1
		stack.append(sign * (v2 % v1))
	if instr == 'duplicate':
		stack.append(stack[-1])
	if instr == 'roll':
		if args:
			v1, v2 = map(int, args)
		else:
			v1 = stack.pop()
			v2 = stack.pop()
		for n in range(v1):
			value = stack.pop()
			# example: depth 3, len 5: [1,2,3,4,5] -pop-> [1,2,3,4] -insert(len-2)-> [1,2,5,3,4]
			stack.insert(len(stack) - (v2-1), value)
	if instr == 'jmp':
		label, = args
		return find_label(label, code)
	if instr == 'jnz':
		label, = args
		value = stack.pop()
		if value != 0:
			return find_label(label, code)
	elif instr == 'terminate': 
		return -1
	return pc + 1

def main(filename, input):
	with open(filename) as f:
		src = f.read().strip().split('\n')
	code = [line.split('#', 1)[0].strip() for line in src]
	code = [(line.split(' ')[0], line.split()[1:]) for line in code]
	stack = []
	input = list(input)
	output = []
	pc = 0
	while pc >= 0:
		old_pc = pc
		pc = process(pc, code, stack, input, output)
		print "{:3d} {} : {}".format(old_pc, src[old_pc], stack)
	output = ''.join(output)
	print "FINAL OUT:", repr(output)

if __name__ == '__main__':
	main(*sys.argv[1:])

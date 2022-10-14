import serial
import time
import os

#for asynchronous keypress detection
import sys
import termios
import atexit
from select import select

#params
serial_addr = '/dev/ttyACM0'
DEFAULT_LOOP_RELAYS = [1,2,3,4]
DEFAULT_INTERLOOP_DELAY = 60.0 # 1 minute in (s)
DEFAULT_OWON_CAPTURE_PRETIME = 5.0 # 5 seconds in (s)
DEFAULT_OWON_CAPTURE_POSTTIME = 5.0 # 5 seconds in (s)
VERBOSE = True
bin_out_folder = "/home/johnathanglyon/Desktop/test_bin_out/"

#init
s = serial.Serial(port=serial_addr, baudrate=9600)
loop_relays = DEFAULT_LOOP_RELAYS.copy()
interloop_delay = DEFAULT_INTERLOOP_DELAY

class KBHit:

	def __init__(self):
		'''Creates a KBHit object that you can call to do various keyboard things.
		'''
		# Save the terminal settings
		self.fd = sys.stdin.fileno()
		self.new_term = termios.tcgetattr(self.fd)
		self.old_term = termios.tcgetattr(self.fd)

		# New terminal setting unbuffered
		self.new_term[3] = (self.new_term[3] & ~termios.ICANON & ~termios.ECHO)
		termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.new_term)

		# Support normal-terminal reset at exit
		atexit.register(self.set_normal_term)
		
		
	def set_normal_term(self):
		''' Resets to normal terminal.
		'''
		termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.old_term)


	def getch(self):
		''' Returns a keyboard character after kbhit() has been called.
		'''
		return sys.stdin.read(1)


	def kbhit(self):
		''' Returns True if keyboard character was hit, False otherwise.
		'''
		dr,dw,de = select([sys.stdin], [], [], 0)
		return dr != []

def clear_and_relay_switch(x):
	clear_relays()
	s.write(bytes(str(x), 'utf-8'))
	time.sleep(0.05)
	data = s.readline()
	if VERBOSE: print(data.decode(),end='')
	return data

def clear_relays():
	s.write(bytes('0', 'utf-8'))
	time.sleep(0.05)
	data = s.readline()
	if VERBOSE: print(data.decode(),end='')
	return data
	
def owon_dump(channel):
	filename = bin_out_folder + str(time.time()) + "_" + str(channel) + "_dump.bin"
	exit_code = os.system("/home/johnathanglyon/Desktop/owon-sds7102-protocol-master/owon-dump > " + filename)
	print("OWONDUMP ran with exit code %d" % exit_code)

def print_loop_settings():
	settings = "LOOPING SEQUENCE: " + str(loop_relays) + "\n" \
				"INTERLOOP DELAY: " + str(interloop_delay) + " (s)"
	print(settings) 

def print_help():
	help_str = "press x to bring up prompt\n" \
				"h : help (this list) \n" \
				"0 : no relay\n" \
				"1-8 : turn on corresponding relay\n" \
				"l : start relay loop\n" \
				"d : set loop delay time\n" \
				"r : set relays to loop over\n" \
				"s : show current loop settings\n" \
				"q : quit\n"
	print(help_str)

if __name__ == "__main__":

	cur_prog = '0'
	kb = KBHit()

	print_help()
	print_loop_settings()
	
	loop_state = "RESTART_LOOP"
	current_loop_relay_index = 0
	loop_time = None

	#mainLoop
	while(True):
		# check for keypress
		if kb.kbhit():
			c = kb.getch()
			if ord(c) == 120: # 'x'
				next_prog = input('Please enter new program code: ')
				print(next_prog) #newline
				if next_prog == 'h':
					print_help()
				elif next_prog == 's':
					print_loop_settings()
				elif next_prog == '0':
					clear_relays()
					cur_prog = next_prog
				elif next_prog == '1':
					clear_and_relay_switch(next_prog)
				elif next_prog == '2':
					clear_and_relay_switch(next_prog)
				elif next_prog == '3':
					clear_and_relay_switch(next_prog)
				elif next_prog == '4':
					clear_and_relay_switch(next_prog)
				elif next_prog == '5':
					clear_and_relay_switch(next_prog)
				elif next_prog == '6':
					clear_and_relay_switch(next_prog)
				elif next_prog == '7':
					clear_and_relay_switch(next_prog)
				elif next_prog == '8':
					clear_and_relay_switch(next_prog)
				elif next_prog == 'l':
					print_loop_settings()
					loop_state = "RESTART_LOOP"
					cur_prog = next_prog
				elif next_prog == 'd':
					print("Current INTERLOOP DELAY: " + str(interloop_delay) + " (s)")
					while(True):
						delay_s = input("Please enter new interloop delay in (s) ['d' for DEFAULT]: ")
						print(delay_s)
						if delay_s == "d":
							delay_s = DEFAULT_INTERLOOP_DELAY
						try:
							delay_s = float(delay_s)
							if delay_s < 0: raise ValueError
						except ValueError:
							print('WARNING: input cannot be interpreted as number; ignoring...')
							break
						confirm = input("CONFIRM?: Change delay to " + str(delay_s) + "s [y | n | (r)etry]")
						print(confirm)
						if confirm == 'y':
							interloop_delay = delay_s
							break
						elif confirm == 'n':
							break
						elif confirm == 'r':
							continue
						else:
							print('WARNING: Unknown input code; ignoring...')
				elif next_prog == 'r':
					print("Current RELAYS FOR LOOPING: " + str(loop_relays) + " (s)")
					while(True):
						relays = input("Please enter relay sequence: ")
						print(relays)
						if relays == "d":
							relays = DEFAULT_LOOP_RELAYS
						else:
							relays = list(relays)
						new_relays = []
						try:
							if len(c) < 1:
								raise ValueError
							for c in relays:
								if int(c) > 0 and int(c) <= 8:
									new_relays.append(int(c))
								else:
									raise ValueError
						except ValueError:
							print('WARNING: input cannot be interpreted as relay numbers; ignoring...')
							break
						confirm = input("CONFIRM?: Change relays to " + str(new_relays) + " [y | n | (r)etry]")
						print(confirm)
						if confirm == 'y':
							loop_relays = new_relays
							loop_state = "RESTART_LOOP"
							break
						elif confirm == 'n':
							break
						elif confirm == 'r':
							continue
						else:
							print('WARNING: Unknown input code; ignoring...')
				elif next_prog == 'q':
					clear_relays()
					exit()
				else:
					print('WARNING: Unknown input code; ignoring...')

		# run loop
		if cur_prog == 'l':
			if loop_state == "RESTART_LOOP":
				clear_and_relay_switch(loop_relays[0])
				current_loop_relay_index = 0
				loop_timer = time.time()
				loop_state = "PRETIMER"
				if VERBOSE: print("\t>PRETIMER: " + str(current_loop_relay_index))
			elif loop_state == "PRETIMER":
				now = time.time()
				if (now - loop_timer) > DEFAULT_OWON_CAPTURE_PRETIME:
					print("OWON DUMP :: " + str(now) + " :: " + str(current_loop_relay_index))
					owon_dump(loop_relays[current_loop_relay_index])
					loop_timer = time.time()
					loop_state = "POSTTIMER"
					if VERBOSE: print("\t>POSTIMER: " + str(current_loop_relay_index))
			elif loop_state == "POSTTIMER":
				now = time.time()
				if (now - loop_timer) > DEFAULT_OWON_CAPTURE_POSTTIME:
					current_loop_relay_index += 1
					if current_loop_relay_index == len(loop_relays):
						clear_relays()
						loop_timer = time.time()
						loop_state = "DELAY"
						if VERBOSE: print("\t>DELAY")
					else:
						clear_and_relay_switch(loop_relays[current_loop_relay_index])
						loop_timer = time.time()
						loop_state = "PRETIMER"
						if VERBOSE: print("\t>PRETIMER: " + str(current_loop_relay_index))
			elif loop_state == "DELAY":
				now = time.time()
				if (now - loop_timer) > interloop_delay:
					loop_state = "RESTART_LOOP"
					if VERBOSE: print("\t>RESTART_LOOP")
			

"""
		# check for serial info (NON BLOCKING)
		if (s.inWaiting()>0):
			data_str = s.read(s.inWaiting()).decode('ascii')
			print(data_str)
"""
